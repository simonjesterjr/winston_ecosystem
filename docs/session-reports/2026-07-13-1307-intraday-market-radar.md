# Session Report — Intraday Market Radar (Live Quotes)

**Date:** 2026-07-13
**Time:** ~12:40–13:07 MDT
**Duration:** ~25m
**Project:** sawtooth Winston ecosystem (Wv2 + Cromwell MCP/skills)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `winston_v2` main; `ecosystem` main (both tracking origin/main)
**Model:** Grok (xAI)
**Operator:** John

---

## 1. Goal & Outcome

**Stated goal:** Replace EOD-parquet-only market snapshot messages with an intraday “weather radar”: active portfolio symbols, live internet prices, compare to prior close + ATR_17, list movers for attention.

**Outcome:** Delivered

**One-line summary:** `wv2_market_snapshot` is now a live-quote ATR radar for Active portfolio Books (not yesterday’s closes dressed up as session news).

---

## 2. Work Completed

- Upgraded `MarketSnapshotService` to combine:
  - **Symbols** from Active Wv2 portfolios
  - **Prior close + atr_17** from DM parquet (boundary reference only)
  - **Current price / session OHLV** from internet (Yahoo chart API via `LiveQuoteFetcher`)
- Added ATR status classification: `quiet` | `testing` (≥0.75×) | `breach_up` / `breach_down` (≥1.0×)
- Parallel quote fetch (8 threads); omit failed/absurd quotes
- Updated MCP tool description, Cromwell skill, heartbeat skill, cron job messages, interface docs
- Specs (7 examples) green; live HTTP smoke on `:3002/internal/market_snapshot`
- Reseeded Cromwell workspace; rebuilt/recreated `winston_mcp` + restarted bot

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `winston_v2/app/services/live_quote_fetcher.rb` | added | Yahoo chart OHL(c)V; nil on failure |
| `winston_v2/app/services/market_snapshot_service.rb` | modified | Radar payload: symbols, movers, summary |
| `winston_v2/app/controllers/internal_controller.rb` | modified | Returns service hash directly |
| `winston_v2/spec/services/live_quote_fetcher_spec.rb` | added | Unit tests (stubbed HTTP) |
| `winston_v2/spec/services/market_snapshot_service_spec.rb` | added | Unit tests (fixture parquet + stubbed quotes) |
| `ai/mcp_winston/mcp_winston/server.py` | modified | Tool description (workspace path; **not in a monolith git repo**) |
| `ecosystem/ai/skills/winston-market-snapshot/SKILL.md` | modified | Live radar playbook |
| `ecosystem/ai/skills/winston-heartbeat/SKILL.md` | modified | Snapshot message guidance |
| `ecosystem/ai/schedule/cromwell-cron.json` | modified | Open + hourly prompts |
| `ecosystem/ai/schedule/README.md` | modified | Marked Phase D-style radar done |
| `ecosystem/interfaces/winston-mcp-tools.md` | modified | Tool surface note |

### Commits

- `winston_v2` `424b94f` — feat(snapshot): live internet quotes vs parquet ATR for market radar
- `ecosystem` `5d0d78a` — docs: live market radar skill, cron, and follow-up tickets

### Branch / PR state at sign-off

- Branch: `main` on `winston_v2` and `ecosystem` — clean after wrap push
- Pushed: yes → `origin/main`
- PR: not opened (direct to main)

---

## 4. Decisions Made

### Decision 1: Internet quotes, not EODHD, for live price
- **Choice:** Yahoo Finance chart API (`query1.finance.yahoo.com/v8/finance/chart/{symbol}`) for current price / session OHLV.
- **Why:** Operator explicitly forbade EODHD and stored data for the live leg; same pattern already exists in WUT legacy downloaders; no new API keys.
- **Alternatives considered:** EODHD delayed quotes (skill Phase D note); Alpha Vantage; skip live entirely.
- **Reversibility:** easy — swap `LiveQuoteFetcher` backend.
- **Promote to ADR?** no — focusing tool, not architecture.

### Decision 2: Keep prior close + ATR from DM parquet
- **Choice:** Boundary reference remains Winston EOD Standard parquet (`atr_17`, last close).
- **Why:** ATR is a derivative we own; live quote is only the “where are we now” leg.
- **Alternatives considered:** Yahoo previousClose for both legs (would diverge from Winston ATR methodology).
- **Reversibility:** easy.
- **Promote to ADR?** no.

### Decision 3: Best-effort omit, not error, when quote fails
- **Choice:** Symbols without a usable live quote are omitted; absurd price vs session range or >8× ATR discarded.
- **Why:** Radar should not invent or scream on bad tickers (e.g. RGI meta mismatch).
- **Alternatives considered:** Return errors per symbol; force EOD fallback as “current”.
- **Reversibility:** easy.
- **Promote to ADR?** no.

---

## 5. Insights Surfaced

- Prior hourly Telegram posts were correctly calling `wv2_market_snapshot` but the tool only had EOD parquet — so “session” messages were weather reports for yesterday.
- ~47 unique symbols on Active Books produced a dense movers list; many “breaches” on small-ATR ETFs are noise for a team focusing tool.
- Some parquet last bars still dated `2026-07-02` while others are `2026-07-10` — live price can be fresh while the ATR boundary is stale.
- `ai/mcp_winston` is outside every monolith git repo; skill/source of truth for skills is `ecosystem/ai`, but MCP Python lives under workspace `ai/` only (image COPY at build time).

---

## 6. Issues & Tickets

### Resolved this session
- Intraday snapshot used EOD parquet only — fixed with live quote + ATR comparison.

