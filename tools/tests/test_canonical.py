"""canonical-json-v1 の回帰テスト。

最重要のテストは test_reproduces_canonical_seed_hash。
これは 2026-07-10 時点の実装が計算した content_hash を、本実装が
バイト単位で再現できることを確認する。このテストが落ちたら、
canonical-json-v1 の規則が壊れている。
"""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import yaml

from signity.canonical import (
    CanonicalizationError,
    canonicalize,
    content_hash,
    strip_excluded,
    verify_content_hash,
)

REPO = Path(__file__).resolve().parents[2]
SEED_V03 = REPO / "seed" / "sample.de_product_rename.v0.3.yaml"
SEED_V02 = REPO / "seed" / "sample.de_signity_rename.v0.2.yaml"

#: 2026-07-10 時点の実装が計算した正本ハッシュ
CANONICAL_SEED_HASH = "f9eb852866535b176c9af8c6e9f0d9fcc18ab5950771b4969b652cd04f6acbf6"


def load_seed(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class TestCanonicalSeed(unittest.TestCase):
    """正本ハッシュとの一致（この実装の存在理由）。"""

    def test_reproduces_canonical_seed_hash(self):
        event = load_seed(SEED_V03)
        self.assertEqual(content_hash(event), CANONICAL_SEED_HASH)

    def test_seed_declares_its_own_hash_correctly(self):
        event = load_seed(SEED_V03)
        matched, recorded, actual = verify_content_hash(event)
        self.assertTrue(matched, f"記録 {recorded} != 再計算 {actual}")

    def test_v02_seed_hash_is_not_reproducible(self):
        """v0.2 の content_hash は本仕様では再現できない（既知の限界 5.3）。

        再現できるようになったら仕様書 5.3 を更新すること。
        """
        event = load_seed(SEED_V02)
        self.assertNotEqual(content_hash(event), event["integrity"]["content_hash"])


class TestExclusion(unittest.TestCase):
    """ハッシュ対象外フィールドの扱い。"""

    def base(self) -> dict:
        return {
            "title": "t",
            "integrity": {
                "algorithm": "sha256",
                "canonicalization": "canonical-json-v1",
                "previous_event_hash": None,
                "content_hash": "pending",
            },
            "signatures": [],
        }

    def test_content_hash_value_does_not_affect_hash(self):
        a, b = self.base(), self.base()
        b["integrity"]["content_hash"] = "0" * 64
        self.assertEqual(content_hash(a), content_hash(b))

    def test_signatures_do_not_affect_hash(self):
        a, b = self.base(), self.base()
        b["signatures"] = [
            {"signer_id": "actor_ken", "algorithm": "ed25519", "signature": "abc"}
        ]
        self.assertEqual(content_hash(a), content_hash(b))

    def test_previous_event_hash_does_affect_hash(self):
        """previous_event_hash は除外しない。これがチェーンを成立させる。"""
        a, b = self.base(), self.base()
        b["integrity"]["previous_event_hash"] = "a" * 64
        self.assertNotEqual(content_hash(a), content_hash(b))

    def test_canonicalization_field_does_affect_hash(self):
        """正規化方式そのものを改ざんできないようにする。"""
        a, b = self.base(), self.base()
        b["integrity"]["canonicalization"] = "canonical-json-v2"
        self.assertNotEqual(content_hash(a), content_hash(b))

    def test_excluded_keys_are_removed_not_nulled(self):
        stripped = strip_excluded(self.base())
        self.assertNotIn("signatures", stripped)
        self.assertNotIn("content_hash", stripped["integrity"])

    def test_input_is_not_mutated(self):
        event = self.base()
        before = json.dumps(event, sort_keys=True)
        content_hash(event)
        self.assertEqual(json.dumps(event, sort_keys=True), before)


class TestSerialization(unittest.TestCase):
    """直列化規則。"""

    def test_keys_are_sorted(self):
        self.assertEqual(canonicalize({"b": 1, "a": 2}), b'{"a":2,"b":1}')

    def test_key_order_in_input_does_not_matter(self):
        self.assertEqual(content_hash({"a": 1, "b": 2}), content_hash({"b": 2, "a": 1}))

    def test_no_insignificant_whitespace(self):
        out = canonicalize({"a": [1, 2], "b": {"c": 3}})
        self.assertEqual(out, b'{"a":[1,2],"b":{"c":3}}')

    def test_non_ascii_is_literal(self):
        out = canonicalize({"t": "名称を変更する"})
        self.assertEqual(out, '{"t":"名称を変更する"}'.encode("utf-8"))
        self.assertNotIn(b"\\u", out)

    def test_array_order_is_preserved(self):
        self.assertNotEqual(content_hash({"a": [1, 2]}), content_hash({"a": [2, 1]}))

    def test_no_trailing_newline(self):
        self.assertFalse(canonicalize({"a": 1}).endswith(b"\n"))

    def test_utf8_encoded(self):
        self.assertEqual(canonicalize({"t": "あ"}), b'{"t":"\xe3\x81\x82"}')

    def test_control_characters_use_short_escapes(self):
        self.assertEqual(canonicalize({"t": "a\nb"}), b'{"t":"a\\nb"}')

    def test_quote_and_backslash_escaped(self):
        self.assertEqual(canonicalize({"t": '"\\'}), b'{"t":"\\"\\\\"}')

    def test_null_is_distinct_from_missing(self):
        self.assertNotEqual(content_hash({"a": 1, "b": None}), content_hash({"a": 1}))

    def test_number_formatting(self):
        self.assertEqual(canonicalize({"a": 8}), b'{"a":8}')
        self.assertEqual(canonicalize({"a": 0.95}), b'{"a":0.95}')

    def test_bool_is_not_number(self):
        self.assertNotEqual(content_hash({"a": True}), content_hash({"a": 1}))

    def test_deterministic_across_calls(self):
        event = load_seed(SEED_V03)
        self.assertEqual(
            {content_hash(copy.deepcopy(event)) for _ in range(20)},
            {CANONICAL_SEED_HASH},
        )


class TestRejections(unittest.TestCase):
    """正規化できない入力。"""

    def test_non_dict_rejected(self):
        for bad in ([], "x", 1, None):
            with self.assertRaises(CanonicalizationError):
                canonicalize(bad)

    def test_nan_rejected(self):
        with self.assertRaises(CanonicalizationError):
            canonicalize({"a": float("nan")})

    def test_infinity_rejected(self):
        with self.assertRaises(CanonicalizationError):
            canonicalize({"a": float("inf")})


class TestTamperDetection(unittest.TestCase):
    """1 文字の改変が検知されること。"""

    def test_single_character_change_is_detected(self):
        event = load_seed(SEED_V03)
        original = content_hash(event)
        tampered = copy.deepcopy(event)
        tampered["changes"][0]["after"] = "Signity Transition Enginе"  # 末尾がキリル文字 е
        self.assertNotEqual(content_hash(tampered), original)

    def test_recorded_hash_detects_field_edit(self):
        event = load_seed(SEED_V03)
        event["title"] = event["title"] + "（改変）"
        matched, _, _ = verify_content_hash(event)
        self.assertFalse(matched)

    def test_reordering_evidence_refs_is_detected(self):
        event = load_seed(SEED_V03)
        original = content_hash(event)
        event["evidence_refs"] = list(reversed(event["evidence_refs"]))
        self.assertNotEqual(content_hash(event), original)


if __name__ == "__main__":
    unittest.main()
