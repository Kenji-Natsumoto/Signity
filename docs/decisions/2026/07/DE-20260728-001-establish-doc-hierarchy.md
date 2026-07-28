# DE-20260728-001: Signity のドキュメント階層を確立し、蓄積運用を開始する

> 承認後はこのファイルを編集しないでください。
> 訂正が必要な場合は `corrects_event_id` を持つ新しい Correction Event を作成します。

```yaml
schema_version: "0.3"
event_id: de_20260728_establish_doc_hierarchy
display_id: DE-20260728-001
event_kind: decision
decision_type: create
status: draft                   # 人間の承認後に approved へ変更する
primary_object_id: do_signity_umbrella
affected_object_ids:
  - do_20260710_001_signity_transition_engine
title: Signity リポジトリにドキュメント階層を確立し、日次の蓄積運用を開始する
occurred_at: "2026-07-28T10:16:12+09:00"
recorded_at: "2026-07-28T10:16:12+09:00"
approved_at: null
effective_at: "2026-07-28T00:00:00+09:00"
changes:
  - path: /documentation/repository
    before: null
    after: Kenji-Natsumoto/Signity
    change_note: 空のリポジトリをドキュメント正本置き場として確立する
  - path: /documentation/hierarchy
    before: null
    after: docs/{architecture,product,domain,decisions,evidence,journal,development}
    change_note: README (1).md の構成に evidence/ と journal/ を追加
  - path: /documentation/accumulation_policy
    before: ad-hoc
    after: daily-journal-to-decision-event
    change_note: journal → evidence → decisions の一方向フローで日次に蓄積する
rationale:
  decision_question: Signity のドキュメントをどこに、どの階層で、どう蓄積していくか
  summary: >
    設計文書が Google Drive 上に散在しており、版と正本の所在が追えなくなっていた。
    Signity 自身が「意思決定を追記型イベントとして蓄積する Decision OS」である以上、
    そのドキュメント管理も同じ原則（追記のみ・Current State は投影・人間承認必須）に
    従うべきと判断した。
  facts:
    - Kenji-Natsumoto/Signity リポジトリは 2026-07-28 時点でコミット 0 件の空リポジトリだった
    - 設計文書 5 点と zip 2 点が Google Drive 上に存在していた
    - README (1).md に想定リポジトリ構成が既に記述されていた
  assumptions:
    - このリポジトリは umbrella brand Signity の正本であり、
      signity-transition-engine は将来別リポジトリへ分離しうる
    - 日次の蓄積は人間が journal を起点に行う
  options_considered:
    - Google Drive をそのまま正本として継続する
    - README (1).md の構成をそのまま採用する
    - README (1).md の構成に evidence/ と journal/ を追加する
  human_value_judgments:
    - 正本の所在が一意であること
    - 蓄積の流れが一方向であること
    - Signity 自身の思想とドキュメント運用が一致していること
  tradeoffs:
    - Drive と Git の二重管理が一時的に発生する
    - 日次 journal の作成が運用負荷になる
  revisit_triggers:
    - signity-transition-engine を別リポジトリへ分離するとき
    - schemas/decision-event.schema.v0.3.json を取り込んだとき
    - 日次 journal の運用が 2 週間継続できなかったとき
  confidence: null
proposed_by:
  - actor_ken
  - agent_claude
approved_by: []
evidence_refs:
  - ev_20260728_drive_design_documents
model_run_refs: []
expected_outcome:
  summary: Signity に関する文書の所在が一意に定まり、意思決定が日次で追跡可能になる
  review_due_at: "2026-08-11T00:00:00+09:00"
  success_metrics:
    - 2 週間で journal が 10 営業日分蓄積されている
    - 新規の設計変更が Decision Event として記録されている
supersedes_event_id: null
corrects_event_id: null
integrity:
  algorithm: sha256
  canonicalization: canonical-json-v1
  previous_event_hash: null    # Ledger 最初のイベント
  content_hash: null           # canonical-json-v1 の実装後に計算する
signatures: []
```

## 背景

Signity の設計文書（Decision OS v0.2、Transition Engine v0.3、Codex ハンドオフ、
シードデータ）は 2026-07-10 に作成され、Google Drive 上に置かれていた。
`Kenji-Natsumoto/Signity` リポジトリは作成済みだったが、2026-07-28 時点でコミットは 0 件だった。

この状態では、どの文書が正本か、どの版が現行かを追跡できない。

## 決定内容

`Kenji-Natsumoto/Signity` を Signity のドキュメント正本置き場とし、
次の階層で今日からドキュメントを蓄積する。

```text
docs/
├── architecture/    確定した設計文書（バージョン付き・過去版を残す）
├── product/         プロダクト定義・コンセプト・スコープ
├── domain/          ドメインモデル・Decision Object の定義
├── decisions/       承認済み Decision Event（編集不可）
├── evidence/        意思決定の根拠となった一次資料（編集不可）
├── journal/         日次ログ（未整理の素材・観測）
└── development/     開発手順・ハンドオフ・運用
```

情報は常に一方向に流れる。

```text
journal/ → evidence/ → decisions/ → architecture/ product/ domain/
```

## 検討した選択肢

| 選択肢 | 採否 | 理由 |
| --- | --- | --- |
| Google Drive を正本として継続 | 見送り | 版管理と差分追跡ができず、正本の所在が曖昧になる |
| `README (1).md` の構成をそのまま採用 | 部分採用 | 骨格は妥当だが、日次の蓄積導線と根拠の保存場所がない |
| 上記に `evidence/` と `journal/` を追加 | **採用** | Signity のアーキテクチャ（Evidence → Decision Event）と階層が一致する |

## 根拠 (Evidence)

- [EV-20260728-001](../../../evidence/2026/07/EV-20260728-001-drive-design-documents.md): Google Drive 上の Signity 設計文書一式

## 影響

- Signity に関する文書の正本は今後このリポジトリになる
- Google Drive 上の文書は Evidence（出典）として扱う
- 設計変更は Decision Event として記録してから確定文書へ反映する
- `docs/README.md` と `AGENTS.md` が運用ルールの正本になる

## 見直しの契機

- `signity-transition-engine` を別リポジトリへ分離するとき
- `schemas/decision-event.schema.v0.3.json` を取り込んだとき
- 日次 journal の運用が 2 週間継続できなかったとき（2026-08-11 に確認）

## 未完了事項

1. `signity-transition-engine-docs-v0.3.zip` から
   `schemas/decision-event.schema.v0.3.json` と
   `seed/sample.de_product_rename.v0.3.yaml` を取り込む
2. `signity_ui_wireframe_ja_bundle.zip` の取り込み要否を判断する
3. `docs/product/concept-v0.1.md` と `docs/domain/decision-object-0001.md` を作成する
4. `canonical-json-v1` を実装し、本 Event の `content_hash` を計算する
5. 本 Event を承認し、`status` を `approved`、`approved_at` を記入する
