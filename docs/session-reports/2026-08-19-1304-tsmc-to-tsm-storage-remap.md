# Session Report — TSMC → TSM in-place storage remap

**Date:** 2026-08-19
**Time:** ~09:00–13:04 MDT
**Duration:** ~4h
**Project:** sawtooth Winston ecosystem — data_manager (DM), winston_v2 (Wv2), winston_unit_test (WUT), live DBs, `portfolio_configs/`
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on `data_manager`, `ecosystem` (Wv2/WUT code not changed this session)
**Model:** Grok 4.6
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Morning “what’s next,” then explain why Schwab has no TSMC listing while Winston has End of Day (EOD) data; after the operator confirmed Tuesday’s paper drafts, remap storage **TSMC → TSM** the way RGI → RSPN was done.

**Outcome:** Delivered

**One-line summary:** Winston’s TSMC book was always the NYSE ADR **TSM**; we now store and book **TSM**. Blue paper lot #587 is the same short 6 @ 418.13, now labeled TSM.

---

## 2. Work Completed

- Morning live check: Tuesday unattended EOD worked (parquet latest **2026-08-18**; five paper enters pending). Operator later confirmed all drafts, including Blue TSMC → journal **940** / lot **#587**.
- Explained TSMC vs Schwab: nickname vs NYSE ticker **TSM** (not TWSE 2330).
- Made **TSM** canonical storage in `TickerRemap` (same pattern as RGI → RSPN).
- Live remap: consumers keep the same `market_id`; DM predecessor TSMC row kept; stale duplicate TSM retired in WUT; TSM parquet refreshed through 2026-08-18.
- Rewrote Portfolio Correlation Score (PCS) snapshots that still keyed Blue books as TSMC (33 Wv2, 38 WUT).
- Updated Blue `portfolio_configs` membership/seed arrays to TSM; descriptions still say the company “TSMC”.
- Walkthrough for operator click-through (Schwab → ops shell → inspect → DM curl → WUT).

---

## 3. Code Delivered

### Files changed

#### data_manager

| File | Change | Notes |
|------|--------|-------|
| `app/services/ticker_remap.rb` | modified | `CANONICAL_STORAGE["TSMC"] = "TSM"`; comments: NYSE ADR, not TWSE 2330 |
| `app/services/data_acquisition_service.rb` | modified | Stamp every canonical predecessor on acquire; `rename_date` |
| `spec/services/ticker_remap_spec.rb` | modified | TSMC remaps storage; `remapped?` true |
| `lib/tasks/symbol_registry.rake` | modified | Seed list AMAT, **TSM**, GLTR, CPER |

#### ecosystem

| File | Change | Notes |
|------|--------|-------|
| `docs/business-context/winston-market-suitability.md` | modified | `import_seeds` example TSM |
| `ai/skills/winston-ad-hoc-fill/SKILL.md` | modified | Example fill TSM |
| `docs/session-reports/2026-08-19-1304-tsmc-to-tsm-storage-remap.md` | added | This report |

#### portfolio_configs (not a git repo)

| File | Change |
|------|--------|
| `portfolio-blue.json`, sidecar, `registry.json`, `portfolio-blue-s4-p2pack.json`, `portfolio-blue-pbr62.json`, `portfolio-blue-pbr80.json`, `portfolio-blue-pbr336.json`, `correlation-litmus-latest.json` | Quoted `"TSMC"` tickers → `"TSM"`; prose “anchored on TSMC” kept |

#### Live / volume (not in git)

| Artifact | Change |
|----------|--------|
| DM Market #2 TSMC | Predecessor: `renamed_to TSM`; parquet folder kept |
| DM Market #2156 TSM | Live coverage 2019-06-19..2026-08-18, 1801 bars; `list_source=seed` |
| `/app/data/markets/TSM/` | Overwritten with live TSMC parquet, then acquire TSMC→TSM |
| Wv2 Market #31 | `TSMC` → `TSM`; same id; `dm_coverages.parquet_path` → `/dm_data/markets/TSM/bars.parquet` |
| Wv2 Position #587 / Journal #940 | Still `market_id=31`; symbol now TSM |
| WUT Market #2248 TSM | Deleted (no books; coverage only) |
| WUT Market #283 | `TSMC` → `TSM`; books/journals/positions kept |
| Wv2 PCS snapshots | 33 Blue rows TSMC→TSM in `symbols` / `books_key` / pair keys |
| WUT PCS snapshots | 38 rows same rewrite |

**Not this session (dirty on other trees — do not mix):** Wv2 Confirmation Intake / mid-month scoreboard files; ecosystem `CONTEXT.md`, L1 tickets, `interfaces/`, `ai/schedule/`, `ai/mcp/`.

### Commits

- **data_manager** `f97d09e` — `feat(dm): store TSMC as NYSE ADR TSM (RGI-style remap)`
- **ecosystem** _(this wrap)_ — docs: TSMC→TSM session report + tickets

### Branch / PR state at sign-off

- Branch: `main` on DM / ecosystem
- Pushed: yes (wrap)
- PR: not opened (direct `main`, same as prior wraps)

