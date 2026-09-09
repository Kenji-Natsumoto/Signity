# Prompts

無人実行される Routine のプロンプト正本を置きます。

Routine はリポジトリの外（Claude Code Remote 側）に保存されるため、
何が毎晩実行されているかがコードレビューの対象になりません。
ここに正本を置き、**Routine を変えたら必ずここも同時に更新する**ことで、
自動実行の内容を Git の履歴に残します。

## 文書

| 文書 | Routine | スケジュール |
| --- | --- | --- |
| [`nightly-capture-prompt.md`](nightly-capture-prompt.md) | Signity 夜間キャプチャループ | 毎日 22:30 JST（cron `30 13 * * *` UTC） |

## 置くもの

- Routine / cron / CI から無人実行されるプロンプト
- そのプロンプトが前提とする権限とコネクタの一覧

## 置かないもの

- 対話セッションで 1 回だけ使った指示
- 資格情報・トークン・実データ
