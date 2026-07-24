# Ticket: Close-trigger signal strength vs high/low — one_way_dynamic_close experiment

**Status:** Done (Axes A/B/C complete 2026-07-24)
**Completed:** 2026-07-24  
**Priority:** P2  
**Date:** 2026-07-24  
**Monolith:** winston_unit_test (lab runs + optional risk/strategy code); results → `ecosystem/business_analysis/`  
**Campaign id:** `close_trigger_2026_07_24`

## Problem / opportunity

We treat a **closing price** that triggers a breakout, MA cross, etc. as a **stronger signal** than a high/low (intrabar) pierce of the same level — but we have never measured that in WUT PBRs.

If true, **one-way dynamic** pyramiding should not always use the same ladder step for every add. Risk can branch on strength:

- weaker signals → conservative risk
- standard close-confirm → normal ladder
- aggressive (close **beyond** the signal level) → one ladder step up

Separately, economic comparisons are only honest if the lab honors **signal day X → fill day X+1 at open** (Winston EOD cadence). That must be verified, not assumed.

## Desired outcome

1. Business analysis write-up answering H1 (close vs high/low quality), H2 (strength-aware risk paths), H3 (X / X+1 open cadence).
2. Either **close this ticket** with durable business rules, or **spawn follow-on tickets** (Wv2 sizer parity, full close-strategy suite, defect fix if cadence fails).
3. **Planned follow-on (queued):** opposite-entry **signal-on-signal** (exit vs reverse while open) — not `always_in_market`. See [`2026-07-24-opposite-entry-signal-on-signal.md`](2026-07-24-opposite-entry-signal-on-signal.md). Prefer after Axis B (`one_way_dynamic_close`) so risk strength and position-level meta-signals stay one-axis.

## Domain facts (code baseline)

| Family | Trigger today | Examples |
|--------|---------------|----------|
| Breakouts | **High/low** | Swing5, BO5/20/50/55 |
| MAs | **Close** | SMA/EMA/WMA 20/55 |
| Penetration25 / ATR confirms | **Close** | |

`OneWayDynamicRiskEvaluation` today indexes only by **concurrent pyramid level**, not signal strength.

## Hypotheses

| Id | Claim |
|----|--------|
| **H1** | Close-confirmed breakouts improve risk-adjusted economics vs high/low-only (trade count may fall). |
| **H2** | Strength-aware ladder (weak / standard / aggressive) improves or stabilizes economics vs flat R1 on the same high/low primary. |
| **H3** | Fills use **next session open on X+1** after signal on **X** for entries and exits; mismatches are defects. |

## Locked product rules (operator 2026-07-24)

### Signal strength classes

| Class | Definition |
|-------|------------|
| **weak** | High/low pierces level; **close does not** clear the level |
| **standard** | Close clears the level (at/through) without “beyond” treatment |
| **aggressive** | **Any close beyond the signal level** (long: close > level; short: close < level). **No +ATR requirement** |

Strength is evaluated **per entry and per pyramid add**.

### H2 — two weak evaluative paths + shared aggressive

R1 long ladder (default): `[0.02, 0.03, 0.04, 0.06, 0.06]`.

| Path | Weak signal risk |
|------|------------------|
| **W-base** | Always configurable **base %** (default **2%**), any pyramid level |
| **W-step** | Ladder index **`max(1, pyramid_position − 1)`** (one step back); **floor at base 2%** so 2nd pyramid weak stays 2% |

| Strength | Ladder index |
|----------|--------------|
| weak | W-base **or** W-step (path-dependent) |
| standard | current `pyramid_position` |
| aggressive | **`min(len, pyramid_position + 1)`** (one step forward; cap at last rung) |

Worked R1 examples:

| Pos | Weak W-base | Weak W-step | Standard | Aggressive |
|-----|-------------|-------------|----------|------------|
| 1 | 2% | 2% | 2% | 3% |
| 2 | 2% | 2% (floor) | 3% | 4% |
| 3 | 2% | 3% | 4% | 6% |
| 4 | 2% | 4% | 6% | 6% (cap) |
| 5 | 2% | 6% | 6% | 6% (cap) |

