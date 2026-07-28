# Signity Transition Engine
## 状態遷移イベント駆動アーキテクチャ v0.3

- Status: Draft for implementation validation
- Date: 2026-07-10
- Authors: 夏本健司 / AIエージェント・ROJINA
- Product owner: 夏本健司

---

## 1. Product definition

Signity Transition Engineは、会議、対話、Slack、文書、承認操作、業務行動、AIエージェント出力などに外部化された情報から、組織として採用される可能性のある状態変化を検出し、根拠付きのイベント候補へ構造化する。

MVPでは、人間が候補を確認・修正・承認した後に、追記型Ledgerへ保存する。

> 人間の代わりに意思決定するのではなく、人間が変化を認識し、説明し、責任を持って承認できる状態を作る。

人間の内面を推測せず、外部化された発言、承認、文書、行動を入力として扱う。

---

## 2. Core concepts

### 2.1 Decision Object

状態やコミットメントが変化する対象の永続的な識別子。

例:

- Project: Signity Transition Engine
- Policy: 音声対話のチェックポイント運用
- Strategy: AI活用型経営モデル
- Product: VibeRush
- Organization: Sprint Japan

Decision Objectは対象を表す。現在状態は承認済みイベント列から計算する。

### 2.2 Ledger Event

追記専用のイベント封筒。承認後は内容を変更しない。

`event_kind` は最低限、次を扱う。

1. `decision`: 方針、選択、コミットメントを承認した
2. `observation`: 外部事実や新しい証拠を確認した
3. `action`: 決定に基づく実行を行った
4. `outcome`: 実行結果、指標、学びを確認した
5. `correction`: 過去イベントを訂正、撤回、置換した

### 2.3 Evidence Record

イベントの根拠となる情報。

- `reference`: 元情報への参照
- `snapshot`: その時点の内容を保存しハッシュ化
- `attestation`: 録音等がない場合の人間による証言

### 2.4 Actor / Agent / Model Run

- Actor: 夏本健司など、責任を持つ主体
- Agent: ROJINAなど、永続するAI役割・設定
- Model Run: その処理で使用したモデル、ツール、プロンプト構成

Agentと実行モデルを分けることで、モデルを変更しても同じ役割とデータ構造を維持できる。

### 2.5 Model Profile

モデル特性をイベントごとに重複記録せず、バージョン管理されたProfileへ保存する。

- provider
- observed_label
- verified_runtime_id
- profile_version
- strengths
- limitations
- valid_from / valid_to
- information_source
- profile_hash

---

## 3. State model

### 3.1 Current State is a projection

Current Stateは入力項目ではない。承認済みイベントを決定的な順序で適用した計算結果とする。

```yaml
current_state:
  value: {}
  as_of_event_id: DE-...
  calculated_at: 2026-07-10T16:31:00+09:00
  projection_hash: sha256-value
```

### 3.2 Structured state

単一の `Concept` や `Prototype` だけで表さず、複数の状態軸へ分ける。

```yaml
state:
  identity:
    name: Signity Transition Engine
  lifecycle:
    stage: concept
  architecture:
    versioning_focus: event-centered
  governance:
    human_approval_required: true
  capture_policy:
    checkpoint_interval_minutes: 8
```

### 3.3 Committed and observed state

- `committed_state`: 組織が承認した方針、予定、コミットメント
- `observed_state`: 現実に確認された実行状況、事実、結果

承認したことと、現実に完了したことを混同しない。

---

## 4. Candidate detection rules

次のいずれかを満たす情報を状態遷移候補として提示する。

1. Decision Objectの属性、方針、ライフサイクルが変わる
2. 人、予算、時間、権限などの資源配分を確定する
3. 新しい方針、ルール、責任を成立させる
4. 過去の判断を置換、撤回、復元する
5. 後日説明責任が生じるコミットメントを行う
6. 実行結果によりObserved Stateが変化する

単なるアイデア、質問、検討途中の発言はEvidenceまたはProposalとして扱う。

