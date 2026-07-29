# Domain

ドメインモデルと Decision Object の定義を置きます。

## Decision Object 一覧

| Display ID | 種別 | 名称 | 定義 |
| --- | --- | --- | --- |
| DO-0001 | project | Signity Transition Engine | [`decision-object-0001.md`](decision-object-0001.md) |

`decision-object-0001.md` は `signity-transition-engine-docs-v0.3.zip` からの取り込み正本です
（SHA-256 `f05c180e…104b880c`、[EV-20260728-002](../evidence/2026/07/EV-20260728-002-transition-engine-docs-v0.3-bundle.md)）。

## 置くもの

- Decision Object の定義（`decision-object-NNNN.md`）
- ドメイン用語集
- 状態軸（state schema）の定義

## Decision Object の種別

- `project`
- `policy`
- `strategy`
- `product`
- `organization`

## まだ Object 化されていないもの

v0.2 アーキテクチャ 9 章は、次を別 Decision Object に分ける余地があると指摘しています。

- `Policy: GPT Live Decision Capture`（チェックポイント運用。現在は DO-0001 の属性として扱われている）
- `Architecture Object`（バージョン管理方針。同上）

分割するかどうかは決定が必要です。

## 注意

- Current State はイベント列からの投影（Projection）です。ここに手で書かないでください。
- Committed State（承認したこと）と Observed State（現実に達成されたこと）を混同しないでください。
