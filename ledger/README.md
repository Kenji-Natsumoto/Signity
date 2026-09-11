# Ledger

追記専用の Decision Event ストアです。`docs/decisions/` の Markdown が人間向けの記録、
ここが機械可読な正本です。

```text
ledger/
├── events/    承認済み・追記専用・ハッシュチェーン接続済み
└── pending/   Draft（承認待ち・チェーン未接続）
```

## 使い方

```sh
./scripts/signity verify                                        # Ledger 全体を検証
./scripts/signity chain                                         # チェーンを表示
./scripts/signity state --object do_01J2H_EXAMPLE_TRANSITION_ENGINE  # Current State を投影
./scripts/signity hash ledger/events/0001-DE-20260710-003.json  # content_hash を計算
./scripts/signity validate                                      # Schema 適合を検証
./scripts/signity append ledger/pending/DE-20260728-001.json    # 承認済み Draft を追記
```

## 絶対の原則

- **`events/` のファイルを編集・削除しない。** 訂正は Correction Event を追記する。
- **`events/` には承認済み（`status: approved`）のみ。** `signity append` が拒否する。
- **連番を飛ばさない・振り直さない。** 連番が追記順そのもの。
- 追記後は必ず `./scripts/signity verify` を通す。

## 現在のチェーン

| seq | Display ID | occurred_at | 内容 | content_hash |
| --- | --- | --- | --- | --- |
| 0001 | DE-20260710-003 | 2026-07-10T15:30+09:00 | 名称を AI Company → Signity Transition Engine | `f9eb8528…` |
| 0002 | DE-20260710-001 | 2026-07-10T14:00+09:00 | versioning_focus を git-centered → event-centered | `2ed81c3e…` |
| 0003 | DE-20260710-002 | 2026-07-10T15:00+09:00 | checkpoint_interval_minutes を null → 8 | `5e0e8661…` |

先頭の `content_hash: f9eb8528…` は `seed/sample.de_product_rename.v0.3.yaml` が
2026-07-10 時点で記録していた値と**同一**です。canonical-json-v1 の実装が
当時の実装と一致していることの証拠になっています。

`occurred_at` が連番順と一致していないのは正常です。
2026-07-10 に起きた 3 件を 2026-07-28 に追記したため、`recorded_at`（追記時刻）順と
`occurred_at`（発生時刻）順が異なります。

## pending

| Display ID | 内容 | 状態 |
| --- | --- | --- |
| DE-20260728-001 | Signity のドキュメント階層を確立する | 承認待ち |
| DE-20260728-002 | canonical-json-v1 の正規化規則を確定・凍結する | 承認待ち |
| DE-20260911-001 | jp.VibeRush の Building in Public チャネル方針を確定する | 承認待ち |
| DE-20260911-002 | Decision Object jp.VibeRush（DO-0002）を発行し初期状態を確定する | 承認待ち |

承認は人間が行います。`status` を `approved` にし、`approved_at` と `approved_by` を
記入したうえで `./scripts/signity append` してください。

### DE-20260911-001 / -002 の追記順

**display_id の番号順ではなく、`DE-20260911-002` を先に追記してください。**

```sh
./scripts/signity append ledger/pending/DE-20260911-002.json   # 先: Object を成立させる create
./scripts/signity append ledger/pending/DE-20260911-001.json   # 後: その Object への方針
```

`-002` が Decision Object `do_20260911_viberush_jp` を成立させる `create` Event、
`-001` がその Object に対する方針です。逆順に追記すると、存在しない Object への
変更が先に記録され、下記「未解決の課題 1」と同じ状態を新しい Object で作ることになります。

`-002` は `before: null` から初期状態を設定するため、strict モードの投影が成立します。
`-001` の `changes` もすべて `before: null` で、`-002` が `/marketing/*` を設定しないことと整合します。

### 承認前に人間が確定すること

| Event | 項目 | 現在の値 | 理由 |
| --- | --- | --- | --- |
| 両方 | `occurred_at` / `effective_at` | Draft 作成時刻 / `null` | 実際に決定した時刻と効力発生時刻は承認時に記入する |
| -002 | `primary_object_id` | `do_20260911_viberush_jp` | ULID を捏造せず日付ベースにした暫定 ID。発行規則の確定は別の決定 |
| -002 | `/lifecycle/stage` | `launched` | stage の語彙が未定義。DO-0001 は `concept` を使っている |
| -002 | 傘下関係 | 状態に含めず | jp.VibeRush が Signity 傘下かは未決定のため `umbrella_brand` を入れていない |

