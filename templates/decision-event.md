# DE-YYYYMMDD-NNN: <title>

> 承認後はこのファイルを編集しないでください。
> 訂正が必要な場合は `corrects_event_id` を持つ新しい Correction Event を作成します。

```yaml
schema_version: "0.3"
event_id: de_<ULID>
display_id: DE-YYYYMMDD-NNN
event_kind: decision            # decision | observation | action | outcome | correction
decision_type: change           # create | change | end | revert | supersede
status: approved                # draft | approved | rejected
primary_object_id: do_<ULID>
affected_object_ids: []
title: <一文で表す決定内容>
occurred_at: "YYYY-MM-DDTHH:MM:SS+09:00"
recorded_at: "YYYY-MM-DDTHH:MM:SS+09:00"
approved_at: "YYYY-MM-DDTHH:MM:SS+09:00"
effective_at: "YYYY-MM-DDTHH:MM:SS+09:00"
changes:
  - path: /<state のパス>
    before: <変更前>
    after: <変更後>
    change_note: <補足>
rationale:
  decision_question: <何を決める必要があったか>
  summary: <なぜそう決めたか>
  facts: []
  assumptions: []
  options_considered: []
  human_value_judgments: []
  tradeoffs: []
  revisit_triggers: []
  confidence: null
proposed_by:
  - actor_<name>
approved_by:
  - actor_<name>
evidence_refs: []
model_run_refs: []
expected_outcome:
  summary: <期待する結果>
  review_due_at: null
  success_metrics: []
supersedes_event_id: null
corrects_event_id: null
integrity:
  algorithm: sha256
  canonicalization: canonical-json-v1
  previous_event_hash: <直前 Event の content_hash>
  content_hash: <computed-sha256>
signatures: []
```

## 背景

<この決定に至るまでの経緯>

## 決定内容

<何を決めたか>

## 検討した選択肢

| 選択肢 | 採否 | 理由 |
| --- | --- | --- |
|  |  |  |

## 根拠 (Evidence)

- EV-YYYYMMDD-NNN: <出典>

## 影響

<この決定によって変わること>

## 見直しの契機

<どうなったら再検討するか>
