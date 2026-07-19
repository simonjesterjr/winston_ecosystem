# Ticket: PBR show pyramid ladder + fix EntryRequirementCalculator cap

**Status:** Partially done (export/validation/Wv2 import 2026-07-19); UI + estimate clamp remain  
**Date:** 2026-07-19  
**Monolith:** winston_unit_test (+ Wv2 importer/sizer)  
**Issue:** `docs/issues/2026-07-19-one-way-dynamic-pyramid-risk-visibility-and-cap.md`  
**ADR:** ADR-008 §E

## Done

- [x] Export embeds `pyramid_risks` / `risk_evaluation_config`  
- [x] `OneWayDynamicRiskValidator` blocks export without ladder  
- [x] Fingerprint + `full_config_json` backfill  
- [x] Wv2 importer → `TradingStrategy.parameters`  
- [x] Wv2 `PositionSizer` reads ladder by pyramid level  

## Remaining scope

1. **Show page** — if `risk_evaluation_strategy == one_way_dynamic`, display long/short risk % per pyramid level from `results_json.risk_evaluation_config.pyramid_risks` (or empty-ladder warning).  
2. **Optional:** journal table column `Risk %` from `position_sizing_risk`.  
3. **Fix** `EntryRequirementCalculator` so one_way ladder levels above base `risk_percentage` are **not** clamped to base % for cash/unit estimates.  
4. **Specs** for calculator + optional request/system check that show includes ladder text.

## Out of scope

- Changing R1 ladder values  
- Soft confirm UX  
- Wv2 daily analysis sizing (follow-up if same clamp exists there)

## Acceptance

- [ ] PBR 80 show renders long `[2,3,4,6,6]%` (or decimal) ladder  
- [ ] Level-3 long estimate uses ~4% of capital_base when ATR/stop allow  
- [ ] Existing static risk PBRs unchanged  
- [ ] Unit tests green
