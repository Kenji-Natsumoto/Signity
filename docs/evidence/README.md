# Evidence

意思決定の根拠となった一次資料です。

## 絶対の原則

- **一度記録した Evidence を書き換えない。** スナップショットとして固定されています。
- 解釈・要約・判断は Evidence ではなく Decision Event 側に書きます。
- 会話ログは Evidence であり、仕様書ではありません。

## 3 つの種別

| 種別 | 内容 |
| --- | --- |
| `reference` | 元データへの参照のみ |
| `snapshot` | その時点の内容を保存し、ハッシュを付ける |
| `attestation` | 録音等がない対面会議について、人間が「こう話し、こう決めた」と証言する |

## 配置と命名

```text
docs/evidence/YYYY/MM/EV-YYYYMMDD-NNN-<slug>.md
```

ひな形: [`templates/evidence.md`](../../templates/evidence.md)

## 索引

| Display ID | 日付 | 種別 | 内容 |
| --- | --- | --- | --- |
| [EV-20260728-001](2026/07/EV-20260728-001-drive-design-documents.md) | 2026-07-28 | reference | Google Drive 上の Signity 設計文書一式 |

## 注意

本番データや秘密情報を Evidence として保存しないでください。
参照が必要な場合は `reference` として出典のみを記録します。
