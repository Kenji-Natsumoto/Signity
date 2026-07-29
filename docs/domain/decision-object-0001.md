# Decision Object: DO-0001

## 基本属性

- 種別: Project
- 名称: Signity Transition Engine
- 目的: 組織の状態変化を検出し、根拠付きのイベントとして構造化し、人間の承認を経て追跡可能な履歴へ保存する
- オーナー: 夏本健司
- Originated at: 2026-01-05T00:00:00+09:00
- Recorded at: 2026-07-10T16:16:00+09:00
- Created event ID: DE-20260710-003

## Current State

Current Stateはこのファイルへ手入力しない。承認済みLedger Eventから自動計算し、表示時には次を付与する。

```yaml
current_state:
  value: {}
  as_of_event_id: null
  calculated_at: null
  projection_hash: null
```

## State model

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
```

## 設計メモ

- Decision Objectは状態変化の対象を表す
- Eventは対象に起きた変化を表す
- Current StateはEvent列を適用したProjectionである
- 製品、顧客、組織、方針なども同じ型で表現できる
- 名称、ライフサイクル、アーキテクチャ方針は別々の状態軸として扱う
