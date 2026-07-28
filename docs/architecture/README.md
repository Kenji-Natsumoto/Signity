# Architecture

Signity の設計・アーキテクチャの確定文書です。

## 現行版

| 文書 | 版 | 状態 | 対象 |
| --- | --- | --- | --- |
| [`signity-decision-os-architecture-v0.2.md`](signity-decision-os-architecture-v0.2.md) | v0.2 | Draft for validation | Signity Decision OS 全体の思想と概念 |
| [`signity-transition-engine-architecture-v0.3.md`](signity-transition-engine-architecture-v0.3.md) | v0.3 | Draft for implementation validation | Signity Transition Engine（実装対象プロダクト） |

## 運用ルール

- **過去版を上書き・削除しない。** 新しいバージョンのファイルを追加し、この表を更新する。
- ファイル名は `<name>-vX.Y.md`。
- アーキテクチャ変更は必ず Decision Event として `docs/decisions/` に記録し、
  その Event からこの文書を参照できるようにする。

## 未取り込みの正本

以下は Google Drive にあり、まだこのリポジトリへ取り込まれていません。

- `schemas/decision-event.schema.v0.3.json`（`signity-transition-engine-docs-v0.3.zip` 内）
- `seed/sample.de_product_rename.v0.3.yaml`（同上）
- UI ワイヤーフレーム一式（`signity_ui_wireframe_ja_bundle.zip`）
