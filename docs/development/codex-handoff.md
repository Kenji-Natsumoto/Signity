# Codex Handoff Guide
## Signity Transition Engine

## 1. 開始手順

1. Private Repository `signity-transition-engine` を作る
2. このパッケージの内容をリポジトリ直下へコピーする
3. Gitで初回コミットする
4. Codexアプリまたは Codex CLI でリポジトリを開く
5. 最初はコードを書かせず、設計レビューのみを依頼する

## 2. 最初のCodexプロンプト

```text
このリポジトリはSignity Transition Engineの新規プロジェクトです。

まだコードを変更しないでください。

次を順番に読んでください。

1. AGENTS.md
2. README.md
3. docs/architecture/signity-transition-engine-architecture-v0.3.md
4. schemas/decision-event.schema.v0.3.json
5. seed/sample.de_product_rename.v0.3.yaml
6. docs/ 以下の関連資料

そのうえで、次を報告してください。

- 理解したプロダクトの目的
- 中核ドメイン概念
- 文書間の矛盾
- 曖昧または未定義の用語
- 実装前に確定すべき事項
- データ整合性とセキュリティのリスク
- MVPから削るべき機能
- 推奨技術構成を最大3案
- 最初の縦切り機能

事実、提案、推測を明確に分けてください。
まだファイルを編集しないでください。
```

## 3. 推奨実装順

1. Domain types and validation
2. Append-only Event Store
3. SHA-256 content hash and hash chain
4. Current State Projection
5. Approval lifecycle
6. Minimal UI
7. Seed Data import
8. Acceptance tests

## 4. 最初の縦切り

次のデモを完成条件とする。

- Signity Transition EngineのDecision Objectを表示できる
- 3件のDecision Eventを時系列表示できる
- 承認済みEventからCurrent Stateを再計算できる
- 承認済みEventを直接編集・削除できない
- 訂正を新しいCorrection Eventとして追加できる
- Hash Chainを検証できる

## 5. 注意点

- 会話ログはEvidenceであり、仕様書ではない
- AIによる自動検出はMVP後に追加する
- Gitの履歴とプロダクト内部Ledgerを混同しない
- ドメインモデルにOpenAI固有型を入れない
- 意味論が固まる前に複数エージェントを並列稼働させない
- 本番データや秘密情報をSeed Dataに使わない
