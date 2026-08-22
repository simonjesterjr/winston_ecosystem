---
id: ISSUE-20260822-unadjusted-reverse-split-jumps
title: Unadjusted reverse-split jumps × cover-at-open blow up stop fills
status: in-progress
type: bug
priority: critical
created: 2026-08-22
updated: 2026-08-22
labels: [data_manager, winston_unit_test, winston_v2, broker_gateway, parquet, capital-safety]
related:
  - docs/analysis/2026-08-22-mint-resting-stop-touch-ruin.md
  - docs/analysis/2026-08-21-resting-stop-touch-v1-scorecard.md
  - docs/tickets/2026-08-20-wut-resting-stop-touch-fill-cadence.md
  - docs/tickets/2026-08-22-corporate-action-stop-safeguards.md
  - interfaces/winston-eod-parquet-standard.md
---

# Unadjusted reverse-split jumps × cover-at-open blow up stop fills

**Status banner (human-readable):** Under investigation / in-progress — WUT split-guard + DM back-adjust + Wv2 CORPORATE_ACTION_HOLD landing this session; BG `order_write` still L3

## Summary

Winston EOD parquet for some energy names still contains **raw reverse-split prints** (USO 1-for-8 on 2020-04-29, XOP 1-for-4 on 2020-03-30, OIH ~1-for-20 on 2020-04-15). A resting stop-market that fills gap-through at the **open** then covers shorts at the post-split print (USO $2.13 → $18.01). That interaction ruined Mint S2 resting PBR 533 (−100% / 101% DD). Next-open survived by filling at the working stop. Live desk / future Broker Gateway (BG) `order_write` can hit the same landmine on the same bars.

## Problem statement

Corporate-action overnight jumps are not tradable gaps. Consumers that treat `open` as a marketable stop fill will pay the post-split print against a pre-split stop. The parquet contract already says adjusted prices where EODHD provides them; these files violate that.

## Current behavior

- DM parquet OHLC jumps 4×–20× across reverse-split sessions; ATR/MAs are computed across the jump.
- WUT `resting_stop_touch` (pre-guard) covers shorts at that raw open.
- Wv2 Stop-Out Reconciliation warns at 1% gap but does not distinguish split-like ratios.
- BG has no `order_write` yet; no hold exists for when it lands.

## Expected behavior

- Parquet history is split-adjusted (continuous OHLC in latest share terms) before ATR/MA bake.
- Resting stop-market still covers **tradable** gaps at open; **split-like** overnight ratios (≥1.8 or ≤1/1.8) cover at the **working stop**, not the raw open.
- Desk / DAR stamps `split_like_gap` / `CORPORATE_ACTION_HOLD` and does not auto-book the post-split print as a stop fill.
- When BG `order_write` exists: do not send a stop-market that would cross a split-like gap without a human confirm.

## Reproduction

### Preconditions

Mint S2 books include USO and XOP. Compose DM parquet as of 2026-08-22.

### Steps

1. `DmParquetLoader.bar_for("USO", Date.new(2020,4,28))` vs `2020-04-29`.
2. Resting PBR 533 vs next-open 532 (already run).

### Observed result

USO close 2.13 → open 18.01. Resting four USO shorts covered at 18.01 ≈ −$6.1k. XOP close 8.03 → open 31.10, three shorts ≈ −$3.1k. Combined ≈ 2020 P&L of −$9.0k. Same-bar exits = 0.

### Reproducibility

Always on these files until back-adjusted.

## Environment

Local compose: `data_manager` :3001, `winston_unit_test` :3000, `winston_v2` :3002, `broker_gateway` :3003. Paper lab. PBRs 532/533.

## Evidence

| Evidence | Source | What it establishes |
|---|---|---|
| Mint ruin diagnosis | `docs/analysis/2026-08-22-mint-resting-stop-touch-ruin.md` | Trigger lots, parquet OHLC, classification |
| Scorecard | `docs/analysis/2026-08-21-resting-stop-touch-v1-scorecard.md` | 533 −100% vs 532 +395% |
| Winston EOD Standard | `interfaces/winston-eod-parquet-standard.md` | “Adjusted prices where the upstream (EODHD) provides them” |
| USCF 1-for-8 USO | public, effective after close 2020-04-28 | Jump is a reverse split |
| State Street 1-for-4 XOP | public, effective 2020-03-30 | Jump is a reverse split |

## Impact and priority

**P0 / critical.** Unadjusted jumps corrupt stop economics in the lab and would be **capital-unsafe** if the same bars drive live or paper stop-markets. Workaround: do not promote resting-touch; do not auto-fill 8× gaps.

## Scope and preservation requirements

### In scope

- Detect and back-adjust split-like jumps in DM parquet; recompute ATR/MAs.
- WUT resting stop-guard: tradable gap still at open; split-like at working stop.
- Wv2 desk/DAR `split_like_gap` / CORPORATE_ACTION_HOLD.
- BG: contract for L3 `order_write` hold (no write path yet).

### Must preserve

- Cover-at-open for **tradable** gaps (live stop-market).
- ADR-009 next-open ops default.
- Resting-touch not pack-promoted.

### Out of scope

- Reverting cover-at-open as a blanket lab change.
- Implementing BG `order_write`.
- Claiming Mint −100% was a same-bar stop bug.

## Acceptance criteria

- [ ] Given USO 2020-04-28 close 2.13 and 2020-04-29 open 18.01, when DM back-adjusts, then prior OHLC is in post-split terms and overnight ratio is no longer split-like.
- [ ] Given a resting short with stop 3.73 and a split-like open 18.01, when WUT checks stops, then cover is at 3.73 not 18.01.
- [ ] Given a tradable gap (open 100 vs prev close 110, stop 102), when WUT checks stops, then cover is still at open 100.
- [ ] Given fill 18.01 vs working stop 3.73, when Wv2 Stop-Out Reconciliation snapshots, then `split_like_gap` is true and warnings include CORPORATE_ACTION_HOLD.
- [ ] Ticket records BG L3 hold requirement; no `order_write` shipped.

## Investigation notes

Confirmed: same-bar exits 0; Dec 2019 cash-negative on **both** arms with $10k equity; ruin is USO+XOP reverse-split covers at open. See analysis.

## Unknowns and clarifying questions

- [ ] Full-universe jump scan after detector lands (other symbols besides USO/XOP/OIH).
- [ ] Whether a fresh EODHD full-history pull is already split-adjusted (client will now scale by `adjusted_close` when present).

## Dependencies and risks

Back-adjusting parquet changes ATR and every future backtest on those symbols. Backup `bars.parquet.pre_split_adjust`. Re-score Mint only after adjust + guard.

## Verification plan

- `bundle exec rspec` focused: CorporateActionJump, resting stop-touch guard, StopOutReconciliation.
- `bin/compose exec -T data_manager bin/rails data:scan_split_jumps`
- `SYMBOLS=USO,XOP,OIH APPLY=1 bin/rails data:back_adjust_splits`
- Mint S2 resting vs next-open re-score (`resting_stop_touch_v2`) after data+guard.

## History

- 2026-08-22 — Created from Mint S2 resting PBR 533 diagnosis.
- 2026-08-22 — WUT split-guard + DM back-adjust USO/XOP/OIH + Wv2 CORPORATE_ACTION_HOLD landed. Additional suspects not auto-applied: UNG 2024-01-24 (~4×), WEAT 2025-11-25 (~5×), AMCR 2026-01-15 (~5×). APLD penny series has many 2× flips — do not blind-adjust. Mint re-score PBRs 536/537 pending.
