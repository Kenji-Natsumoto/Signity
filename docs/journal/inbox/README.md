# Inbox

**未加工の素材の受け口**です。夜間キャプチャループが読み取り、journal へ要約します。

```text
docs/journal/inbox/YYYY-MM-DD/   # 対象日。実行日ではない
```

## ここに入るもの

| 経路 | 対象 | 誰が置くか |
| --- | --- | --- |
| Mac 側コレクタ | Mac のローカル議事録・メモ・当日更新ファイル | [`scripts/mac-collect.sh`](../../../scripts/mac-collect.sh)（launchd 00:50 JST・前日分） |
| 手動投下 | コネクタのない SaaS の書き出し（LINE / Chatwork / Teams / Discord / X など） | 人間 |

コネクタのある Slack / Gmail / Calendar / Drive / GitHub は **ここを経由しません。**
ループが直接読みます。二重に置かないでください。

通知メールを受け取れる SaaS は、inbox ではなく Gmail のラベル `Signity/Inbox` へ
転送するほうが確実です。ループはそのラベルを優先して読みます。

## ここに入れないもの

- 資格情報・アクセストークン・API キー
- 個人の連絡先、契約金額などの機微情報
- 人事・評価・健康に関する記録

`AGENTS.md` 3 章と [`nightly-capture-loop.md`](../../development/nightly-capture-loop.md) 7 章に従います。
**このリポジトリが private であることは前提であって、免罪符ではありません。**

## 保持期間

素材であって正本ではありません。
`docs/evidence/` へ昇格したもの、および journal から参照されたものが残るべき記録です。
inbox 自体の掃除方針は未決（[`nightly-capture-loop.md`](../../development/nightly-capture-loop.md) 11 章）。

## 状態

現在、日付ディレクトリはまだありません。
最初の Mac 側コレクタの実行、または最初の手動投下で作られます。
