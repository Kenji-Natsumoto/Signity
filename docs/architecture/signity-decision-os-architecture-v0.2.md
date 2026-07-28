# Signity Decision OS
## 意思決定イベント駆動アーキテクチャ v0.2（設計レビュー統合版）

- Status: Draft for validation
- Date: 2026-07-10
- Authors: 夏本健司 / AIエージェント・ROJINA
- Source documents:
  - `260710STRADE.txt`
  - `260710Decision Object0001.txt`
  - `260710de_aa0001.txt`
  - `260710de_bb0001.txt`
  - `260710de_cc0001.txt`

---

## 1. 一文で表す思想

> 組織はドキュメントではなく、採用された意思決定と、その根拠・実行・結果の連鎖によってバージョン管理される。

Signityは、会議・対話・Slack・文書・AIエージェントの出力などに分散した情報から、組織として採用された認識・方針・コミットメントの変化を検出し、追記型のイベントとして記録するDecision OSである。

### 重要な表現修正

「社長や役員の意識の状態を検出する」ではなく、次のように定義する。

> 人間の内面を推測するのではなく、外部化された発言・承認・文書・行動から、組織として採用された認識・方針・コミットメントの変化を検出する。

---

## 2. コア概念

### 2.1 Decision Object

意思決定によって状態やコミットメントが変化する対象の、永続的な識別子。

例:

- Project: Signity
- Policy: GPT Live会話のチェックポイント運用
- Strategy: AI 95% / Human 5% 経営モデル
- Product: VibeRush
- Organization: Sprint Japan

Decision Objectは「対象」を表し、履歴そのものは持たない。現在状態はイベント列から計算する。

### 2.2 Ledger Event

追記専用・承認後は不変のイベント封筒。すべての履歴はこの共通形式で保存する。

`event_kind` は最低限、次の5種類とする。

1. `decision`: 方針・選択・コミットメントを承認した
2. `observation`: 外部事実や新しい証拠を確認した
3. `action`: 決定に基づく実行を行った
4. `outcome`: 実行結果・指標・学びを確認した
5. `correction`: 過去のイベントを訂正・撤回・置換した

Decision EventはLedger Eventの一種であり、すべての状態変化を無理に「意思決定」と呼ばない。

### 2.3 Evidence Record

意思決定を支えた出典を表す。Slack、会議、ChatGPT Live、文書、音声、手入力、コード変更などを同じ形式で参照できるようにする。

Evidenceは次の3方式を許容する。

- `reference`: 元データへの参照のみ
- `snapshot`: その時点の内容を保存し、ハッシュを付ける
- `attestation`: 録音等がない対面会議について、人間が「こう話し、こう決めた」と証言する

### 2.4 Actor / Agent / Model Run

次の3つを分離する。

- Actor: 夏本健司など、責任主体
- Agent: ROJINA、春本など、永続的なAI役割・設定
- Model Run: その1回の処理に実際に使われたモデル、ツール、プロンプト構成

これにより、ROJINAというAgentを維持したまま、GPT、Claude、Codexなどの実行モデルを交換できる。

### 2.5 Model Profile

AIモデルの特性は各Decision Eventに長文で重複記録せず、バージョン管理されたModel Profileに保存し、Eventから参照する。

Model Profileの例:

- provider
- user-visible model label
- verified runtime model ID（取得できる場合）
- profile version
- known strengths / limitations
- valid_from / valid_to
- information source
- profile hash

ユーザー画面の表示名と、実際のランタイムIDが同一とは限らないため、`observed_label` と `verified_runtime_id` を分ける。

---

## 3. 状態モデル

### 3.1 Current Stateは手入力しない

`Current State` はイベントの入力項目ではなく、承認済みイベントを時系列に適用して得る計算結果（Projection）とする。

Objectファイルに表示する場合も、次を付けて自動生成する。

- `as_of_event_id`
- `calculated_at`
- `projection_hash`

### 3.2 Stateは単一ラベルではなく構造化する

`Concept` / `Prototype` だけではなく、対象ごとに複数の状態軸を持つ。

例: Signity Project

```yaml
state:
  identity:
    name: Signity
  lifecycle:
    stage: concept
  architecture:
    versioning_focus: decision-event-centered
  governance:
    human_approval_required: true
```

