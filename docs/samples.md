# Published Samples

This repo publishes partial excerpts of selected datasets rather than full raw captures.

## Sampling rule

For each published sample file:

- keep the original filename
- copy only the first `3,000` lines
- preserve the original format (`.jsonl` or `.csv`)

These files are intended to show structure and representative activity, not to serve as the complete research corpus.

## Why sample instead of publishing the full raw data

The full captures are too large for a normal Git repository and include several files in the hundreds of megabytes. Publishing excerpts keeps the repo usable while still letting readers inspect:

- schema and message shape
- relative density of quotes, trades, and L2 updates
- derived event file structure
- the style of research data that was collected

## Included sample datasets

- `france_sweden_orderbook_live`
- `france_morocco_live`
- `argentina_egypt_live`

## Included sample file types

Depending on the dataset, samples may include:

- `metadata.jsonl`
- `ws_bbo.jsonl`
- `ws_trades.jsonl`
- `ws_l2book.jsonl`
- `rest_mid_samples.csv`
- selected derived event files

## Important caveat

Because the files are truncated to the first `3,000` lines, they are not statistically representative of the entire match window in a strict sense. They are publication samples for inspection and orientation.
