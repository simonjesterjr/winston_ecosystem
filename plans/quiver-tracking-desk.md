# Plan: Wv2 Quiver Tracking Desk (PDF HITL → gap tasks)

**Status:** Proposed — v1 authorized as paper tracking only; scrape bot and Broker Gateway (BG) fills are **not now**  
**Date:** 2026-08-21  
**Monoliths:** Winston v2 (Wv2) primary; data_manager (DM) for parquet + optional filing footnote; Cromwell/Telegram as an upload alternate  
**Builds on:** ADR-006, ADR-009, ADR-011; analysis `docs/analysis/2026-08-21-quiver-quant-vs-api-vs-dm.md`  
**Public URL:** `https://sawtooth-ai.tail944ffb.ts.net/wv2/quiver_tracking`  
**Related:** WUT Quiver Skim (lab reconstruction); existing Wv2 copy-book `qcls13030-l30-filedate-v1` (do not mix)

---

## 1. Why this plan exists

The operator will **download a PDF from Quiver Quantitative** (human in the loop), upload it (Telegram or the tracking page), and have **Winston v2 (Wv2)** compare that published book to a **paper Congress Long-Short Tracking Portfolio** (starts empty). Wv2 emits **tasks that close the gap**: pull parquet in data_manager (DM), add/drop/reweight names on the tracking book, plus any HITL leftovers.

This is **not** Trend Following (TF) Daily Analysis. It is not the WUT Quiver Skim reconstruction. It is a **tracking desk**: paper journals, pending, positions, equity curve, scoped to tracking portfolios only.

## 2. Product shape

| Surface | Behavior |
|---|---|
| `/quiver_tracking` | Same visual language as ops shell (`ops_shell.css`), **separate route**. No TF pending bleed. |
| Tracking Portfolio | One paper Operational Portfolio (OP) for Congress Long-Short tracking. Starts **empty**. Recipe/fingerprint distinct from TF and from the old copy-book 15/10 reconstruction. |
| Target book | Parsed from the uploaded PDF (Holdings: ticker, side, `% of NAV` / amount). |
| Current book | Open lots + pending tracking tasks on that OP (empty at first). |
| Gap tasks | Automated where we can (`dm_pull`, `add_book`, `drop_book`, `reweight`); HITL where we cannot (ambiguous ticker, unreadable PDF page, remap). |
| Artifacts | PDFs under `storage/reports/quiver_tracking/` (same family as Daily Activity Report (DAR) `storage/reports/`). |
| Daily Analysis | **Skip** this OP (`quiver_tracking_book`). No TF signals. |
| Desk / paper forms | Humans confirm population and weighting changes (enter/exit/reweight) — Human-Gated, same journal/confirm spine, fractional units OK. |
| BG | Paper: dummy_sim (production-ready-WQ Phase 1). Live Schwab: [`production-ready-wq.md`](production-ready-wq.md) Phases 2–4. Old `quiver-tracking-bg-fulfillment.md` superseded. |

## 3. Sources of truth (priority)

See the analysis. Summary:

1. **DM parquet** — prices, coverage, “pull data on X markets.”
2. **HITL PDF** — published Quiver holdings / weights for the tracking target.
3. **DM Alt Filings + book catalog** — optional footnote (“filing reconstruction vs PDF”). Never the task generator for v1.
4. **Quiver API** — stays in DM for filings only. Wv2 never holds the key.
5. **Website scrape** — later plan, not v1.

## 4. Workflow (v1)

```text
Operator (HITL)
  download PDF from Quiver Strategies → Congress Long-Short
  upload via /quiver_tracking  OR  Telegram document (alternate)
        ↓
Wv2 ingest
  store PDF + checksum + as_of + operator
  parse holdings table → target legs (ticker, side, weight)
        ↓
Diff vs current Tracking Portfolio (empty at first)
  missing in Wv2 + in PDF     → add_book + size
  in Wv2 not in PDF           → drop_book / exit
  both, weight drifted        → reweight
  ticker unknown to DM parquet → dm_pull (auto) + wait/HITL if still missing
  parse failure / remap       → HITL task
        ↓
Tracking desk
  pending / journals / positions / equity for this OP only
  paper confirm closes a gap (engages the OP — ADR-006 still applies)
```

First run against an empty OP is “add everything in the PDF” plus DM pulls. That is expected.

