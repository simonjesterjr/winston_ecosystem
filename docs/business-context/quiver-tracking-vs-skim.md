# Quiver Tracking vs Skim vs Alt Filings

**Date:** 2026-08-21  
**Status:** Draft domain explainer (pairs with CONTEXT terms)  
**Law:** ADR-011 still holds for events. Tracking does not make Alt Filings into Daily Analysis signals.

## Three books, three jobs

| Name | Home | Source | Used for |
|---|---|---|---|
| **Alt Filing** | DM `quiver_filings` | Quiver **API** (Congress/insider events) | Event store; file-date only |
| **Quiver Skim** | WUT `/quiver_skim` + DM catalog | Reconstruction from Alt Filings | Lab NAV / diffs; not published CAGR |
| **Quiver Tracking Portfolio** | Wv2 `/quiver_tracking` | **Quiver Snapshot PDF** (HITL) | Paper membership that follows the **published** Premium holdings |

Prices for Skim and Tracking both come from **DM parquet** (EODHD). Neither uses Quiver as a bar vendor.

## Tracking is not TF

- No Daily Analysis enter/pyramid/exit from a PDF or a filing.
- Ingest (PDF or TXT) builds a **Monday Rebalance Plan**. **Plan Approve** is the Human-Gated verb; approved legs auto-execute at next session open (dummy_sim in test).
- Two exclusive calendar modes: flatten-all on a weekday, or rebalance-to-published-book (Monday live cadence).
- Membership may mutate in place on this paper shadow OP (that is the desk). Test blow-away wipes paper tracking lots only.
- First journal still **engages** the OP (ADR-006) for TF books; the tracking exception is this in-place plan path.
- Broker Gateway dummy_sim sandbox fills are the test fulfillment path. Live Schwab write is after test cycles, on a separate WQ binding from Wv2 Ops.

## API vs site

Use the API only through DM, and only for filings. Published `% of NAV` is not in that API. v1 accepts a PDF; a login bot is a later plan.
