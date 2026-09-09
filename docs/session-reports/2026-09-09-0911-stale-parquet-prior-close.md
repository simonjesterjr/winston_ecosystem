# Session Report — Stale parquet prior-close (P1 Done)

**Date:** 2026-09-09
**Time:** ~17:16–17:50 MDT (2026-09-08 work); wrap 09:11 MDT (2026-09-09)
**Duration:** ~35m active
**Project:** sawtooth Winston ecosystem (data_manager + Winston v2 + ecosystem)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `winston_v2` main (`9d01a56` then later `89144ce`); `ecosystem` main (`2635ab2` then later `aaa35ad`)
**Model:** Grok (xAI)
**Operator:** John

---

## 1. Goal & Outcome

**Stated goal:** Close P1 ticket `docs/tickets/2026-07-13-stale-parquet-prior-close-active-symbols.md` (Proposed → Done). Inventory Active Book parquet last-dates, root-cause lag, repair, optional radar age warning.

**Outcome:** Delivered

**One-line summary:** Live Active Book parquet is through 2026-09-08; July mixed last-dates were the after-close skip family (already ADR-012). Radar now canonicalizes aliases and flags a prior close more than one weekday session old.

---

## 2. Work Completed

- Inventoried 9 Active Operational Portfolios, 94 unique books vs completed New York session **2026-09-08**
- Confirmed 93/94 parquet files `max(date)=2026-09-08`; missing folder is `BRK.B` (alias of current `BRK-B`)
- Root-caused July 13 mixed bars (`2026-07-02` vs `2026-07-10`) as the same family as ADR-012 / `SessionCoverageRetryJob`
- Documented repair path: `SessionCoverage.stale_among` + `dm:symbol_registry:acquire_symbols` + `data:reconcile`
- Winston v2 (Wv2) `MarketSnapshotService`: canonicalize `TickerRemap` (BRK.B → BRK-B); `previous_close_stale` when weekday sessions behind > 1
- Updated Cromwell market-snapshot skill + MCP tool note
- Archived ticket as **P1 Done**; refreshed `docs/tickets/INDEX.md`
- Restarted `winston_v2` + `winston_v2_sidekiq`; seeded Cromwell workspace; restarted `nanobot_cromwell`

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `winston_v2/app/services/market_snapshot_service.rb` | modified | Canonicalize symbols; stale prior-close fields on row + summary |
| `winston_v2/spec/services/market_snapshot_service_spec.rb` | modified | Fresh fixture date; stale + BRK.B canonicalize examples |
| `ecosystem/ai/skills/winston-market-snapshot/SKILL.md` | modified | Annotate stale movers; extra quiet line if summary stale |
| `ecosystem/interfaces/winston-mcp-tools.md` | modified | `previous_close_stale` + alias note on `wv2_market_snapshot` |
| `ecosystem/docs/tickets/INDEX.md` | modified | Row → P1 Done, archive path |
| `ecosystem/docs/tickets/2026-07-13-stale-parquet-prior-close-active-symbols.md` | moved | Archived with inventory + repair path |

### Commits

- `winston_v2` `9d01a56` — feat(snapshot): warn when prior-close parquet is more than one session old
- `ecosystem` `2635ab2` — docs: close P1 stale parquet prior-close ticket

Later same-branch commits (other sessions, not this work): Wv2 `89144ce` (Winston Ecosystem View); ecosystem `f62e4dc` / `aaa35ad`.

### Branch / PR state at sign-off

- Branch: `main` on `winston_v2` and `ecosystem` — dirty with **unrelated** WQ / Ecosystem View files (not this session)
- Pushed: **yes** — `9d01a56` and `2635ab2` are ancestors of `origin/main`
- PR: not opened (direct to main)

---

## 4. Decisions Made

### Decision 1: Do not delete the `BRK.B` book
- **Choice:** Canonicalize radar/parquet lookup; leave WQ OP#1372 books as-is.
- **Why:** Executed journal #1331 (0.4576 units) is on market `BRK.B`.
- **Alternatives considered:** Drop the alias book; rewrite journal market_id to `BRK-B`.
- **Reversibility:** easy.
- **Promote to ADR?** no.

### Decision 2: Stale = more than one weekday session behind
- **Choice:** `previous_close_stale` when weekday sessions behind > 1 vs yesterday-weekday (radar prior close, not today’s incomplete print).
- **Why:** Ticket said “>1 session old”; one session of EODHD lag / holiday miss (Labor Day Monday 2026-09-07) should not alarm.
- **Alternatives considered:** Warn on any bar older than `CompletedNySession.date`; copy DM session clock into Wv2.
- **Reversibility:** easy.
- **Promote to ADR?** no.

### Decision 3: Leave SMOKE demand as residual
- **Choice:** Do not filter `/internal/active_markets` this session.
- **Why:** Demand is all portfolios, not Active-only; SMOKE1/2/3 are inactive test books, not Active freshness.
- **Alternatives considered:** Skip `SMOKE*` in DM discover; Active-only demand.
- **Reversibility:** easy.
- **Promote to ADR?** no.

---

## 5. Insights Surfaced

- After-close contract + session-coverage retry already keep Active parquet on the completed session; the July radar bug was that family, not a separate downloader hole.
- Wv2 `active_markets` already canonicalizes; `MarketSnapshotService#resolved_symbols` did not — so `BRK.B` + `BRK-B` both hit the hourly radar until this change (live population 94 → 93).
- `DmParquetPaths.file_for` already remapped storage; live Yahoo fetch on `BRK.B` was the remaining miss.
- Labor Day 2026-09-07 has no print; Friday 2026-09-04 vs Tuesday 2026-09-08 is one weekday session behind under a no-holiday calendar — threshold >1 avoids a false stale flag.