## 5. Isolation from TF ops shell

Reuse the copy-book lesson: filter **in SQL before `limit(25)`**.

- Tracking tasks/journals tagged `source=quiver_tracking`, `copy_book` **false**, `tracking_book` true (do not overload the Congress reconstruction tag).
- Ops shell `/operations` does **not** list tracking pending in the TF 25-row cap. Optional one-line “Tracking desk has N pending” link to `/quiver_tracking`.
- Daily Analysis, DAR chapters, parquet-missing for DA, stale-expire-on-TF-window: exclude tracking OPs.
- `/quiver_tracking` panels: last PDF, target vs current, pending, positions, journals, equity, DM coverage.

Existing Friday copy-book packager (`QuiverCongressLongShortRebalanceJob`) must **not** mint TF-style enters onto the tracking OP. Either skip tracking fingerprints or retire that job once tracking ingest is live (ticket).

## 6. Implementation slices (tickets)

| Order | Ticket | Notes |
|---|---|---|
| 1 | `docs/tickets/2026-08-21-wv2-quiver-tracking-page.md` | Route, shell chrome, empty paper OP bootstrap, isolation |
| 2 | `docs/tickets/2026-08-21-wv2-quiver-pdf-ingest-and-gap-tasks.md` | Store PDF, parse, diff, task mint, Telegram alternate |
| 3 | `docs/tickets/2026-08-21-dm-parquet-for-quiver-tracking-books.md` | `dm_pull` → DM Symbol Demand; coverage on the tracking desk |
| 4 | `docs/tickets/2026-08-21-wv2-quiver-tracking-population-forms.md` | Paper enter/exit/reweight forms on the tracking page |
| later | `docs/tickets/2026-08-21-quiver-pdf-bot-scrape.md` | Bot/scrape — **not now** |
| later | `docs/tickets/2026-08-30-production-ready-wq.md` | BG / Schwab — production-ready WQ phases 1–4 |

Also keep `2026-08-20-mount-quiver-env-live-alt-filing-sync.md` if we want the DM footnote reconstruction.

## 7. Domain / UI constraints

- **Responsive Page** (ADR-005): shell first; PDF parse and DM pull async (Sidekiq).
- **Engaged OP:** first tracking journal locks Books + recipe until Close / successor (ADR-006). Reweight of an existing name is a **population/weight** desk action on the same OP, not a silent re-import. Adding a **new** name is a Book add — treat as shape change: prefer successor if already engaged, **unless** we carve an explicit “tracking membership may mutate in place” exception. **v1 recommendation:** tracking membership **may mutate in place** (that is the point of the desk) with an audit row per PDF ingest; TF OPs stay frozen. Promote this exception to an ADR addendum before coding if grill disagrees.
- Execution mode: **paper**. Capital: operator-chosen seed (default `$2,000` to match prior copy-book, or `$100,000` lab NAV — pick in ticket 1; default **$2,000 paper**).
- Fractional `units` already on journals/positions.
- Tailscale Serve already prefixes `/wv2`; route is `quiver_tracking` inside the app.

## 8. Non-goals (v1)

- Daily Analysis / TF signals on the tracking OP
- Matching published CAGR
- Quiver API from Wv2
- Login scrape of Quantbase
- Broker Gateway `order_write` / dummy_sim as the tracking fill path (paper confirm is enough)
- WUT PBR of the PDF book
- Auto-activating a second Congress copy-book from reconstructed filings

## 9. Grill / ADR follow-ups

- In-place membership mutation vs successor (section 7).
- Whether DM Skim reconstruction appears as a third column (PDF / tracking OP / filing-reconstruct).
- Telegram ingest: Cromwell attachment → Wv2 internal POST, vs Wv2 watching a drop folder.

## 10. Acceptance (epic)

- [ ] `GET /wv2/quiver_tracking` renders ops-shell-styled desk, not `/operations`
- [ ] Empty paper tracking OP exists; TF Active books unchanged
- [ ] Upload PDF (web) stores under `storage/reports/quiver_tracking/` and appears in a list like DARs
- [ ] Parse + diff mints gap tasks; confirming them updates Books/positions/journals
- [ ] Missing parquet names enqueue DM pull; coverage visible on the desk
- [ ] Daily Analysis still skips the tracking OP
- [ ] Telegram upload is an alternate, not the only path
- [ ] No Quiver API key on Wv2
