#!/usr/bin/env bash
# 指定日の journal を用意する。既にあれば何もしない（冪等）。
#
#   ./scripts/new-journal.sh                       # 今日 (JST)
#   ./scripts/new-journal.sh --yesterday --nightly  # 夜間キャプチャループが使う形
#   ./scripts/new-journal.sh 2026-09-09
#   ./scripts/new-journal.sh 2026-09-09 --nightly   # 夜間スキャン用のひな形を使う
#
# 夜間キャプチャループは 01:00 JST に走り、対象日は前日です。日付を省略するときは
# --yesterday を付けてください。
#
# 標準出力に journal のパスを返す。

set -euo pipefail

cd "$(dirname "$0")/.."

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
TEMPLATE="templates/journal-daily.md"
DATE=""
for arg in "$@"; do
  case "$arg" in
    --yesterday) BACK=1 ;;
    --nightly)   TEMPLATE="templates/nightly-scan-section.md" ;;
    --*)         echo "不明なオプション: $arg" >&2; exit 1 ;;
    *)           DATE="$arg" ;;
  esac
done

[ -n "$DATE" ] || DATE="$(jst_date "$BACK")"

if ! printf '%s' "$DATE" | grep -Eq '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'; then
  echo "日付は YYYY-MM-DD 形式で指定してください: $DATE" >&2
  exit 1
fi

YEAR="${DATE:0:4}"
MONTH="${DATE:5:2}"
DIR="docs/journal/$YEAR/$MONTH"
FILE="$DIR/$DATE.md"

if [ -e "$FILE" ]; then
  echo "$FILE"
  exit 0
fi

mkdir -p "$DIR"
sed "s/YYYY-MM-DD/$DATE/g" "$TEMPLATE" > "$FILE"
echo "$FILE"
