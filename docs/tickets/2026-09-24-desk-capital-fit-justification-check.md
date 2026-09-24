# Ticket: Click the desk Capital fit line

**Status:** Proposed
**Priority:** P0
**Date:** 2026-09-24
**Lane:** B (verification only)
**Implementer:** next desk session
**DoD:** A human or agent opens Desk Workflow on a draft that carries `capital_fit_reason` and sees Turtle shares, fitted units, the reason, the slice, and the budget.
**Parent:** [`2026-09-22-min-atr-capital-consumption-guard.md`](2026-09-22-min-atr-capital-consumption-guard.md)
**Session:** [`../session-reports/2026-09-24-0854-capital-fit-usdu-guard.md`](../session-reports/2026-09-24-0854-capital-fit-usdu-guard.md)

## Goal

Winston v2 Justification (`app/views/operations/desk_workflows/_justification.html.erb`) renders a Capital fit row when `capital_fit_reason` is present. Specs cover the sizer and confirm. Nobody opened the panel in a browser during the session that added the row.

## Work items

- [ ] Produce or find a draft whose fulfillment details include `capital_fit_reason`, `capital_fit_units`, `capital_fit_slices`, and `capital_fit_budget`.
- [ ] Open `http://127.0.0.1:3002/operations/workflow?journal_id=<id>`.
- [ ] Confirm the Capital fit line shows the Turtle count, the fitted count, the reason, the slice, and a dollar budget.
- [ ] Note the journal id on this ticket. No code change unless the line is missing or wrong.

## System One harness

**State:** The partial prints the row only when `details["capital_fit_reason"]` is present. Confirm and the task generator stamp those keys.

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| line_visible | Noul | The Justification panel shows Capital fit with both unit counts and a budget | noul ≥ 0.85 |

**Runner:** browser on the workflow URL. Skip `jev ask`.
**On fail:** file what the panel actually showed and fix the partial.

## Non-goals

- Restyling the desk.
- Re-opening the USDU overdraft decision (sibling ticket `2026-09-24-teal-indigo-usdu-overdraft.md`).
