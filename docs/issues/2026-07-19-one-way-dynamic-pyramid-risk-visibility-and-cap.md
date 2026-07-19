# Issue: One-way dynamic pyramid risk hard to see + estimate path caps acceleration

**Status:** Partially fixed (export/validation 2026-07-19); UI + estimate cap still open  
**Date:** 2026-07-19  
**Monolith:** winston_unit_test (+ Wv2 import/sizer)  
**Related:** ADR-008, PBR 80 (confirm winner), `EntryRequirementCalculator`, PBR show UI

## Symptom

On PBR show (e.g. `/wut/portfolio_backtest_runs/80`), risk evaluation reads **One way dynamic**, but operators cannot see the R1 ladder or per-add risk %. Journals/UI do not make it obvious that later concurrent pyramids use 3% / 4% / 6%. Easy to conclude “risk is flat 2%.”

## What is actually true (verified on PBR 80)

Config present in `results_json`:

```json
"risk_evaluation_config": {
  "pyramid_risks": {
    "long":  [0.02, 0.03, 0.04, 0.06, 0.06],
    "short": [0.02, 0.02, 0.02, 0.03, 0.03]
  }
}
```

Journal `position_sizing_risk` histogram (entry-sized rows): ~2% dominant (level-1 / re-entries), with clear mass at 3%, 4%, 6%.  
TSLA concurrent pyramid sequence example: **0.02 → 0.03 → 0.04 → 0.06** with rising unit counts.

So **scale-in is implemented** on the PositionManager path; it is not “overlooked” as a missing strategy choice on PBR 80.

## Why it *looks* flat

1. **Show page** prints strategy name only — not the ladder (`show.html.erb` “Risk Evaluation: One way dynamic”).  
2. **Journal listing** does not show `position_sizing_risk`.  
3. **Most adds are pyramid level 1** — after flat or new market entry, index resets to 2%. Ladder applies only while **multiple concurrent lots** exist on that market.  
4. **Short ladder is flatter** by design (`[2,2,2,3,3]`).  
5. Units ≠ pure risk % — ATR and capital_base change; level-2 can still show “small” units on expensive names.

## Real defect (estimate path)

`PortfolioBacktest::EntryRequirementCalculator` clamps risk to `portfolio_backtest_run.risk_percentage` (often **0.02**) whenever effective risk exceeds that:

```ruby
if size_mult >= 1.0 && effective_risk_pct > max_risk_pct * 1.001
  risk_amount = capital_base * max_risk_pct
```

That **caps cash-check estimates** for pyramid levels 2+ even when the one-way ladder says 3–6%.  
Actual fill sizing uses `PositionManager` + `OneWayDynamicRiskEvaluation` **without** that clamp — so fills can accelerate while pass/cash logic thinks everything is 2%. Risk of wrong `insufficient_cash` / priority behavior under heavy pyramids.

## Expected product behavior (operator intent)

> One-way dynamic = as we add pyramid positions we treat that as confirmation of a longer trend (e.g. 3 ATR moves → expect longer run) and **scale risk into the exponential move**.

That is the ladder. Confirmational **entry** strategies are a separate, initial-entry filter (ADR-008).

## Fixed 2026-07-19 (handoff JSON)

- `PortfolioConfigExporter` embeds `pyramid_risks` + `risk_evaluation_config` at portfolio root and under `trading_strategy`.  
- `OneWayDynamicRiskValidator` **refuses export** if `one_way_dynamic` without a valid ladder.  
- Fingerprint capture includes ladder in payload + `full_config_json` (methodology identity).  
- Wv2 importer stores ladder on `TradingStrategy.parameters`; PositionSizer reads ladder for level sizing.  
- Re-export PBR 80 (and any one_way_dynamic OP) before ops use.

## Still open (ticket)

1. **UI:** On PBR show, render ladder table.  
2. **Journals:** Optional `position_sizing_risk` column.  
3. **Calculator:** Estimate path clamp to base 2%.  
4. Specs for estimate alignment.

## Severity

- **Export omission:** Critical for Wv2 (was silent flat risk) — **fixed**.  
- **Visibility / estimate cap:** Medium — remaining ticket work.
