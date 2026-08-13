# Session Report — Hourly market snapshot: shuffle + 3 movers via Sidekiq

**Date:** 2026-08-13
**Time:** ~12:00–12:48 MDT
**Duration:** ~48m
**Project:** sawtooth Winston ecosystem (Wv2 + ecosystem MCP/skill)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on `winston_v2` and `ecosystem` (started from each repo’s `origin/main`)
**Model:** Grok 4.6
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Stop the hourly Telegram market snapshot from always walking the same alphanumeric names (AAAU / AAL / AAPL). Shuffle the market population each run, live-evaluate until 3 non-quiet markets, do those evaluations asynchronously on Sidekiq. Leave the rest of the message and the ATR evaluations alone.

**Outcome:** Delivered (Wv2 service + Sidekiq job; specs green; live compose smoke showed 3 shuffled movers). MCP image not rebuilt.

**One-line summary:** `wv2_market_snapshot` now shuffles Active Operational Portfolio books and Sidekiq-evaluates live quotes until 3 non-quiet names, so Cromwell can no longer truncate onto AAAU / AAL / AAPL.

---

## 2. Work Completed

- Confirmed root cause: `MarketSnapshotService#resolved_symbols` used `.uniq.sort`; the full-symbol payload was truncated, so Cromwell always narrated the A-head of the list.
- Shuffle the Active-book population every call (optional `all_portfolios` still supported).
- Live-evaluate in batches of 8 until **3** `testing` / `breach_up` / `breach_down` rows, or the population is exhausted.
- Per-symbol `MarketSnapshotSymbolJob` + Redis (or in-memory) `MarketSnapshotScan` collector; HTTP request waits and falls back inline if Sidekiq/Redis fails.
- Payload `symbols` / `movers` now contain **at most those 3**; quiet scans stay in `summary`.
- MCP tool marked long-running (90s timeout) and description updated; skill + interface one-liner updated.
- Restarted `winston_v2_sidekiq` so the new job class loads.
- Hand-updated the live Cromwell workspace skill copy (SOT remains `ecosystem/ai/skills/`).

---

## 3. Code Delivered

### Files changed (this session — intended commit set)

#### winston_v2

| File | Change | Notes |
|------|--------|-------|
| `app/services/market_snapshot_service.rb` | modified | shuffle, early-stop, Sidekiq orchestrate, movers-only payload |
| `app/services/market_snapshot_scan.rb` | added | Redis + MemoryStore collector |
| `app/jobs/market_snapshot_symbol_job.rb` | added | one live evaluation; always records |
| `app/controllers/internal_controller.rb` | modified | comment on shuffle / 3-mover scan |
| `spec/services/market_snapshot_service_spec.rb` | modified | quiet omit, shuffle, stop-at-3 |
| `spec/services/market_snapshot_scan_spec.rb` | added | MemoryStore complete / wait |
| `spec/services/market_snapshot_service_async_spec.rb` | added | inline-adapter job path |
| `spec/jobs/market_snapshot_symbol_job_spec.rb` | added | record + exception → omitted |

**Do not commit leftover dirty files from other sessions:** `app/views/operations/desk_workflows/_actions.html.erb`, `app/services/operations/exit_at_stop_service.rb`, `spec/services/operations/exit_at_stop_service_spec.rb`, `docs/session-reports/2026-08-03-1013-desk-workflow-exit-at-stop.md`.

#### ecosystem

| File | Change | Notes |
|------|--------|-------|
| `ai/mcp/mcp_winston/server.py` | modified | tool description + 90s GET timeout |
| `ai/mcp/mcp_winston/tools_schema.py` | modified | `wv2_market_snapshot` long-running 90s |
| `ai/skills/winston-market-snapshot/SKILL.md` | modified | shuffle + 3-mover contract |
| `interfaces/winston-mcp-tools.md` | modified | convenience-tool one-liner |
| `docs/session-reports/2026-08-13-1248-hourly-snapshot-shuffle-movers.md` | added | this report |

**Do not commit other dirty ecosystem tickets/analysis** left from prior sessions.

#### runtime (not a git repo)

| File | Change | Notes |
|------|--------|-------|
| `ai/data/cromwell-bot/workspace/skills/winston-market-snapshot/SKILL.md` | modified | live Cromwell copy; re-seed from ecosystem SOT later |

