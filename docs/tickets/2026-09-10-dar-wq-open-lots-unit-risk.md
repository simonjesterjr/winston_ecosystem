# Ticket: Unit-risk column on DAR and Winston Quiver open-lot tables

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-09-10  
**Monolith:** winston_v2  
**Mode:** contractor  
**Graph nodes:** winston_v2  
**See:** session [`winston_v2/docs/session-reports/2026-09-10-1532-walnut-unit-risk-inspect-layout.md`](../../../winston_v2/docs/session-reports/2026-09-10-1532-walnut-unit-risk-inspect-layout.md); helper `winston_v2/app/services/operations/unit_risk.rb`

---

## Problem

Portfolio live, ops-shell Positions (by band), and Signal Inspect lots now show **Unit risk** (dollars from mark to working stop) next to P&L. Daily Analysis Report (DAR) open-lot tables and Winston Quiver (WQ) tracking lots do not. Same semantic, different surfaces — operators will see P&L without remaining unit risk on those pages.

## Scope

Reuse `Operations::UnitRisk.remaining` / `at_entry`. Do not invent a second formula.

- DAR payload + markdown/PDF open-lots table (Trend Following Operational Portfolios)
- WQ tracking current-book / open-lots table on `/quiver_tracking`

Caption: remaining dollars to the working stop, not share notional. $0 when through the stop.

## Acceptance

- [ ] DAR JSON/markdown/PDF lot row includes `unit_risk` (and tooltip/original if the surface has room)
- [ ] WQ open-lots table shows the column next to P&L
- [ ] Specs on the DAR renderer and WQ page (or payload) assert the field
- [ ] If GTC-vs-row-stop (`2026-09-10-unit-risk-vs-parked-gtc.md`) lands first, these tables follow that rule

## Out of scope

- Changing sizing or Quiver plan weights
- Extra-modal / LEAP remaining-premium math

## Origin

Wrap follow-up item 5 from session `2026-09-10-1532-walnut-unit-risk-inspect-layout.md`.
