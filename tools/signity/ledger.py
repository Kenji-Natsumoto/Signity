"""追記専用 Ledger の読み込み、ハッシュチェーンの計算と検証。

Ledger の実体は ledger/events/NNNN-<display_id>.json である。
連番が追記順そのもので、recorded_at から推測しない。
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from .canonical import ALGORITHM, CANONICALIZATION, content_hash

FILENAME_RE = re.compile(r"^(\d{4})-(.+)\.json$")


@dataclass
class Entry:
    """Ledger 内の 1 件。"""

    sequence: int
    path: Path
    event: dict

    @property
    def display_id(self) -> str:
        return self.event.get("display_id") or self.event.get("event_id", "?")

    @property
    def recorded_at(self) -> datetime | None:
        raw = self.event.get("recorded_at")
        try:
            return datetime.fromisoformat(raw) if raw else None
        except (TypeError, ValueError):
            return None


@dataclass
class Report:
    """検証結果。"""

    checked: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def load(events_dir: str | Path) -> list[Entry]:
    """Ledger を連番順に読み込む。

    連番の重複・欠番はここでは判定せず、verify_chain が報告する。
    """
    events_dir = Path(events_dir)
    entries: list[Entry] = []
    for path in sorted(events_dir.glob("*.json")):
        m = FILENAME_RE.match(path.name)
        if not m:
            raise ValueError(
                f"Ledger のファイル名が規則に合わない: {path.name}"
                " (NNNN-<display_id>.json)"
            )
        event = json.loads(path.read_text(encoding="utf-8"))
        entries.append(Entry(sequence=int(m.group(1)), path=path, event=event))
    return entries


def verify_chain(entries: list[Entry]) -> Report:
    """content_hash とハッシュチェーンの整合性を検証する。"""
    report = Report(checked=len(entries))

    # 連番が 1 から欠番なく続いているか
    for i, entry in enumerate(entries, start=1):
        if entry.sequence != i:
            report.errors.append(
                f"{entry.path.name}: 連番が飛んでいる（期待 {i:04d}、実際 {entry.sequence:04d}）"
            )

    previous_hash: str | None = None
    previous_recorded: datetime | None = None
    previous_id = ""

    for entry in entries:
        name = entry.path.name
        integrity = entry.event.get("integrity")
        if not isinstance(integrity, dict):
            report.errors.append(f"{name}: integrity がない")
            continue

        # 正規化方式とアルゴリズムの宣言
        declared = integrity.get("canonicalization")
        if declared != CANONICALIZATION:
            report.errors.append(
                f"{name}: canonicalization は {CANONICALIZATION!r} のみ対応"
                f"（実際: {declared!r}）"
            )
            continue
        if integrity.get("algorithm") != ALGORITHM:
            report.errors.append(
                f"{name}: algorithm は {ALGORITHM!r} のみ対応"
                f"（実際: {integrity.get('algorithm')!r}）"
            )
            continue

        # Ledger は承認済みのみ
        status = entry.event.get("status")
        if status != "approved":
            report.errors.append(
                f"{name}: Ledger には承認済み Event のみ追記できる（実際: status={status!r}）"
            )

        # content_hash の再計算
        recorded = integrity.get("content_hash")
        actual = content_hash(entry.event)
        if recorded == "pending":
            report.errors.append(f"{name}: content_hash が pending のまま追記されている")
        elif recorded != actual:
            report.errors.append(
                f"{name}: content_hash 不一致\n"
                f"      記録   {recorded}\n"
                f"      再計算 {actual}"
            )

        # チェーンの連結
        prev_declared = integrity.get("previous_event_hash")
        if prev_declared != previous_hash:
            report.errors.append(
                f"{name}: previous_event_hash がチェーンと合わない\n"
                f"      記録   {prev_declared}\n"
                f"      期待   {previous_hash}"
                + (f" ({previous_id} の content_hash)" if previous_id else " (先頭なので null)")
            )

        # 追記順と recorded_at の整合（誤りではなく警告）
        current_recorded = entry.recorded_at
        if current_recorded and previous_recorded and current_recorded < previous_recorded:
            report.warnings.append(
                f"{name}: recorded_at が直前の Event より古い"
                f"（{current_recorded.isoformat()} < {previous_recorded.isoformat()}）"
            )
        if current_recorded:
            previous_recorded = current_recorded

        previous_hash = actual
        previous_id = entry.display_id

    return report


def compute_chain(events: list[dict]) -> list[dict]:
    """整合したハッシュチェーンを持つ Event 列を新しく組み立てて返す。

    入力は変更しない。追記時に previous_event_hash と content_hash を
    埋めるために使う。
    """
    out: list[dict] = []
    previous_hash: str | None = None
    for event in events:
        e = json.loads(json.dumps(event))
        integrity = e.setdefault("integrity", {})
        integrity["algorithm"] = ALGORITHM
        integrity["canonicalization"] = CANONICALIZATION
        integrity["previous_event_hash"] = previous_hash
        integrity.pop("content_hash", None)
        integrity["content_hash"] = content_hash(e)
        previous_hash = integrity["content_hash"]
        out.append(e)
    return out


def collect_evidence_refs(entries: list[Entry]) -> dict[str, list[str]]:
    """evidence_ref -> それを参照する Event の display_id 一覧。"""
    refs: dict[str, list[str]] = {}
    for entry in entries:
        for ref in entry.event.get("evidence_refs", []):
            refs.setdefault(ref, []).append(entry.display_id)
    return refs