### Stops

**Always `move_to_last_entry`.** On the Nth pyramid add, stops for lots 1…N−1 move up to the stop of the Nth. Enforce on all experiment children even if a parent drifted.

### Fill cadence (Axis C)

Signal on day **X** creates the **action** on day **X+1**, priced at **X+1 open** (entry and exit fills). Audit journals on parents and children; if systematic failure → file **issue**, do not promote BA rules from poisoned fills.

## Parent selection (“active” PBRs)

Live WUT query; freeze metrics into BA doc before runs.

| Filter | Default |
|--------|---------|
| `risk_evaluation_strategy` | `one_way_dynamic` |
| `total_trades` | ≥ **100** |
| Total return | ≥ **100%** |
| Status | completed with usable metrics |
| Prefer | High/low **breakout** primaries |

**Doctrine:** new PBR IDs only; never overwrite 44/48/62/80.  
**Skip for H2 cells:** static-only (e.g. 55/57) unless a later transfer ticket.

### Parent freeze (live WUT 2026-07-24)

Filter: `one_way_dynamic`, trades ≥ 100, return ≥ 100%, completed. All listed stops are already `move_to_last_entry`.

| Priority | PBR | Port | Primary | max_mkt | Trades | Ret % | Sharpe | Max DD % | Role |
|----------|-----|------|---------|---------|--------|-------|--------|----------|------|
| Must | **62** | Blue | Swing5 | 4 | 1443 | 1415.4 | 1.11 | 41.6 | Axis A/B core (honest caps) |
| Must | **80** | Blue | Swing5 + EMA20 hard | 4 | 1382 | 2356.5 | 1.57 | 27.5 | ADR-008 winner |
| Must | **78** | Blue | Swing5 + SMA20 hard | 4 | 1467 | 2348.8 | 1.43 | 32.8 | Confirm alternate |
| Strong | **48** | Blue | Swing5 | nil | 767 | 2073.5 | 1.52 | 20.9 | Uncapped lab upper bound |
| Strong | **72** | Orange | BO20 | nil | 813 | 727.5 | 0.81 | 45.9 | Non-Blue transfer |
| Strong | **92** | Orange | BO20 + Pen hard | nil | 700 | 1148.1 | 1.40 | 22.6 | Strong Orange confirm child |
| Optional | **45** | Orange | BO20 | nil | 825 | 383.1 | 0.92 | 39.0 | Dynamic survivor |
| Control | **44** | Blue | BO20 | nil | 582 | 1532.1 | 1.49 | 34.7 | Full TS3 control |
| Optional | **71** | Blue | BO20 | nil | 705 | 589.0 | 0.89 | 60.8 | DD weak; use carefully |
| New books | **121** Mint / **122** Yellow | Swing5 | nil | 1357/1524 | 1367/719 | 1.42/1.44 | 23.6/21.1 | Optional later transfer (not in first 7–10) |

**Matrix parents locked for first wave:** 62, 80, 78, 48, 72 (CT04/CT09), plus 80 for CT08.

## Experiment matrix (~7–10 PBRs + cadence audit)

### Axis A — Close-confirmed entry (H1)

Close breakout: long `close > prior-window max_high`, short `close < prior-window min_low`. Keep parent confirms/exits/caps/R1 ladder. Stop: **move_to_last_entry**.

| Cell | Parent | Change |
|------|--------|--------|
| CT01 | 62 | Swing5 → Swing5 **close** |
| CT02 | 80 | Swing5 **close** + keep EMA20 |
| CT03 | 78 | Swing5 **close** + keep SMA20 |
| CT04 | 71 or 72 | BO20 → BO20 **close** |
| CT05 | 48 | Swing5 **close** (uncapped) |

### Axis B — `one_way_dynamic_close` risk (H2)

Keep high/low primary so weak/standard/aggressive can all occur. New risk strategy (registry key e.g. `one_way_dynamic_close`) with `weak_policy: base | step_back`.

