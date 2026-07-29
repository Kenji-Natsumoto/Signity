# EV-20260728-002: Signity Transition Engine 文書バンドル v0.3

```yaml
evidence_id: ev_20260728_transition_engine_docs_v03
display_id: EV-20260728-002
evidence_type: snapshot
source: 文書 (Google Drive)
source_ref: signity-transition-engine-docs-v0.3.zip
source_file_id: 1yBHSGjvle0_CnURvVDcXZiw9SDKgoHic
generated_at: "2026-07-10T00:00:00+09:00"
captured_at: "2026-07-28T10:16:12+09:00"
captured_by: actor_ken
verification: manifest-sha256-verified
```

## 内容

2026-07-10 に生成された Signity Transition Engine の文書バンドル。
バンドル同梱の `MANIFEST.md` が全ファイルの SHA-256 を記録しているため、
取り込み時に全件を照合した。

- Package: Signity Transition Engine documents v0.3
- Generated: 2026-07-10
- Files: 11
- JSON Schema validation: passed
- Prohibited-name scan: passed

## 検証結果

取り込んだ 10 ファイルすべてが MANIFEST の SHA-256 と一致した。

| ファイル（バンドル内パス） | SHA-256 | 照合 |
| --- | --- | --- |
| `docs/architecture/signity-transition-engine-architecture-v0.3.md` | `efa1d5b6…04791f35` | 一致 |
| `docs/decisions/de-aa0001.md` | `47807a04…2524a84f` | 一致 |
| `docs/decisions/de-bb0001.md` | `4ef50c56…75067e6f` | 一致 |
| `docs/decisions/de-cc0001.md` | `0db6d13f…af4f6c409` | 一致 |
| `docs/development/codex-handoff.md` | `01ac8a95…4834e30f` | 一致 |
| `docs/domain/decision-object-0001.md` | `f05c180e…104b880c` | 一致 |
| `docs/product/concept-v0.1.md` | `22c7c354…b50fe5cea` | 一致 |
| `schemas/decision-event.schema.v0.3.json` | `a31341f5…11ff995f3` | 一致 |
| `seed/sample.de_product_rename.v0.3.yaml` | `af27acc6…cafe08981b` | 一致 |

バンドル同梱の `AGENTS.md` / `README.md` は、このリポジトリが umbrella brand `Signity` を
対象としているため取り込まず、リポジトリ固有の内容で作成した。

再検証は `scripts/verify-manifest.sh` で行える。

## 取り込み時のパス変更

Decision Event はこのリポジトリの命名規則（表示 ID ベース）へ改名した。
`de-aa0001` 等の旧表示 ID は、v0.2 アーキテクチャ 7 章で
「属性や意味を ID 自体に埋め込みすぎない」として見直し対象になっていたもの。

内容は 1 バイトも変更していないため、SHA-256 による照合は改名後も成立する。

| バンドル内パス | リポジトリ内パス |
| --- | --- |
| `docs/decisions/de-aa0001.md` | `docs/decisions/2026/07/DE-20260710-001-versioning-focus-event-centered.md` |
| `docs/decisions/de-bb0001.md` | `docs/decisions/2026/07/DE-20260710-002-capture-checkpoint-interval.md` |
| `docs/decisions/de-cc0001.md` | `docs/decisions/2026/07/DE-20260710-003-rename-to-transition-engine.md` |
| `MANIFEST.md` | `docs/evidence/2026/07/EV-20260728-002-manifest-v0.3.md` |

その他のファイルはバンドル内と同じ相対パスに配置した。

## 発見した矛盾

取り込み時に、文書間の矛盾を 3 件確認した。
`AGENTS.md` の規約に従い、独断で修正せず矛盾として記録する。

### 1. プロジェクト名称の到達点が v0.2 と v0.3 で異なる

同一の意思決定（`/identity/name` の変更）について、2 つの記述が存在する。

| 出典 | before | after |
| --- | --- | --- |
| `seed/sample.de_signity_rename.v0.2.yaml` | AI Company | **Signity** |
| `seed/sample.de_product_rename.v0.3.yaml` | AI Company | **Signity Transition Engine** |
| `docs/decisions/2026/07/DE-20260710-003-…` | AI Company | **Signity Transition Engine** |

どちらも `DE-20260710-003` を名乗り、`occurred_at` も同じ 2026-07-10。
umbrella brand（Signity）とプロダクト名（Signity Transition Engine）が
1 つの Decision Event に混在している可能性がある。

### 2. Drive 上の architecture v0.3 に 2 つの版が存在する

| 出典 | SHA-256 | 差異 |
| --- | --- | --- |
| バンドル内（正本） | `efa1d5b6…04791f35` | — |
| Drive 単体 `.md` ファイル | `1d013d96…cc27113c` | 3.1 節が「適用しした」（誤記） |

リポジトリにはバンドル内の正本を採用した。

### 3. `de-bb0001` の before 値が v0.2 アーキテクチャの記述と異なる

- `docs/decisions/2026/07/DE-20260710-002-…`: `before: null`
- `docs/architecture/signity-decision-os-architecture-v0.2.md` 9 章:
  `before: null または ad-hoc`

v0.3 側で `null` に確定したものと読めるが、明示的な決定記録はない。

## 参照している Decision Event

- DE-20260728-001