Decision Type:

- `create`
- `change`
- `end`
- `revert`
- `supersede`

---

## 5. Approval lifecycle

```text
情報取得
  ↓
状態遷移候補の検出
  ↓
Draft Event生成
  ↓
根拠・差分・提案理由の提示
  ↓
人間による承認 / 却下 / 修正
  ↓
正規化EventをLedgerへ追記
  ↓
Content HashとHash Chainを計算
  ↓
Current Stateを再計算
  ↓
実行エージェントへ連携
  ↓
Action / OutcomeをLedgerへ戻す
```

MVPでは承認済みLedgerへの書き込み確定は人間のみが行う。

---

## 6. Integrity and signatures

### 6.1 Separate mechanisms

- `content_hash`: 内容が変わっていないことを検証する
- `hash_chain`: 過去Eventの削除や差し替えを検知しやすくする
- `digital_signature`: 承認者の秘密鍵で署名し、本人性を検証する
- `trusted_timestamp`: 指定時刻以前に存在したことを外部証明する

ハッシュだけでは誰が承認したかを証明できない。

### 6.2 MVP sequence

1. canonical JSONを生成
2. ハッシュ対象外フィールドを除外
3. SHA-256で `content_hash` を計算
4. `previous_event_hash` を保存
5. 承認者IDと承認時刻を記録
6. 後続版でデジタル署名を追加

承認済みEventは編集せず、訂正はCorrection Eventで行う。

---

## 7. IDs and time

### IDs

- Machine ID: ULIDまたはUUIDv7
- Display ID: `DE-20260710-003`

意味をMachine IDへ埋め込みすぎない。

### Timestamps

- `occurred_at`: 出来事が起きた時刻
- `recorded_at`: システムへ登録した時刻
- `approved_at`: 承認した時刻
- `effective_at`: 効力を持つ時刻

ISO 8601とタイムゾーンを必須にする。

---

## 8. Minimal data model

### Decision Object

```yaml
schema_version: "0.3"
object_id: do_01...
display_id: DO-20260710-001
object_type: project
name: Signity Transition Engine
purpose: 組織の状態変化を検出し、根拠付きイベントとして構造化・承認・追跡する
owner_actor_ids:
  - actor_ken
created_event_id: de_01...
originated_at: 2026-01-05T00:00:00+09:00
recorded_at: 2026-07-10T16:16:00+09:00
```

### Decision Event

Schemaの正本は `schemas/decision-event.schema.v0.3.json` とする。

---

## 9. MVP scope

### Include

1. Decision Object作成
2. 手入力によるDraft Decision Event作成
3. Before / After差分表示
4. Evidence参照登録
5. 人間のApprove / Reject / Edit
6. 承認Eventの追記保存
7. SHA-256ハッシュチェーン
8. Current State自動Projection
9. Markdown / JSONエクスポート
10. Event検索と現在状態の説明

### Exclude initially

- Git互換実装
- 自動マージ
- AIによる自律承認
- ブロックチェーン
- Slackや会議録の常時監視
- 高度な権限管理
- モデル特性の自動評価

### Suggested storage

- Append-only Event Store: SQLite
- Evidence snapshots: ローカルまたはオブジェクトストレージ
- Projection: 再計算可能なDBテーブルまたはキャッシュ
- Human-readable export: Markdown / YAML / JSON

---

## 10. Implementation readiness

次の条件を正本として扱う。

1. EventをDecision / Observation / Action / Outcome / Correctionに分ける
2. Current Stateを手入力せずProjectionにする
3. Committed StateとObserved Stateを分ける
4. MVPでは人間承認を必須にする
5. Content HashとDigital Signatureを別概念として扱う
6. AIプロバイダーに依存しないDomain Modelを維持する

次の成果物はCodexで作成する。

- Product Requirements Document
- Repository structure
- API contract
- SQLite schema
- acceptance tests
- current Decision EventsからのSeed Data
