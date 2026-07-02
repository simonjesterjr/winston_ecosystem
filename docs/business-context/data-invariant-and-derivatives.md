# Data Invariant: 3+ Years and DM-Owned Derivatives

**Type:** Domain rule (authoritative for ecosystem)
**Related ADR:** ADR-003
**Related interface:** `interfaces/winston-eod-parquet-standard.md`

## The invariant

For every **Market** that any **Consumer** (WUT portfolio, Wv2 portfolio) cares about, **DM** must ensure:

1. **At least ~3 years** of contiguous recent end-of-day (EOD) bars, **plus** the latest trading day
2. **All required derivative columns** baked into the **Winston EOD Standard** parquet (ATR-17, supported MAs)
3. **DataCoverage** metadata in PG accurately reflects what is on disk (via **Reconciliation**)

"3+ years" means sufficient history for strategy evaluation (breakout periods, MA lookbacks, ATR warm-up). More history is acceptable; less is a gap DM must fill.

## Who owns what

| Concern | Owner | Artifact |
|---------|-------|----------|
| Fetching EOD from EODHD | DM | DownloadRun / DownloadTask |
| Computing ATR-17 and MAs | DM | parquet columns |
| Knowing what data exists | DM | DataCoverage row |
| Using data for signals | WUT, Wv2 | read parquet (or loaded activities) |
| Triggering a download | Cromwell (future), API (now) | DM trigger endpoint |

## Worked example

A Wv2 **Portfolio** has **Books** for AAPL, MSFT, IBM. On daily analysis:

1. Wv2 (or DM on behalf of consumers) verifies parquet exists for each symbol with `latest_date >= yesterday`
2. If AAPL is stale, DM fetches the gap from EODHD, recomputes atr_17 and MAs over the relevant history, writes `data/markets/AAPL/bars.parquet`
3. DM updates DataCoverage: `earliest_date`, `latest_date`, `indicators_present: ["atr_17", "sma_20", ...]`
4. Wv2 reads precomputed atr_17 from parquet for stop placement — does not recalculate

## When the invariant breaks

| Symptom | Likely cause | Resolution |
|---------|--------------|------------|
| Strategy shows no signals | Missing parquet for a Book's Market | `dm:sync_from_wv2` or consumer-triggered download |
| WUT backtest ≠ Wv2 live signals | Different indicator values | Verify both read DM parquet; check DM atr_17 semantics |
| DM thinks data missing but files exist | PG out of sync | Run `data:reconcile` |

## Source of truth hierarchy

1. On-disk parquet (what actually exists)
2. DataCoverage (what DM believes exists — must match after reconciliation)
3. Consumer local activities (WUT legacy path — transitional)