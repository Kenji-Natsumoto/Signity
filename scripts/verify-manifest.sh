#!/usr/bin/env bash
# Signity Transition Engine 文書バンドル v0.3 の整合性を再検証する。
#
# 正本の SHA-256 は docs/evidence/2026/07/EV-20260728-002-manifest-v0.3.md
# （バンドル同梱の MANIFEST.md をそのまま保存したもの）に記録されている。
# 取り込み時に一部ファイルを命名規則に合わせて改名しているため、
# バンドル内パスとリポジトリ内パスの対応をここで持つ。
#
# 使い方: ./scripts/verify-manifest.sh

set -uo pipefail

cd "$(dirname "$0")/.."

MANIFEST="docs/evidence/2026/07/EV-20260728-002-manifest-v0.3.md"

# バンドル内パス -> リポジトリ内パス
map_path() {
  case "$1" in
    docs/decisions/de-aa0001.md)
      echo "docs/decisions/2026/07/DE-20260710-001-versioning-focus-event-centered.md" ;;
    docs/decisions/de-bb0001.md)
      echo "docs/decisions/2026/07/DE-20260710-002-capture-checkpoint-interval.md" ;;
    docs/decisions/de-cc0001.md)
      echo "docs/decisions/2026/07/DE-20260710-003-rename-to-transition-engine.md" ;;
    AGENTS.md|README.md)
      echo "" ;;   # バンドル版は取り込んでいない
    *)
      echo "$1" ;;
  esac
}

ok=0; fail=0; skip=0

while read -r bundle_path expected; do
  repo_path="$(map_path "$bundle_path")"

  if [ -z "$repo_path" ]; then
    printf 'SKIP  %s (バンドル版は未取り込み)\n' "$bundle_path"
    skip=$((skip + 1))
    continue
  fi

  if [ ! -f "$repo_path" ]; then
    printf 'FAIL  %s (ファイルがない: %s)\n' "$bundle_path" "$repo_path"
    fail=$((fail + 1))
    continue
  fi

  actual="$(sha256sum "$repo_path" | cut -d' ' -f1)"
  if [ "$actual" = "$expected" ]; then
    printf 'OK    %s\n' "$repo_path"
    ok=$((ok + 1))
  else
    printf 'FAIL  %s\n      expected %s\n      actual   %s\n' "$repo_path" "$expected" "$actual"
    fail=$((fail + 1))
  fi
done < <(sed -n 's/^- `\([^`]*\)` — SHA-256 `\([a-f0-9]\{64\}\)`.*/\1 \2/p' "$MANIFEST")

printf '\n一致 %d / 不一致 %d / 未取り込み %d\n' "$ok" "$fail" "$skip"
[ "$fail" -eq 0 ]
