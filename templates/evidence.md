# EV-YYYYMMDD-NNN: <title>

> Evidence は意思決定の根拠となった一次資料です。
> 一度記録したら書き換えないでください。解釈や要約は Decision Event 側に書きます。

```yaml
evidence_id: ev_<ULID>
display_id: EV-YYYYMMDD-NNN
evidence_type: reference        # reference | snapshot | attestation
source: <Slack / 会議 / ChatGPT Live / 文書 / 音声 / 手入力 / コード変更>
source_ref: <URL やファイルパス>
captured_at: "YYYY-MM-DDTHH:MM:SS+09:00"
captured_by: actor_<name>
content_hash: <snapshot の場合は sha256>
```

## 種別の使い分け

- `reference`: 元データへの参照のみ
- `snapshot`: その時点の内容を保存し、ハッシュを付ける
- `attestation`: 録音等がない対面会議について、人間が「こう話し、こう決めた」と証言する

## 内容

<一次資料の本文、またはスナップショット>

## 参照している Decision Event

- DE-YYYYMMDD-NNN
