# Decisions

承認済みの Decision Event を保存します。
このディレクトリは**人間向けの記録**、[`ledger/`](../../ledger/) が**機械可読な正本**です。

## 絶対の原則

- **承認済みイベントを編集・削除しない。**
- 訂正が必要な場合は、`corrects_event_id` を持つ新しい Correction Event を追加する。
- 置換する場合は `supersedes_event_id` を持つ新しい Event を追加する。

Git の履歴と、この Ledger は別物です。Git は「ファイルを書いた記録」、
Decision Event は「組織が承認した記録」です。

## 配置と命名

```text
docs/decisions/YYYY/MM/DE-YYYYMMDD-NNN-<slug>.md   # 人間向け
ledger/events/NNNN-DE-YYYYMMDD-NNN.json            # 機械可読・ハッシュチェーン
```

ひな形: [`templates/decision-event.md`](../../templates/decision-event.md)

## 索引

| Display ID | 日付 | 種別 | 内容 | 状態 | Ledger |
| --- | --- | --- | --- | --- | --- |
| [DE-20260710-001](2026/07/DE-20260710-001-versioning-focus-event-centered.md) | 2026-07-10 | change | versioning_focus を git-centered → event-centered | approved | `0002` |
| [DE-20260710-002](2026/07/DE-20260710-002-capture-checkpoint-interval.md) | 2026-07-10 | change | チェックポイント間隔を 8 分に定める | approved | `0003` |
| [DE-20260710-003](2026/07/DE-20260710-003-rename-to-transition-engine.md) | 2026-07-10 | change | 名称を AI Company → Signity Transition Engine | approved | `0001` |
| [DE-20260728-001](2026/07/DE-20260728-001-establish-doc-hierarchy.md) | 2026-07-28 | create | ドキュメント階層を確立し、蓄積運用を開始する | **draft** | pending |
| [DE-20260728-002](2026/07/DE-20260728-002-canonical-json-v1.md) | 2026-07-29 | create | canonical-json-v1 を確定・凍結する | **draft** | pending |

Ledger 列は `ledger/events/` の連番です。連番と Display ID の番号が一致しないのは、
連番が**追記順**、Display ID が**発生日の連番**だからです。
DE-20260710-003 は正本シードとして先に機械可読化されていたため、追記順では先頭になります。

## 検証

```sh
./scripts/signity verify   # content_hash とチェーンの整合性
./scripts/signity chain    # チェーンの一覧
```

## 未解決の矛盾・課題

- **DE-20260710-003 の到達点**が v0.2 系では `Signity`、v0.3 系では `Signity Transition Engine` と
  食い違っています。詳細は [EV-20260728-002](../evidence/2026/07/EV-20260728-002-transition-engine-docs-v0.3-bundle.md)。
- **Decision Object を成立させる `create` Event がありません。**
  先頭 Event の `before` が Ledger 開始前の状態を指しており、strict モードの投影が失敗します。
  詳細は [`ledger/README.md`](../../ledger/README.md) の「未解決の課題」。
- **evidence_refs 2 件が解決しません。** 2026-07-10 の ChatGPT Live 対話と朝のブリーフィングが
  Evidence として保存されていません。

いずれも独断で修正せず、決定として解消してください。

## Decision Type

| Type | 意味 |
| --- | --- |
| `create` | 対象や方針を新規に成立させる |
| `change` | 既存の属性・方針を変更する |
| `end` | 対象や方針を終了させる |
| `revert` | 過去の決定を撤回し、以前の状態へ戻す |
| `supersede` | 過去の決定を新しい決定で置き換える |
