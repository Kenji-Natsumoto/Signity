# tools

Signity Ledger の参照実装です。

正本は `docs/architecture/` の設計文書と `schemas/decision-event.schema.v0.3.json` であり、
このコードはその実装です。食い違った場合は正本を正とします。

## 依存

- Python 3.11 以上
- PyYAML（YAML の Event を読むときのみ。JSON だけなら不要）

外部の JSON Schema ライブラリは使いません。`validate.py` は
`decision-event.schema.v0.3.json` が実際に使うキーワードだけを実装した**部分実装**です。
未対応のキーワードがスキーマに現れた場合は例外を投げます（黙って無視しません）。

## 構成

| モジュール | 役割 |
| --- | --- |
| [`signity/canonical.py`](signity/canonical.py) | canonical-json-v1 の正規化と `content_hash` |
| [`signity/ledger.py`](signity/ledger.py) | Ledger の読み込み、ハッシュチェーンの構築と検証 |
| [`signity/projection.py`](signity/projection.py) | Current State の投影 |
| [`signity/validate.py`](signity/validate.py) | Schema 検証（部分実装） |
| [`signity/cli.py`](signity/cli.py) | CLI |

仕様書: [`docs/architecture/canonical-json-v1.md`](../docs/architecture/canonical-json-v1.md)

## 使い方

```sh
./scripts/signity verify                        # Ledger 全体を検証
./scripts/signity chain                         # チェーンを表示
./scripts/signity state --object <object_id>    # Current State を投影
./scripts/signity hash <event.json|yaml>        # content_hash を計算
./scripts/signity hash <path> --show-canonical  # 正規化後の JSON も表示
./scripts/signity validate [path...]            # Schema 適合を検証
./scripts/signity append <pending/xxx.json>     # 承認済み Draft を追記
```

## テスト

```sh
PYTHONPATH=tools python3 -m unittest discover -s tools/tests -t tools
```

または全部まとめて:

```sh
./scripts/verify-all.sh
```

### 最重要のテスト

`tools/tests/test_canonical.py::TestCanonicalSeed::test_reproduces_canonical_seed_hash`

2026-07-10 時点の実装が計算した `content_hash`
（`f9eb852866535b176c9af8c6e9f0d9fcc18ab5950771b4969b652cd04f6acbf6`）を
本実装が再現できることを確認します。

**このテストが落ちたら canonical-json-v1 が壊れています。**
実装を直してください。テストの期待値を書き換えてはいけません。
過去のすべての `content_hash` がその値を前提にしています。

### 改ざん検知のテスト

`test_ledger.py::TestTamperDetection` は実際に Event を改変して、検証が失敗することを確かめます。
`content_hash` を再計算して自己整合させた場合も、チェーンの連結で検知されることを含みます。

## 設計上の約束

- `canonical.py` は入力を変更しません（`copy.deepcopy` してから加工します）
- `compute_chain` は入力を変更せず、新しい Event 列を返します
- `append` は既存 Event のハッシュが変わっていないことを確認してから書き込みます
- `append` は `status: approved` 以外を拒否します。承認は人間が行います
- Ledger のファイルを上書きしません
