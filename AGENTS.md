# AGENTS.md

Signity リポジトリで作業する AI エージェント向けの規約です。
人間の作業者にも同じルールが適用されます。

## 1. このリポジトリの性質

ここはコードリポジトリではなく、**意思決定の追記型台帳**です。
Git の履歴と、`docs/decisions/` の Ledger は別物として扱ってください。
Git の commit は「ファイルを書いた記録」、Decision Event は「組織が承認した記録」です。

## 2. 読む順序

1. `README.md`
2. `docs/README.md`（階層と運用ルール）
3. `docs/architecture/` の現行版
4. 作業対象のディレクトリの `README.md`

## 3. 絶対に守ること

- **承認済みの Decision Event を編集・削除しない。**
  訂正が必要なら、`corrects_event_id` を持つ新しい Correction Event を追加する。
- **`docs/evidence/` を書き換えない。** スナップショットとして固定されている。
- **Current State を手入力しない。** イベント列からの投影として扱う。
- **人間の承認なしに Decision Event を確定しない。**
  AI ができるのは候補の提示と Draft の生成までで、`status: approved` を自分で付けない。
- **意味論を独断で変更しない。** 文書間に矛盾があれば、直さずに矛盾として報告する。
- **本番データ・秘密情報を `seed/` や `docs/` に入れない。**

## 4. 文書の優先順位

矛盾がある場合、上位の文書を正とします。

1. `docs/architecture/` の最新版
2. `schemas/` の JSON Schema
3. `docs/domain/`
4. `docs/product/`
5. `docs/decisions/` 以下のイベント記録
6. `docs/journal/`

## 5. 新しいドキュメントを追加するとき

1. `docs/README.md` の階層表で置き場所を確認する
2. `templates/` の該当ひな形から作る
3. 命名規則（`docs/README.md` 2 章）に従う
4. そのディレクトリの `README.md` の索引に追記する

## 6. 用語

曖昧な用語を使わないでください。

| 使う | 使わない |
| --- | --- |
| 外部化された認識・方針・コミットメント | 意識・内面 |
| 改ざん検知可能 | 改ざん不能 |
| Current State は Projection | Current State は入力項目 |
| Committed State / Observed State | 単なる「状態」 |
| Evidence | 仕様書・議事録（会話ログの意味で） |

## 7. 報告するとき

作業後は次を明確に分けて報告してください。

- 事実（文書に書かれていること）
- 提案（あなたの判断）
- 推測（確認が取れていないこと）
