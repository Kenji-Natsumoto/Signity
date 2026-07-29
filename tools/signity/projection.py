"""Current State の投影（Projection）。

architecture v0.3 の 3.1 節に従い、Current State は入力項目ではなく、
承認済みイベントを決定的な順序で適用した計算結果として扱う。

Decision Event は Committed State を変更する。Action / Outcome /
Observation Event は Observed State を更新するが、v0.3 の Schema は
event_kind: decision のみを対象とするため、本モジュールも
Committed State だけを投影する。
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any

from .canonical import canonicalize
from .ledger import Entry


class ProjectionError(ValueError):
    """投影できない変更が含まれていた。"""


def _split(path: str) -> list[str]:
    if not path.startswith("/"):
        raise ProjectionError(f"changes[].path は / で始まらなければならない: {path!r}")
    return [seg for seg in path.strip("/").split("/") if seg]


def _get(state: dict, segments: list[str]) -> Any:
    node: Any = state
    for seg in segments:
        if not isinstance(node, dict) or seg not in node:
            return None
        node = node[seg]
    return node


def _set(state: dict, segments: list[str], value: Any) -> None:
    node = state
    for seg in segments[:-1]:
        nxt = node.get(seg)
        if not isinstance(nxt, dict):
            nxt = {}
            node[seg] = nxt
        node = nxt
    node[segments[-1]] = value


def project(
    entries: list[Entry],
    object_id: str | None = None,
    *,
    strict: bool = True,
) -> dict:
    """Committed State を投影する。

    object_id を指定すると、その Decision Object を primary_object_id に
    持つ Event だけを適用する。

    strict=True の場合、changes[].before が現在値と食い違う Event を
    エラーにする。before は「その時点の値」なので、食い違いは
    Event の欠落・順序の誤り・重複適用を示す。
    """
    state: dict = {}
    applied: list[str] = []
    conflicts: list[str] = []
    last_event_id: str | None = None

    for entry in entries:
        event = entry.event
        if object_id and event.get("primary_object_id") != object_id:
            continue
        if event.get("status") != "approved":
            continue

        for change in event.get("changes", []):
            segments = _split(change["path"])
            current = _get(state, segments)
            expected = change.get("before")
            if current != expected:
                message = (
                    f"{entry.display_id}: {change['path']} の before が現在値と違う"
                    f"（before={expected!r} / 現在={current!r}）"
                )
                if strict:
                    conflicts.append(message)
                    continue
                conflicts.append(message)
            _set(state, segments, change["after"])

        applied.append(entry.display_id)
        last_event_id = event.get("display_id") or event.get("event_id")

    if conflicts and strict:
        raise ProjectionError(
            "投影中に before の不一致が発生した:\n  - " + "\n  - ".join(conflicts)
        )

    projection_hash = hashlib.sha256(canonicalize({"state": state})).hexdigest()

    return {
        "value": state,
        "as_of_event_id": last_event_id,
        "applied_events": applied,
        "calculated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "projection_hash": projection_hash,
        "conflicts": conflicts,
    }
