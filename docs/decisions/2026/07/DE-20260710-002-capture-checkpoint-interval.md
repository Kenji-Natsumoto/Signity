# Decision Event: DE-20260710-002

## タイトル

意思決定に関する音声対話を短いチェックポイントで区切る運用ルールを定める

## 基本情報

- 日付: 2026-07-10
- 時刻: 15:00 JST
- 旧表示ID: de_bb0001
- 提案者: 夏本健司 / AIエージェント・ROJINA
- 承認者: 夏本健司
- ステータス: Approved
- Primary Decision Object: DO-0001

## 状態変更

```yaml
changes:
  - path: /capture_policy/checkpoint_interval_minutes
    before: null
    after: 8
    change_note: 音声セッションが途切れる可能性を考慮し、重要な対話を短い単位で要約・保存する
```

## 根拠

- 2026-07-10のChatGPT Live対話
- 音声セッションが約8〜10分で途切れる現象を複数回確認したこと
- 長い会話を一括処理するより、短いチェックポイントの方が記録漏れを防げるという判断

## 運用上の意味

8分のチェックポイントは自動的にDecision Eventになるわけではない。チェックポイントはEvidenceとして保存し、状態変化が認められた場合のみEvent候補へ昇格させる。

## 人の価値判断

- 記録の継続性
- 会話の消失防止
- 運用負荷の低さ
- 後から検証できること
