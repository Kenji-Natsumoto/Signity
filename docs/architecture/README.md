# Architecture

Signity の設計・アーキテクチャの確定文書です。

## 現行版

| 文書 | 版 | 状態 | 対象 |
| --- | --- | --- | --- |
| [`signity-decision-os-architecture-v0.2.md`](signity-decision-os-architecture-v0.2.md) | v0.2 | Draft for validation | Signity Decision OS 全体の思想と概念 |
| [`signity-transition-engine-architecture-v0.3.md`](signity-transition-engine-architecture-v0.3.md) | v0.3 | Draft for implementation validation | Signity Transition Engine（実装対象プロダクト） |
| [`canonical-json-v1.md`](canonical-json-v1.md) | v1.0 | **Normative / 凍結** | Decision Event の正規化と `content_hash` の計算規則 |

`canonical-json-v1.md` は architecture v0.3 の 6.2 節が名称のみ定めていた正規化方式を
規則として確定したものです。**凍結されており、変更は `canonical-json-v2` として別定義します。**
参照実装は [`tools/signity/canonical.py`](../../tools/signity/canonical.py)。

v0.2 と v0.3 は同一文書の版更新ではありません。対象が異なります。
v0.2 は umbrella brand としての Signity、v0.3 は傘下プロダクトの Transition Engine を扱います。

## 出典と整合性

| 文書 | 出典 | 正本ハッシュ |
| --- | --- | --- |
| v0.2 | Google Drive 単体ファイル `Signity_Decision_OS_Architecture_v0.2.md` | なし（下記の注記を参照） |
| v0.3 | `signity-transition-engine-docs-v0.3.zip` 同梱の正本 | `efa1d5b6…04791f35`（[EV-20260728-002](../evidence/2026/07/EV-20260728-002-transition-engine-docs-v0.3-bundle.md)） |

v0.3 は `./scripts/verify-manifest.sh` で SHA-256 照合できます。

> **v0.2 に関する注記**
> v0.2 はハッシュ付きバンドルが存在せず、Drive 上の単体ファイルから取り込みました。
> 取り込み時に、インラインコード（`` ` ``）前後の空白を整形し、
> 判読不能な文字化け 1 箇所（2.4 節「ROJINAという Agent」）を修正しています。
> 内容は変えていませんが、Drive 上の原本とバイト単位では一致しません。
> ハッシュ付き正本が必要な場合は、v0.3 と同様のバンドルを作り直してください。

## 運用ルール

- **過去版を上書き・削除しない。** 新しいバージョンのファイルを追加し、この表を更新する。
- ファイル名は `<name>-vX.Y.md`。
- アーキテクチャ変更は必ず Decision Event として `docs/decisions/` に記録し、
  その Event からこの文書を参照できるようにする。

## 未取り込み

- UI ワイヤーフレーム一式（Google Drive の `signity_ui_wireframe_ja_bundle.zip`、約 10 MB）
