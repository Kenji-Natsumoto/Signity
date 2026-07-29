"""Current State の投影のテスト。

architecture v0.3 3.1 節「Current State は入力項目ではない」を実装で保証する。
"""

from __future__ import annotations

import unittest
from pathlib import Path

from signity.ledger import load
from signity.projection import ProjectionError, project

from .test_ledger import as_entries, minimal
from signity.ledger import compute_chain

REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "ledger" / "events"
TRANSITION_ENGINE = "do_01J2H_EXAMPLE_TRANSITION_ENGINE"


def chain(*events) -> list:
    return as_entries(compute_chain(list(events)))


class TestProjection(unittest.TestCase):
    def test_applies_changes_in_order(self):
        entries = chain(
            minimal("DE-T-001", path="/identity/name", before=None, after="A",
                    recorded="2026-01-01T00:00:00+09:00"),
            minimal("DE-T-002", path="/identity/name", before="A", after="B",
                    recorded="2026-01-02T00:00:00+09:00"),
        )
        result = project(entries, "do_test")
        self.assertEqual(result["value"], {"identity": {"name": "B"}})
        self.assertEqual(result["as_of_event_id"], "DE-T-002")

    def test_nested_paths_create_intermediate_objects(self):
        entries = chain(
            minimal("DE-T-001", path="/a/b/c", before=None, after=1,
                    recorded="2026-01-01T00:00:00+09:00"),
        )
        self.assertEqual(project(entries, "do_test")["value"], {"a": {"b": {"c": 1}}})

    def test_separate_state_axes_do_not_interfere(self):
        """名称変更は lifecycle を変えない（v0.2 architecture 3.2 節）。"""
        entries = chain(
            minimal("DE-T-001", path="/lifecycle/stage", before=None, after="concept",
                    recorded="2026-01-01T00:00:00+09:00"),
            minimal("DE-T-002", path="/identity/name", before=None, after="Signity",
                    recorded="2026-01-02T00:00:00+09:00"),
        )
        result = project(entries, "do_test")
        self.assertEqual(result["value"]["lifecycle"]["stage"], "concept")
        self.assertEqual(result["value"]["identity"]["name"], "Signity")

    def test_before_mismatch_raises_in_strict_mode(self):
        entries = chain(
            minimal("DE-T-001", path="/a", before=None, after=1,
                    recorded="2026-01-01T00:00:00+09:00"),
            minimal("DE-T-002", path="/a", before=99, after=2,
                    recorded="2026-01-02T00:00:00+09:00"),
        )
        with self.assertRaises(ProjectionError):
            project(entries, "do_test")

    def test_before_mismatch_is_reported_in_lenient_mode(self):
        entries = chain(
            minimal("DE-T-001", path="/a", before=None, after=1,
                    recorded="2026-01-01T00:00:00+09:00"),
            minimal("DE-T-002", path="/a", before=99, after=2,
                    recorded="2026-01-02T00:00:00+09:00"),
        )
        result = project(entries, "do_test", strict=False)
        self.assertEqual(len(result["conflicts"]), 1)
        self.assertEqual(result["value"], {"a": 2})

    def test_other_objects_are_ignored(self):
        a = minimal("DE-T-001", path="/a", before=None, after=1,
                    recorded="2026-01-01T00:00:00+09:00")
        b = minimal("DE-T-002", path="/b", before=None, after=2,
                    recorded="2026-01-02T00:00:00+09:00")
        b["primary_object_id"] = "do_other"
        entries = chain(a, b)
        self.assertEqual(project(entries, "do_test")["value"], {"a": 1})

    def test_projection_hash_is_deterministic(self):
        entries = chain(
            minimal("DE-T-001", path="/a", before=None, after=1,
                    recorded="2026-01-01T00:00:00+09:00"),
        )
        self.assertEqual(
            project(entries, "do_test")["projection_hash"],
            project(entries, "do_test")["projection_hash"],
        )

    def test_projection_hash_changes_with_state(self):
        one = chain(minimal("DE-T-001", path="/a", before=None, after=1,
                            recorded="2026-01-01T00:00:00+09:00"))
        two = chain(minimal("DE-T-001", path="/a", before=None, after=2,
                            recorded="2026-01-01T00:00:00+09:00"))
        self.assertNotEqual(
            project(one, "do_test")["projection_hash"],
            project(two, "do_test")["projection_hash"],
        )

    def test_empty_ledger_projects_to_empty_state(self):
        result = project([], "do_test")
        self.assertEqual(result["value"], {})
        self.assertIsNone(result["as_of_event_id"])

    def test_relative_path_is_rejected(self):
        entries = chain(
            minimal("DE-T-001", path="/a", before=None, after=1,
                    recorded="2026-01-01T00:00:00+09:00"),
        )
        entries[0].event["changes"][0]["path"] = "a"
        with self.assertRaises(ProjectionError):
            project(entries, "do_test")


class TestRealLedgerProjection(unittest.TestCase):
    """実際の Ledger の投影。

    先頭 Event の before が投影開始時の値と食い違う。これは Ledger に
    Decision Object を成立させる create Event がないためで、
    未解決の課題として ledger/README.md に記録されている。
    """

    def setUp(self):
        self.entries = load(LEDGER)

    def test_strict_projection_reports_missing_genesis(self):
        with self.assertRaises(ProjectionError) as ctx:
            project(self.entries, TRANSITION_ENGINE)
        self.assertIn("before", str(ctx.exception))

    def test_lenient_projection_yields_expected_state(self):
        result = project(self.entries, TRANSITION_ENGINE, strict=False)
        self.assertEqual(
            result["value"],
            {
                "identity": {"name": "Signity Transition Engine"},
                "architecture": {"versioning_focus": "event-centered"},
                "capture_policy": {"checkpoint_interval_minutes": 8},
            },
        )

    def test_projection_matches_documented_state_model(self):
        """docs/domain/decision-object-0001.md の state model と一致する。

        ただし lifecycle.stage と governance.human_approval_required は
        Decision Event になっていないため投影に現れない。
        """
        value = project(self.entries, TRANSITION_ENGINE, strict=False)["value"]
        self.assertNotIn("lifecycle", value)
        self.assertNotIn("governance", value)


if __name__ == "__main__":
    unittest.main()