名称変更は `/identity/name` の変更であり、必ずしも `/lifecycle/stage` の変更ではない。

### 3.3 Committed StateとObserved Stateを分ける

承認したことと、現実に実行・達成されたことは同一ではない。

- `committed_state`: 組織が承認した方針・予定・コミットメント
- `observed_state`: 現実に確認できた実行状況・結果

Decision Eventは主にCommitted Stateを変更し、Action / Outcome / Observation EventはObserved Stateを更新する。

---

## 4. Decision Eventを作る条件

AIは会話のすべてをDecision Eventにしない。次のいずれかを満たすものを候補化する。

1. Decision Objectの属性・方針・ライフサイクルが変わる
2. 人・予算・時間・権限などの資源配分を確定する
3. 新しい方針・ルール・責任を成立させる
4. 過去の意思決定を置換・撤回・復元する
5. 後日、説明責任を求められる可能性があるコミットメントを行う

単なるアイデア、質問、検討途中の発言はEvidenceまたはProposalとして残し、承認されるまで確定Eventにしない。

### 基本のDecision Type

- `create`
- `change`
- `end`
- `revert`
- `supersede`

---

## 5. 承認フロー

```text
情報取得
  ↓
状態遷移候補の検出
  ↓
Draft Eventの生成
  ↓
根拠・差分・提案理由の提示
  ↓
人間による承認 / 却下 / 修正
  ↓
正規化されたEventをLedgerへ追記
  ↓
ハッシュ計算・署名
  ↓
State Projectionを再計算
  ↓
実行エージェントへ連携
  ↓
Action / Outcomeを再びLedgerへ返す
```

MVPでは、承認済みLedgerへ書き込めるのは人間のみとする。AI承認は、権限範囲・上限・有効期限・監査ルールを別途定義してから導入する。

---

## 6. ハッシュと署名

### 6.1 用語を分ける

- `content_hash`: 内容が変わっていないことを検証するSHA-256等のハッシュ
- `hash_chain`: 直前Eventのハッシュを次のEventに含め、削除・差し替えを検知しやすくする仕組み
- `digital_signature`: 誰が承認したかを秘密鍵・公開鍵で検証する署名
- `trusted_timestamp`: その時刻以前に存在したことを外部に証明する時刻アンカー

ハッシュだけでは「誰が承認したか」は証明できない。また、「改ざん不能」ではなく「改ざん検知可能」と表現する。

### 6.2 MVPの順序

1. canonical JSONを生成
2. hash対象外フィールドを除外
3. SHA-256で `content_hash` を計算
4. `previous_event_hash` を保存
5. 承認者IDと承認時刻を記録
6. 後続版でデジタル署名を追加

承認後のEventは編集せず、訂正は新しいCorrection Eventで行う。

---

## 7. IDと時刻

### ID

機械用IDと人間用表示IDを分ける。

- Machine ID: ULIDまたはUUIDv7などの衝突しにくいID
- Display ID: `DE-20260710-003` のような読みやすい番号

`aa` / `bb` / `cc` は表示用エイリアスとして残せるが、属性や意味をID自体に埋め込みすぎない。

### 時刻

次を分け、ISO 8601とタイムゾーンを必須にする。

- `occurred_at`: 実際に意思決定が起きた時刻
- `recorded_at`: システムへ登録した時刻
- `approved_at`: 承認した時刻
- `effective_at`: 決定が効力を持つ時刻

例: `2026-07-10T15:30:00+09:00`

---

## 8. 最小データモデル

### Decision Object

```yaml
schema_version: "0.2"
object_id: do_01...
display_id: DO-20260710-001
object_type: project
name: Signity
purpose: AIネイティブ企業のためのDecision OSを実現する
owner_actor_ids:
  - actor_ken
parent_object_id: null
created_event_id: de_01...
originated_at: 2026-01-05T00:00:00+09:00
recorded_at: 2026-07-10T16:16:00+09:00
```

### Decision Event

