#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_ROOT="/home/aj/deploy-box/algo"

mkdir -p "$ROOT/collectors" "$ROOT/analysis" "$ROOT/data/raw" "$ROOT/data/derived"

copy_if_exists() {
  local src="$1"
  local dst="$2"
  if [[ -e "$src" ]]; then
    cp -R "$src" "$dst"
    printf 'copied %s -> %s\n' "$src" "$dst"
  else
    printf 'missing %s\n' "$src" >&2
  fi
}

for file in \
  build_unified_timeseries.py \
  export_local_db.py \
  mm_backtest.py \
  monitor_hip4_outcomes.py
do
  copy_if_exists "$SRC_ROOT/$file" "$ROOT/analysis/"
done

for file in "$SRC_ROOT"/collect_*_game.py; do
  copy_if_exists "$file" "$ROOT/collectors/"
done

for dir in \
  argentina_cape_verde_live \
  argentina_egypt_live \
  france_morocco_live \
  france_sweden_orderbook_live \
  germany_paraguay_live \
  netherlands_morocco_live
do
  copy_if_exists "$SRC_ROOT/outputs/$dir" "$ROOT/data/raw/"
done

for dir in \
  brazil_japan_live_test \
  netherlands_morocco_live_smoke \
  norway_ivory_coast_live_smoke
do
  copy_if_exists "$SRC_ROOT/outputs/$dir" "$ROOT/data/raw/"
done

printf 'sync complete\n'
