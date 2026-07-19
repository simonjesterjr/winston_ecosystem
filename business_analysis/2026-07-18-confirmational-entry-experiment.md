# Confirmational Entry Experiment — Matrix on Winning PBRs

**Date:** 2026-07-18 (results + ADR 2026-07-19)  
**Status:** **Complete** (20/20 cells); decisions captured in **ADR-008**  
**Campaign id:** `confirm_entry_2026_07_18`  
**Monolith:** WUT  
**Doctrine:** Confirm only on **initial entry** (not pyramids). One axis per run (confirm / soft mode). No ladder, exit, or cap changes vs parent.  
**ADR:** `ecosystem/docs/adr/ADR-008-confirmational-entry-and-risk-scale.md`

## Context

Winning / transfer parents used **empty** `confirmational_entry_strategy_ids`. Architecture already AND-gates primary + confirm for entries via `TestingStrategy`; pyramids remain ATR-step risk adds outside that gate.

Soft mode: primary alone still enters at **0.5× risk**; primary+confirm enters at **1.0×**. Pyramids always full ladder risk.

## Parents (baselines — not overwritten)

| PBR | Portfolio | Risk | Caps | Primary | Exit | Ret % | Max DD % | Sharpe | Trades |
|-----|-----------|------|------|---------|------|-------|----------|--------|--------|
| **62** | Blue | one_way_dynamic R1 | max_mkt=4 | Swing5 | Vol | 1415.4 | 41.6 | 1.11 | 1443 |
| **71** | Blue | one_way_dynamic | uncapped | 20d | dual | 589.0 | 60.8 | 0.89 | 705 |
| **72** | Orange | one_way_dynamic | uncapped | 20d | dual | 727.5 | 45.9 | 0.81 | 813 |
| **57** | Mango | static | max_mkt=4 | 5d | Vol | 671.5 | 55.0 | 0.83 | 814 |
| **55** | Green | static | max_mkt=4 | 55d | Vol | 292.4 | 48.3 | 0.95 | 323 |

## Full matrix results

| Cell | PBR | Parent | Confirm | Mode | Ret % | Max DD % | Sharpe | Trades | ΔRet | ΔDD | ΔSh | Verdict |
|------|-----|--------|---------|------|-------|----------|--------|--------|------|-----|------|---------|
| C01 | 78 | 62 | sma20 | hard | **2348.8** | **32.8** | **1.43** | 1467 | +934 | −8.7 | +0.32 | **Best Blue 62** |
| C02 | 79 | 62 | sma55 | hard | 1322.8 | **26.7** | 1.32 | 1239 | −93 | −14.8 | +0.20 | Sharpe+DD win |
| C03 | 80 | 62 | ema20 | hard | **2356.5** | **27.5** | **1.57** | 1382 | +941 | −14.1 | +0.46 | **Best Sharpe overall** |
| C04 | 81 | 62 | penetration | hard | 1285.0 | **21.9** | 1.34 | 810 | −130 | −19.6 | +0.23 | Best DD on 62 |
| C05 | 82 | 62 | bo20 | hard | 748.1 | 27.3 | 1.14 | 956 | −667 | −14.2 | +0.03 | DD/Sharpe ok, ret down |
| C06 | 83 | 62 | bo55 | hard | 296.7 | 43.4 | 0.78 | 637 | −1119 | +1.9 | −0.33 | Fail |
| C07 | 84 | 62 | atr_contract | hard | 1612.8 | 49.2 | 1.25 | 988 | +197 | +7.7 | +0.14 | Ret/Sharpe up, DD worse |
| C08 | 85 | 62 | atr_expand | hard | 1140.3 | 33.3 | 1.31 | 1200 | −275 | −8.3 | +0.20 | Sharpe+DD, ret down |
| C09 | 86 | 62 | sma20 | soft 0.5 | 1569.6 | 47.9 | 1.12 | 1437 | +154 | +6.3 | +0.01 | Soft ≪ hard SMA20 |
| C10 | 87 | 62 | penetration | soft 0.5 | 1264.5 | 43.0 | 1.20 | 1447 | −151 | +1.5 | +0.09 | Soft ≪ hard Pen |
| C11 | 88 | 71 | sma20 | hard | 577.0 | 60.8 | 0.89 | 713 | −12 | 0 | 0 | Flat vs parent |
| C12 | 89 | 71 | penetration | hard | **675.5** | **32.9** | **1.26** | 599 | +87 | −27.9 | +0.37 | **Strong 71 transfer** |
| C13 | 90 | 71 | atr_contract | hard | 549.3 | 39.3 | 1.03 | 461 | −40 | −21.5 | +0.13 | DD/Sharpe win |
| C14 | 91 | 72 | sma20 | hard | 342.7 | 51.1 | 0.80 | 791 | −385 | +5.1 | −0.01 | Fail |
| C15 | 92 | 72 | penetration | hard | **1148.1** | **22.6** | **1.40** | 700 | +421 | −23.3 | +0.59 | **Best Orange transfer** |
| C16 | 93 | 72 | atr_contract | hard | 266.9 | 33.8 | 0.80 | 569 | −461 | −12.1 | −0.01 | Fail |
| C17 | 94 | 57 | sma20 | hard | 655.2 | 62.3 | 0.82 | 776 | −16 | +7.3 | −0.01 | Fail |
| C18 | 95 | 57 | penetration | hard | 487.8 | 48.5 | 0.81 | 569 | −184 | −6.6 | −0.03 | Fail |
| C19 | 96 | 55 | sma20 | hard | 292.4 | 48.3 | 0.95 | 323 | 0 | 0 | 0 | **Identical to parent** (noop) |
| C20 | 97 | 55 | penetration | hard | 181.7 | **27.7** | **1.03** | 149 | −111 | −20.6 | +0.08 | DD/Sharpe, ret down |