承認後に `docs/domain/decision-object-0002.md` を作成し、`docs/domain/README.md` の
Decision Object 一覧に追記してください（`docs/README.md` の一方向フローのとおり、
確定文書への反映は承認後です）。

根拠は `docs/journal/2026/09/2026-09-11.md` に URL と確認日付きで残しています。
`docs/evidence/` への固定は未実施のため、両 Event の `evidence_refs` は空です。

## 取り込み時に補った値

`DE-20260710-001` と `DE-20260710-002` の出典
（`docs/decisions/2026/07/DE-20260710-00{1,2}-*.md`）には Schema 必須フィールドの一部が
ありませんでした。**推測した値を以下に明記します。誤りがあれば Correction Event で訂正してください。**

| フィールド | 値 | 根拠 |
| --- | --- | --- |
| `recorded_at` | `2026-07-28T10:16:12+09:00` | 出典に記載なし。**この Ledger へ追記した時刻**を入れた。`recorded_at` の定義は「システムへ登録した時刻」であり、2026-07-10 時点にシステムは存在しなかった |
| `approved_at` | `occurred_at` と同じ | 出典は「ステータス: Approved」「時刻: 14:00 / 15:00 JST」のみ。DE-20260710-003 も `approved_at == occurred_at` であり、同一セッション内の承認と読める |
| `effective_at` | `occurred_at` と同じ | 同上 |
| `event_id` | `de_aa0001` / `de_bb0001` | 出典の「旧表示 ID」をそのまま使った。ULID を発行すると識別子を捏造することになる |
| `primary_object_id` | `do_01J2H_EXAMPLE_TRANSITION_ENGINE` | 出典は `DO-0001` と書いているが、DE-20260710-003（正本・ハッシュ確定済み）はこの ID を使っている。投影を成立させるため揃えた。下記の課題 2 を参照 |
| `model_run_refs` | `mr_20260710_rojina_live_session` | 出典の 3 件はすべて同じ 2026-07-10 の ChatGPT Live セッション由来 |
| `decision_type` | `change` | いずれも既存属性の変更 |

`title` / `changes` / `rationale` / `proposed_by` / `approved_by` は出典の記述をそのまま移しました。

## 未解決の課題

`./scripts/signity verify` と `state` が機械的に検出したものです。

### 1. Decision Object を成立させる create Event がない

`./scripts/signity state --object do_01J2H_EXAMPLE_TRANSITION_ENGINE` を実行すると、
strict モードで投影が失敗します。

```text
DE-20260710-003: /identity/name の before が現在値と違う（before='AI Company' / 現在=None）
DE-20260710-001: /architecture/versioning_focus の before が現在値と違う（before='git-centered' / 現在=None）
```

先頭 Event の `before` が「Ledger 開始前の状態」を指しているためです。
`AI Company` という名称と `git-centered` という方針は、記録される前から存在していました。

`docs/domain/decision-object-0001.md` は `created_event_id: DE-20260710-003` としていますが、
その Event の `decision_type` は `create` ではなく `change` です。

**必要な決定:** Decision Object の初期状態を確定する `create` Event を
先頭に追記するか、`before` を投影の開始点として扱わないことにするか。

`--lenient` を付けると不一致を警告に留めて投影を続けます。

### 2. `primary_object_id` が例示値のまま

`do_01J2H_EXAMPLE_TRANSITION_ENGINE` は文字列に `EXAMPLE` を含んでいます。
正本シードの値であるため変更していません（変更すると `f9eb8528…` が無効になります）。

**必要な決定:** 正式な Object ID を発行し、Correction Event で移行するか、この値を正式採用するか。

### 3. evidence_refs が解決しない

`./scripts/signity verify` が報告します。

```text
ev_20260710_chatgpt_live_transition_engine（参照元: DE-20260710-003, DE-20260710-001, DE-20260710-002）
ev_20260710_morning_brief（参照元: DE-20260710-003）
```

いずれも `docs/evidence/` に対応する記録がありません。
2026-07-10 の ChatGPT Live 対話と朝のブリーフィングの内容が Evidence として保存されていないためです。

**必要な作業:** 当該 Evidence を `docs/evidence/2026/07/` に記録する。
一次資料が残っていない場合は `attestation`（人間による証言）として記録する。

### 4. lifecycle と governance が Event になっていない

`docs/domain/decision-object-0001.md` の state model には
`lifecycle.stage: concept` と `governance.human_approval_required: true` がありますが、
これらを設定した Decision Event が存在しないため、投影に現れません。

**必要な決定:** 手入力の値として文書に残すのをやめ、Decision Event として記録する。