```yaml
schema_version: "0.2"
event_id: de_01...
display_id: DE-20260710-003
event_kind: decision
decision_type: change
status: approved
primary_object_id: do_01...
affected_object_ids: []
title: プロジェクト名をAI CompanyからSignityへ変更する
occurred_at: 2026-07-10T15:30:00+09:00
recorded_at: 2026-07-10T16:20:00+09:00
approved_at: 2026-07-10T15:30:00+09:00
effective_at: 2026-07-10T15:30:00+09:00
changes:
  - path: /identity/name
    before: AI Company
    after: Signity
rationale:
  summary: 仕組みと思想が定義され、固有のブランド名が必要になったため
  human_value_judgments:
    - 固有性
    - 長期的なブランド資産
  assumptions: []
  options_considered: []
proposed_by:
  - actor_ken
  - agent_rojina
approved_by:
  - actor_ken
evidence_refs:
  - ev_01...
model_run_refs:
  - mr_01...
expected_outcome:
  summary: 固有ブランドとして一貫して認識・使用される
  review_due_at: null
supersedes_event_id: null
corrects_event_id: null
integrity:
  algorithm: sha256
  canonicalization: canonical-json-v1
  previous_event_hash: null
  content_hash: <computed-sha256>
signatures: []
```

---

## 9. 現行5ファイルの移行方針

### Decision Object 0001

- `作成日` を、対象そのものの開始日とレコード作成日に分ける
- `現在の状態` は手入力から削除し、自動Projectionへ移す
- Signityが2026-01-05から存在したなら、`originated_at` をその日にする
- `created_event_id` を持たせる

### de_aa0001

- `Current State` を削除する
- 変更を構造化する:
  - path: `/architecture/versioning_focus`
  - before: `git-centered`
  - after: `decision-event-centered`
- 主対象はSignity Projectでもよいが、Architecture Objectを分ける余地を残す

### de_bb0001

空欄を次のように埋める。

- 変更:
  - path: `/capture_policy/checkpoint_interval_minutes`
  - before: `null` または `ad-hoc`
  - after: `8`
- これはSignity Projectそのものより、`Policy: GPT Live Decision Capture` を別Objectにする方が自然
- 8分ごとの会話ログはEvidenceであり、毎回Decision Eventではない

### de_cc0001

- 変更対象は `/identity/name`
- `Concept → Prototype` の変更ではないため、Lifecycleを同時変更しない
- Lifecycle変更が本当に起きたなら、別のDecision Eventとして記録する

### STRADE v0.1

次を修正する。

- 「意識」→「外部化された認識・方針・コミットメント」
- 「改ざん不能」→「改ざん検知可能」
- `Decision Event` だけでなくEvidence / Action / Outcomeを区別
- `Current State` はEventから計算するProjectionと明記
- AIモデルの特性はModel Profileへ分離
- AI承認はMVP外、人間承認を必須にする

---

## 10. Codexで作るMVP

### MVPで入れるもの

1. Decision Objectの作成
2. 会話または手入力からDraft Decision Eventを生成
3. Before / After差分の表示
4. Evidence参照の登録
5. 人間のApprove / Reject / Edit
6. 承認Eventの追記保存
7. SHA-256ハッシュチェーン
8. Current Stateの自動Projection
9. Markdown / JSONエクスポート
10. Event検索と「なぜ現在こうなっているか」の説明

### MVPで入れないもの

- Git互換実装
- 自動マージ
- 複数AIによる自律承認
- ブロックチェーン
- Slackや会議録の全自動常時監視
- 高度な権限管理
- モデル特性の自動評価

### 推奨ストレージ

Gitを再実装せず、最初は次で十分。

- append-only Event Store: SQLiteまたはPostgreSQL
- Evidence snapshot: ローカルまたはオブジェクトストレージ
- Projection: DBテーブルまたは再計算可能なキャッシュ
- Human-readable export: Markdown / YAML

Gitはエクスポート先またはバックアップとして使えるが、ドメインの中心には置かない。

---

## 11. Codex着手条件

次の5点が合意できれば、実装開始可能。

1. EventをDecision / Observation / Action / Outcome / Correctionに分ける
2. Current Stateを手入力せずProjectionにする
3. Committed StateとObserved Stateを分ける
4. MVPでは人間承認を必須にする
5. ハッシュと署名を別概念として扱う

この条件が固まれば、次はCodex向けに以下を生成する。

- Product Requirements Document
- Repository structure
- JSON Schema / validation rules
- API contract
- SQLite schema
- acceptance tests
- seed data from the three current Decision Events
