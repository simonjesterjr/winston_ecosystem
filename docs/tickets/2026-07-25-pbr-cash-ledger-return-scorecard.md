# Ticket: PBR free-cash ledger — total-return scorecard

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-07-25  
**Monolith:** winston_unit_test  
**Related:** session `ecosystem/docs/session-reports/2026-07-25-1310-pbr-fill-queue-pyramid-cash.md`; cash ledger partial `_cash_ledger.html.erb`; `PortfolioPositionManager#cash_snapshot`

---

## Problem

Operators reading the free-cash ledger end_of_run row often treat **free cash Δ** as strategy success. That misleads under two-way books:

- **Shorts credit free cash** on entry; longs debit it.
- Canonical wealth is **equity** = free cash + long MV − short MV.
- **Gross MV** (long + short) answers “markets controlled,” not return.

Example (session): free cash ~+47% while equity total return ~+26% with ~$40k gross / ~$10k capital.

The recon strip already shows free cash, equity, long/short MV, but does **not** surface return % vs free-cash Δ, gross/net exposure, or leverage in one glance.

---

## Proposed UX (recon strip + optional end_of_run reason line)

| Metric | Formula | Label intent |
|--------|---------|--------------|
| Total return % | (final equity − initial) / initial | Primary success |
| Free cash Δ % | (final free − initial) / initial | Annotated: “includes short proceeds” |
| Gross controlled | long MV + short MV | Footprint |
| Net exposure | long MV − short MV | Directional bias |
| Leverage | gross / equity (or / initial) | Intensity |

Do **not** replace equity return with free-cash %. Add annotations only.

---

## Acceptance

- [ ] PBR show cash recon strip shows total return % from `initial_capital` and stored/final equity
- [ ] Free-cash change labeled so it is not confused with return
- [ ] Gross MV and net exposure visible at end_of_run without hand calc
- [ ] Docs blurb in cash ledger intro updated (one line is enough)

---

## Out of scope

- Changing cash accounting identity
- Heat / unit limits (see heat ticket)
- Wv2 ops DAR equity presentation (unless parity is wanted later)
