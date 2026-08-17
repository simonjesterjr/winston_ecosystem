# Ticket: Wv2 equity WUT-parity — short flow + DAR + shell

**Status:** Done  
**Priority:** P1  
**Date:** 2026-08-17  
**Monolith:** winston_v2  
**Issue:** [`../issues/2026-08-17-wv2-short-flow-breaks-wut-equity.md`](../issues/2026-08-17-wv2-short-flow-breaks-wut-equity.md)  
**Supersedes investigation:** [`2026-08-13-investigate-negative-risk-equity-active-ops.md`](2026-08-13-investigate-negative-risk-equity-active-ops.md)

## Problem

Wv2 risk equity uses the WUT PBR identity but short stock/proxy journal flows are long-signed. Shell and DAR then present the collapsed number and call free cash `capital`.

## Workstreams

### A — D1 cash identity (root)

- [x] `RelatedInstrumentFulfillment.signed_flow` takes `direction`
- [x] Stock/proxy short enter +, exit −; long unchanged; option-like always purchase-signed
- [x] All callers pass direction (confirm, draft edit, amend, ad-hoc enter/exit)
- [x] Idempotent backfill rake for existing short stock/proxy journals
- [x] Specs green

### B — D3 recon + D2 DAR totals

- [x] Cash-identity equity vs position-PnL equity recon on series/snapshot
- [x] Disagree flag when `|delta|` exceeds epsilon — including negative risk equity
- [x] DAR summary: **Total risk equity** (not summed free cash as Total capital)
- [x] Status table: keep Free cash + Risk equity; End equity only as series endpoint (not a third duplicate wealth column, or clearly labeled)
- [x] Markdown + PDF + payload specs

### C — D2 ops shell

- [x] `list` / `status` / `positions` print free cash + risk equity (stop `capital=$` free cash)
- [x] `InternalPortfolioStatus` exposes dual metrics
- [x] Specs green

## Verification (2026-08-17)

Backfill applied on `winston_v2_dev`: scanned 122, updated 30, skipped 92. Active snapshots as-of 2026-08-16:

| OP | Free cash | Risk equity | Δ cash vs PnL |
|----|----------:|------------:|--------------:|
| Rust #11 | −2,615 | 9,795 | 0 |
| Orange #308 | 10,712 | 9,484 | 0 |
| Blue #381 | 13,287 | 9,168 | 0 |
| Mint #384 | 22,040 | 9,508 | 0 |
| Mango #385 | −1,969 | 9,850 | 0 |
| Mint Turtle #797 | 8,206 | 10,001 | 0 |
| Yellow Turtle #798 | 9,385 | 9,997 | 0 |

DAR `storage/reports/wv2_20260816.md` regenerated (no Telegram send). Combined specs 73 examples, 0 failures.

## Acceptance

See issue acceptance criteria. Live smoke: after backfill, Mint #384 / Orange #308 / Blue #381 risk equity in the ~$9k band, not negative thousands.

## Non-goals

- Telegram redelivery
- Changing `OVER_DEPLOYED_RATIO`
- WUT PBR code
