# canonical-json-v1
## Decision Event 正規化仕様 v1.0

- Status: Normative
- Date: 2026-07-28
- 対象: `integrity.canonicalization: canonical-json-v1` を宣言するすべての Ledger Event
- 決定記録: [DE-20260728-002](../decisions/2026/07/DE-20260728-002-canonical-json-v1.md)

---

## 1. この仕様が必要な理由

`signity-transition-engine-architecture-v0.3.md` 6.2 節は `content_hash` の計算手順として
「canonical JSON を生成」「ハッシュ対象外フィールドを除外」と定めていますが、
正規化の具体的な規則は定義していませんでした。

規則が曖昧だと、同じ Event から異なるハッシュが出ます。
その状態では `content_hash` は「内容が変わっていないことを検証する」役目を果たせません。

本仕様はその規則を確定します。

## 2. 由来と検証

本仕様は新規に設計したものではなく、**既存の正本ハッシュから復元し、一致を確認したもの**です。

`seed/sample.de_product_rename.v0.3.yaml`（v0.3 バンドルの正本、SHA-256 照合済み）は
`content_hash: f9eb852866535b176c9af8c6e9f0d9fcc18ab5950771b4969b652cd04f6acbf6`
を持っています。本仕様どおりに計算すると、この値がバイト単位で再現されます。

つまり本仕様は、2026-07-10 時点の実装が実際に用いていた規則です。
回帰テストは `tools/tests/test_canonical.py` にあります。

## 3. 正規化手順

### 3.1 ハッシュ対象外フィールドの除去

入力 Event オブジェクトから、次の 2 つを**キーごと削除**します（`null` を入れるのではなく削除）。

| 除外するもの | 理由 |
| --- | --- |
| `integrity.content_hash` | 自分自身のハッシュ。含めると計算が循環する |
| `signatures`（ルート直下） | 署名はハッシュ確定後に付与される。含めると署名追加でハッシュが変わる |

`integrity.previous_event_hash` は**除外しません**。ハッシュ対象に含めます。
これによりハッシュチェーンが成立します（4 章）。

`integrity.algorithm` と `integrity.canonicalization` も対象に含めます。
正規化方式そのものを改ざんできないようにするためです。

### 3.2 直列化

削除後のオブジェクトを、次の規則で JSON 文字列にします。

1. **オブジェクトのキーを昇順に並べる。** 比較は Unicode コードポイント順。
2. **余分な空白を入れない。** 区切りは `,` と `:` のみ（値の前後に空白を置かない）。
3. **非 ASCII 文字はそのまま出力する。** `\uXXXX` へエスケープしない。
4. **文字列のエスケープは JSON の最小形。** `"` と `\` はバックスラッシュで、
   制御文字は `\b` `\f` `\n` `\r` `\t` があればその短縮形、
   それ以外は小文字 4 桁の `\u00XX`。
5. **配列の順序は保持する。** 並べ替えない。
6. **数値**は整数はそのまま、小数は往復可能な最短表記。
7. **UTF-8 でエンコードし、末尾に改行を付けない。**

### 3.3 ハッシュ

3.2 で得たバイト列に SHA-256 を適用し、**小文字 16 進 64 文字**で表します。

```text
content_hash = lowercase_hex( SHA-256( UTF-8( canonical_json( event − 除外フィールド ) ) ) )
```

### 3.4 参照実装

```python
import hashlib, json

def canonicalize(event: dict) -> bytes:
    e = json.loads(json.dumps(event))          # 深いコピー
    e.pop("signatures", None)
    if isinstance(e.get("integrity"), dict):
        e["integrity"].pop("content_hash", None)
    return json.dumps(
        e, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")

def content_hash(event: dict) -> str:
    return hashlib.sha256(canonicalize(event)).hexdigest()
```

正式な実装は [`tools/signity/canonical.py`](../../tools/signity/canonical.py) です。

## 4. ハッシュチェーン

Ledger は追記専用です。各 Event は直前の Event の `content_hash` を
`integrity.previous_event_hash` に保持します。

```text
Event 1: previous_event_hash = null
         content_hash = H1
Event 2: previous_event_hash = H1
         content_hash = H2
Event 3: previous_event_hash = H2
         content_hash = H3
```

`previous_event_hash` はハッシュ対象に含まれるため、
過去の Event を 1 件でも改変・削除・差し替えすると、
それ以降のすべての `content_hash` が合わなくなります。

### 4.1 追記順序

チェーンの順序は、**Ledger 内のファイル名の連番**で決まります。

```text
ledger/events/NNNN-<display_id>.json
```

連番は追記順そのものです。`recorded_at` から推測しません。
検証時には、連番順と `recorded_at` の昇順が矛盾していないことも確認します。

`occurred_at`（出来事が起きた時刻）が連番順と一致する必要はありません。
過去に起きた意思決定を後から追記する場合、`occurred_at` は古く、
`recorded_at` は新しくなります。これは正常です。

### 4.2 検証できること・できないこと

| できる | できない |
| --- | --- |
| 内容が改変されていないことの検知 | 誰が承認したかの証明 |
| 過去 Event の削除・差し替えの検知 | その時刻に存在したことの証明 |
| 追記順序の一貫性の確認 | Ledger 全体の差し替えの検知 |

「改ざん不能」ではなく「**改ざん検知可能**」です。
本人性は `signatures`（デジタル署名）、時刻証明は `trusted_timestamp` が担います。
どちらも v0.3 の範囲外です。

## 5. 既知の限界

### 5.1 浮動小数点数

小数の表記は Python の最短往復表記に依存します。
指数表記が必要な極端な値（`1e21` 以上など）では、他言語の実装と食い違う可能性があります。

Decision Event で小数を取る唯一のフィールドは `rationale.confidence`（0〜1）です。
この範囲では問題は起きません。**それ以外の用途で小数を使わないでください。**

### 5.2 BMP 外の文字をキーに使わない

キーの並べ替えは Unicode コードポイント順です。
RFC 8785 (JCS) は UTF-16 コード単位順を規定しており、
基本多言語面（BMP）外の文字をキーに使った場合のみ結果が異なります。

Decision Event のキーはすべて ASCII の識別子であるため、実害はありません。
**キーに絵文字などを使わないでください。** 値には使えます。

### 5.3 v0.2 の content_hash は再現できない

`seed/sample.de_signity_rename.v0.2.yaml` の
`content_hash: cab89584cad2f598bafcad85214a715222a9581978b6e590f9c9427ddc4c8b3a`
は本仕様では再現できませんでした。

原因は特定できていません。次のいずれかと考えられます。

- v0.2 当時の正規化規則が異なっていた
- ハッシュ対象フィールドの集合が異なっていた
- 当該値が実際には計算されていない例示値だった

v0.2 の値は**検証不能な旧値**として扱い、新規の Event には使いません。
`tools/signity` は v0.2 形式の Event を検証対象外とします。

## 6. 変更方針

本仕様を変更すると、過去のすべての `content_hash` が無効になります。

そのため、**canonical-json-v1 は凍結します。** 規則を変える場合は
`canonical-json-v2` として新しい方式を定義し、`integrity.canonicalization` で
Event ごとにどちらで計算されたかを判別できるようにします。
過去の Event を再計算してはいけません。
