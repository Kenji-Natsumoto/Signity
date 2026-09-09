# DE-20260909-001: 夜間キャプチャループを Signity の Capture 層として導入する

> 承認後はこのファイルを編集しないでください。
> 訂正が必要な場合は `corrects_event_id` を持つ新しい Correction Event を作成します。

機械可読な正本: [`ledger/events/0004-DE-20260909-001.json`](../../../../ledger/events/0004-DE-20260909-001.json)
運用仕様: [`docs/development/nightly-capture-loop.md`](../../../development/nightly-capture-loop.md)

```yaml
schema_version: "0.3"
event_id: de_20260909_nightly_capture_loop
display_id: DE-20260909-001
event_kind: decision
decision_type: create
status: approved
primary_object_id: do_signity_umbrella
occurred_at: "2026-09-09T10:30:00+09:00"
recorded_at: "2026-09-09T10:36:53+09:00"
approved_at: "2026-09-09T10:58:36+09:00"
effective_at: "2026-09-09T22:30:00+09:00"
approved_by:
  - actor_ken
integrity:
  algorithm: sha256
  canonicalization: canonical-json-v1
  previous_event_hash: 5e0e8661366341b8c87e5e51d4d920f9c4bae772137619ba94c308867c07a462
  content_hash: 06be2fbb308eb4025bc13d24f7b4579230c571ea807aba140724be659593b31d
```

## 背景

`docs/README.md` 3 章の日次運用フローは、次の 5 段階を人間が手で行う前提で書かれていました。

1. その日の journal を作る
2. 会議・対話・Slack で出たものをそのまま書く
3. 状態遷移の候補に印を付ける
4. その日の最後に候補を見直し、承認するものを Decision Event にする
5. 承認したものを反映する

この前提のまま運用した結果、`docs/journal/` には 2026-07-28 と 2026-07-29 の 2 日分しか
残りませんでした。DE-20260728-001 の success_metrics「2 週間で journal が 10 営業日分
蓄積されている」は達成されず、同 Event の revisit_triggers「日次 journal の運用が
2 週間継続できなかったとき」に該当しています。

**日次蓄積が人手に依存している限り、抜けた日の情報は永久に復元できません。**

## 決定内容

1〜3（journal 作成・観測の書き起こし・候補への印付け）を機械に任せ、
4（承認）は人間に残します。「確定して記録する」の意味を 3 層に分けます。

| 層 | 名前 | 誰が確定するか | 出力先 |
| --- | --- | --- | --- |
| L1 | Observed | AI が確定してよい | journal の「観測」 |
| L2 | Candidate | AI は提示のみ | journal の「候補」＋ `ledger/pending/` |
| L3 | Approved | 人間のみ | `ledger/events/` |

**夜間ループが確定するのは L1 だけです。** `ledger/events/` に書き込みません。
`status: approved` を自分で付けません。

判定は三分類にします。

- 決まったこと（主体・内容・効力発生時点が揃っていて反対が出ていない）
- 決まっていないこと（論点が提示され、結論が出ていない）
- **決まったつもりのもの**（合意に見えるが、主体・期日・範囲のいずれかが欠けている）

3 つ目の可視化が主目的です。滞留と誤解はここから生まれます。
横断で「返していない球」も検出します。

## 検討した選択肢

| 選択肢 | 採否 | 理由 |
| --- | --- | --- |
| 人間が毎晩 journal を手で書く運用を継続する | 不採用 | 2 週間で破綻したことが観測されている |
| AI が全ソースをスキャンし、決定まで確定して `ledger/events/` に追記する | 不採用 | `AGENTS.md` 3 章「人間の承認なしに Decision Event を確定しない」に反する |
| AI が観測のみ確定し、候補と Draft を提示して、承認は人間が翌朝行う | **採用** | 人間の仕事を「思い出して書き起こすこと」から「並べられた候補を承認するか決めること」に変えられる |

## 根拠 (Evidence)

- 2026-09-09 の要望（10:30）: 「夜就寝したら、案件・部門ごとに連携させている Slack・メール・
  その他メッセンジャー・SNS の情報と、Mac に格納されているその日決まったこと・決まっていないこと・
  議事録をすべてスキャンして、最新の情報を確定して記録する。これを毎日繰り返すループを作りたい。」
- [`docs/journal/2026/09/2026-09-09.md`](../../../journal/2026/09/2026-09-09.md)

Evidence Record としての固定は未了です（`evidence_refs` は空）。

## 影響

- `docs/development/nightly-capture-loop.md` が Capture 層の運用仕様になります。
- `docs/journal/YYYY/MM/YYYY-MM-DD.md` に加えて `YYYY-MM-DD.scan.json`（機械可読な
  スキャン記録）が毎日増えます。取得できなかったソースは `status: unavailable` として
  必ず記録します。**読めなかったものを黙って省略しません。**
- 業務の生ログは Git に入れません。参照（Slack permalink / Gmail message id / Drive file id）と
  要約だけを書きます。
- Claude Code Remote は隔離コンテナで動くため Mac のファイルに触れません。ローカル素材は
  `scripts/mac-collect.sh`（launchd 22:20 JST）が `docs/journal/inbox/` へ push する橋渡しに
  依存します。橋渡しが止まればローカル素材は静かに欠落します（`scan.json` で検出）。

## 見直しの契機

- 2 週間運用して journal が 10 日分蓄積されなかったとき
- 生成された Draft の承認率が著しく低いとき（候補の質が低い）
- コネクタのないソースが業務の主戦場になったとき
- 案件 / 部門を Decision Object として定義したとき

`expected_outcome.review_due_at` は 2026-09-23。

## この Event が決めていないこと

- **起動時刻。** `effective_at` は 22:30 JST を置いていますが、Routine の登録は
  この Event に含まれません。2026-09-09 時点で Routine は未登録です。
- **案件 / 部門の Decision Object 化。** 当面はチャンネル名・スレッド・参加者からの
  ヒューリスティックです。
- **inbox 素材を `docs/evidence/` へ昇格させる判断を誰がいつ行うか。**
