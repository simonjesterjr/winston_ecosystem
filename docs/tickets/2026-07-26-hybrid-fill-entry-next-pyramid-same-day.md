# Ticket: Hybrid fill cadence — next-bar entry, same-day pyramid

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-07-26  
**Monoliths:** winston_unit_test (lab first); winston_v2 / desk later (broker API)  
**Related:** ADR `2026-07-25-lab-t1-fill-queue.md`; ADR-009 ops signal/fill; bakeoff `2026-07-25-strategy-bakeoff-v1-phase1`; operator goal: higher Compound Annual Growth Rate (CAGR) with controlled risk  

---

## Problem

Lab Portfolio Backtest Run (PBR) fill cadence is **global** today:

| Mode | Initial entry | Pyramid add |
|------|---------------|-------------|
| `next_bar_open` | Signal day T → fill open T+1 | Same (queue both as tickets) |
| `same_bar_open` | Fill same bar (legacy science) | Same |

Operator doctrine under test:

> **Initial entries:** `next_bar_open` (ops-honest, no same-bar lookahead on new risk).  
> **Pyramids:** **same-day fill** after the book is already live (scale-in can be faster when trend confirms).

That split is not only a lab experiment. It matches a **live brokerage automation** path:

1. New name: human/API can wait for next session open (or explicit confirm).  
2. Add-on to an open position: same-day marketable order once the pyramid rule fires is often desirable and operationally different.

If same-day pyramids **materially lift CAGR / Sharpe** on winners (or fix Elephant survivability blowups), that **prioritizes** broker API work for partial automation of scale-ins. If not, keep T+1 for everything and de-prioritize same-day pyramid plumbing.

---

## Current code (gap)

Winston Unit Test (WUT) `PortfolioBacktestRunner`:

- `next_bar_open_fill?` is a single flag (`LabFillCadence`).
- `process_entries` and `process_pyramids` both branch on that flag → either `enqueue_entry` or immediate `execute_entry`.
- T+1 ticket queue treats entry and pyramid kinds similarly at adjudication (open T+1).

**No** `entry_fill_cadence` / `pyramid_fill_cadence` split yet.

---

## Product rules to implement (lab)

### A. Initial entry (flat → first lot)

- Cadence: **`next_bar_open`** only (for this experiment).  
- Queue ticket on signal T; adjudicate open T+1; rank/reserve/expire as existing T+1 queue.  
- Stops/exits unchanged (stops already same-session once live).

### B. Pyramid (live position → add)

- Cadence: **`same_day_fill`** for this experiment.  
- **Integrity (decide and lock before coding):**

| Option | When pyramid rule uses close of day T | Lab fill | Ops analogy | Integrity |
|--------|----------------------------------------|----------|-------------|-----------|
| **B1 Close-fill (recommended lab default)** | Trigger known at EOD T | Fill at **close T** (or last price T) | EOD desk “add before bell” / MOC | No open-lookahead |
| **B2 Open-fill same bar** | Trigger from close T | Fill at **open T** | Impossible without foresight | **Reject** for science |
| **B3 Intraday (future)** | Rule fires on partial bar | Fill mid-session | Live API | Needs intraday data — out of scope |

**Lab v1 recommendation:** implement **B1** labeled `same_day_close` (or document that “same_day_fill” for EOD bars = fill on signal bar at **close** after rule evaluated on that bar).  
If product wants “same day as decision but next print,” that is still T+1 open — not this experiment.

### C. Config surface

Seed on PBR `results_json` (and optional ENV later):

```json
{
  "fill_cadence": "hybrid_entry_next_pyramid_same_day",
  "entry_fill_cadence": "next_bar_open",
  "pyramid_fill_cadence": "same_day_close"
}
```

Backward compatible: bare `fill_cadence: next_bar_open | same_bar_open` unchanged.

### D. Interaction notes

- Pyramid only if **live** position exists (already true).  
- After T+1 **initial** fill on morning T+1, pyramid signals generated later that **same calendar day** may same-day fill (B1 on that day’s close) — path differs from pure T+1 where pyramid waits until T+2 open.  
- Cash/slots: same-day pyramid must still respect portfolio limits; order vs pending entry tickets = define (suggest: adjudicate morning entries first, then EOD pyramids after signals).  
- Passed signals: tag pyramid skips with existing reasons; add `pyramid_same_day` in logs for audit.

---

## Lab step design (after code ships)

