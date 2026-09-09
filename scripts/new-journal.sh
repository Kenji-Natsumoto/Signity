#!/usr/bin/env bash
# 指定日の journal を用意する。既にあれば何もしない（冪等）。
#
#   ./scripts/new-journal.sh                # 今日 (JST)
#   ./scripts/new-journal.sh 2026-09-09
#   ./scripts/new-journal.sh 2026-09-09 --nightly   # 夜間スキャン用のひな形を使う
#
# 標準出力に journal のパスを返す。

set -euo pipefail

cd "$(dirname "$0")/.."

DATE="${1:-}"
if [ -z "$DATE" ] || [ "${DATE:0:2}" = "--" ]; then
  DATE="$(TZ=Asia/Tokyo date +%Y-%m-%d)"
fi

if ! printf '%s' "$DATE" | grep -Eq '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'; then
  echo "日付は YYYY-MM-DD 形式で指定してください: $DATE" >&2
  exit 1
fi

TEMPLATE="templates/journal-daily.md"
for arg in "$@"; do
  [ "$arg" = "--nightly" ] && TEMPLATE="templates/nightly-scan-section.md"
done

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
