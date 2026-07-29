# Decision Event: DE-20260710-001

## タイトル

Signity Transition Engineの最初の運用原則を定める

## 基本情報

- 日付: 2026-07-10
- 時刻: 14:00 JST
- 旧表示ID: de_aa0001
- 提案者: 夏本健司 / AIエージェント・ROJINA
- 承認者: 夏本健司
- ステータス: Approved
- Primary Decision Object: DO-0001

## 状態変更

```yaml
changes:
  - path: /architecture/versioning_focus
    before: git-centered
    after: event-centered
    change_note: ファイル差分を中心に考えるのではなく、組織に採用された状態変化を中心に記録する
```

## 根拠

- ChatGPT Liveで行った2026-07-10の対話
- ファイル管理だけでは、判断理由、承認者、根拠、結果の関係を十分に表せないという検討

## 判断理由

対話を通じて、Gitやファイルを中心とした管理より、Decision Objectに対する状態変化を追記型イベントとして記録することが本質だと判断した。

## 人の価値判断

- 説明責任
- 履歴の追跡可能性
- 過去を上書きしないこと
- 特定ツールへの依存を避けること

## Integrity

- Algorithm: SHA-256
- Content hash: 承認済み正規化データから生成
- Previous event hash: なし
- Digital signature: MVP後続段階
