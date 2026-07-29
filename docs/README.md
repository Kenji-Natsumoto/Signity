# Signity ドキュメント階層

このディレクトリは Signity のドキュメント正本です。
**どこに置くか迷ったら、この表に戻ってください。**

## 1. 階層の役割分担

| ディレクトリ | 置くもの | 置かないもの | 変更可否 |
| --- | --- | --- | --- |
| `architecture/` | 設計・アーキテクチャの確定文書 | 検討途中のメモ | バージョンを上げて新規追加。過去版は残す |
| `product/` | プロダクト定義・コンセプト・スコープ | 実装詳細 | バージョンを上げて新規追加 |
| `domain/` | ドメインモデル、Decision Object の定義 | 一時的な議論 | 対象ごとに追記・更新可 |
| `decisions/` | 承認済み Decision Event（人間向け） | 未承認の提案 | **編集不可**（訂正は Correction Event） |
| `evidence/` | 意思決定の根拠となった一次資料 | 加工・要約した解釈 | **編集不可**（スナップショットのため） |
| `journal/` | 日次ログ、未整理の観測・素材 | 確定した仕様 | 当日中は追記可。翌日以降は追記のみ |
| `development/` | 開発手順、ハンドオフ、運用ルール | 設計思想そのもの | 随時更新可 |

`docs/` の外にある関連ディレクトリ:

| ディレクトリ | 置くもの |
| --- | --- |
| [`ledger/events/`](../ledger/) | 承認済み Decision Event の機械可読な正本（追記専用・ハッシュチェーン） |
| [`ledger/pending/`](../ledger/) | Draft Event（承認待ち） |
| [`tools/signity/`](../tools/) | Ledger の参照実装 |
| `schemas/` | JSON Schema |

情報の流れは常に一方向です。

```text
journal/ (素材・観測)
   ↓  候補として抽出
evidence/ (根拠として固定)
   ↓  人間が承認
ledger/pending/ → ledger/events/ (Decision Event として封印・ハッシュチェーン接続)
   ↓  同内容を人間向けに記述
decisions/
   ↓  投影
architecture/ product/ domain/ (確定文書へ反映)
```

Current State は `./scripts/signity state` で投影します。手で書きません。

## 2. 命名規則

### Decision Event

```text
docs/decisions/YYYY/MM/DE-YYYYMMDD-NNN-<slug>.md
例: docs/decisions/2026/07/DE-20260728-001-establish-doc-hierarchy.md
```

- `NNN` はその日の連番（`001` から）。欠番を作らない。
- `slug` は英小文字とハイフンのみ。

### Evidence

```text
docs/evidence/YYYY/MM/EV-YYYYMMDD-NNN-<slug>.md
```

### 日次ログ

```text
docs/journal/YYYY/MM/YYYY-MM-DD.md
```

1 日 1 ファイル。ファイルを分割しない。

### バージョン付き文書

```text
<name>-vX.Y.md
例: signity-transition-engine-architecture-v0.3.md
```

- 過去版は削除しない。上書きもしない。新しいバージョンのファイルを追加する。
- 各ディレクトリの `README.md` に現行版を明記する。

## 3. 日次の運用フロー

1. **その日の最初に** `docs/journal/YYYY/MM/YYYY-MM-DD.md` を
   [`templates/journal-daily.md`](../templates/journal-daily.md) から作る。
2. 会議・対話・Slack・AI セッションで出たものを、判断せずそのまま journal に書く。
3. 状態遷移の候補（下記 4 章）に当たるものに `→ 候補` と印を付ける。
4. **その日の最後に** 候補を見直し、承認するものだけを Decision Event として
   `docs/decisions/` に書き出す。根拠は `docs/evidence/` に固定する。
5. 確定文書（architecture / product / domain）への反映が必要なら、
   Decision Event から参照できる形で更新する。

承認しなかった候補は journal に残したままにします。消さないでください。

## 4. Decision Event を作る条件

次のいずれかを満たすものだけが Decision Event になります。

1. Decision Object の属性・方針・ライフサイクルが変わる
2. 人・予算・時間・権限などの資源配分を確定する
3. 新しい方針・ルール・責任を成立させる
4. 過去の意思決定を置換・撤回・復元する
5. 後日、説明責任を求められる可能性があるコミットメントを行う

単なるアイデア、質問、検討途中の発言は Evidence または提案として残し、
承認されるまで確定 Event にしません。

Decision Type は次の 5 種類です。

- `create` / `change` / `end` / `revert` / `supersede`

## 5. タイムスタンプ

ISO 8601 とタイムゾーンを必須にします。

- `occurred_at`: 実際に意思決定が起きた時刻
- `recorded_at`: システムへ登録した時刻
- `approved_at`: 承認した時刻
- `effective_at`: 決定が効力を持つ時刻

例: `2026-07-28T15:30:00+09:00`

## 6. 承認と追記の手順

Decision Event を承認したら、機械可読な正本を Ledger へ追記します。

```sh
# 1. Draft を書く（ひな形から）
cp templates/decision-event.md docs/decisions/2026/07/DE-YYYYMMDD-NNN-<slug>.md
# 対応する JSON を ledger/pending/DE-YYYYMMDD-NNN.json に作る

# 2. Schema 適合を確認する
./scripts/signity validate ledger/pending/DE-YYYYMMDD-NNN.json

# 3. 人間が承認する
#    status を approved にし、approved_at と approved_by を記入する

# 4. Ledger へ追記する（previous_event_hash と content_hash が自動で確定する）
./scripts/signity append ledger/pending/DE-YYYYMMDD-NNN.json

# 5. 検証する
./scripts/signity verify
```

`append` は `status: approved` 以外を拒否します。AI が承認済みにしてはいけません。

## 7. やってはいけないこと

- 承認済み Decision Event のファイルを編集・削除する
- `ledger/events/` のファイルを編集・削除する。連番を振り直す
- `journal/` の過去日を書き換える
- Current State を手入力で書く（`./scripts/signity state` で投影する）
- `canonical-json-v1` の規則を変更する（凍結済み。変更は v2 として別定義）
- 会話ログをそのまま仕様書として扱う
- 本番データや秘密情報を `seed/` に入れる
