# EV-20260728-001: Google Drive 上の Signity 設計文書一式

```yaml
evidence_id: ev_20260728_drive_design_documents
display_id: EV-20260728-001
evidence_type: reference
source: 文書 (Google Drive)
source_ref: https://drive.google.com/drive/folders/1gmMKuOUB3Khr181upLhpIOFblMcwT7nv
captured_at: "2026-07-28T10:16:12+09:00"
captured_by: actor_ken
content_hash: null   # reference のためスナップショットなし
```

## 内容

Signity のドキュメント階層を設計するにあたり参照した一次資料。すべて Google Drive 上に存在する。

| 文書 | 作成日 | 取り込み状況 |
| --- | --- | --- |
| `Signity_Decision_OS_Architecture_v0.2.md` | 2026-07-10 | 取り込み済み → `docs/architecture/signity-decision-os-architecture-v0.2.md` |
| `signity-transition-engine-architecture-v0.3.md` | 2026-07-10 | 取り込み済み → `docs/architecture/signity-transition-engine-architecture-v0.3.md` |
| `README (1).md` | 2026-07-10 | 内容を `README.md` / `docs/README.md` へ反映 |
| `codex-handoff.md` | 2026-07-10 | 取り込み済み → `docs/development/codex-handoff.md` |
| `sample.de_signity_rename.v0.2.yaml` | 2026-07-10 | 取り込み済み → `seed/sample.de_signity_rename.v0.2.yaml` |
| `signity-transition-engine-docs-v0.3.zip` | 2026-07-10 | **未取り込み** |
| `signity_ui_wireframe_ja_bundle.zip` | 2026-07-11 | **未取り込み** |

## 階層設計の根拠となった記述

`README (1).md` に記載されていたリポジトリ構成。

```text
signity-transition-engine/
├── AGENTS.md
├── README.md
├── docs/
│   ├── architecture/
│   ├── product/
│   ├── domain/
│   ├── decisions/
│   └── development/
├── schemas/
└── seed/
```

`README (1).md` に記載されていた Source of truth の優先順位。

1. `docs/architecture/signity-transition-engine-architecture-v0.3.md`
2. `schemas/decision-event.schema.v0.3.json`
3. `seed/sample.de_product_rename.v0.3.yaml`
4. `docs/product/concept-v0.1.md`
5. `docs/domain/decision-object-0001.md`
6. `docs/decisions/` 以下のイベント記録

## 参照している Decision Event

- DE-20260728-001