### Commits

- `winston_v2` `a6c7b2a` — feat(radar): shuffle snapshot population and stop at 3 movers
- `ecosystem` — this wrap commit (docs + MCP/skill)

### Branch / PR state at sign-off

- Branch: `main` on `winston_v2` and `ecosystem`
- Pushed: pending wrap push
- PR: not opened (work is on `main`)

---

## 4. Decisions Made

### Decision 1: Population = Active Operational Portfolio books (existing source)
- **Choice:** Keep `Portfolio.where(active: true)` books as the shuffle universe (`all_portfolios` still expands to all portfolios). Do not switch to every `Market` / parquet file.
- **Why:** Operator said “one small change”; the AAAU/AAL/AAPL bug is fully explained by `.sort` on the existing list. Widening the universe is a product call (and collides with the open radar-scope ticket).
- **Alternatives considered:** All `Market` rows; all names with DM parquet; a tagged “core” subset.
- **Reversibility:** easy — `resolved_symbols` is one method.
- **Promote to ADR?** no

### Decision 2: Return at most 3 movers; omit quiet names from `symbols`
- **Choice:** `symbols` == `movers` (≤3). Quiet/omitted counts live only in `summary`.
- **Why:** Cromwell dumps whatever is in `symbols`. Returning scanned quiet names would recreate the Telegram alphabet dump even after shuffle.
- **Alternatives considered:** Return all evaluated rows; return a short quiet sample.
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 3: Sidekiq per-symbol jobs; request waits; inline fallback
- **Choice:** Batch-enqueue `MarketSnapshotSymbolJob`, wait on Redis/MemoryStore, fall back to in-process scan if the worker or Redis fails.
- **Why:** Operator asked for async Sidekiq evaluations; MCP/cron still needs a one-shot payload (`wv2_market_snapshot` with `{}`).
- **Alternatives considered:** One parent job only; fire-and-forget + poll tool (would break cron playbook).
- **Reversibility:** easy
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- The hourly “always AAAU / AAL / AAPL” complaint was not Cromwell picking favorites. It was **A-sort + payload truncation**. AAL at −0.3× ATR is still classified `quiet` (`testing` starts at 0.75×).
- Live Active-book population was **70** names at smoke time (was ~47 in the July radar ticket).
- `defined?(MarketSnapshotSymbolJob)` is unsafe as a Sidekiq-availability check under Zeitwerk — it can be `nil` before autoload and force the inline path forever.

---

## 6. Issues & Tickets

### Resolved this session
- Hourly snapshot always starts at AAAU / AAL / AAPL — fixed in `MarketSnapshotService` (shuffle + early-stop + movers-only payload).

### Deferred
- Rebuild `winston_mcp` — [`2026-08-13-rebuild-winston-mcp-snapshot-timeout.md`](../tickets/2026-08-13-rebuild-winston-mcp-snapshot-timeout.md)
- Official `bin/seed-cromwell-workspace` — [`2026-08-13-reseed-cromwell-snapshot-skill.md`](../tickets/2026-08-13-reseed-cromwell-snapshot-skill.md)
- Product rule: Active books vs full parquet — [`2026-08-13-snapshot-universe-active-vs-parquet.md`](../tickets/2026-08-13-snapshot-universe-active-vs-parquet.md); existing [`2026-07-13-market-radar-core-portfolio-scope.md`](../tickets/2026-07-13-market-radar-core-portfolio-scope.md) updated (mover-list length marked partial).
- Observe next natural hourly — [`2026-08-13-observe-shuffled-hourly-snapshot.md`](../tickets/2026-08-13-observe-shuffled-hourly-snapshot.md)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Shuffle / stop-at-3 / quiet omit | host `rspec` (no DB) | ✅ 9/9 |
| Scan collector + job + async path | compose `rspec` | ✅ 12/12 |
| Live `/internal/market_snapshot` | compose curl 2026-08-13 18:12Z | ✅ SHY / SOYB / AXON; scanned 16 of 70; `stopped_early` |
| MCP image / next hourly Telegram | not rebuilt / not observed | ⚠️ |

**Test command(s):**

