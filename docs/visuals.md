# Visuals

Static PNG exports of selected HTML research dashboards from the original local
analysis workspace.

These are included as documentation artifacts rather than complete interactive
dashboards. Each visual is linked to the dataset or dataset family it explains.

## `argentina_egypt_live`

Dataset sample:
[`data/samples/argentina_egypt_live`](../data/samples/argentina_egypt_live)

This dataset is the strongest published sample for cross-market lag detection.
The visuals below show both the apparent opportunity and the execution problem
that made the signal hard to monetize.

![Argentina vs Egypt failed lag exploit](assets/visuals/argentina_egypt_failed_lag_exploit.png)

Source HTML:
`outputs/failed_lag_exploit_viz/argentina_egypt_failed_lag_exploit.html`

![Argentina vs Egypt market dashboard](assets/visuals/argentina_egypt_market_dashboard.png)

Source HTML:
`outputs/world_cup_match_analysis/argentina_egypt_live_2026-07-07_19-40-57Z/dashboard.html`

## `france_sweden_orderbook_live`

Dataset sample:
[`data/samples/france_sweden_orderbook_live`](../data/samples/france_sweden_orderbook_live)

This is the strongest published order-book sample. These visuals summarize
lag-response behavior and the asymmetric quality of France and Sweden response
signals.

![France vs Sweden order-book overview](assets/visuals/france_sweden_orderbook_overview.png)

Source HTML:
`outputs/france_sweden_orderbook_analysis/overview.html`

![France order-book lag dashboard](assets/visuals/france_sweden_france_lag_dashboard.png)

Source HTML:
`outputs/france_sweden_orderbook_analysis/france_lag_dashboard.html`

![Sweden order-book lag dashboard](assets/visuals/france_sweden_sweden_lag_dashboard.png)

Source HTML:
`outputs/france_sweden_orderbook_analysis/sweden_lag_dashboard.html`

## Cross-Market Lead-Lag Summary

Linked datasets:

- [`argentina_egypt_live`](../data/samples/argentina_egypt_live)
- [`france_morocco_live`](../data/samples/france_morocco_live)
- `germany_paraguay_live`
- `netherlands_morocco_live`

The cross-market overview is useful as a summary figure, but only the first two
linked datasets above currently have public samples in this repository.

![Cross-market lead-lag overview](assets/visuals/cross_market_lead_lag_overview.png)

Source HTML:
`outputs/cross_market_lead_lag_all/lead_lag_dashboard.html`

## World Cup Showcase

Static PNG exports of the cleaner World Cup showcase dashboards.

These were added here so the World Cup visuals render directly inside GitHub,
without needing to open local HTML files. The new set keeps the useful
match-vs-outright comparison and drops the older gross-edge framing.

### Overview

![World Cup showcase overview](assets/visuals/world_cup_showcase_overview.png)

Source HTML:
`outputs/world_cup_showcase/showcase_overview.html`

### Brazil vs Japan

![Brazil vs Japan showcase](assets/visuals/world_cup_brazil_japan_showcase.png)

Source HTML:
`outputs/world_cup_showcase/world_cup_round_of_32_brazil_vs_japan.html`

### Germany vs Paraguay

![Germany vs Paraguay showcase](assets/visuals/world_cup_germany_paraguay_showcase.png)

Source HTML:
`outputs/world_cup_showcase/world_cup_round_of_32_germany_vs_paraguay.html`

### Netherlands vs Morocco

![Netherlands vs Morocco showcase](assets/visuals/world_cup_netherlands_morocco_showcase.png)

Source HTML:
`outputs/world_cup_showcase/world_cup_round_of_32_netherlands_vs_morocco.html`

### Ivory Coast vs Norway

![Ivory Coast vs Norway showcase](assets/visuals/world_cup_ivory_coast_norway_showcase.png)

Source HTML:
`outputs/world_cup_showcase/world_cup_round_of_32_ivory_coast_vs_norway.html`

### Argentina vs Egypt

![Argentina vs Egypt showcase](assets/visuals/world_cup_argentina_egypt_showcase.png)

Source HTML:
`outputs/world_cup_showcase/world_cup_round_of_16_argentina_vs_egypt.html`

What the new World Cup pages show:

- Raw match-market mids and matching champion-yes mids for the same teams.
- Rebased move-from-open views in basis points, so reaction size is easier to compare.
- Quoted spread in basis points of mid, which makes low-priced outrights and higher-priced match markets comparable.
- Trade activity by minute, so you can see whether moves were actually printing or only sitting in quotes.
