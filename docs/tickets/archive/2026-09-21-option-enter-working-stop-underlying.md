# Ticket: Option enter must keep Working Stop on the underlying

**Status:** Done  
**Priority:** P0  
**Date:** 2026-09-21  
**Mode:** contractor  
**Graph nodes:** winston_v2 (`desk_workflows/show`, `_fill_stop_adjust_script`, `JournalConfirmationService`, `Position#updated_stop`)  
**Implementer:** Winston Dev  
**Human gates:** Mode C paper; do not Desk-Send; correcting booked lots is operator-gated cash/stop hygiene, not a silent flatten  
**DoD:** Option-like Confirm leaves Working Stop at 2N under/over the **underlying**. Fill-stop JS does not subtract ATR from option premium. Spec locks it. Booked 1943/1946 stops corrected or explicitly left with an operator note.  
**Origin:** Wrap [`../session-reports/2026-09-21-1457-mode-c-furthest-call-desk-uat.md`](../session-reports/2026-09-21-1457-mode-c-furthest-call-desk-uat.md) §14 item 1  
**Related:** Issue [`../issues/2026-09-21-option-enter-working-stop-from-premium.md`](../issues/2026-09-21-option-enter-working-stop-from-premium.md); ADR-018 Working Stop on underlying; exit-mark ticket [`2026-09-20-mode-c-leap-exit-at-stop-option-mark.md`](2026-09-20-mode-c-leap-exit-at-stop-option-mark.md) (different: STC fill)

## Why P0

Two live Mode C paper option lots already have through-the-market `updated_stop` values. Anything that treats Working Stop as an underlying GTC will false-trigger stop-out.

| Journal | Pos | Booked stop | Intended (~2N under close) |
|---------|-----|-------------|----------------------------|
| 1943 SEF 4× Feb 30C | Mango | 0.78 | ~29.95 |
| 1946 BITQ 2× Apr 28C | Indigo #889 | 2.33 | ~24.89 |

## Scope

1. Skip fill-stop JS rewrite when fulfillment is option-like (`leap` / `standard_call` / `option`).  
2. Confirm path: persist underlying suggested stop, not `price − 2N` when price is premium.  
3. Request spec: Plan B standard_call GET/confirm does not land `updated_stop` in premium space.  
4. Operator-gated correction of 1943 and 1946 `original_stop` / `updated_stop` (and journal details `stop_price`) to the underlying 2N values.

## Non-goals

- Changing ATR multiple or pyramid geometry  
- Silent IBKR STP  
- Using Working Stop as the option fill (that is the other P0 ticket)

## Acceptance

- [x] GET Plan B call: Stop field stays ~2N under underlying while Price is option mid  
- [x] Confirm does not write premium−ATR onto `Position#updated_stop`  
- [x] 1943 and 1946 stops corrected or operator-noted  
- [x] Stock enter fill-stop JS still retargets when the operator edits the **share** fill
