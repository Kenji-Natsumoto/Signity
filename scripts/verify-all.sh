#!/usr/bin/env bash
# 取り込み正本のハッシュ、Ledger のチェーン、テストをまとめて検証する。
#
#   ./scripts/verify-all.sh

set -uo pipefail

cd "$(dirname "$0")/.."

fail=0

echo "=============================================="
echo " 1. 取り込み正本の SHA-256 照合 (MANIFEST)"
echo "=============================================="
./scripts/verify-manifest.sh || fail=1

echo
echo "=============================================="
echo " 2. Decision Event の Schema 適合"
echo "=============================================="
./scripts/signity validate || fail=1

echo
echo "=============================================="
echo " 3. Ledger のハッシュチェーン"
echo "=============================================="
./scripts/signity verify || fail=1

echo
echo "=============================================="
echo " 4. canonical-json-v1 のテスト"
echo "=============================================="
PYTHONPATH="$PWD/tools" python3 -m unittest discover -s tools/tests -t tools -q || fail=1

echo
if [ "$fail" -eq 0 ]; then
  echo "すべて成功"
else
  echo "失敗あり"
fi
exit "$fail"
