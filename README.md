# hip4_market_data

Research archive for Hyperliquid HIP-4 World Cup markets.

During the World Cup I collected a large amount of HIP-4 market data on Hyperliquid and tested several directions:

- market microstructure for selective market making
- lag detection between related markets
- execution feasibility under shallow books
- order-book impulse and liquidity event analysis

The main conclusion was negative but useful: there were visible inefficiencies, and in some cases clear lag, but the market quality was usually too thin to convert those signals into a robust deployable strategy. In practice, fills were the constraint. A naive MM in these markets would mostly behave like a money rinser unless it was extremely selective about where and when to quote.

## What is in scope

This repo is for:

- collector scripts used to record live HIP-4 market data
- exported datasets and dataset quality notes
- monitor/backtest utilities used to evaluate liquidity and quoting conditions
- documentation of what was tried, what looked promising, and why it still failed

This repo is not claiming a profitable strategy. The point is to preserve the work, the data, and the reasoning.

## Research summary

Three areas produced the most signal:

- Microstructure: some markets had enough L2 and BBO coverage to study book pressure, spread behavior, and local liquidity shocks.
- Cross-market lag: related markets sometimes moved with observable delay, but exploitable size was usually not available at the prices you would need.
- Execution simulation: market-making opportunity scores looked better on paper than in live fill-constrained conditions.

The practical bottleneck across almost all ideas was the same:

- weak depth at the top of book
- inconsistent executable size
- adverse selection risk after improving quotes
- insufficient fill quality even when directionally correct

## Best datasets

The strongest datasets are not the same for every use case.

### For microstructure research

1. `argentina_cape_verde_live`
2. `france_sweden_orderbook_live`
3. `france_morocco_live`

### For lag detection

1. `argentina_egypt_live`
2. `france_morocco_live`
3. `germany_paraguay_live` / `netherlands_morocco_live`

### For execution simulation

1. `france_morocco_live`
2. `france_sweden_orderbook_live`
3. `argentina_egypt_live`

Weakest quality were the smoke or test captures:

- `brazil_japan_live_test`
- `netherlands_morocco_live_smoke`
- `norway_ivory_coast_live_smoke`

`brazil_japan_live` is weaker for cross-market lag work specifically because champion-market BBO coverage was missing from the exported set, even though raw game-market files exist.

## Highlight dataset

`france_sweden_orderbook_live` is one of the best order-book research captures:

- `ws_l2book.jsonl`: 133,111 lines
- `ws_bbo.jsonl`: 4,965 lines
- `ws_trades.jsonl`: 1,744 lines
- `ws_l2_impulses.jsonl`: 3,606 lines
- `orderbook_pressure_events.csv`: 133,106 lines

That makes it especially useful for order-book impulse analysis, even if it is not the best trade-density dataset.

## Data layout

The original working material currently lives outside this repo under:

- `/home/aj/deploy-box/algo`
- `/home/aj/deploy-box/algo/outputs`

This repo includes documentation and a sync script so the relevant files can be copied in cleanly.

For public publication, the repo is intended to track sampled excerpts rather than full raw captures. See [docs/samples.md](/home/aj/github/hip4_market_data/docs/samples.md).

Suggested repo layout after syncing:

```text
hip4_market_data/
├── README.md
├── docs/
│   ├── datasets.md
│   └── findings.md
│   └── samples.md
├── scripts/
│   └── sync_from_deploy_box.sh
├── collectors/
├── analysis/
└── data/
    ├── raw/
    ├── samples/
    └── derived/
```

## Key source scripts

From the original working directory:

- collectors: `collect_*_game.py`
- market monitor: `monitor_hip4_outcomes.py`
- execution simulation: `mm_backtest.py`
- export utility: `export_local_db.py`
- unified timeseries builder: `build_unified_timeseries.py`

The collectors generally subscribe to:

- websocket trades
- websocket BBO
- websocket L2 book
- websocket candles
- periodic REST snapshots for mids and books

Some collectors also derive event files such as impulse or order-book pressure events.

## Reproduction notes

Typical workflow in the original project:

1. Run a market-specific collector during live trading.
2. Store raw websocket and REST snapshots under `outputs/<dataset>/`.
3. Export local HIP-4 database snapshots when needed.
4. Run monitor or backtest tools against the stored data.
5. Compare apparent signal quality against actual executable liquidity.

This last step is where most ideas failed.

## Why publish this

There is value in showing a serious trading research process even when the result is "do not build this." This archive is intended to show:

- what was collected
- how the data was structured
- what hypotheses were tested
- where the edge looked real
- why the edge was still not monetizable

## Next steps

- Sync selected collectors and analysis scripts into this repo.
- Publish `3,000`-line excerpts into `data/samples/`.
- Add a short write-up per experiment with charts and failure modes.
- Add a compact scored dataset table for quick orientation.

See [docs/datasets.md](/home/aj/github/hip4_market_data/docs/datasets.md), [docs/findings.md](/home/aj/github/hip4_market_data/docs/findings.md), and [docs/samples.md](/home/aj/github/hip4_market_data/docs/samples.md).