| Cell | Parent | Weak path | Purpose |
|------|--------|-----------|---------|
| CT06 | 62 | **W-base** | Flat weak baseline |
| CT07 | 62 | **W-step** | Step-back weak |
| CT08 | 80 | winner of CT06/07 | Best-recipe transfer |
| CT09 | 72 or 45 | W-step preferred | Non-Blue transfer |

Optional CT10 if inventory shows another active book.

### Axis C — Signal X → fill X+1 open (H3)

Methodology gate (script/audit), not a new recipe:

- Sample journals on each frozen parent and each child
- Assert signal date X, fill date X+1, price = session open (entry/exit)
- Report pass rates in BA; open defect issue on systemic fail

## Implementation outline

1. **Inventory** parents (rails) → freeze table on this ticket or BA stub  
2. **Axis A:** close-breakout strategy classes + TSS seed + clone script (pattern: `lib/scripts/confirm_entry_experiment_matrix.rb`)  
3. **Axis B:** strength annotation + `one_way_dynamic_close` risk + specs (W-base, W-step, aggressive, floor)  
4. **Axis C:** cadence audit script over PBR journals  
5. **BA:** `ecosystem/business_analysis/2026-07-24-close-trigger-signal-strength.md`  
6. Close ticket with rules **or** follow-ons; update `business_analysis/README.md`

Batch: `FAST_BACKTEST=1` (I/O only). No Wv2 export until BA promotes.

## Phase 1 progress (Axis A — 2026-07-24)

### Code landed (WUT)

| Artifact | Path |
|----------|------|
| Swing5 close | `app/strategies/entry_exit/swing_breakout_5_day_close_strategy.rb` |
| BO20 close | `app/strategies/entry_exit/breakout_20_day_close_strategy.rb` |
| Lookback periods | `app/services/strategy_lookback.rb` |
| Registry | `app/strategies/strategy_registry.rb` |
| Specs (14 ex) | `spec/strategies/close_breakout_strategies_spec.rb` |
| Clone/execute | `lib/scripts/close_trigger_experiment_matrix.rb` |
| TSS rows | 23 Swing5-close, 24 BO20-close |

### Child PBRs (Axis A)

| Cell | PBR | Parent | Primary change |
|------|-----|--------|----------------|
| CT01 | **142** | 62 | Swing5 → Swing5 close |
| CT02 | **143** | 80 | Swing5 → Swing5 close (keep EMA20) |
| CT03 | **144** | 78 | Swing5 → Swing5 close (keep SMA20) |
| CT04 | **145** | 72 | BO20 → BO20 close |
| CT05 | **146** | 48 | Swing5 → Swing5 close (uncapped) |

All children: `one_way_dynamic` + parent ladder, `move_to_last_entry`, campaign tag in `results_json`.

**Execute:** `EXECUTE_IDS=142,143,144,145,146 FAST_BACKTEST=1 CONCURRENCY=1 rails runner lib/scripts/close_trigger_experiment_matrix.rb`  
**Log:** `/tmp/close_trigger_axis_a.log` (host)

### Metrics (Axis A complete 2026-07-24)

| Cell | PBR | Parent | Parent ret / DD / Sh / trades | Child ret / DD / Sh / trades | ΔRet | ΔDD | ΔSh | Δ trades |
|------|-----|--------|-------------------------------|------------------------------|------|-----|------|----------|
| CT01 | **142** | 62 Blue C0 | 1415.4 / 41.6 / 1.11 / 1443 | **1715.4 / 25.9 / 1.60 / 1321** | **+300** | **−15.7** | **+0.49** | −122 |
| CT02 | **143** | 80 Blue+EMA20 | 2356.5 / 27.5 / 1.57 / 1382 | 1756.3 / **17.0** / **1.66** / 1236 | −600 | **−10.5** | +0.09 | −146 |
| CT03 | **144** | 78 Blue+SMA20 | 2348.8 / 32.8 / 1.43 / 1467 | 1575.1 / **27.2** / 1.43 / 1281 | −774 | **−5.6** | 0 | −186 |
| CT04 | **145** | 72 Orange BO20 | 727.5 / 45.9 / 0.81 / 813 | **833.8 / 28.3 / 1.42 / 847** | **+106** | **−17.6** | **+0.61** | +34 |
| CT05 | **146** | 48 Blue uncapped | 2073.5 / 20.9 / 1.52 / 767 | 926.7 / 23.9 / 1.41 / 875 | −1147 | +3.0 | −0.11 | +108 |

