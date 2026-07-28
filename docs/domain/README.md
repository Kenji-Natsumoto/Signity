# Domain

ドメインモデルと Decision Object の定義を置きます。

## Decision Object 一覧

| Display ID | 種別 | 名称 | 状態 |
| --- | --- | --- | --- |
| DO-20260710-001 | project | Signity Transition Engine | concept |

（`docs/decisions/` の Event から投影される内容です。Current State を手入力しないでください。）

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

## 注意

- Current State はイベント列からの投影（Projection）です。ここに手で書かないでください。
- Committed State（承認したこと）と Observed State（現実に達成されたこと）を混同しないでください。
