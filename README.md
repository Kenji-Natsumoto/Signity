# Signity

> 組織は、採用された意思決定と、その根拠・実行・結果の連鎖によってバージョン管理される。

Signity は、会議・対話・Slack・文書・AI エージェントの出力など、外部化された情報から
組織として採用された認識・方針・コミットメントの変化を検出し、追記型のイベントとして記録する
**Decision OS** です。

このリポジトリは Signity のドキュメントを蓄積していくための正本置き場です。
コードではなく、**意思決定とその根拠の履歴**が中心にあります。

- Umbrella brand: `Signity`
- Product owner: 夏本健司
- Documentation start: 2026-07-28

## まずここを読む

| 目的 | 読む場所 |
| --- | --- |
| ドキュメント階層と運用ルールを知る | [`docs/README.md`](docs/README.md) |
| Signity の設計思想を知る | [`docs/architecture/`](docs/architecture/) |
| 何が決まったかを追う | [`docs/decisions/`](docs/decisions/) |
| 今日何があったかを追う | [`docs/journal/`](docs/journal/) |
| AI エージェントとして作業する | [`AGENTS.md`](AGENTS.md) |
| 毎晩の自動スキャンの仕組みを知る | [`docs/development/nightly-capture-loop.md`](docs/development/nightly-capture-loop.md) |

## リポジトリ階層

```text
Signity/
├── AGENTS.md            # AI エージェント向けの作業規約
├── README.md            # このファイル
├── docs/
│   ├── architecture/    # 設計・アーキテクチャ（バージョン付き・確定文書）
│   ├── product/         # プロダクト定義・コンセプト・スコープ
│   ├── domain/          # ドメインモデル・Decision Object の定義
│   ├── decisions/       # Decision Event（承認済みの意思決定記録）
│   ├── evidence/        # Evidence（意思決定の根拠となった一次資料）
│   ├── journal/         # 日次ログ（未整理の素材・観測）
│   └── development/     # 開発手順・ハンドオフ・運用
├── ledger/
│   ├── events/          # 承認済み Decision Event（追記専用・ハッシュチェーン）
│   └── pending/         # Draft（承認待ち）
├── schemas/             # JSON Schema / バリデーション規則
├── scripts/             # CLI ラッパーと検証スクリプト
├── seed/                # サンプル・シードデータ
├── templates/           # 各ドキュメント種別のひな形
└── tools/signity/       # Ledger の参照実装（canonical-json-v1 / 投影 / 検証）
```

`docs/decisions/` が人間向けの記録、`ledger/events/` が機械可読な正本です。

## 動かす

```sh
./scripts/verify-all.sh    # 正本ハッシュ・Schema・チェーン・テストをまとめて検証
```

```sh
./scripts/signity chain                                              # ハッシュチェーンを表示
./scripts/signity verify                                             # Ledger を検証
./scripts/signity state --object do_01J2H_EXAMPLE_TRANSITION_ENGINE  # Current State を投影
./scripts/signity hash ledger/events/0001-DE-20260710-003.json       # content_hash を計算
```

Ledger の先頭 Event の `content_hash` は、2026-07-10 時点の実装が計算した
`f9eb8528…` と同一です。詳しくは
[`docs/architecture/canonical-json-v1.md`](docs/architecture/canonical-json-v1.md)。

## 中核概念

| 概念 | 説明 |
| --- | --- |
| Decision Object | 状態やコミットメントが変化する対象の永続的な識別子 |
| Decision Event | 承認済みの意思決定を封じた追記専用イベント |
| Evidence Record | 意思決定を支えた出典（参照 / スナップショット / 証言） |
| Current State | イベント列から計算される投影（Projection）。手入力しない |
| Committed / Observed | 「承認したこと」と「現実に達成されたこと」を混同しない |

詳細は [`docs/architecture/signity-decision-os-architecture-v0.2.md`](docs/architecture/signity-decision-os-architecture-v0.2.md) を参照してください。

## 原則

1. **追記のみ。** 承認済み Decision Event は編集しない。訂正は新しい Correction Event で行う。
2. **Current State は手で書かない。** 常にイベント列からの投影として扱う。
3. **会話ログは Evidence であり、仕様書ではない。** 発言をそのまま決定にしない。
4. **人間の承認を必須にする。** AI は候補を提示するところまで。
5. **「改ざん不能」ではなく「改ざん検知可能」と表現する。**
