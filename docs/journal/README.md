# Journal

日次ログです。会議・対話・Slack・AI セッションで出たものを、**判断せずそのまま**書きます。

ここは Evidence の素材置き場であり、仕様書ではありません。
確定した内容をここに書かないでください。

## 配置と命名

```text
docs/journal/YYYY/MM/YYYY-MM-DD.md
```

1 日 1 ファイル。分割しません。

ひな形: [`templates/journal-daily.md`](../../templates/journal-daily.md)
夜間キャプチャループ用のひな形: [`templates/nightly-scan-section.md`](../../templates/nightly-scan-section.md)

`./scripts/new-journal.sh` で当日分を用意できます（既にあれば何もしません）。

## 素材の受け口

コネクタのないソースと Mac のローカル素材は [`inbox/`](inbox/README.md) に入ります。
Slack / Gmail / Calendar / Drive / GitHub は
[夜間キャプチャループ](../development/nightly-capture-loop.md)が直接読むため、inbox を経由しません。

## 運用

毎晩 01:00 JST の[夜間キャプチャループ](../development/nightly-capture-loop.md)が
**前日分**について 1〜3 を自動で行います。4 は人間がその朝行います。

1. その日の最初にひな形からファイルを作る
2. 出てきたものをそのまま書く
3. 状態遷移の候補には印を付ける
4. その日の最後に候補を見直し、承認するものだけを Decision Event へ書き出す
5. 承認しなかった候補も消さずに残す

## 過去日の扱い

翌日以降、過去日のファイルを書き換えないでください。
後から判明したことは、その日の journal に「YYYY-MM-DD 追記」として追記するか、
当日の journal に記載します。

## 索引

| 日付 | 内容 |
| --- | --- |
| [2026-07-28](2026/07/2026-07-28.md) | ドキュメント階層の確立、Drive 設計文書と v0.3 バンドルの取り込み |
| [2026-07-29](2026/07/2026-07-29.md) | canonical-json-v1 の確定、Ledger とハッシュチェーンの稼働 |
| [2026-09-09](2026/09/2026-09-09.md) | 夜間キャプチャループの設計、Capture 層の 3 層分離 |
