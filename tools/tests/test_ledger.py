"""ハッシュチェーンの構築・検証と、改ざん検知の受け入れテスト。

「改ざん不能」ではなく「改ざん検知可能」であることを、実際に改変して確かめる。
"""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from signity.canonical import content_hash
from signity.ledger import Entry, compute_chain, load, verify_chain

REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "ledger" / "events"

GENESIS_HASH = "f9eb852866535b176c9af8c6e9f0d9fcc18ab5950771b4969b652cd04f6acbf6"


def minimal(display_id: str, *, path: str, before, after, recorded: str) -> dict:
    return {
        "schema_version": "0.3",
        "event_id": f"de_{display_id.lower().replace('-', '_')}",
        "display_id": display_id,
        "event_kind": "decision",
        "decision_type": "change",
        "status": "approved",
        "primary_object_id": "do_test",
        "affected_object_ids": [],
        "title": f"test {display_id}",
        "occurred_at": recorded,
        "recorded_at": recorded,
        "approved_at": recorded,
        "effective_at": recorded,
        "changes": [{"path": path, "before": before, "after": after, "change_note": None}],
        "rationale": {"summary": "test"},
        "proposed_by": ["actor_test"],
        "approved_by": ["actor_test"],
        "evidence_refs": [],
        "model_run_refs": [],
        "supersedes_event_id": None,
        "corrects_event_id": None,
        "integrity": {
            "algorithm": "sha256",
            "canonicalization": "canonical-json-v1",
            "previous_event_hash": None,
            "content_hash": "pending",
        },
        "signatures": [],
    }


def as_entries(events: list[dict]) -> list[Entry]:
    return [
        Entry(sequence=i, path=Path(f"{i:04d}-{e['display_id']}.json"), event=e)
        for i, e in enumerate(events, start=1)
    ]


class TestRealLedger(unittest.TestCase):
    """リポジトリ内の実際の Ledger。"""

    def setUp(self):
        self.entries = load(LEDGER)

    def test_ledger_is_not_empty(self):
        self.assertGreater(len(self.entries), 0)

    def test_ledger_verifies(self):
        report = verify_chain(self.entries)
        self.assertTrue(report.ok, "\n".join(report.errors))

    def test_genesis_hash_is_the_canonical_seed_hash(self):
        """先頭 Event は正本シードと同一のハッシュを持つ。"""
        first = self.entries[0]
        self.assertIsNone(first.event["integrity"]["previous_event_hash"])
        self.assertEqual(first.event["integrity"]["content_hash"], GENESIS_HASH)

    def test_every_event_links_to_its_predecessor(self):
        for prev, cur in zip(self.entries, self.entries[1:]):
            self.assertEqual(
                cur.event["integrity"]["previous_event_hash"],
                content_hash(prev.event),
                f"{cur.display_id} が {prev.display_id} に繋がっていない",
            )

    def test_all_ledger_events_are_approved(self):
        for entry in self.entries:
            self.assertEqual(entry.event["status"], "approved", entry.display_id)


class TestChainConstruction(unittest.TestCase):
    def test_chain_links_are_computed(self):
        events = [
            minimal("DE-T-001", path="/a", before=None, after=1, recorded="2026-01-01T00:00:00+09:00"),
            minimal("DE-T-002", path="/a", before=1, after=2, recorded="2026-01-02T00:00:00+09:00"),
            minimal("DE-T-003", path="/a", before=2, after=3, recorded="2026-01-03T00:00:00+09:00"),
        ]
        chained = compute_chain(events)
        self.assertIsNone(chained[0]["integrity"]["previous_event_hash"])
        for prev, cur in zip(chained, chained[1:]):
            self.assertEqual(
                cur["integrity"]["previous_event_hash"], prev["integrity"]["content_hash"]
            )
        self.assertTrue(verify_chain(as_entries(chained)).ok)

    def test_compute_chain_does_not_mutate_input(self):
        events = [minimal("DE-T-001", path="/a", before=None, after=1, recorded="2026-01-01T00:00:00+09:00")]
        snapshot = json.dumps(events, sort_keys=True)
        compute_chain(events)
        self.assertEqual(json.dumps(events, sort_keys=True), snapshot)

    def test_appending_does_not_change_earlier_hashes(self):
        base = [
            minimal("DE-T-001", path="/a", before=None, after=1, recorded="2026-01-01T00:00:00+09:00"),
            minimal("DE-T-002", path="/a", before=1, after=2, recorded="2026-01-02T00:00:00+09:00"),
        ]
        first = compute_chain(base)
        extended = compute_chain(base + [
            minimal("DE-T-003", path="/a", before=2, after=3, recorded="2026-01-03T00:00:00+09:00")
        ])
        for a, b in zip(first, extended):
            self.assertEqual(a["integrity"]["content_hash"], b["integrity"]["content_hash"])


