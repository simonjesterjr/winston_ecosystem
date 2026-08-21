# Plan: Automate Quiver Strategies PDF / scrape (future)

**Status:** Proposed — **not v1**. Human-in-the-loop PDF download is the tracking-desk ingest.  
**Date:** 2026-08-21  
**Monoliths:** possibly a small worker beside DM; **not** Wv2; never a Quiver key on Wv2  
**Depends on:** `quiver-tracking-desk.md` shipping PDF ingest first  
**Ticket:** `docs/tickets/2026-08-21-quiver-pdf-bot-scrape.md`  
**Analysis:** `docs/analysis/2026-08-21-quiver-quant-vs-api-vs-dm.md`

## Why this is later

Published Congress Long-Short **holdings and `% of NAV`** live on the Premium Quiver Strategies page. The Quiver API we already use (DM Alt Filings) does **not** return that book. A bot that logs in and grabs the same PDF (or HTML table) the operator prints today would only **remove HITL**, not change the tracking desk.

v1 must work with a hand-uploaded PDF so parser, gap tasks, and the desk exist before we take on:

- Quiver login / session / 2FA
- Terms-of-service and ToS risk
- Brittle DOM / print-CSS
- Secret storage (Quiver **site** credentials ≠ `QUIVER_API_KEY`)

## What we would automate

1. Scheduled (weekly, after Quiver’s rebalance — currently **Friday** on the public page) login to `quiverquant.com/strategies/s/Congress%20Long-Short/`.
2. Export or print-to-PDF the Holdings (+ optional Upcoming / Opened / Liquidated).
3. POST the bytes to Wv2’s existing ingest (`internal` API used by the tracking desk), **or** drop into `storage/reports/quiver_tracking/inbox/` for the same job.
4. Fail closed: if login/PDF fails, HITL task “download the PDF yourself” — never invent a book from filings.

## What we would not do

- Scrape as a substitute for DM Alt Filings (filings stay on the API → DM).
- Call undocumented “strategy holdings” API from Wv2.
- Put site cookies in Wv2 or Cromwell chat logs.
- Treat a successful scrape as matching published CAGR.

## Owner when we build it

Prefer a **DM-adjacent worker** (same secret isolation pattern as EODHD/Quiver API) that only **writes files + notifies**. Wv2 continues to own parse, diff, and tasks. Do not teach Cromwell to hold Quiver passwords.

## Acceptance (when scheduled)

- [ ] Tracking desk v1 ingest is green on hand-uploaded fixtures
- [ ] Secret store and ToS review written
- [ ] Bot failure becomes a HITL task, not a reconstructed filing book
- [ ] No strategy holdings path that bypasses the PDF/parser contract
