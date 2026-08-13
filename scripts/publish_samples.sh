#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_ROOT="/home/aj/deploy-box/algo/outputs"
DST_ROOT="$ROOT/data/samples"
LINES="${LINES:-3000}"

mkdir -p "$DST_ROOT"

copy_head() {
  local src="$1"
  local dst="$2"
  local parent
  parent="$(dirname "$dst")"
  mkdir -p "$parent"
  head -n "$LINES" "$src" > "$dst"
  printf 'sampled %s -> %s (%s lines)\n' "$src" "$dst" "$LINES"
}

write_manifest() {
  local dataset="$1"
  local dir="$2"
  local manifest="$dir/SAMPLE_INFO.md"
  cat > "$manifest" <<EOF
# ${dataset}

This folder contains publication samples from \`${dataset}\`.

- source: \`${SRC_ROOT}/${dataset}\`
- sampling_rule: first ${LINES} lines per included file
- purpose: representative structural sample for public inspection

Included files are truncated excerpts, not full captures.
EOF
}

sample_dataset() {
  local dataset="$1"
  shift
  local out_dir="$DST_ROOT/$dataset"
  mkdir -p "$out_dir"
  write_manifest "$dataset" "$out_dir"
  for rel in "$@"; do
    copy_head "$SRC_ROOT/$dataset/$rel" "$out_dir/$rel"
  done
}

sample_dataset "france_sweden_orderbook_live" \
  "metadata.jsonl" \
  "ws_bbo.jsonl" \
  "ws_trades.jsonl" \
  "ws_l2book.jsonl" \
  "ws_l2_impulses.jsonl" \
  "orderbook_pressure_events.csv" \
  "rest_mid_samples.csv"

sample_dataset "france_morocco_live" \
  "metadata.jsonl" \
  "ws_bbo.jsonl" \
  "ws_trades.jsonl" \
  "ws_l2book.jsonl" \
  "event_shocks.jsonl" \
  "event_state_snapshots.jsonl" \
  "rest_mid_samples.csv"

sample_dataset "argentina_egypt_live" \
  "metadata.jsonl" \
  "ws_bbo.jsonl" \
  "ws_trades.jsonl" \
  "ws_l2book.jsonl" \
  "rest_mid_samples.csv"

printf 'published samples under %s\n' "$DST_ROOT"
