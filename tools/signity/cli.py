"""signity CLI。

  python3 -m signity hash <event.json|yaml>   content_hash を計算する
  python3 -m signity validate [path...]       Schema 適合を検証する
  python3 -m signity verify                   Ledger 全体を検証する
  python3 -m signity chain                    ハッシュチェーンを表示する
  python3 -m signity state [--object ID]      Current State を投影する
  python3 -m signity append <draft.json>      Draft をチェーンに接続して追記する
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .canonical import canonicalize, content_hash, verify_content_hash
from .ledger import (
    collect_evidence_refs,
    compute_chain,
    load,
    verify_chain,
)
from .projection import ProjectionError, project
from .validate import load_schema, validate

REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "ledger" / "events"
PENDING = REPO / "ledger" / "pending"
SCHEMA = REPO / "schemas" / "decision-event.schema.v0.3.json"
EVIDENCE = REPO / "docs" / "evidence"

GREEN, RED, YELLOW, DIM, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"


def _load_event(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        import yaml  # YAML を読むときだけ必要

        return yaml.safe_load(text)
    return json.loads(text)


def cmd_hash(args) -> int:
    path = Path(args.path)
    event = _load_event(path)
    matched, recorded, actual = verify_content_hash(event)
    if args.show_canonical:
        sys.stdout.write(canonicalize(event).decode("utf-8") + "\n")
    print(f"file            {path}")
    print(f"canonical bytes {len(canonicalize(event))}")
    print(f"content_hash    {actual}")
    if recorded and recorded != "pending":
        mark = f"{GREEN}一致{RESET}" if matched else f"{RED}不一致{RESET}"
        print(f"記録されている値 {recorded}  {mark}")
        return 0 if matched else 1
    print(f"記録されている値 {recorded or '(なし)'}")
    return 0


def cmd_validate(args) -> int:
    schema = load_schema(SCHEMA)
    paths = [Path(p) for p in args.paths] if args.paths else sorted(
        list(LEDGER.glob("*.json")) + list(PENDING.glob("*.json"))
    )
    failed = 0
    for path in paths:
        errors = validate(_load_event(path), schema)
        if errors:
            failed += 1
            print(f"{RED}NG{RESET}   {path.relative_to(REPO) if path.is_absolute() else path}")
            for e in errors:
                print(f"       {e}")
        else:
            print(f"{GREEN}OK{RESET}   {path.relative_to(REPO) if path.is_absolute() else path}")
    print(f"\n適合 {len(paths) - failed} / 不適合 {failed}")
    return 1 if failed else 0


def cmd_chain(args) -> int:
    entries = load(LEDGER)
    if not entries:
        print("Ledger が空。")
        return 0
    print(f"{'seq':>4}  {'display_id':<18} {'occurred_at':<26} content_hash")
    print("-" * 100)
    for entry in entries:
        h = content_hash(entry.event)
        prev = (entry.event.get("integrity") or {}).get("previous_event_hash")
        link = f"{DIM}← {prev[:12]}…{RESET}" if prev else f"{DIM}← null (先頭){RESET}"
        print(
            f"{entry.sequence:>4}  {entry.display_id:<18} "
            f"{entry.event.get('occurred_at', '?'):<26} {h[:16]}…  {link}"
        )
    return 0


def cmd_verify(args) -> int:
    entries = load(LEDGER)
    report = verify_chain(entries)

    print(f"Ledger: {LEDGER.relative_to(REPO)}  ({report.checked} 件)\n")

    schema = load_schema(SCHEMA)
    schema_failed = 0
    for entry in entries:
        errors = validate(entry.event, schema)
        if errors:
            schema_failed += 1
            report.errors.append(f"{entry.path.name}: Schema 不適合 -> " + "; ".join(errors))

    for entry in entries:
        h = content_hash(entry.event)
        recorded = (entry.event.get("integrity") or {}).get("content_hash")
        mark = GREEN + "OK  " + RESET if recorded == h else RED + "NG  " + RESET
        print(f"{mark} {entry.sequence:04d} {entry.display_id:<18} {h[:16]}…")

    if report.warnings:
        print(f"\n{YELLOW}警告{RESET}")
        for w in report.warnings:
            print(f"  - {w}")

    # Evidence 参照の解決性
    dangling: list[str] = []
    for ref, users in sorted(collect_evidence_refs(entries).items()):
        hits = list(EVIDENCE.rglob("*.md"))
        found = any(ref in p.read_text(encoding="utf-8") for p in hits)
        if not found:
            dangling.append(f"{ref}（参照元: {', '.join(users)}）")
    if dangling:
        print(f"\n{YELLOW}未解決の evidence_refs{RESET}  docs/evidence/ に該当する記録がない")
        for d in dangling:
            print(f"  - {d}")

    if report.errors:
        print(f"\n{RED}エラー{RESET}")
        for e in report.errors:
            print(f"  - {e}")
        print(f"\n{RED}検証失敗{RESET}: {len(report.errors)} 件")
        return 1

    print(
        f"\n{GREEN}検証成功{RESET}: content_hash {report.checked} 件一致 / "
        f"チェーン連結 OK / Schema 適合 {report.checked - schema_failed} 件"
    )
    return 0


def cmd_state(args) -> int:
    entries = load(LEDGER)
    try:
        result = project(entries, args.object, strict=not args.lenient)
    except ProjectionError as exc:
        print(f"{RED}投影失敗{RESET}\n{exc}")
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def cmd_append(args) -> int:
    """Draft を Ledger の末尾に接続して追記する。

    既存の Event は読むだけで書き換えない。追記後は必ず verify で確認する。
    """
    draft_path = Path(args.path)
    draft = _load_event(draft_path)

    schema = load_schema(SCHEMA)
    errors = validate(draft, schema)
    if errors:
        print(f"{RED}Schema 不適合のため追記しない{RESET}")
        for e in errors:
            print(f"  - {e}")
        return 1

    if draft.get("status") != "approved":
        print(
            f"{RED}追記しない{RESET}: Ledger には承認済み Event のみ追記できる"
            f"（status={draft.get('status')!r}）"
        )
        print("  承認は人間が行う。status を approved にし、approved_at と approved_by を記入すること。")
        return 1

    entries = load(LEDGER)
    chained = compute_chain([e.event for e in entries] + [draft])
    new_event = chained[-1]

    # 既存分のハッシュが変わっていないことを確認する（変わったら中止）
    for entry, recomputed in zip(entries, chained):
        recorded = (entry.event.get("integrity") or {}).get("content_hash")
        if recorded != recomputed["integrity"]["content_hash"]:
            print(f"{RED}中止{RESET}: 既存 Event {entry.display_id} のハッシュが合わない。")
            print("  先に verify で原因を調べること。")
            return 1

    seq = len(entries) + 1
    display = new_event.get("display_id") or new_event["event_id"]
    out = LEDGER / f"{seq:04d}-{display}.json"
    if out.exists():
        print(f"{RED}中止{RESET}: {out.name} が既にある。追記専用の Ledger は上書きしない。")
        return 1

    out.write_text(
        json.dumps(new_event, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"{GREEN}追記{RESET} {out.relative_to(REPO)}")
    print(f"  previous_event_hash {new_event['integrity']['previous_event_hash']}")
    print(f"  content_hash        {new_event['integrity']['content_hash']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="signity", description="Signity Ledger の整合性検証と投影"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("hash", help="content_hash を計算する")
    p.add_argument("path")
    p.add_argument("--show-canonical", action="store_true", help="正規化後の JSON を表示する")
    p.set_defaults(func=cmd_hash)

    p = sub.add_parser("validate", help="Schema 適合を検証する")
    p.add_argument("paths", nargs="*")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("chain", help="ハッシュチェーンを表示する")
    p.set_defaults(func=cmd_chain)

    p = sub.add_parser("verify", help="Ledger 全体を検証する")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("state", help="Current State を投影する")
    p.add_argument("--object", help="対象の primary_object_id")
    p.add_argument("--lenient", action="store_true", help="before の不一致を警告に留める")
    p.set_defaults(func=cmd_state)

    p = sub.add_parser("append", help="承認済み Draft を Ledger へ追記する")
    p.add_argument("path")
    p.set_defaults(func=cmd_append)

    args = parser.parse_args(argv)
    return args.func(args)