---

## 4. Decisions Made

### Decision 1: In-place storage remap TSMC → TSM
- **Choice:** Canonical storage **TSM**; keep consumer `market_id`s; DM keeps TSMC as predecessor (RGI pattern).
- **Why:** Same NYSE ADR. Schwab/NYSE ticker is TSM. TSMC was a Winston book nickname. TWSE 2330 is a different instrument.
- **Alternatives considered:** Keep TSMC storage + vendor alias only (status quo — desk cannot find the name at Schwab); extra-modal packaging without rename (wrong — this is the same US listing).
- **Reversibility:** easy (rename markets back) but parquet path is now TSM.
- **Promote to ADR?** no — `TickerRemap` is enough (same as RGI).

### Decision 2: Retire unused WUT TSM #2248, keep live #283
- **Choice:** Delete duplicate Market #2248 (0 books) so unique `trading_symbol` can move onto #283.
- **Why:** WUT unique index on `trading_symbol`; #283 holds 5,048 lab positions and the Blue book.
- **Alternatives considered:** Point books at #2248 (not in-place; would break `market_id` FKs).
- **Reversibility:** costly (would need to re-create #2248).
- **Promote to ADR?** no

### Decision 3: Keep TSMC parquet folder as predecessor
- **Choice:** Leave `/data/markets/TSMC/` on disk like RGI.
- **Why:** RGI archive still exists; consumers no longer have a TSMC Market so Daily Analysis will not score it.
- **Alternatives considered:** Delete TSMC folder (would make `data_ready?("TSMC")` false; cleaner, not required for RGI parity).
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 4: Rewrite historical PCS snapshots
- **Choice:** Replace TSMC with TSM in snapshot `symbols`, `books_key`, and pair keys (33 Wv2, 38 WUT).
- **Why:** PCS identity is Books membership. Leaving TSMC keys would orphan Blue’s series after the book rename (`resolve_for` primary lookup is `books_key`).
- **Alternatives considered:** Seed-name fallback only (works for latest, breaks heat pair matching).
- **Reversibility:** easy (rewrite back).
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- TSMC vs TSM is **not** extra-modal fulfillment. It is a nickname vs listing ticker. EODHD was already fetching TSM (`list_metadata.eodhd_symbol`).
- DM had **two** TSM identities: live seed parquet under TSMC (#2) and a stale TSM folder (#2156, last bar 2026-07-21). Consumers read the TSMC path. After remap, TSM path must be current **before** renaming consumer markets or they would load July tape.
- `request_consumer_sync` canonicalizes first: POST `{"symbols":["TSMC"]}` returns `"requested_symbols":["TSM"]`.
- `ParquetLookbackLoader.data_ready?("TSMC")` is still true because the predecessor parquet folder remains. Harmless while no Market is named TSMC.
- Tuesday’s unattended EOD (the 2026-08-18 observe ticket) **did** run: coverage latest 2026-08-18, five paper enters, operator confirmed including Blue TSM (then still labeled TSMC).

---

## 6. Issues & Tickets

### Resolved this session
- Schwab “missing TSMC” — not a data gap; storage nickname. Remap delivered.

### Deferred
- Operator click-through of the TSM walkthrough — See: [`docs/tickets/2026-08-19-tsm-remap-operator-clickthrough.md`](../tickets/2026-08-19-tsm-remap-operator-clickthrough.md)
- Tonight’s unattended **Wednesday 2026-08-19** EOD: DAR should name **TSM** — See: [`docs/tickets/2026-08-19-observe-wednesday-eod-tsm.md`](../tickets/2026-08-19-observe-wednesday-eod-tsm.md)
- Rust lots #565 GOOGL / #566 RXT booked at Tuesday **close** — See: [`docs/tickets/2026-08-19-googl-rxt-correct-fill-if-open-gaps.md`](../tickets/2026-08-19-googl-rxt-correct-fill-if-open-gaps.md)
- Leftover TSMC parquet makes `data_ready?("TSMC")` true — See: [`docs/tickets/2026-08-19-delete-predecessor-tsmc-parquet.md`](../tickets/2026-08-19-delete-predecessor-tsmc-parquet.md)
- Tuesday unattended EOD observe — **Done**, archived [`docs/tickets/archive/2026-08-18-observe-tuesday-unattended-eod-cycle.md`](../tickets/archive/2026-08-18-observe-tuesday-unattended-eod-cycle.md)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| `TickerRemap` specs | `bundle exec rspec spec/services/ticker_remap_spec.rb` in DM | ✅ 6 examples, 0 failures (inotify noise on `db:test:prepare` only) |
| Acquire TSMC → TSM | `POST /api/v1/triggers/request_consumer_sync` `{"symbols":["TSMC"]}` | ✅ `requested_symbols: ["TSM"]`, 1801 bars, no failures |
| Wv2 Market #31 / lot #587 / journal #940 | SQL + rails runner + ingest | ✅ symbol TSM; same ids; path `/dm_data/markets/TSM/bars.parquet` |
| TSM session bar 2026-08-18 | `ParquetLookbackLoader.session_bar_for("TSM", 2026-08-18)` | ✅ O=417.00 H=419.63 L=410.77 C=413.41 |
| WUT Market #283 | SQL + `DmParquetIngester.ingest(["TSM"])` | ✅ TSM; 1 book; 5048 positions; 78062 journals; #2248 gone |
| PCS Blue `resolve_for(#381)` | rails runner | ✅ snapshot 359, `books_key` includes TSM, 0 TSMC left |
| Operator UI / Schwab / Tailscale | not exercised this session | ⚠️ walkthrough written, not click-verified |
| Wednesday unattended EOD | not yet | ⚠️ |

**Test command(s):**

```bash
podman exec data_manager bash -lc 'cd /app && bundle exec rspec spec/services/ticker_remap_spec.rb --format documentation'
curl -s -X POST http://localhost:3001/api/v1/triggers/request_consumer_sync \
  -H 'Content-Type: application/json' \
  -d '{"symbols":["TSMC"],"consumer":"manual"}'
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None
- **Services:** existing compose; restarted `data_manager` + `data_manager_sidekiq` to load `TickerRemap`
- **Migrations:** None
- **Data:** paper OP #381 journal 940 executed, position 587; DM/WUT/Wv2 market identity TSM; PCS snapshots rewritten; `portfolio_configs` JSON on disk (no git)

---

## 9. Risks & Technical Debt

- Predecessor `/data/markets/TSMC/` still makes `data_ready?("TSMC")` true if any caller still passes that string.
- Unrelated dirty trees (Wv2 L1 intake, ecosystem L1 tickets, MMS) must not land in this wrap commit.
- `portfolio_configs/` is not a git repo — Blue TSM membership lives only on disk.
- Rust #565/#566 still booked at Tuesday close, not Wednesday open (prior session).

---

## 10. Open Questions

- **Did 2026-08-19 GOOGL/RXT opens gap vs 340.19 / 3.51?** — needs answer from: parquet after close / operator; blocks: honest T+1 fills on lots #565/#566.
- **Did the operator complete the TSM click-through?** — needs answer from: operator; blocks: nothing (code path already green).

---

## 11. Handoff & Resume Notes

- **Where I left off:** Remap live; walkthrough given; wrap report written; commit pending follow-up promotion.
- **Next concrete step:** Operator: hard-refresh `/wv2/operations`, confirm Blue #381 shows **TSM** short 6. After close: Wednesday DAR should say TSM.
- **Files to read first:**
  1. `data_manager/app/services/ticker_remap.rb`
  2. `ecosystem/docs/session-reports/2026-08-17-1247-rgi-rspn-session-handoff.md` (pattern)
  3. This report

---

## 12. Stakeholder Communications

- _None._ Paper desk only. Schwab research name is TSM; no Telegram send.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, session-report, wrap (in progress)
- **What worked well:** Treating TSMC→TSM as RGI→RSPN (same `market_id`, predecessor registry, consumer ingest after parquet is current).
- **Friction points:** DM `rails runner` / rspec hit host inotify EMFILE; used `psql -i` and HTTP acquire instead. `podman exec` heredoc needs `-i` or SQL is silently dropped.
- **Subagent usage:** _None._

---

## 14. Follow-up Actions

- [ ] Operator click-through: Schwab TSM, ops shell Blue #381, signal inspect `symbol=TSM&as_of=2026-08-18`, WUT portfolio 7 — See: [`docs/tickets/2026-08-19-tsm-remap-operator-clickthrough.md`](../tickets/2026-08-19-tsm-remap-operator-clickthrough.md)
- [ ] Observe Wednesday 2026-08-19 unattended EOD; DAR/tasks must say **TSM** — See: [`docs/tickets/2026-08-19-observe-wednesday-eod-tsm.md`](../tickets/2026-08-19-observe-wednesday-eod-tsm.md)
- [ ] Compare GOOGL/RXT 2026-08-19 open vs lots #565/#566; correct-fill if gap matters — See: [`docs/tickets/2026-08-19-googl-rxt-correct-fill-if-open-gaps.md`](../tickets/2026-08-19-googl-rxt-correct-fill-if-open-gaps.md)
- [ ] Optional: delete leftover TSMC parquet so `data_ready?("TSMC")` is false — See: [`docs/tickets/2026-08-19-delete-predecessor-tsmc-parquet.md`](../tickets/2026-08-19-delete-predecessor-tsmc-parquet.md)

---

## 15. Appendix (optional)

**Wv2 inspect URL:**  
`https://sawtooth-ai.tail944ffb.ts.net/wv2/operations/signal_inspect?portfolio_id=381&symbol=TSM&as_of=2026-08-18`

**Tuesday pending that the operator confirmed (then TSMC renamed):**  
task 710 / journal 940 / Blue #381 — now TSM short 6 @ 418.13 lot 587.

**Acquire response (session):**

```json
{"status":"accepted","consumer":"manual","requested_symbols":["TSM"],"acquired":[{"symbol":"TSM","bars":1801}],"failures":[]}
```
