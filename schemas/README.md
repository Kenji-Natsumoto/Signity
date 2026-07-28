# Schemas

JSON Schema とバリデーション規則を置きます。

## 正本

| Schema | 版 | 状態 |
| --- | --- | --- |
| `decision-event.schema.v0.3.json` | v0.3 | **未取り込み** — Google Drive の `signity-transition-engine-docs-v0.3.zip` 内にあります |

`docs/architecture/signity-transition-engine-architecture-v0.3.md` 8 章では、
Decision Event の Schema 正本を `schemas/decision-event.schema.v0.3.json` と定めています。
このファイルを取り込むまで、Decision Event の構造は
[`templates/decision-event.md`](../templates/decision-event.md) を暫定の基準としてください。

## 運用ルール

- Schema は破壊的変更を伴う場合、必ず `schema_version` を上げて新しいファイルを追加する。
- Schema の変更は Decision Event として `docs/decisions/` に記録する。
