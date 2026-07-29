"""decision-event.schema.v0.3.json に対する検証。

外部依存を持たないため、JSON Schema の**部分実装**である。
schemas/decision-event.schema.v0.3.json が実際に使っているキーワードだけを
サポートする。汎用の JSON Schema バリデータではない。

サポートするキーワード:
  type, const, enum, required, properties, additionalProperties,
  items, minItems, minLength, uniqueItems, pattern, minimum, maximum,
  format(date-time のみ), allOf, if/then

未対応のキーワードがスキーマに現れた場合は例外を投げる（黙って無視しない）。
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

SUPPORTED = {
    "$schema", "$id", "title", "default", "description",
    "type", "const", "enum", "required", "properties", "additionalProperties",
    "items", "minItems", "minLength", "uniqueItems", "pattern",
    "minimum", "maximum", "format", "allOf", "if", "then",
}

_TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "null": type(None),
}


class SchemaUnsupported(Exception):
    """スキーマがこの部分実装の範囲外のキーワードを使っている。"""


def load_schema(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _is_type(value, name: str) -> bool:
    expected = _TYPES[name]
    if name == "number":
        # JSON では bool は数値ではない
        return isinstance(value, expected) and not isinstance(value, bool)
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    return isinstance(value, expected)


def _is_date_time(value: str) -> bool:
    try:
        datetime.fromisoformat(value)
    except ValueError:
        return False
    # タイムゾーンを必須にする（architecture v0.3 7章）
    return datetime.fromisoformat(value).tzinfo is not None


def _check(schema: dict, value, path: str, errors: list[str]) -> None:
    unknown = set(schema) - SUPPORTED
    if unknown:
        raise SchemaUnsupported(
            f"{path or '/'}: 未対応のキーワード {sorted(unknown)}"
        )

    loc = path or "/"

    if "const" in schema and value != schema["const"]:
        errors.append(f"{loc}: {schema['const']!r} でなければならない（実際: {value!r}）")

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{loc}: {schema['enum']} のいずれかでなければならない（実際: {value!r}）")

    if "type" in schema:
        names = schema["type"]
        if isinstance(names, str):
            names = [names]
        if not any(_is_type(value, n) for n in names):
            errors.append(f"{loc}: 型は {names}（実際: {type(value).__name__}）")
            return  # 型が違えば以降の検査は無意味

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{loc}: {schema['minLength']} 文字以上必要（実際: {len(value)}）")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{loc}: パターン {schema['pattern']} に一致しない（実際: {value!r}）")
        if schema.get("format") == "date-time" and not _is_date_time(value):
            errors.append(f"{loc}: ISO 8601 のタイムゾーン付き日時が必要（実際: {value!r}）")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{loc}: {schema['minimum']} 以上（実際: {value}）")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{loc}: {schema['maximum']} 以下（実際: {value}）")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{loc}: {schema['minItems']} 要素以上必要（実際: {len(value)}）")
        if schema.get("uniqueItems"):
            seen = [json.dumps(v, sort_keys=True, ensure_ascii=False) for v in value]
            if len(set(seen)) != len(seen):
                errors.append(f"{loc}: 要素が重複している")
        if "items" in schema:
            for i, item in enumerate(value):
                _check(schema["items"], item, f"{path}/{i}", errors)

    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{loc}: 必須フィールド {key!r} がない")
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in props:
                    errors.append(f"{loc}: 未定義のフィールド {key!r}（additionalProperties: false）")
        for key, subschema in props.items():
            if key in value:
                _check(subschema, value[key], f"{path}/{key}", errors)

    for sub in schema.get("allOf", []):
        _check(sub, value, path, errors)

    if "if" in schema:
        probe: list[str] = []
        _check(schema["if"], value, path, probe)
        if not probe and "then" in schema:
            _check(schema["then"], value, path, errors)


def validate(event: dict, schema: dict) -> list[str]:
    """スキーマ違反のメッセージ一覧を返す。空なら適合。"""
    errors: list[str] = []
    _check(schema, event, "", errors)
    return errors