### Deferred
- **Active Book sprawl / noise** — See ticket [`docs/tickets/2026-07-13-market-radar-core-portfolio-scope.md`](../tickets/2026-07-13-market-radar-core-portfolio-scope.md).
- **Stale prior-close for some symbols** — See ticket [`docs/tickets/2026-07-13-stale-parquet-prior-close-active-symbols.md`](../tickets/2026-07-13-stale-parquet-prior-close-active-symbols.md).
- **MCP source not in git** — See ticket [`docs/tickets/2026-07-13-mcp-winston-source-git-home.md`](../tickets/2026-07-13-mcp-winston-source-git-home.md).
- **Observe hourly Telegram with live radar** — Linked into existing ticket [`docs/tickets/2026-07-13-observe-cromwell-market-snapshot-hourlies.md`](../tickets/2026-07-13-observe-cromwell-market-snapshot-hourlies.md) (not re-filed).
- **podman-compose recreate fragility** — Operational note only (manual `podman run` recovery); no ticket unless it recurs.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Unit specs | `bundle exec rspec spec/services/live_quote_fetcher_spec.rb spec/services/market_snapshot_service_spec.rb` (in `winston_v2` container) | ✅ 7/7 |
| Live service | `MarketSnapshotService.call` via rails runner | ✅ 47 symbols, movers ranked |
| HTTP | `GET :3002/internal/market_snapshot` | ✅ `source: live_quote_plus_parquet_atr` |
| MCP tool text | `list_tools` inside `winston_mcp` | ✅ “Intraday attention radar…” |
| Scheduled Telegram post | Natural hourly cron | ⚠️ not waited for; skill + cron reseeded |

**Test command(s):**

```bash
./bin/compose exec -T winston_v2 bundle exec rspec \
  spec/services/live_quote_fetcher_spec.rb \
  spec/services/market_snapshot_service_spec.rb --format documentation
curl -sS http://127.0.0.1:3002/internal/market_snapshot | head
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** none new (uses existing `httparty`, DuckDB, parquet mount)
- **Services:** `winston_v2` (code live); `winston_mcp` recreated from `localhost/sawtooth_winston_mcp:latest`; `nanobot_cromwell` recreated; Cromwell workspace reseeded via `bin/seed-cromwell-workspace`
- **Migrations:** none
- **Outbound network:** Wv2 container can reach Yahoo chart API

---

## 9. Risks & Technical Debt

- Yahoo unauthenticated endpoints can rate-limit or change shape; fetcher already fails soft.
- Sequential DuckDB opens per symbol for EOD bar (quotes are parallel; parquet load is not) — fine at ~50 symbols, not for hundreds.
- Dense movers list may spam Sawtooth Main until scope is narrowed or quiet-only messaging is preferred on noisy days.
- MCP description change lives outside monolith git.

---

## 10. Open Questions

- **Should radar limit to a named Active subset (e.g. “core” portfolios) vs all Active Books?** — needs operator preference; blocks noise control.
- **Where should `ai/mcp_winston` be versioned long-term?** — needs repo home decision; blocks durable MCP source control.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Feature live and verified; wrap in progress (report → follow-ups → commits).
- **Next concrete step:** Commit `winston_v2` + `ecosystem`; decide follow-up tickets for scope/noise and MCP git home; optional observe next hourly Telegram post.
- **Files to read first:**
  1. `winston_v2/app/services/market_snapshot_service.rb`
  2. `winston_v2/app/services/live_quote_fetcher.rb`
  3. `ecosystem/ai/skills/winston-market-snapshot/SKILL.md`

---

## 12. Stakeholder Communications

- Team already receives hourly radar on Sawtooth Main; next posts should list **movers with prev → now + ATR**, not full EOD dump. No separate stakeholder email required.

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report (this doc)
- **What worked well:** Yahoo chart API available from container; thin service + MCP proxy kept work in Wv2.
- **Friction points:** podman-compose recreate of `winston_mcp`/`nanobot_cromwell` failed (dependent containers / name-in-use / volume path TypeError); recovered with explicit `podman rm -f` + `podman run` matching compose env/volumes.
- **Subagent usage:** none

---

## 14. Follow-up Actions

- [ ] Core portfolio radar scope — ticket: [`docs/tickets/2026-07-13-market-radar-core-portfolio-scope.md`](../tickets/2026-07-13-market-radar-core-portfolio-scope.md)
- [ ] Stale parquet prior close — ticket: [`docs/tickets/2026-07-13-stale-parquet-prior-close-active-symbols.md`](../tickets/2026-07-13-stale-parquet-prior-close-active-symbols.md)
- [ ] MCP source git home — ticket: [`docs/tickets/2026-07-13-mcp-winston-source-git-home.md`](../tickets/2026-07-13-mcp-winston-source-git-home.md)
- [ ] Observe hourlies (live movers format) — existing ticket: [`docs/tickets/2026-07-13-observe-cromwell-market-snapshot-hourlies.md`](../tickets/2026-07-13-observe-cromwell-market-snapshot-hourlies.md)

---

## 15. Appendix (optional)

### Sample mover shape (smoke)

```
DBA   prev=26.74  → 27.73  ATR 0.25   +3.94× breach_up
COMB  prev=24.06  → 25.14  ATR 0.30   +3.55× breach_up
FXI   prev=31.91  → 33.45  ATR 0.56   +2.73× breach_up
BIB   prev=106.84 → 99.16  ATR 3.29   -2.33× breach_down
```

### Status thresholds

- testing: `|move|/atr >= 0.75`
- breach: `|move|/atr >= 1.0`
- discard: `|atr_multiple| > 8` or price absurdly outside session high/low band
