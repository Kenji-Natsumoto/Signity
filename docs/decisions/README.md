# Decisions

承認済みの Decision Event を保存する追記型 Ledger です。

## 絶対の原則

- **承認済みイベントを編集・削除しない。**
- 訂正が必要な場合は、`corrects_event_id` を持つ新しい Correction Event を追加する。
- 置換する場合は `supersedes_event_id` を持つ新しい Event を追加する。

Git の履歴と、この Ledger は別物です。Git は「ファイルを書いた記録」、
Decision Event は「組織が承認した記録」です。

## 配置と命名

```text
docs/decisions/YYYY/MM/DE-YYYYMMDD-NNN-<slug>.md
```

ひな形: [`templates/decision-event.md`](../../templates/decision-event.md)

## 索引

| Display ID | 日付 | 種別 | 内容 |
| --- | --- | --- | --- |
| [DE-20260728-001](2026/07/DE-20260728-001-establish-doc-hierarchy.md) | 2026-07-28 | create | Signity のドキュメント階層を確立し、蓄積運用を開始する |

## Decision Type

| Type | 意味 |
| --- | --- |
| `create` | 対象や方針を新規に成立させる |
| `change` | 既存の属性・方針を変更する |
| `end` | 対象や方針を終了させる |
| `revert` | 過去の決定を撤回し、以前の状態へ戻す |
| `supersede` | 過去の決定を新しい決定で置き換える |