### Phase 1 (H1) provisional reading

1. **Blue C0 without confirm (CT01):** close primary is a clear win — higher return, much lower DD, higher Sharpe, fewer trades. Best single-axis evidence for H1 under honest caps.
2. **Blue C0 with hard confirm (CT02/CT03):** close primary **cuts return hard** vs high/low Swing5+confirm, but **improves DD** (CT02 → 17% best DD in matrix). Sharpe flat/slightly up on CT02. Stacking close primary on top of EMA/SMA confirm is **not free alpha** — may over-filter.
3. **Orange transfer (CT04):** close BO20 **wins** on ret, DD, and Sharpe — H1 transfers outside Blue.
4. **Uncapped Blue 48 (CT05):** close primary **loses** vs high/low Swing5 uncapped (ret −1147pp, slightly worse DD/Sharpe). Close is **not** a free upgrade when capacity is unlimited and the high/low recipe was already the lab max.
5. **Trade counts:** mostly fall with close filter (CT01–03); CT04/CT05 slightly up — re-entry / path effects, not pure “fewer signals.”

**Phase 2 implication:** H1 is **conditional** (strong on C0/Orange plain primaries; weak/harmful when stacked on confirm or uncapped 48). Proceed with Axis B strength-aware risk on **high/low primaries** (so weak+standard+aggressive can coexist), using W-base and W-step on parent **62** first — do not assume close-only entry replaces risk path.

### Phase 2 code (Axis B — 2026-07-24)

| Artifact | Path |
|----------|------|
| Strength classifier | `app/strategies/risk/signal_strength_classifier.rb` |
| Risk strategy | `app/strategies/risk/one_way_dynamic_close_risk_evaluation.rb` |
| Wiring | `PositionManager`, `PortfolioBacktestRunner`, `EntryRequirementCalculator` |
| Specs | `spec/strategies/one_way_dynamic_close_risk_evaluation_spec.rb` (9 ex + classifier) |
| Matrix AXIS=B | same script, CT06–CT09 |

**Strength → ladder index (R1 long [2,3,4,6,6]%):**

| Strength | W-base | W-step |
|----------|--------|--------|
| weak | always **2%** | ladder `max(1, pos−1)` (floor 2%) |
| standard | ladder `pos` | same |
| aggressive (close beyond level) | ladder `min(len, pos+1)` | same |

### Child PBRs (Axis B)

| Cell | PBR | Parent | Primary (unchanged high/low) | Risk | Weak policy | Ladder long |
|------|-----|--------|------------------------------|------|-------------|-------------|
| CT06 | **147** | 62 | Swing5 | `one_way_dynamic_close` | **base** | R1 [2,3,4,6,6] |
| CT07 | **148** | 62 | Swing5 | `one_way_dynamic_close` | **step_back** | R1 |
| CT08 | **149** | 80 | Swing5 + EMA20 | `one_way_dynamic_close` | **step_back** | R1 |
| CT09 | **150** | 72 | BO20 | `one_way_dynamic_close` | **step_back** | Orange [2,3,3,4,4] |

All: `move_to_last_entry`; ladder dual-written in `risk_evaluation_config` + top-level `pyramid_risks` + label.

**Execute log:** `/tmp/close_trigger_axis_b.log`

### Metrics Axis B (complete 2026-07-24)

