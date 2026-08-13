# hip4_market_data

Research archive for Hyperliquid HIP-4 World Cup markets.

During the World Cup I collected a large amount of HIP-4 market data on Hyperliquid on my server and tested several directions:

- market microstructure for selective market making
- lag detection between related markets
- execution feasibility under shallow books
- order-book impulse and liquidity event analysis

The main conclusion was negative but useful: there were visible inefficiencies, and in some cases clear lag, but the market quality was usually too thin to convert those signals into a robust deployable strategy. In practice, fills were the constraint. A naive MM in these markets would mostly behave like a money rinser unless it was extremely selective about where and when to quote.

## Research summary

Three areas produced the most signal:

- Microstructure: some markets had enough L2 and BBO coverage to study book pressure, spread behavior, and local liquidity shocks.
- Cross-market lag: related markets sometimes moved with observable delay, but exploitable size was usually not available at the prices you would need. I mainly looked for lag between the separate game markets and the implied probability of a team winning the World Cup.
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

I cannot put the full datasets into this repo because they are too large for GitHub.

For public publication, the repo is intended to showcase how the timeseries are structured sampled excerpts rather than full raw captures. See [docs/samples.md](docs/samples.md).



The collectors generally subscribe to:

- websocket trades
- websocket BBO
- websocket L2 book
- websocket candles
- periodic REST snapshots for mids and books

[Hyperliquid websocket docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket)


Some collectors also derive event files such as impulse or order-book pressure events.



## workflow:  

1. Run a market-specific collector during live trading.
2. Store raw websocket and REST snapshots under `outputs/<dataset>/`.
3. Export local HIP-4 database snapshots when needed.
4. Run monitor or backtest tools against the stored data.
5. Compare apparent signal quality against actual executable liquidity.

This last step is where most ideas failed.

See [docs/datasets.md](docs/datasets.md), [docs/findings.md](docs/findings.md),
[docs/samples.md](docs/samples.md), and [docs/visuals.md](docs/visuals.md).
