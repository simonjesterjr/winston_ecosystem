# Close-Trigger Signal Strength + one_way_dynamic_close

**Date:** 2026-07-24  
**Status:** Complete (Axes A/B/C)  
**Campaign:** `close_trigger_2026_07_24`  
**Monolith:** WUT lab  
**Ticket:** `ecosystem/docs/tickets/2026-07-24-close-trigger-signal-strength-one-way-dynamic.md`  
**Related:** ADR-008 (confirm vs pyramid risk), ADR-009 (ops signal T / fill T+1 open)

---

## Executive snapshot

| Question | Answer |
|----------|--------|
| Is close a stronger breakout trigger than high/low (H1)? | **Conditional yes** — wins on Blue C0 (62) and Orange (72); hurts when stacked on hard confirm (80/78) or uncapped Blue 48 |
| Should one-way dynamic size by strength (H2)? | **Conditional** — neutral on bare 62; big return lift with confirm (80→CT08) at DD cost; Orange quality win (DD/Sharpe) |
| Does lab honor signal X → fill X+1 open (H3)? | **No** — 100% of sampled entries fill at **same-day open** of the signal bar (`PositionManager#market_price` → `activity.open`). Ops ADR-009 uses T+1 open. |
| Promote close-breakout as default? | **Yes for capped Swing5/BO20 science**, not as a free stack on confirm or uncapped recipes |
| Promote `one_way_dynamic_close` to ops? | **Not yet** — interesting on CT08; needs T+1 cadence honesty first, then walk-forward |

---

## Hypotheses

| Id | Claim | Verdict |
|----|--------|---------|
| **H1** | Close-confirmed breakouts improve risk-adjusted economics vs high/low | **Partial accept** |
| **H2** | Strength-aware ladder (weak base/step, aggressive pos+1) improves vs flat R1 | **Partial accept** (recipe-dependent) |
| **H3** | Lab fills at next session open after signal day | **Reject (lab path)** — same-day open |

---

## Axis A — Close entry (H1)

**Change only:** primary → close-breakout (`SwingBreakout5DayClose` / `Breakout20DayClose`). Risk stayed parent `one_way_dynamic` + ladder. Stop: `move_to_last_entry`.

| Cell | PBR | Parent | Child ret/DD/Sh/tr | Parent ret/DD/Sh/tr | ΔRet | ΔDD | ΔSh |
|------|-----|--------|--------------------|---------------------|------|-----|------|
| CT01 | 142 | 62 Blue C0 Swing5 | **1715 / 25.9 / 1.60 / 1321** | 1415 / 41.6 / 1.11 / 1443 | **+300** | **−15.7** | **+0.49** |
| CT02 | 143 | 80 + EMA20 | 1756 / **17.0** / 1.66 / 1236 | 2357 / 27.5 / 1.57 / 1382 | −600 | **−10.5** | +0.09 |
| CT03 | 144 | 78 + SMA20 | 1575 / 27.2 / 1.43 / 1281 | 2349 / 32.8 / 1.43 / 1467 | −774 | −5.6 | 0 |
| CT04 | 145 | 72 Orange BO20 | **834 / 28.3 / 1.42 / 847** | 728 / 45.9 / 0.81 / 813 | **+106** | **−17.6** | **+0.61** |
| CT05 | 146 | 48 Blue uncapped | 927 / 23.9 / 1.41 / 875 | 2074 / 20.9 / 1.52 / 767 | −1147 | +3.0 | −0.11 |

### H1 reading

1. **C0 Swing5 without confirm (CT01):** strongest positive — higher return, much better DD/Sharpe, fewer trades.  
2. **Hard confirm + close primary (CT02/CT03):** over-filters return; DD still improves (CT02 best DD in A matrix). Do not stack blindly.  
3. **Orange transfer (CT04):** close BO20 wins quality and return.  
4. **Uncapped 48 (CT05):** close loses badly — capacity/recipe dependent.

**Risk on Axis A children:** verified `one_way_dynamic` with parent ladders (R1 or Orange shallower). Journal risk hist showed 2/3/4/6% mass. UI blank ladder is display-only (known issue).

---

## Axis B — one_way_dynamic_close (H2)

**Change only:** risk → `one_way_dynamic_close`; **keep high/low primary**. Strength:

| Strength | Definition | Ladder index |
|----------|------------|--------------|
| weak | high/low pierces; close does not clear | W-base: flat 2%; W-step: `max(1, pos−1)` |
| standard | indeterminate / at level | `pos` |
| aggressive | **any close beyond level** | `min(len, pos+1)` |

| Cell | PBR | Parent / policy | Child ret/DD/Sh/tr | Parent ret/DD/Sh/tr | ΔRet | ΔDD | ΔSh |
|------|-----|-----------------|--------------------|---------------------|------|-----|------|
| CT06 | 147 | 62 W-base | 1383 / 41.7 / 1.11 / 1349 | 1415 / 41.6 / 1.11 / 1443 | −32 | +0.1 | 0 |
| CT07 | 148 | 62 W-step | 1383 / 41.7 / 1.11 / 1349 | same | −32 | +0.1 | 0 |
| CT08 | 149 | 80 W-step | **3398 / 31.8 / 1.66 / 1411** | 2357 / 27.5 / 1.57 / 1382 | **+1041** | +4.3 | +0.09 |
| CT09 | 150 | 72 W-step | 633 / **31.2** / **1.11** / 853 | 728 / 45.9 / 0.81 / 813 | −95 | **−14.7** | **+0.30** |

**CT06 ≡ CT07** (identical metrics + risk histograms). Weak path does not separate on this book — early-level floor and/or close-required pyramids dominate.

