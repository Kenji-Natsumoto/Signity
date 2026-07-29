# Seed

サンプル・シードデータを置きます。

| ファイル | 版 | 内容 |
| --- | --- | --- |
| [`sample.de_product_rename.v0.3.yaml`](sample.de_product_rename.v0.3.yaml) | v0.3 | Decision Event サンプル（正本・`decision-event.schema.v0.3.json` に適合） |
| [`sample.de_signity_rename.v0.2.yaml`](sample.de_signity_rename.v0.2.yaml) | v0.2 | Decision Event サンプル（旧版・v0.2 形式） |

## 2 つのサンプルの関係

どちらも `DE-20260710-003`（プロジェクト名変更）を表していますが、変更後の名称が異なります。

| ファイル | after |
| --- | --- |
| v0.2 | `Signity` |
| v0.3 | `Signity Transition Engine` |

これは未解決の矛盾です。詳細は
[EV-20260728-002](../docs/evidence/2026/07/EV-20260728-002-transition-engine-docs-v0.3-bundle.md) を参照してください。
新規に作るデータは v0.3 を基準にしてください。

## 注意

**本番データや秘密情報を Seed Data に使わないでください。**
サンプルは常に架空または公開可能な内容にします。