```bash
# host (no Postgres)
cd winston_v2 && bundle exec rspec \
  spec/services/market_snapshot_service_spec.rb \
  spec/services/market_snapshot_scan_spec.rb

# compose
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 \
  bundle exec rspec \
  spec/services/market_snapshot_service_spec.rb \
  spec/services/market_snapshot_scan_spec.rb \
  spec/services/market_snapshot_service_async_spec.rb \
  spec/jobs/market_snapshot_symbol_job_spec.rb

# live smoke
./bin/compose exec -T winston_v2 curl -sS --max-time 60 \
  http://127.0.0.1:3000/internal/market_snapshot
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None added
- **Services:** `winston_v2_sidekiq` restarted to load `MarketSnapshotSymbolJob`. `winston_v2` bind-mount already had the service.
- **Migrations:** None

---

## 9. Risks & Technical Debt

- If Sidekiq is down, the request falls back inline (same algorithm, request-thread Yahoo). Correct, but slower and can approach Puma’s 60s budget on a fully quiet 70-name scan.
- MCP still has the old 30s client timeout until the image is rebuilt. Smoke finished quickly; a slow Yahoo day could 30s-timeout Cromwell.
- Live Cromwell skill is a hand-edit; next seed from ecosystem SOT will refresh it if the SOT commit landed.

---

## 10. Open Questions

- **Is the shuffle universe Active books, or every market we have parquet for?** — needs answer from: operator; blocks: widening `resolved_symbols`.
- **Did the next hourly Telegram post use 3 shuffled movers and skip the quiet table?** — needs answer from: live observe; blocks: closing the attention-discipline cluster.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Live smoke succeeded (SHY / SOYB / AXON). Sidekiq restarted. Session report written; wrap commit not yet run.
- **Next concrete step:** Follow-up promotion, then commit/push only this session’s files on `winston_v2` and `ecosystem`. Optionally rebuild `winston_mcp`.
- **Files to read first:**
  1. `winston_v2/app/services/market_snapshot_service.rb`
  2. `winston_v2/app/jobs/market_snapshot_symbol_job.rb`
  3. `winston_v2/app/services/market_snapshot_scan.rb`
  4. `ecosystem/ai/skills/winston-market-snapshot/SKILL.md`

---

## 12. Stakeholder Communications

- _None._ Hourly channel copy is unchanged; only which three names appear should change.

---

## 13. Tools & Workflow Notes

- **Skills used:** `operator-prose`, `session-report`, `wrap` (in progress)
- **What worked well:** Live compose smoke immediately proved the alphabet bug is gone.
- **Friction points:** Host `rspec` cannot use Postgres; Rails specs must run in compose. `winston_mcp` is image-only (no bind mount).
- **Subagent usage:** _None._

---

## 14. Follow-up Actions

- [ ] Rebuild `winston_mcp` — [`2026-08-13-rebuild-winston-mcp-snapshot-timeout.md`](../tickets/2026-08-13-rebuild-winston-mcp-snapshot-timeout.md)
- [ ] Observe next natural hourly — [`2026-08-13-observe-shuffled-hourly-snapshot.md`](../tickets/2026-08-13-observe-shuffled-hourly-snapshot.md)
- [ ] Confirm shuffle universe — [`2026-08-13-snapshot-universe-active-vs-parquet.md`](../tickets/2026-08-13-snapshot-universe-active-vs-parquet.md)
- [ ] Re-seed Cromwell workspace — [`2026-08-13-reseed-cromwell-snapshot-skill.md`](../tickets/2026-08-13-reseed-cromwell-snapshot-skill.md)
- [ ] Existing radar-scope ticket updated (mover-list length partial) — [`2026-07-13-market-radar-core-portfolio-scope.md`](../tickets/2026-07-13-market-radar-core-portfolio-scope.md)

---

## 15. Appendix (optional)

Live smoke (`2026-08-13T18:12:36Z`):

```
source live_quote_plus_parquet_atr
summary: count=16 quiet=13 testing=2 breach_up=1
         omitted=0 population=70 scanned=16 mover_target=3 stopped_early=true
movers: SHY breach_up +1.637; SOYB testing +0.986; AXON testing -0.883
symbols: SHY, SOYB, AXON
```
