# Resting stop-touch vs next-open — Turtle Mint S2 / Yellow S1

**Experiment:** `resting_stop_touch_v1`  
**Ticket:** `2026-08-20-wut-resting-stop-touch-fill-cadence`  
**Scored:** 2026-08-21  
**Chassis:** Turtle Systems V1 — static 1%, 0.5N pyramid, max 4/12, ATR×2, `move_to_last_entry`, no VolatilityExit, $10k  
**Window:** same overlap as parent PBRs 432 (Mint S2) and 433 (Yellow S1)

## Call (freeze)

| Decision | Value |
|----------|--------|
| Promote `resting_stop_touch` as pack / Turtle paper default? | **No** |
| Change ADR-009 ops next-open? | **No** |
| Keep the lab switch? | **Yes** (opt-in; geometry specs stay) |
| Automate live resting buy-stops from this panel? | **No** — parent BG ticket stays blocked |

**v1 median (contaminated Mint):** Δret **−205**, Δdd **+33**.  
**v2 Mint only (adjusted parquet + stop guard, 536 vs 537):** Δret **+148**, Δdd **−2**. Resting survived and beat next-open on this book. Still **no pack promotion** — one exclusive book, Yellow DD still worse, ADR-009 unchanged.

## Doctrine tested

| Arm | Entry | Pyramid |
|-----|-------|---------|
| `next_bar_open` (532, 534) | T+1 open queue | T+1 open queue |
| `resting_stop_touch` (533, 535) | Donchian level on signal bar | existing `price_level_touch` |

## Results

| Book | Resting PBR | Next-open PBR | Resting ret / DD / CAGR / trades / pyr | Next-open ret / DD / CAGR / trades / pyr | Δret | Δdd | Δpyr |
|------|-------------|---------------|----------------------------------------|------------------------------------------|------|-----|------|
| Mint S2 (TS#77) | **533** | **532** | **−100.2 / 100.6 / ruin / 97 / 0** | **+394.7 / 44.4 / +26.5 / 747 / 6** | **−495** | **+56** | −6 |
| Yellow S1 (TS#75) | **535** | **534** | +205.5 / 39.8 / +16.9 / 1174 / 1 | +120.6 / 29.7 / +11.7 / 1267 / 5 | **+85** | +10 | −4 |

Parent hybrid-price Mint S2 **432** was +537 / 54 DD / 767 trades — a third path, not this comparison.

## Reading

**Mint S2 resting ruined the book in H1 2020 — but not for the reasons we first named.** Full diagnosis: [`2026-08-22-mint-resting-stop-touch-ruin.md`](2026-08-22-mint-resting-stop-touch-ruin.md).

| Hypothesis | Verdict |
|------------|---------|
| Same-bar gap-through **entry** then same-bar protective stop | **Falsified.** 0 same-bar exits on 533 and 532. |
| Short-margin cash accounting as the unique ruin | **Falsified as unique.** Both arms cash-negative on 2019-12-31 with ~$10k equity still intact (VNQ short cover). Terminal −$23 is leftover after equity hit zero. |
| Unadjusted reverse-split jumps × cover-at-open | **Confirmed.** USO 1-for-8 (2020-04-29 open $18.01 vs prior close $2.13) and XOP 1-for-4 (2020-03-30 open $31.10 vs $8.03). Resting covered at the **open**; next-open covered at the **stop**. Those lots ≈ **−$9.2k** vs 2020 P&L **−$9.0k**. |

**Yellow S1 resting made more money** (+85 ret, +5 Compound Annual Growth Rate) with **+10 drawdown** and still ended with **negative free cash** (−$971) while mark-to-market equity was ~$30k. Yellow’s books have no USO/XOP/OIH, so it is the only trustworthy cadence pair on this panel. Pyramids almost vanished (1 vs 5). One exclusive book with worse DD is not a promotion case.

Split panel → **no pack change**. Do not treat Mint’s −100% as “Turtle is broken” or as a fair resting-vs-next-open score until parquet reverse-splits are adjusted.

## v2 Mint re-score (2026-08-22)

After USO/XOP/OIH reverse-split back-adjust and the corporate-action stop guard. **Fair pair is 536 vs 537** (same adjusted bars). Do not compare 537 to 532 — v1 next-open rode unadjusted energy prints.

| Arm | PBR | Ret | DD | CAGR | Trades | Terminal equity | 2021-06 equity |
|-----|-----|-----|----|------|--------|-----------------|----------------|
| Next-open | **536** | +93.8 | 58.0 | +10.2 | 691 | $19.4k | $18.6k |
| Resting | **537** | **+241.8** | 56.0 | **+19.8** | 795 | $34.2k | $39.9k |
| Δ (resting − next) | | **+148** | **−2** | **+9.6** | +104 | | |

v1 restated for honesty:

| Arm | PBR | Ret / DD | Note |
|-----|-----|----------|------|
| Next-open unadjusted | 532 | +395 / 44 | Contaminated: stop-at-level through 8× USO/XOP jumps |
| Resting unadjusted | 533 | −100 / 101 | Ruin: cover-at-open through those jumps |
| Next-open adjusted | 536 | +94 / 58 | Honest next-open on stitched energy |
| Resting adjusted | 537 | +242 / 56 | Guard did **not** fire (jumps already stitched); data fix was load-bearing |

Resting never went below $5k. 2020-06 equity $16.5k vs v1 resting $3.2k. USO Apr 2020 on 537 is one short at fill **40.64** (post-split terms) that exited 27.5 — not four shorts covered at $18 against a $3 stop.

## Reading (updated)

The v1 “resting is path-destructive” freeze **on Mint** was a **data artifact**, not Turtle geometry. On stitched bars, Mint S2 resting **beats** next-open on return and is a hair better on drawdown. Yellow S1 (no USO/XOP/OIH, already fair) still shows resting **+85 ret / +10 DD**.

Together: exclusive-book resting-touch looks **economically interesting**, not ruined. That is **not** enough to stamp S4 or Turtle paper Operational Portfolios (OPs), or to change ADR-009. It **is** enough to stop treating 533 as evidence that Donchian stop-entry cannot work.

## Next

- Do **not** stamp live Mint/Yellow Turtle OPs to resting-touch yet.
- Parent `2026-08-20-resting-session-stop-orders` stays Blocked on Broker Gateway (BG) L3.
- Remaining parquet suspects (not auto-applied): UNG 2024-01-24, WEAT 2025-11-25, AMCR 2026-01-15. APLD penny 2× flips — leave alone.
- Optional: Yellow S1 re-run is unnecessary for the split story (those books had no jumps).