**Experiment key:** `hybrid_fill_pyr_same_day_v1`  
**Parent:** strategy bakeoff + Phase 2 S4 freezes where relevant.

### Chassis (freeze unless noted)

| Knob | Value |
|------|--------|
| Entry fill | `next_bar_open` |
| Pyramid fill | `same_day_close` (B1) |
| Risk | One-Way Dynamic (OWD) ladder A / 2% base (Phase 1) **or** dual arm at Elephant 1% — see arms |
| Pyramid Average True Range (ATR) mult | **1.0** (Phase 2 step 1 freeze) |
| Max per symbol | **5** until step 2 score freezes another value |
| Capital | $10,000 |

### Arms

| Arm | Trading Strategy (TS) | Risk pack | Why |
|-----|----------------------|-----------|-----|
| **W** | S4 FastBO5 (#48) | ladder A / 2% | Clear winners — CAGR / Sharpe uplift? |
| **E** | S1 Elephant (#45) | ladder A / 2% | Survivability kill zone under pure next_open |
| **E1** optional | S1 Elephant | ~1% unit (flat) | Does same-day pyramid + calm risk stack? |

### Portfolios

| Tier | Books | Role |
|------|-------|------|
| **Survivability (Elephant pain)** | Orange, Rust, Blue | Where S1@2% next_open blew up or lagged |
| **Winners (S4)** | Blue, Mango, Mint | Strong next_open S4 — material CAGR/Sharpe change? |
| **Optional** | Green | Weak S4 control (expect still hard) |

### Suggested cell count (v1, no E1)

| | Orange | Rust | Blue | Mango | Mint |
|--|--------|------|------|-------|------|
| S4 hybrid | — | — | ✓ | ✓ | ✓ |
| S1 hybrid @2% | ✓ | ✓ | ✓ | — | — |

= **3 + 3 = 6** hybrid PBRs, each scored vs **existing pure `next_bar_open` baseline** same TS/portfolio (bakeoff or Phase 2).

Optional +S4 Orange, +S1 Mango, +E1 on Orange/Blue → keep ≤ **12** cells.

### Baselines (do not re-run if completed)

| Compare hybrid to | Source |
|-------------------|--------|
| S4 pure next_open | Bakeoff S4: Blue 201, Mango 221, Mint 246 |
| S1 pure next_open @2% | Bakeoff S1: Orange 203, Rust 223, Blue 198 |
| S1 @1% | elephant_risk panel Orange/Blue if needed |

### Metrics (operator goal: exceptional vs calm)

Per cell and median by arm:

1. Total return and **CAGR** (window from overlap range)  
2. Maximum drawdown  
3. Practical Sharpe  
4. Calmar (total return / max DD)  
5. Trade count, pyramid count (adds), passed pyramid reasons  
6. Qualitative: did Orange/Rust S1 stop full wipeout?

**Promotion signal for broker API priority:**

- Hybrid improves **S4 winner CAGR or Sharpe** without large DD regression on Blue/Mango/Mint, **or**  
- Hybrid restores **S1 survivability** on Orange/Rust with acceptable DD  

Either result → prioritize same-day scale-in automation.  
Neither → keep T+1 pyramids; broker work focuses on entry confirm only.

---

## Implementation tasks (WUT)

1. Extend `LabFillCadence` (or sibling) for hybrid mode + pyramid-specific cadence.  
2. `process_pyramids`: if pyramid same-day → `execute_entry` with fill price = close (B1); else enqueue.  
3. `process_entries` / initial only: always enqueue under hybrid.  
4. Specs: unit for cadence resolver; integration smoke one market entry T+1 + pyramid same close.  
5. Setup/scorecard scripts mirroring bakeoff (`hybrid_fill_pyr_same_day_v1_*`).  
6. Short note in ADR or follow-on ADR: hybrid fill doctrine (lab + ops intent).

**Out of scope for lab v1:** intraday bars, broker API itself, partial fills, slippage model beyond open/close.

---

## Acceptance

- [ ] Hybrid cadence implemented and tested  
- [ ] ≥6 hybrid PBRs completed vs baselines  
- [ ] Written call: prioritize same-day pyramid automation **yes/no** with CAGR/Sharpe/DD table  
- [ ] Ticket updated; optional ADR accepted if doctrine freezes  

---

## Operator note

Cannot run this lab step on current main until the hybrid branch exists — setting up “pending PBRs” with only `fill_cadence: next_bar_open` would **not** exercise same-day pyramids (they would stay T+1).
