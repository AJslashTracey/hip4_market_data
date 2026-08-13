# Findings

## Core conclusion

The data showed multiple forms of inefficiency, but not a robust deployable edge.

The strongest recurring pattern was this:

- apparent signal existed
- order-book depth was too weak
- fills were too hard to obtain at the required prices
- realized opportunity was materially worse than observed opportunity

## What looked promising

### 1. Selective market making

The initial idea was not broad MM across all HIP-4 markets. The only plausible version was highly selective deployment into markets with:

- wider spreads
- enough displayed depth to survive quote improvement
- stable enough parity behavior between paired outcomes

This was the logic behind ranking datasets for execution simulation and the existence of `mm_backtest.py`.

What failed:

- top-of-book depth was often too small
- improving the quote increased adverse-selection exposure
- the best-looking opportunities were often not meaningfully fillable

### 2. Cross-market lag

Related markets sometimes moved with visible delay. This was real enough to be interesting.

What failed:

- lag did not imply executable edge
- the resting book usually could not provide enough size
- by the time a trade was realistically fillable, much of the value was gone

### 3. Order-book impulse analysis

Some captures, especially `france_sweden_orderbook_live`, are strong enough to study:

- book pressure shifts
- local liquidity withdrawal
- spread changes around impulses
- short-horizon microstructure response

This is the most publishable part of the archive even if it did not lead to a production strategy.

## Why the result still matters

Negative trading research is still research. This project demonstrates:

- how to collect structured live prediction-market data
- how to compare perceived inefficiency with executable inefficiency
- how thin books can invalidate otherwise valid signals

The useful output is not "here is alpha." It is "here is a concrete example of why apparent alpha in shallow markets often does not survive execution."