---

## 6. Issues & Tickets

### Resolved this session
- P1 `2026-07-13-stale-parquet-prior-close-active-symbols` — inventory, root cause, repair path, radar warning — archived Done.

### Deferred
- **SMOKE1/2/3 in DM demand** — inactive smoke-test books advertised on `/internal/active_markets`; EODHD returns nothing every sync. Not Active Book lag.
- **WQ dual `BRK.B` / `BRK-B` books** — OP#1372; journal #1331 on `BRK.B`. Radar canonicalizes; book identity not collapsed.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Inventory | DM DuckDB `max(date)` vs `CompletedNySession` for 94 Active books | ✅ 93 at 2026-09-08; `BRK.B` missing folder |
| Demand coverage | `EcosystemDataSyncService.demand_symbols` vs `DataCoverage.latest` | ✅ 113 fresh; SMOKE1/2/3 missing |
| Specs | `bundle exec rspec spec/services/market_snapshot_service_spec.rb spec/services/market_snapshot_service_async_spec.rb spec/jobs/market_snapshot_symbol_job_spec.rb` | ✅ 12 examples, 0 failures |
| Live `evaluate_one("BRK.B")` | rails runner | ✅ symbol `BRK-B`, date 2026-09-08, stale false |
| HTTP radar | `GET :3002/internal/market_snapshot` after compose restart | ✅ population 93, `stale_previous_close=0`, no movers (after close) |

**Test command(s):**

```bash
./bin/compose exec -T winston_v2 bundle exec rspec \
  spec/services/market_snapshot_service_spec.rb \
  spec/services/market_snapshot_service_async_spec.rb \
  spec/jobs/market_snapshot_symbol_job_spec.rb --format documentation
curl -sS http://127.0.0.1:3002/internal/market_snapshot
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** none new
- **Services:** restarted `winston_v2`, `winston_v2_sidekiq`, `nanobot_cromwell`; `bin/seed-cromwell-workspace` (skill copy)
- **Migrations:** none
- **Outbound:** Yahoo chart API from Wv2 container (radar smoke)

---

## 9. Risks & Technical Debt

- Radar `expected_prior_close_date` is UTC yesterday-weekday, not DM `CompletedNySession` (16:00 ET). Fine for 7:30 AM–2:00 PM MT hourlies; after-hours HTTP can show expected=prior weekday while parquet already has today (still `stale=false` because bar ≥ expected).
- Async scan only flags stale among evaluated rows; omitted quote-misses without a row are not in `stale_previous_close_symbols` on the Sidekiq path.
- Unrelated dirty trees on both `main` checkouts (WQ desk / Ecosystem View) — do not mix into this wrap commit.

---

## 10. Open Questions

- **Should Wv2 `/internal/active_markets` drop inactive smoke / test books from DM demand?** — needs answer from: operator; blocks: wasted EODHD calls, not radar correctness.
- **Should WQ collapse `BRK.B` → `BRK-B` on the book and journal #1331?** — needs answer from: operator; blocks: dual-name blotter; capital-sensitive.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Ticket archived; radar live on compose; session commits already on `origin/main` via later WEV wrap. This wrap is the session report + follow-up promotion.
- **Next concrete step:** Operator shortcut on the two deferred items; then commit this report on `ecosystem` `main` and push.
- **Files to read first:**
  1. `ecosystem/docs/tickets/archive/2026-07-13-stale-parquet-prior-close-active-symbols.md`
  2. `winston_v2/app/services/market_snapshot_service.rb`
  3. `ecosystem/ai/skills/winston-market-snapshot/SKILL.md`

---

## 12. Stakeholder Communications

- _None._ Hourly Telegram already uses the radar; stale annotation only appears if a mover’s parquet bar is >1 session old. No separate email.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, wrap, session-report; ponytail (no extra DM rake)
- **What worked well:** live DuckDB + `DataCoverage` inventory answered “is it still stale?” in one runner; ADR-012 work had already repaired the systematic lag.
- **Friction points:** `GET /internal/market_snapshot` times out at 8s while Sidekiq/Yahoo scan runs; 20s curl succeeded. Wv2 `rspec` printed `ActiveRecord::ConnectionNotEstablished` on test DB purge then still ran the 12 examples green.
- **Subagent usage:** none

---

## 14. Follow-up Actions

Wrap promotion **skip all** (2026-09-09): left in this report only; no new tickets/tasks.

- [ ] Decide whether to exclude `SMOKE*` (inactive test books) from DM demand discovery — owner: operator — due: unscheduled
- [ ] Decide whether to collapse WQ OP#1372 `BRK.B` book/journal #1331 onto `BRK-B` — owner: operator — due: unscheduled

---

## 15. Appendix (optional)

Inventory 2026-09-08 after NY close:

```
session=2026-09-08 demand=116 FRESH=113 STALE=0 MISSING=SMOKE1,SMOKE2,SMOKE3
Active books=94 parquet max(date)=2026-09-08 ×93 missing=BRK.B
Live snapshot after restart: population=93 stale=0 expected=2026-09-07 movers=[]
```

Repair (when a real name lags):

```bash
./bin/compose exec -T data_manager bin/rails runner '
session = CompletedNySession.date
puts SessionCoverage.stale_among(EcosystemDataSyncService.demand_symbols, session).inspect
'
```