class TestTamperDetection(unittest.TestCase):
    """改ざん検知。実際に改変して、検証が失敗することを確かめる。"""

    def chain(self) -> list[dict]:
        return compute_chain([
            minimal("DE-T-001", path="/a", before=None, after=1, recorded="2026-01-01T00:00:00+09:00"),
            minimal("DE-T-002", path="/a", before=1, after=2, recorded="2026-01-02T00:00:00+09:00"),
            minimal("DE-T-003", path="/a", before=2, after=3, recorded="2026-01-03T00:00:00+09:00"),
        ])

    def test_editing_a_past_event_is_detected(self):
        chained = self.chain()
        chained[0]["title"] = "改変された"
        report = verify_chain(as_entries(chained))
        self.assertFalse(report.ok)
        self.assertTrue(any("content_hash 不一致" in e for e in report.errors))

    def test_editing_and_rehashing_still_breaks_the_chain(self):
        """内容を変えて content_hash を再計算しても、後続との連結が切れる。

        これがハッシュチェーンの効果。単体の content_hash だけでは
        「整合するように作り直す」ことができてしまう。
        """
        chained = self.chain()
        chained[0]["title"] = "改変された"
        chained[0]["integrity"]["content_hash"] = content_hash(chained[0])
        report = verify_chain(as_entries(chained))
        self.assertFalse(report.ok)
        self.assertTrue(any("previous_event_hash" in e for e in report.errors))

    def test_deleting_a_middle_event_is_detected(self):
        chained = self.chain()
        del chained[1]
        report = verify_chain(as_entries(chained))
        self.assertFalse(report.ok)
        self.assertTrue(any("previous_event_hash" in e for e in report.errors))

    def test_reordering_events_is_detected(self):
        chained = self.chain()
        chained[1], chained[2] = chained[2], chained[1]
        self.assertFalse(verify_chain(as_entries(chained)).ok)

    def test_pending_hash_in_ledger_is_rejected(self):
        chained = self.chain()
        chained[2]["integrity"]["content_hash"] = "pending"
        report = verify_chain(as_entries(chained))
        self.assertFalse(report.ok)
        self.assertTrue(any("pending" in e for e in report.errors))

    def test_draft_in_ledger_is_rejected(self):
        chained = self.chain()
        chained[1]["status"] = "draft"
        chained = compute_chain(chained)
        report = verify_chain(as_entries(chained))
        self.assertFalse(report.ok)
        self.assertTrue(any("承認済み" in e for e in report.errors))

    def test_unknown_canonicalization_is_rejected(self):
        chained = self.chain()
        chained[0]["integrity"]["canonicalization"] = "canonical-json-v2"
        report = verify_chain(as_entries(chained))
        self.assertFalse(report.ok)
        self.assertTrue(any("canonicalization" in e for e in report.errors))

    def test_sequence_gap_is_detected(self):
        chained = self.chain()
        entries = as_entries(chained)
        entries[2].sequence = 9
        report = verify_chain(entries)
        self.assertFalse(report.ok)
        self.assertTrue(any("連番" in e for e in report.errors))

    def test_recorded_at_going_backwards_is_a_warning_not_an_error(self):
        chained = compute_chain([
            minimal("DE-T-001", path="/a", before=None, after=1, recorded="2026-03-01T00:00:00+09:00"),
            minimal("DE-T-002", path="/a", before=1, after=2, recorded="2026-01-01T00:00:00+09:00"),
        ])
        report = verify_chain(as_entries(chained))
        self.assertTrue(report.ok, "\n".join(report.errors))
        self.assertTrue(any("recorded_at" in w for w in report.warnings))


class TestLoad(unittest.TestCase):
    def test_bad_filename_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "DE-20260710-003.json").write_text("{}", encoding="utf-8")
            with self.assertRaises(ValueError):
                load(d)

    def test_empty_dir_loads_as_empty(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(load(d), [])


if __name__ == "__main__":
    unittest.main()