Risk histograms confirm non-flat ladders (e.g. 147: ~661@2%, 462@3%, 120@4%, 106@6%).

### H2 reading

1. Strength risk alone on bare Blue 62 ≈ flat.  
2. **Confirm + strength risk (CT08)** is the headline return cell; accepts higher DD.  
3. Orange strength risk improves **quality** (DD/Sharpe), not max return.  
4. Do not promote `one_way_dynamic_close` to Wv2 until cadence (H3) is honest and CT08 is walk-forwarded.

---

## Axis C — Fill cadence (H3)

**Operator requirement:** signal day **X** → action day **X+1** at **open**.

### Method

For entry journals (non-null `position_action_initiation`), compare `position.execution_price` to:

- same-bar open (`bar_date` open)  
- next-session open after `bar_date`  

Sampled **50 entries each** on parents 62/80 and children 142/147/149/150.

### Results

| PBR | bar_date == trade_date | Match same-day open | Match next-day open |
|-----|------------------------|---------------------|---------------------|
| 62, 80, 142, 147, 149 | 50/50 | **100%** | **0%** |
| 150 | 50/50 | **100%** | ~2% (price ties) |

**Code:** `PositionManager#market_price` → `activity.open` on the **same activity** used for signal evaluation (high/low/close of that bar).

**Exits:** evaluated and priced on the signal bar (`activity.close` or stop), not next open.

### H3 verdict

| Layer | Cadence |
|-------|---------|
| **WUT lab PBR (current)** | Signal on day X using X’s range/close; **fill at X open** (same bar) |
| **Ops / ADR-009** | Signal date T; **fill date T+1** next session open |

This is a **methodology gap**, not a bug unique to this campaign — parents and children share it. Economic comparisons within the lab remain **internally consistent**, but they are **not** ops-identical and have same-bar information for entries (signal uses close/high; fill uses that day’s open).

**Follow-on (filed):** lab T+1 open fill path for entry/exit parity with ADR-009.

---

## Business rules (from this campaign)

1. **Close-breakout as lab axis is real.** Prefer close primaries for **capped** Swing5/BO20 exploration when DD/Sharpe matter (CT01, CT04).  
2. **Do not stack close primary on hard confirm by default** (CT02/CT03 return damage). Prefer either close primary **or** high/low + confirm, not both, until retested.  
3. **Uncapped Blue 48 is not the place to force close** (CT05).  
4. **`one_way_dynamic_close` is research-only.** CT08 is the promotion candidate *cell*, not a general rule. W-base vs W-step indistinguishable on 62 — default **step_back** for further research only if needed for theory; otherwise either is fine on this book.  
5. **Always `move_to_last_entry`** for one-way dynamic experiments (enforced on all CT children).  
6. **Do not claim ops parity** for PBR economics until Axis C gap is fixed (same-day open ≠ T+1 open).  
7. **Ladder must live in `results_json.risk_evaluation_config.pyramid_risks`** — UI may still hide it; verify via config or journal risk hist.

---

## Code delivered (WUT)

| Piece | Location |
|-------|----------|
| Swing5 / BO20 close strategies | `app/strategies/entry_exit/*_close_strategy.rb` |
| Strength classifier | `app/strategies/risk/signal_strength_classifier.rb` |
| `OneWayDynamicCloseRiskEvaluation` | `app/strategies/risk/one_way_dynamic_close_risk_evaluation.rb` |
| Wiring | `PositionManager`, `PortfolioBacktestRunner`, `EntryRequirementCalculator` |
| Matrix script | `lib/scripts/close_trigger_experiment_matrix.rb` (`AXIS=A\|B`) |
| Specs | close breakout + close risk (23 examples green) |

---

## PBR ID map

| Cell | PBR | Axis | Parent |
|------|-----|------|--------|
| CT01–05 | 142–146 | A close entry | 62,80,78,72,48 |
| CT06–09 | 147–150 | B strength risk | 62,62,80,72 |

---

## Follow-ons

| Priority | Item |
|----------|------|
| P1 | **Lab fill cadence:** signal day X → fill X+1 open (entries + exits) for ADR-009 parity |
| P2 | Walk-forward CT08 (80 + strength risk) before any paper recipe change |
| P3 | Optional: weak-path diagnostics (why CT06≡CT07); pyramid strength when adds are close-only |
| P3 | PBR show ladder UI (existing issue) |

---

## Acceptance

- [x] Parent freeze + campaign tags  
- [x] Axis A 5 cells  
- [x] Axis B 4 cells  
- [x] Axis C audit (fail vs ops doctrine; evidence logged)  
- [x] Business rules written  
- [x] Follow-on ticket for lab T+1 fills  


---

## Lab fill cadence fixed (same day, 2026-07-24)

**Default lab mode is now `next_bar_open`:** Signal(T) → queue → fill at next session **open** (position/journal fill date = T+1; `TradingSignal.bar_date` = T).

- Code: `LabFillCadence`, pending fills in `PortfolioBacktestRunner`, `fill_activity` on `PositionManager`
- Bugfix: removed `TradingSignal` `attr_accessor :bar_date/:market_id` that blocked signal-date persistence
- Legacy: `LAB_FILL_CADENCE=same_bar_open` for pre-fix comparisons
- Smoke: PBR **153** (short window from 62) — 43/43 fills with fill_date > signal_date
- **PBRs 142–150 (close-trigger campaign) were run under old same-day open** — metrics not re-run under T+1

Ticket: `docs/tickets/archive/2026-07-24-lab-pbr-signal-x-fill-x1-open.md`
