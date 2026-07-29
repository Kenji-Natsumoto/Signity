"""canonical-json-v1: Decision Event の正規化と content_hash の計算。

仕様は docs/architecture/canonical-json-v1.md（正本）。
本モジュールはその参照実装であり、仕様と実装が食い違った場合は仕様を正とする。

canonical-json-v1 は凍結されている。規則を変えると過去のすべての
content_hash が無効になるため、変更する場合は canonical-json-v2 を
新設し、Event の integrity.canonicalization で判別できるようにする。
"""

from __future__ import annotations

import copy
import hashlib
import json

CANONICALIZATION = "canonical-json-v1"
ALGORITHM = "sha256"

#: ハッシュ計算から除外するフィールド。
#: integrity.content_hash は自分自身のハッシュなので含めると循環する。
#: signatures はハッシュ確定後に付与されるので含めると署名追加で値が変わる。
#: integrity.previous_event_hash は「除外しない」。これがチェーンを成立させる。
EXCLUDED = ("signatures", "integrity.content_hash")


class CanonicalizationError(ValueError):
    """正規化できない入力が与えられた。"""


def strip_excluded(event: dict) -> dict:
    """ハッシュ対象外フィールドをキーごと削除したコピーを返す。

    None を代入するのではなく削除する。{"signatures": None} と
    signatures なしは別のバイト列になるため。
    """
    e = copy.deepcopy(event)
    e.pop("signatures", None)
    integrity = e.get("integrity")
    if isinstance(integrity, dict):
        integrity.pop("content_hash", None)
    return e


def canonicalize(event: dict) -> bytes:
    """canonical-json-v1 のバイト列を返す。

    - オブジェクトのキーは Unicode コードポイント昇順
    - 区切りは "," と ":" のみ（余分な空白なし）
    - 非 ASCII はそのまま出力（\\uXXXX へエスケープしない）
    - UTF-8、末尾改行なし
    """
    if not isinstance(event, dict):
        raise CanonicalizationError(
            f"Event はオブジェクトでなければならない: {type(event).__name__}"
        )
    stripped = strip_excluded(event)
    try:
        text = json.dumps(
            stripped,
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
            allow_nan=False,
        )
    except ValueError as exc:
        # NaN / Infinity は JSON で表現できない
        raise CanonicalizationError(f"正規化できない値が含まれている: {exc}") from exc
    return text.encode("utf-8")


def content_hash(event: dict) -> str:
    """Event の content_hash（小文字 16 進 64 文字）を返す。"""
    return hashlib.sha256(canonicalize(event)).hexdigest()


def verify_content_hash(event: dict) -> tuple[bool, str, str]:
    """(一致したか, 記録されている値, 再計算した値) を返す。

    記録値が "pending"（未確定の Draft）の場合は一致とみなさない。
    """
    recorded = ""
    integrity = event.get("integrity")
    if isinstance(integrity, dict):
        recorded = integrity.get("content_hash") or ""
    actual = content_hash(event)
    return (recorded == actual, recorded, actual)
