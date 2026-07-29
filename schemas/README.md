# Schemas

JSON Schema とバリデーション規則を置きます。

## 正本

| Schema | 版 | 状態 | SHA-256 |
| --- | --- | --- | --- |
| [`decision-event.schema.v0.3.json`](decision-event.schema.v0.3.json) | v0.3 | 現行 | `a31341f5…11ff995f3` |

`docs/architecture/signity-transition-engine-architecture-v0.3.md` 8 章が定める
Decision Event の Schema 正本です。`signity-transition-engine-docs-v0.3.zip` から取り込み、
MANIFEST の SHA-256 と一致することを確認しています（[EV-20260728-002](../docs/evidence/2026/07/EV-20260728-002-transition-engine-docs-v0.3-bundle.md)）。

再検証:

```sh
./scripts/verify-manifest.sh
```

## v0.3 の必須フィールド

```text
schema_version, event_id, event_kind, status, primary_object_id,
title, occurred_at, recorded_at, changes, rationale, proposed_by,
evidence_refs, model_run_refs, integrity, decision_type
```

`additionalProperties: false` のため、定義外のフィールドは検証に通りません。
`event_kind` は `"decision"` 固定です（他の Ledger Event 種別は v0.3 の Schema 対象外）。

## 運用ルール

- Schema は破壊的変更を伴う場合、必ず `schema_version` を上げて新しいファイルを追加する。
- Schema の変更は Decision Event として `docs/decisions/` に記録する。
- 過去版の Schema ファイルを削除しない。
