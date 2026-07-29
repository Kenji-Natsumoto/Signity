# Decision Event: DE-20260710-003

## タイトル

プロジェクト名称を「AI Company」から「Signity Transition Engine」へ変更する

## 基本情報

- 日付: 2026-07-10
- 時刻: 15:30 JST
- 旧表示ID: de_cc0001
- 提案者: 夏本健司 / AIエージェント・ROJINA
- 承認者: 夏本健司
- ステータス: Approved
- Primary Decision Object: DO-0001

## 状態変更

```yaml
changes:
  - path: /identity/name
    before: AI Company
    after: Signity Transition Engine
    change_note: 一般的な仮称から、機能と人間補佐の役割を明確にする名称へ変更する
```

## 根拠

- 朝のブリーフィング
- 2026-07-10のChatGPT Live対話
- プロダクトが人間の代わりに意思決定するものではなく、状態変化の検出と記録を補佐するものであるという整理
- 開発段階で機能を誤解なく表す説明的名称が必要であるという判断

## 判断理由

仕組みと責任分担が具体化したため、プロダクトの中核機能を明確に表し、AIが人間の意思決定を代替するという誤解を避けられる名称へ統一する。

## 人の価値判断

- 人間中心であること
- 機能の明瞭さ
- 誤解の回避
- Codexを含む開発エージェントがスコープを正しく理解できること

## 期待結果

- リポジトリ、設計文書、Schema、Seed Dataで名称が統一される
- 開発対象が状態遷移の検出・構造化・承認・追跡に集中する