## Headline findings

1. **Confirmational entries matter on Blue 62** — unused confirms left substantial edge on the table. Top cells:
   - **C03 EMA20 hard:** Sharpe **1.57**, ret **+2357%**, DD **27.5%** (parent 1.11 / 1415% / 41.6%)
   - **C01 SMA20 hard:** Sharpe **1.43**, ret **+2349%**, DD **32.8%**
   - **C04 Penetration hard:** best DD on 62 (**21.9%**), Sharpe 1.34, lower ret

2. **Soft confirm did not replace hard confirm** on Blue 62. Soft SMA20 (C09) and soft Penetration (C10) underperform their hard twins on return/DD/Sharpe.

3. **Transfer is recipe-dependent, not universal:**
   - **Penetration** transfers well: 71 (C12), 72 (C15), 55 (C20 DD/Sharpe).
   - **SMA20** fails or no-ops outside Blue Swing5 (C14/C17 fail; C19 identical on Green 55d primary).
   - **ATR contraction** mixed: helps 71 DD (C13); hurts 72 ret (C16); on 62 raises ret but worsens DD (C07).

4. **Longer same-family breakout as confirm (BO55) failed** on Swing5 Blue (C06) — over-filtering.

5. **Green 55 + SMA20 is a tautology/noop** (C19 exact parent metrics) — primary is already 55d breakout; SMA20 filter rarely binds differently in aggregate.

6. **Non-price ATR confirms are real signals** (not dead code): expansion improved Sharpe/DD on 62 (C08); contraction is a different tradeoff (more ret, worse DD).

## One-way dynamic on winner PBR 80 — was scale-in overlooked?

**Short answer: No — the R1 ladder is configured and fires. It is easy to miss in the UI.**

| Layer | PBR 80 state |
|-------|----------------|
| Strategy label | `one_way_dynamic` |
| Ladder in `results_json` | long `[2,3,4,6,6]%`, short `[2,2,2,3,3]%` (from parent 62 / TS3 R1) |
| Fills | `position_sizing_risk` on journals: mass at 2%, 3%, 4%, 6% |
| Example (TSLA concurrent adds) | 0.02 → 0.03 → 0.04 → 0.06 with rising units |

**How to read “confirmation” in this stack (ADR-008):**

1. **Confirmational entry (EMA20 on PBR 80)** — filter on *whether to open* the first lot (and soft-size research). **Not** applied to pyramids.  
2. **One-way dynamic pyramid** — *after* entry, each additional concurrent ATR add is trend confirmation in **price path**; risk % **steps up** the ladder so we scale into a sustained move (operator intent: 3 ATR continuation → size for a longer run).

**Why the page can look “flat 2%”:**

- Show only prints “One way dynamic”, **not** the ladder table (issue filed).  
- Journals don’t display `position_sizing_risk`.  
- Most opens are **level 1** (new market or re-entry after flat → ladder resets to 2%). Acceleration only while **multiple lots open** on the same market.  
- Units also move with ATR and capital_base, so risk % up ≠ always obvious unit jump on expensive names.

**Separate bug:** cash/unit *estimate* path in `EntryRequirementCalculator` can clamp risk back to base `risk_percentage` (2%) even when the ladder says 3–6%. Actual `PositionManager` fills still use the ladder. Fix ticket filed.

See: `docs/issues/2026-07-19-one-way-dynamic-pyramid-risk-visibility-and-cap.md`, ADR-008.

## Recommended next steps (science)

| Priority | Action |
|----------|--------|
| 1 | Freeze **Blue 62 + EMA20 confirm (C03 / PBR 80)** and **SMA20 (C01 / PBR 78)** as paper-candidate confirm recipes under max_markets=4 |
| 2 | Re-export / paper-observe C03 vs current Blue 62 OP (include confirm + pyramid_risks in fingerprint) |
| 3 | Prefer **Penetration** as default transfer confirm for non-Blue books (C12/C15 evidence) |
| 4 | Do **not** promote soft 0.5× without more work |
| 5 | Optional: walk-forward on C03 only (anti-overfit) before real capital |
| 6 | UI + estimate-cap fix for one-way ladder (ticket) |
| 7 | File broader strategy tickets (passed-signal P3, R ladders, multi-OP) — still open |

## Code added this campaign

- `AtrContractionConfirmStrategy` / `AtrExpansionConfirmStrategy` (TSS 21/22)
- `TestingStrategy` soft confirm + `risk_size_multiplier` on entry only
- Soft size through `EntryRequirementCalculator` + `PositionManager`
- Lookback fix: `entry_lookback_period` + StrategyLookback periods for confirms
- **FAST_BACKTEST=1** batch path (~10–15× wall-clock): throttle status writes, slim payloads, quiet logs, gate debug file, skip ER unless `COMPUTE_ER=1`
- Script: `winston_unit_test/lib/scripts/confirm_entry_experiment_matrix.rb`

## Run command (reproducible)

```bash
bin/compose exec -e FAST_BACKTEST=1 -e SKIP_BACKTEST_THROTTLE=1 -e STATUS_EVERY_N=50 -e CONCURRENCY=2 \
  winston_unit_test bundle exec rails runner lib/scripts/confirm_entry_experiment_matrix.rb
```