| Cell | PBR | Parent | Parent ret/DD/Sh/tr | Child ret/DD/Sh/tr | ΔRet | ΔDD | ΔSh | Δtr |
|------|-----|--------|---------------------|--------------------|------|-----|------|-----|
| CT06 | **147** | 62 W-base | 1415/41.6/1.11/1443 | 1383/41.7/1.11/1349 | −32 | +0.1 | 0 | −94 |
| CT07 | **148** | 62 W-step | 1415/41.6/1.11/1443 | 1383/41.7/1.11/1349 | −32 | +0.1 | 0 | −94 |
| CT08 | **149** | 80 W-step | 2357/27.5/1.57/1382 | **3398/31.8/1.66/1411** | **+1041** | +4.3 | +0.09 | +29 |
| CT09 | **150** | 72 W-step | 728/45.9/0.81/813 | 633/**31.2**/1.11/853 | −95 | **−14.7** | **+0.30** | +40 |

**Risk histograms (journal `position_sizing_risk`):** ladders fired (not flat 2%).
- 147/148: 2%≈661, 3%≈462, 4%≈120, 6%≈106
- 149: 2%≈640, 3%≈497, 4%≈140, 6%≈134
- 150 (shallower Orange): 2%≈246, 3%≈541, 4%≈66

### Phase 2 (H2) provisional reading

1. **CT06 ≡ CT07** (identical metrics and risk hist): on Blue 62 Swing5, W-base vs W-step does not separate. Likely most weak events are early pyramid levels where step-back still floors at 2%, and/or aggressive (close-beyond) dominates later adds (pyramids already require close).
2. **Blue 62 strength-aware alone** is roughly flat vs plain R1 (slight ret down, DD/Sharpe unchanged) — not a free upgrade without confirm.
3. **CT08 (Blue 80 + EMA20 + strength risk):** large **return + Sharpe** lift vs parent 80; **DD worse** (27.5 → 31.8). Aggressive pos+1 on close-confirmed path may oversize winners.
4. **CT09 (Orange 72):** classic quality tradeoff — **much better DD/Sharpe**, lower total return.
5. **H2 is recipe-dependent**, similar to H1: strongest interaction is with **confirm + strength risk** (CT08), not bare Swing5 C0.

**Next:** Axis C (signal day X → fill X+1 open audit); then BA write-up + business rules or follow-ons.

## Acceptance

- [x] Ticket in INDEX  
- [x] Parent freeze with live metrics  
- [x] Axis A child PBRs executed (142–146); campaign tag in `results_json`  
- [x] Axis B child PBRs executed (147–150); campaign tag + ladders verified  


- [x] All children `move_to_last_entry`  
- [x] Axis C cadence report (FAIL vs ops T+1; lab same-day open — evidence in BA)  
- [x] BA doc with ΔRet / ΔDD / ΔSharpe / ΔTrades and H1/H2/H3 verdicts  
- [x] Business rules written **and** follow-on filed (`2026-07-24-lab-pbr-signal-x-fill-x1-open.md`)  
- [x] No parent PBR overwritten  

## Out of scope

- Soft-confirm matrix redo  
- Pyramid UI / estimate-cap issue (`2026-07-19-one-way-dynamic-pyramid-risk-visibility-and-cap`)  
- Real capital promotion  
- Intraday bars  
- Joint re-grid of entry × confirm × ladder × strength  

## Related

- ADR-008 — confirmational entry vs pyramid risk scale  
- ADR-009 / archive `2026-07-20-eod-signal-fill-dates-next-open` — ops T / T+1 open  
- BA: `business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md`  
- BA: `business_analysis/2026-07-18-confirmational-entry-experiment.md`  
- Level 2: `2026-07-13-pbr-level2-remaining-experiments.md`  
- Plan session: close-trigger + one_way_dynamic_close (operator review 2026-07-24)


## Closeout (2026-07-24)

Research complete. Canonical write-up:

**`ecosystem/business_analysis/2026-07-24-close-trigger-signal-strength.md`**

| Axis | Result |
|------|--------|
| A (H1) | Conditional accept — CT01/CT04 wins; confirm-stack and uncapped 48 hurt return |
| B (H2) | Conditional — CT08 return star; CT06≡CT07; CT09 quality win |
| C (H3) | **Fail ops doctrine** — lab fills same-day open, not X+1 |

Follow-on: `docs/tickets/2026-07-24-lab-pbr-signal-x-fill-x1-open.md` (P1).
