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

| Display ID | 日付 | 種別 | 内容 | 状態 |
| --- | --- | --- | --- | --- |
| [DE-20260710-001](2026/07/DE-20260710-001-versioning-focus-event-centered.md) | 2026-07-10 | change | バージョン管理の焦点を git-centered から event-centered へ | approved |
| [DE-20260710-002](2026/07/DE-20260710-002-capture-checkpoint-interval.md) | 2026-07-10 | change | 音声対話のチェックポイント間隔を 8 分に定める | approved |
| [DE-20260710-003](2026/07/DE-20260710-003-rename-to-transition-engine.md) | 2026-07-10 | change | プロジェクト名称を AI Company から Signity Transition Engine へ | approved |
| [DE-20260728-001](2026/07/DE-20260728-001-establish-doc-hierarchy.md) | 2026-07-28 | create | Signity のドキュメント階層を確立し、蓄積運用を開始する | **draft** |

DE-20260710-001〜003 は `signity-transition-engine-docs-v0.3.zip` からの取り込みです。
旧表示 ID（`de_aa0001` / `de_bb0001` / `de_cc0001`）から改名しましたが、内容は 1 バイトも変えていません。
対応表は [EV-20260728-002](../evidence/2026/07/EV-20260728-002-transition-engine-docs-v0.3-bundle.md) にあります。

## 未解決の矛盾

DE-20260710-003 の到達点が、v0.2 系の資料では `Signity`、v0.3 系では `Signity Transition Engine` と
食い違っています。詳細は [EV-20260728-002](../evidence/2026/07/EV-20260728-002-transition-engine-docs-v0.3-bundle.md) の「発見した矛盾」を参照してください。
独断で修正せず、決定として解消してください。

## Decision Type

| Type | 意味 |
| --- | --- |
| `create` | 対象や方針を新規に成立させる |
| `change` | 既存の属性・方針を変更する |
| `end` | 対象や方針を終了させる |
| `revert` | 過去の決定を撤回し、以前の状態へ戻す |
| `supersede` | 過去の決定を新しい決定で置き換える |
