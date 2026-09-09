#!/usr/bin/env bash
# Mac 側コレクタ。Mac のローカル素材を Signity の inbox へ集めて push する。
#
# Claude Code Remote は隔離コンテナで動くため Mac のファイルに触れません。
# このスクリプトが Mac 側で動くことで、はじめてローカル情報が夜間ループの対象になります。
#
#   ./scripts/mac-collect.sh --yesterday    # 前日分（launchd から毎晩 00:50 に走る形）
#   ./scripts/mac-collect.sh                # 今日 (JST) の更新分
#   ./scripts/mac-collect.sh 2026-09-09
#   SIGNITY_DRY_RUN=1 ./scripts/mac-collect.sh --yesterday   # コピーも push もせず対象だけ出す
#
# 夜間キャプチャループは 01:00 JST に走り、対象日は前日です。
# launchd は 00:50 に --yesterday 付きで起動します。実行日と対象日は 1 日ずれます。
#
# 収集対象は SIGNITY_COLLECT_DIRS で上書きできます（コロン区切り）。
#   export SIGNITY_COLLECT_DIRS="$HOME/Documents/議事録:$HOME/Desktop/Signity"
#
# 除外パターンは SIGNITY_COLLECT_EXCLUDE（コロン区切りの grep -E パターン）。

set -euo pipefail

cd "$(dirname "$0")/.."
REPO="$PWD"

# JST の日付を返す。--yesterday なら前日。
# macOS (BSD date) と Linux (GNU date) の両方で動く。
jst_date() {
  local back="${1:-0}"
  if [ "$back" -eq 0 ]; then
    TZ=Asia/Tokyo date +%Y-%m-%d
  elif TZ=Asia/Tokyo date -v-1d +%Y-%m-%d >/dev/null 2>&1; then
    TZ=Asia/Tokyo date -v-1d +%Y-%m-%d          # BSD / macOS
  else
    TZ=Asia/Tokyo date -d "yesterday" +%Y-%m-%d # GNU / Linux
  fi
}

# YYYY-MM-DD の翌日を返す。スキャン窓の上端に使う。
next_day() {
  if date -j -f %Y-%m-%d -v+1d "$1" +%Y-%m-%d >/dev/null 2>&1; then
    date -j -f %Y-%m-%d -v+1d "$1" +%Y-%m-%d    # BSD / macOS
  else
    date -d "$1 + 1 day" +%Y-%m-%d              # GNU / Linux
  fi
}

BACK=0
DATE=""
for arg in "$@"; do
  case "$arg" in
    --yesterday) BACK=1 ;;
    --*)         echo "不明なオプション: $arg" >&2; exit 1 ;;
    *)           DATE="$arg" ;;
  esac
done

[ -n "$DATE" ] || DATE="$(jst_date "$BACK")"

if ! printf '%s' "$DATE" | grep -Eq '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'; then
  echo "日付は YYYY-MM-DD 形式で指定してください: $DATE" >&2
  exit 1
fi

END="$(next_day "$DATE")"

DEFAULT_DIRS="$HOME/Documents/Signity:$HOME/Documents/Meetings:$HOME/Desktop"
IFS=':' read -r -a DIRS <<< "${SIGNITY_COLLECT_DIRS:-$DEFAULT_DIRS}"

# 秘密情報の混入を防ぐ。ここを緩めないこと。
DEFAULT_EXCLUDE='(^|/)\.(env|git|ssh|aws|gnupg)(/|$)|\.(key|pem|p12|pfx|keychain|kdbx)$|(^|/)(id_rsa|id_ed25519|credentials|secrets?)(\.|$)'
EXCLUDE="${SIGNITY_COLLECT_EXCLUDE:-$DEFAULT_EXCLUDE}"

MAX_BYTES="${SIGNITY_COLLECT_MAX_BYTES:-2000000}"   # 1 ファイル 2MB まで
DEST="$REPO/docs/journal/inbox/$DATE"

echo "== Signity mac-collect =="
echo "対象日 : $DATE（$DATE 00:00:00 〜 $END 00:00:00）"
echo "実行日 : $(TZ=Asia/Tokyo date +%Y-%m-%d\ %H:%M)"
echo "収集元 : ${DIRS[*]}"
echo "収集先 : docs/journal/inbox/$DATE"
echo

found=0
copied=0
skipped=0

for dir in "${DIRS[@]}"; do
  [ -d "$dir" ] || { echo "  (なし) $dir"; continue; }

  while IFS= read -r -d '' f; do
    found=$((found + 1))

    if printf '%s' "$f" | grep -Eq "$EXCLUDE"; then
      echo "  除外   $f"
      skipped=$((skipped + 1))
      continue
    fi

    size=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f" 2>/dev/null || echo 0)
    if [ "$size" -gt "$MAX_BYTES" ]; then
      echo "  大きい $f (${size}B)"
      skipped=$((skipped + 1))
      continue
    fi

    echo "  収集   $f"
    if [ -z "${SIGNITY_DRY_RUN:-}" ]; then
      mkdir -p "$DEST"
      base="$(basename "$f")"
      target="$DEST/$base"
      n=1
      while [ -e "$target" ]; do
        target="$DEST/${base%.*}__$n.${base##*.}"
        n=$((n + 1))
      done
      cp -p "$f" "$target"
    fi
    copied=$((copied + 1))
  done < <(find "$dir" -type f -newermt "$DATE 00:00:00" ! -newermt "$END 00:00:00" -print0 2>/dev/null)
done

echo
echo "対象 $found / 収集 $copied / 除外 $skipped"

if [ -n "${SIGNITY_DRY_RUN:-}" ]; then
  echo "SIGNITY_DRY_RUN のため、コピーも push もしていません。"
  exit 0
fi

if [ "$copied" -eq 0 ]; then
  echo "収集対象なし。push しません。"
  exit 0
fi

# 収集元の一覧を残す。何を集めなかったかも夜間ループが判断できるようにする。
{
  echo "collected_at: $(TZ=Asia/Tokyo date -Iseconds)"
  echo "date: $DATE"
  echo "window: $DATE 00:00:00 .. $END 00:00:00"
  echo "host: $(hostname)"
  echo "dirs:"
  for dir in "${DIRS[@]}"; do echo "  - $dir"; done
  echo "found: $found"
  echo "copied: $copied"
  echo "skipped: $skipped"
} > "$DEST/_manifest.yaml"

# 既定はチェックアウト中のブランチ。SIGNITY_COLLECT_BRANCH で上書きできる。
BRANCH="${SIGNITY_COLLECT_BRANCH:-$(git rev-parse --abbrev-ref HEAD)}"
git add "docs/journal/inbox/$DATE"
if git diff --cached --quiet; then
  echo "変更なし。push しません。"
  exit 0
fi
git commit -q -m "Collect Mac inbox material for $DATE"

for delay in 2 4 8 16 0; do
  if git push -u origin "$BRANCH"; then
    echo "push 完了: $BRANCH"
    exit 0
  fi
  [ "$delay" -eq 0 ] && break
  echo "push 失敗。${delay}s 後に再試行します。" >&2
  sleep "$delay"
done

echo "push に 4 回失敗しました。手動で確認してください。" >&2
exit 1
