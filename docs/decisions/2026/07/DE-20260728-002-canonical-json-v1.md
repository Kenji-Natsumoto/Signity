# DE-20260728-002: canonical-json-v1 の正規化規則を確定し、凍結する

> 承認後はこのファイルを編集しないでください。
> 訂正が必要な場合は `corrects_event_id` を持つ新しい Correction Event を作成します。

機械可読な正本: [`ledger/pending/DE-20260728-002.json`](../../../../ledger/pending/DE-20260728-002.json)
仕様書: [`docs/architecture/canonical-json-v1.md`](../../../architecture/canonical-json-v1.md)

```yaml
schema_version: "0.3"
event_id: de_20260728_canonical_json_v1
display_id: DE-20260728-002
event_kind: decision
decision_type: create
status: draft                   # 人間の承認後に approved へ変更する
primary_object_id: do_01J2H_EXAMPLE_TRANSITION_ENGINE
occurred_at: "2026-07-29T00:00:00+09:00"
approved_at: null
changes:
  - path: /integrity/canonicalization_spec
    before: null
    after: docs/architecture/canonical-json-v1.md
  - path: /integrity/hash_excluded_fields
    before: null
    after: [signatures, integrity.content_hash]
  - path: /integrity/canonicalization_frozen
    before: null
    after: true
integrity:
  algorithm: sha256
  canonicalization: canonical-json-v1
  previous_event_hash: null     # 承認して追記するときに確定する
  content_hash: pending
```

## 背景

`signity-transition-engine-architecture-v0.3.md` 6.2 節は `content_hash` の計算手順として
「canonical JSON を生成」「ハッシュ対象外フィールドを除外」と定めていましたが、
正規化の規則そのものは定義していませんでした。

規則が曖昧だと、同じ Event から実装ごとに違うハッシュが出ます。
その状態では `content_hash` は「内容が変わっていないことを検証する」役目を果たしません。

## 決定内容

正規化規則を新規に設計せず、**既存の正本ハッシュから復元して確定しました。**

`seed/sample.de_product_rename.v0.3.yaml`（v0.3 バンドルの正本）は
`content_hash: f9eb852866535b176c9af8c6e9f0d9fcc18ab5950771b4969b652cd04f6acbf6` を
持っています。次の規則で計算すると、この値がバイト単位で再現されました。

1. `signatures` と `integrity.content_hash` をキーごと削除する
   （`integrity.previous_event_hash` は削除しない）
2. オブジェクトのキーを Unicode コードポイント昇順に並べる
3. 区切りは `,` と `:` のみ、余分な空白を入れない
4. 非 ASCII 文字はそのまま出力する
5. UTF-8 でエンコードし、末尾に改行を付けない
6. SHA-256 を小文字 16 進 64 文字で表す

そして **canonical-json-v1 を凍結します。** 規則を変えると過去のすべての
`content_hash` が無効になるため、変更が必要な場合は `canonical-json-v2` を
新設し、`integrity.canonicalization` で Event ごとに判別できるようにします。
過去の Event を再計算してはいけません。

## 検討した選択肢

| 選択肢 | 採否 | 理由 |
| --- | --- | --- |
| RFC 8785 (JCS) をそのまま採用 | 見送り | 正本シードのハッシュが再現できず、過去の値が無効になる |
| 既存の正本ハッシュから規則を復元 | **採用** | 2026-07-10 時点の実装と一致することが検証できる |
| 独自に設計し、過去のハッシュを再計算 | 見送り | 「承認済み Event を編集しない」という原則に反する |

## 根拠 (Evidence)

- [EV-20260728-002](../../../evidence/2026/07/EV-20260728-002-transition-engine-docs-v0.3-bundle.md):
  Transition Engine 文書バンドル v0.3（`sample.de_product_rename.v0.3.yaml` を含む・SHA-256 照合済み）

## 影響

- `content_hash` が誰の環境でも同じ値になり、改ざん検知が実際に機能する
- 追記専用 Ledger（`ledger/events/`）が成立した。先頭 Event のハッシュは
  正本シードの値と同一
- `tools/signity` が参照実装になった。回帰テストが正本ハッシュの再現を保証する
- `rationale.confidence` 以外の小数を Decision Event で使えない（仕様書 5.1）
- キーに BMP 外の文字を使えない（仕様書 5.2）

## 見直しの契機

- Python 以外の言語で実装し、ハッシュが一致しない事例が出た場合
- `rationale.confidence` 以外に小数フィールドを追加する場合
- v0.2 の `content_hash` の算出方法が判明した場合（仕様書 5.3）

## 残っている限界

`seed/sample.de_signity_rename.v0.2.yaml` の
`content_hash: cab89584…` は本仕様では再現できませんでした。原因は特定できていません。
検証不能な旧値として扱い、新規の Event には使いません。
