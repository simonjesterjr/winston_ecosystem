# Session Report — WUT Hang Fix + Responsive Pages ADR

**Date:** 2026-07-09
**Time:** ~07:30–07:45 MDT
**Duration:** ~15m
**Project:** sawtooth Winston ecosystem (WUT + ecosystem)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` (ecosystem + winston_unit_test)
**Model:** Grok
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Diagnose WUT not responding on localhost:3000; fix hang on `/wut/portfolios`; capture responsive-UI rule as ADR.

**Outcome:** Delivered

**One-line summary:** Restored WUT UI responsiveness by removing request-path full-history/activity loads on portfolios, hardened catalog ensure, and accepted ADR-005 for snappy progressive pages across monoliths.

---

## 2. Work Completed

- Diagnosed WUT: container up; bare `:3000` 302 → `/wut/`; app routes hung under Puma overload
- Root-caused `/wut/portfolios`: full parquet history + activities eager-load; concurrent `MarketCatalog.load!` thrash
- Fixed WUT portfolios path and catalog ensure
- Restarted `winston_unit_test` (+ sidekiq earlier); verified snappy responses
- Wrote **ADR-005** (responsive user pages) + glossary/AGENTS cross-links

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `winston_unit_test/app/models/portfolio.rb` | modified | `test_data_date_range` uses DmCoverage / SQL aggregates |
| `winston_unit_test/app/controllers/portfolios_controller.rb` | modified | index includes `markets: :dm_coverage` only |
| `winston_unit_test/app/services/market_catalog.rb` | modified | `ensure_registry!` inserts missing symbols only |
| `winston_unit_test/app/views/portfolios/index.html.erb` | modified | `.size` on loaded association |
| `ecosystem/docs/adr/ADR-005-responsive-user-pages.md` | added | Responsive / progressive UI ADR |
| `ecosystem/CONTEXT.md` | modified | Glossary: **Responsive Page** |
| `ecosystem/AGENTS.md` | modified | ADR index → 001..005 |
| `ecosystem/docs/session-reports/2026-07-09-0745-wut-responsive-pages-adr.md` | added | This report |

### Commits

_Pending at report write; filled by wrap commit step._

### Branch / PR state at sign-off

- Branch: `main` (both repos)
- Pushed: yes (wrap)
- PR: not opened (direct main)

---

## 4. Decisions Made

### Decision 1: Responsive user pages (ADR-005)
- **Choice:** First paint must be snappy; heavy data via Sidekiq, Hotwire progressive hooks, or coverage/aggregate metadata — never full-history on list pages
- **Why:** Operator UI hung under real data volume; synchronous completeness does not scale
- **Alternatives considered:** Sync-complete pages; denormalize all summaries into PG
- **Reversibility:** easy for individual pages; ADR is durable policy
- **Promote to ADR?** Yes — ADR-005 Accepted

### Decision 2: Portfolios date range from coverage, not full_history
- **Choice:** Prefer `DmCoverage` earliest/latest/bar_count; legacy uses SQL MIN/MAX/COUNT
- **Why:** Index only needs overlap summary
- **Reversibility:** easy
- **Promote to ADR?** Covered by ADR-005

---

## 5. Insights Surfaced

- WUT is mounted at **`/wut`** (`RAILS_RELATIVE_URL_ROOT`); bare `/` only redirects — easy to misread as “down”
- Under load, trivial queries appeared ~100–300ms while direct `psql` stayed sub-ms (contention)
- Concurrent bad pages (catalog thrash + positions N+1 on backtest views) can starve the whole Puma process
- Compose `(starting)` health for many services can be cosmetic noise without HTTP healthchecks on Rails services

---

## 6. Issues & Tickets

### Resolved this session
- WUT `/wut/portfolios` hang — fixed request-path data loading

### Deferred
- Portfolio backtest result pages still N+1 on journals/positions (`calculate_win_loss_stats`, positions table partial) — can re-saturate Puma
- Sidekiq `DailyOperationsJob` fails: missing `positions.active_account_id` column (schema drift)
- Other list pages may still call expensive paths; ADR-005 conformance is incremental
- Unrelated untracked ecosystem tickets/reports left uncommitted (not this session)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| `GET /` | curl | ✅ 302 → `/wut/` ~ms |
| `GET /wut/` | curl after restart | ✅ 200 ~0.03–0.4s |
| `GET /wut/portfolios` before fix | curl 45s | ❌ timeout |
| `GET /wut/portfolios` after fix | curl | ✅ 200 ~32ms cold, ~12ms warm |
| Spec suite | not run | ⚠️ |
| Browser manual | operator | assumed after fix |

**Test command(s):**

```bash
curl -sS -m 15 -o /dev/null -w "%{http_code} %{time_total}\n" http://127.0.0.1:3000/wut/portfolios
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None
- **Services:** Restarted `winston_unit_test`, `winston_unit_test_sidekiq` (compose/podman)
- **Migrations:** None

---

## 9. Risks & Technical Debt

- ADR-005 not yet applied to all heavy WUT show/result pages
- Daily ops job schema error may spam Sidekiq retries
- Development Puma with high thread count + verbose SQL logging amplifies contention symptoms

---

## 10. Open Questions

- **Should portfolios show use the same date-range path only, or also Turbo-frame charts?** — product preference; does not block
- **Is `positions.active_account_id` a pending migration or dead code path?** — needs schema audit

---

## 11. Handoff & Resume Notes

- **Where I left off:** ADR-005 filed; WUT portfolios responsive; wrap in progress
- **Next concrete step:** Optionally ticket N+1 on portfolio_backtest_runs positions table; fix DailyOperationsJob column
- **Files to read first:**
  1. `ecosystem/docs/adr/ADR-005-responsive-user-pages.md`
  2. `winston_unit_test/app/models/portfolio.rb`
  3. `winston_unit_test/app/controllers/portfolios_controller.rb`

---

## 12. Stakeholder Communications

- Operators: use `http://localhost:3000/wut/` (not bare `:3000`); portfolios list should be fast again
- Architecture: ADR-005 is binding for human UI routes

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report
- **What worked well:** curl + compose logs + psql volume checks for hang diagnosis
- **Friction points:** compose `ps` wrapper quirks; long `podman logs` under SQL spam
- **Subagent usage:** _None._

---

## 14. Follow-up Actions

- [ ] Ticket: portfolio_backtest_runs positions/journals N+1 — owner: next session — due: when UI hangs again
- [ ] Ticket/fix: DailyOperationsJob `active_account_id` missing — owner: next WUT ops session
- [ ] Optional: Hotwire progressive panels for heavy result pages per ADR-005

---

## 15. Appendix (optional)

**Pre-fix symptoms**

- `HomeController#index` completed once in ~11–59s under load
- Logs: `MarketCatalog#load!` per-symbol BEGIN/COMMIT; journals N+1 from positions table
- Activities for portfolio markets: ~59k rows when wrongly eager-loaded

**Post-fix**

```
portfolios: 200 0.031719s size=32944
portfolios2: 200 0.011934s
```
