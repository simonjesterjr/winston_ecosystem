# Portfolio Correlation Litmus

**Date:** 2026-07-11  
**Plan:** [`plans/portfolio-correlation-methodology-and-score.md`](../../plans/portfolio-correlation-methodology-and-score.md)  
**ADR:** [`ADR-007`](../adr/ADR-007-portfolio-correlation-score-sot.md)  
**Implementation:** WUT `PortfolioCorrelationLitmus`, `MarketSeriesQuality`, rake `portfolios:correlation_litmus`

## Purpose

Prove the **correlation calculator** is healthy on liquid market pairs, and make **membership quality** (max \|r\|, junk series) transparent **before** corr_v2 builder changes.

This is **not** a scrape of third-party sites. Bands are documented expectations aligned with:

- Portfolio Visualizer asset-class correlation regimes (equity vs gold low; etc.)
- Equinox 2018 notes in `winston_unit_test/planning/equinox_correlation_insights.md`
- Live WUT audit 2026-07-11

## How to run

```bash
# From sawtooth root
./bin/compose exec -T winston_unit_test bin/rails portfolios:correlation_litmus

# Write JSON report
./bin/compose exec -T winston_unit_test env \
  JSON_PATH=/portfolio_configs/correlation-litmus-latest.json \
  bin/rails portfolios:correlation_litmus

# Fail the process if required golden pairs break (CI-style)
./bin/compose exec -T winston_unit_test env STRICT=1 \
  bin/rails portfolios:correlation_litmus
```

Env:

| Env | Meaning |
|-----|---------|
| `JSON_PATH` | Optional path to write full report JSON |
| `STRICT=1` | `abort` when overall report `pass` is false |
| `SKIP_REGISTRY=1` | Skip registry portfolio summaries |
| `EXTRA_SYMBOLS` | Comma symbols added to quality scan |

## Golden pairs (daily Pearson, population std)

| Name | Pair | Band | Role |
|------|------|------|------|
| metals identity | GLTR / GLD | r > 0.80 | Calculator trust |
| cross-asset low | SPY / GLD | \|r\| < 0.35 | Diversifier regime |
| stress sign | SPY / VXX | r ≤ 0 | Sign check |
| equity cluster | AAPL / XLK | 0.35–0.75 | Moderate cluster |
| semi cluster | NVDA / SMH | 0.35–0.80 | Optional |
| twin diagnostic | DBE / OILK full | report only | Non-stationary |
| twin diagnostic | DBE / OILK ≥2022-01-01 | report only | Often r ≫ full sample |

Monthly Pearson is **reported** for PV-style comparison; **assertions use daily**.

### 2026-07-11 live reference (pre-automation)

| Pair | Daily r (approx) |
|------|------------------|
| GLTR / GLD | 0.91 |
| SPY / GLD | 0.13 |
| SPY / VXX | −0.28 |
| AAPL / XLK | 0.49 |
| NVDA / SMH | 0.55 |
| DBE / OILK full | 0.18 |
| DBE / OILK 2022+ | 0.93 |
| COPR / CPER | −0.03 (junk COPR) |

## Quality gates (`MarketSeriesQuality`)

A symbol **fails** if any:

| Gate | Default |
|------|---------|
| Min bars | 1000 |
| Min unique closes | 200 |
| Max zero-return fraction | 30% |
| Min close | > 1e-6 |

**Expected fail:** `COPR` (audit: ~77% zero returns). Unexpected fails on registry members should be fixed or excluded in corr_v2.

## Registry portfolio section

For each `portfolio_configs/registry.json` entry:

- Recompute full correlation matrix (intersection window)
- Report **mean \|r\|**, **max \|r\|**, high pairs (\|r\| > 0.70)
- List quality failures among members

Interpretation (corr_v1 reality):

- Low mean + high max → **twins diluted by junk** (White pattern)
- High pairs → diversification rating should be weak (already true for White)

## Exit criteria (Phase 1)

- [x] One rake command prints golden pairs, quality, registry max\|r\|
- [x] Unit specs for quality + matrix stats
- [x] Analysis doc with bands and run instructions
- [x] Operator run on live compose confirms golden PASS and documents White high pairs / COPR fail (2026-07-11)

### Live run notes (2026-07-11)

- Overall **PASS**; DBE/OILK full ≈ 0.18 vs post-2022 ≈ **0.93** (window clamp fix).
- White: max\|r\| **0.928** DBE/OILK; quality fails CIZ, CMDT, COPR.
- Orange: max\|r\| 0.57; COPR quality fail (no pair > 0.70).
- Red / Blue: no high pairs; max\|r\| 0.48 / 0.44.

## Next (Phase 2)

Hard max-pairwise reject, quality prefilter, fixed window, PCS scorer — see plan.
