# Ticket: Corporate-action stop safeguards (DM / WUT / Wv2 / BG)

**Status:** In progress  
**Priority:** P0  
**Date:** 2026-08-22  
**Monoliths:** data_manager, winston_unit_test, winston_v2, broker_gateway  
**Issue:** [`../issues/2026-08-22-unadjusted-reverse-split-jumps.md`](../issues/2026-08-22-unadjusted-reverse-split-jumps.md)  
**Parent analysis:** [`../analysis/2026-08-22-mint-resting-stop-touch-ruin.md`](../analysis/2026-08-22-mint-resting-stop-touch-ruin.md)

**Authorization:** Lab + parquet hygiene + desk warnings. No Broker Gateway (BG) `order_write`. Do not promote resting-touch.

---

## Why P0

Unadjusted reverse-split jumps × cover-at-open is **capital-unsafe** on any path that treats session **open** as a stop fill (Winston Unit Test (WUT) resting-touch, future live stop-markets). Mint S2 resting PBR 533 went to −100% on USO 1-for-8 and XOP 1-for-4 prints.

## Workstreams

| Owner | Safeguard | Status |
|-------|-----------|--------|
| **data_manager (DM)** | Detect overnight `open/prev_close` ≥ 1.8 or ≤ 1/1.8; back-adjust prior OHLC; recompute ATR/MAs; scale new EODHD bars by `adjusted_close` when present | **Landed** USO/XOP/OIH (backups `*.pre_split_adjust`) |
| **WUT** | Resting v2: tradable gap still covers at open; split-like covers at **working stop**. Fingerprint `corporate_action_stop_guard` | **Landed** |
| **Winston v2 (Wv2)** | Stop-Out Reconciliation `split_like_gap` + `CORPORATE_ACTION_HOLD` — Confirm **refuses** a split-like adverse fill until named override (`tradable_gap` / `broker_print`) + audit notes. Recommends Exit at stop, then Pass Signal. | **Landed** (refuse 2026-09-07) |
| **BG** | When `order_write` exists: hold/refuse stop-market if fill/stop ratio is split-like until human confirm. L1 cannot send. | Deferred (L3) — already this row; live write path is [`2026-08-20-resting-session-stop-orders.md`](2026-08-20-resting-session-stop-orders.md) (Blocked). Do not clone. |

## Must preserve

- Cover-at-open for ordinary gaps (live stop-market).
- ADR-009 next-open default.
- Resting-touch remains opt-in, not pack default.

## Re-score

After parquet back-adjust **and** WUT guard: new Mint S2 pair (`resting_stop_touch_v2`) vs `next_bar_open`. Do not overwrite PBRs 532/533. **Done** — PBR 536 next-open +94% / 58% DD; PBR 537 resting +242% / 56% DD.

```
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/resting_stop_touch_v2_mint_setup.rb
```

## Commands

```
bin/compose exec -T data_manager bin/rails data:scan_split_jumps
bin/compose exec -T data_manager bin/rails data:back_adjust_splits SYMBOLS=USO,XOP,OIH   # dry-run
bin/compose exec -T data_manager bin/rails data:back_adjust_splits SYMBOLS=USO,XOP,OIH APPLY=1
```

## Child tickets (2026-09-07)

- Classify leftover jumps: [`2026-09-07-classify-remaining-split-jump-parquet.md`](2026-09-07-classify-remaining-split-jump-parquet.md)  
- Optional Mint re-score: [`2026-09-07-mint-s2-rescore-after-ung-weat-amcr.md`](2026-09-07-mint-s2-rescore-after-ung-weat-amcr.md)
