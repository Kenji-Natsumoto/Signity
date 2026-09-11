# Development

開発手順・ハンドオフ・運用ルールを置きます。

## 文書

| 文書 | 内容 |
| --- | --- |
| [`codex-handoff.md`](codex-handoff.md) | Signity Transition Engine の実装を Codex に引き継ぐための手順 |
| [`viberush-jp-channel-smoke-test.md`](viberush-jp-channel-smoke-test.md) | jp.VibeRush のチャネル配分仮説を 2 週間で検証する実行手順（2026-09-12 〜 09-25） |

`codex-handoff.md` は `signity-transition-engine-docs-v0.3.zip` からの取り込み正本です
（SHA-256 `01ac8a95…4834e30f`、[EV-20260728-002](../evidence/2026/07/EV-20260728-002-transition-engine-docs-v0.3-bundle.md)）。

> 注意: `codex-handoff.md` はバンドルを `signity-transition-engine` リポジトリ直下へ
> 展開する前提で書かれています。このリポジトリでは umbrella brand `Signity` の下に
> 取り込んでいるため、参照パスが一部異なります。分離する際に読み替えてください。

## スクリプト

| スクリプト | 内容 |
| --- | --- |
| [`../../scripts/verify-all.sh`](../../scripts/verify-all.sh) | 下記すべてとテストをまとめて実行する |
| [`../../scripts/verify-manifest.sh`](../../scripts/verify-manifest.sh) | v0.3 バンドル取り込み分の SHA-256 を正本 MANIFEST と照合する |
| [`../../scripts/signity`](../../scripts/signity) | Ledger の CLI（`verify` / `chain` / `state` / `hash` / `validate` / `append`） |

実装は [`tools/`](../../tools/README.md)。

## 置くもの

- 実装ハンドオフ手順
- 環境構築・運用手順
- リリース手順

## 置かないもの

- 設計思想（`docs/architecture/` へ）
- 意思決定の記録（`docs/decisions/` へ）

> `viberush-jp-channel-smoke-test.md` の置き場所は暫定です。`docs/README.md` の階層表には
> マーケティング実行手順の置き場所がなく、「運用手順」として暫定的にここに置いています。
> `docs/operations/` の新設か、このディレクトリの定義を広げるかは未決定です。

このディレクトリの文書は随時更新可能です。
