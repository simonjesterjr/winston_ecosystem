# Session Report — Close + Successor Rebalance Services

**Date:** 2026-07-17  
**Time:** ~11:30–12:15 MDT  
**Duration:** ~45m  
**Project:** sawtooth Winston ecosystem (cross-monolith)  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `ecosystem` / `winston_v2` — `main`  
**Model:** Grok 4.5 (xAI)  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Implement Close + successor rebalance services (ADR-006 ticket). Keep essential daily-ops demo matrix as wrap-up ticket filing (not expand this ticket).

**Outcome:** Delivered  

**One-line summary:** Operators can formally close an OP series and open a successor A′ (new Books/TS) via domain services, Ops shell, rake, internal API, and MCP — journals stay on A; DA skips closed series.

---

## 2. Work Completed

- Scoped decision: do **not** expand Close+successor into mega “all essential desk functions” ticket; file demo matrix as follow-ups.
- Implemented `Operations::PortfolioCloseService` (paper soft-close; real flat-required; force residue; dry_run).
- Implemented `Operations::PortfolioSuccessorService` (close A + open A′ in one transaction; journals on A; new initial CashEvent).
- Wired internal API, rake, Ops shell (`close_portfolio` / `successor`), MCP tools + reply_text.
- Daily Analysis: `open_series` filter + readiness reason `:closed`.
- Specs 10/10; live disposable smoke #193–#195.
- Ticket marked **Done**; lifecycle + MCP interface docs updated.

---

## 3. Code Delivered

### Files changed (winston_v2)

| File | Change |
|------|--------|
| `app/services/operations/portfolio_close_service.rb` | **added** |
| `app/services/operations/portfolio_successor_service.rb` | **added** |
| `spec/services/operations/portfolio_close_service_spec.rb` | **added** (6 ex) |
| `spec/services/operations/portfolio_successor_service_spec.rb` | **added** (4 ex) |
| `app/controllers/internal_controller.rb` | close + successor actions |
| `config/routes.rb` | POST close / successor |
| `lib/tasks/wv2.rake` | `portfolios:close`, `portfolios:successor` |
| `app/services/operations/ops_shell_chat.rb` | shell verbs + HELP |
| `app/services/operations/portfolio_readiness.rb` | skip `:closed` |
| `app/services/operations/daily_analysis_runner.rb` | `active.open_series` |

### Files changed (ecosystem)

| File | Change |
|------|--------|
| `docs/tickets/2026-07-14-wv2-close-and-successor-rebalance-services.md` | **Done** |
| `docs/business-context/wv2-operational-portfolio-lifecycle.md` | implemented verb table |
| `interfaces/winston-mcp-tools.md` | §6d / §6e |
| `docs/session-reports/2026-07-17-1214-…` | **this report** |
| Demo epic + thin tickets (wrap Step 2) | **added** |

### Host (not in monolith git)

| File | Change |
|------|--------|
| `ai/mcp_winston/mcp_winston/server.py` | `wv2_close_portfolio`, `wv2_successor_portfolio` |
| `ai/mcp_winston/mcp_winston/errors.py` | tool-specific 404/422 guidance |

### Commits

- `winston_v2` `fb9286a` — feat(ops): ADR-006 Close and successor rebalance services  
- `ecosystem` `5edf2eb` — docs(ops): Close/successor Done, demo epic tickets, session report  

### Branch / PR state at sign-off

- `winston_v2` `main` — committed; push this wrap  
- `ecosystem` `main` — committed (session files only; unrelated dirt left unstaged)  
- Host MCP — untracked by monolith gits (rebuild required)  
- PR: not opened (direct main)

---

## 4. Decisions Made

### Decision 1: Keep Close+successor ticket narrow
- **Choice:** Lifecycle only; essential desk functions as separate tickets at wrap.  
- **Why:** Avoid unbounded acceptance; Close is keystone for engaged shape change.  
- **Alternatives considered:** Mega ticket with blotter/LEAP/graphs.  
- **Reversibility:** easy.  
- **Promote to ADR?** no (implements existing ADR-006).  

### Decision 2: Real force = soft-close with residue (not auto-flatten)
- **Choice:** `force=true` allows real close with open positions/drafts; no price invent.  
- **Why:** Force-flatten needs fills; out of scope.  
- **Reversibility:** easy (later force-flatten ticket).  

### Decision 3: Shell terminology split
- **Choice:** `exit`/`close` = position; `close_portfolio` = series.  
- **Why:** Avoid ADR-006 vs desk verb collision.  

### Decision 4: Successor capital defaults to source capital_base
- **Choice:** New initial CashEvent; override via `initial_capital`.  
- **Why:** New series narrative; journals never copy.  

---

## 5. Insights Surfaced

- Preflight must use Close `dry_run` — calling Close twice would mutate before successor create.  
- Successor close+create should be one DB transaction so failed A′ does not leave A closed.  
- Host MCP still outside git; image rebuild required for Telegram tool list.  
- Disposable smoke left OPs #193–#195 closed in live DB (harmless archive).

---

## 6. Issues & Tickets

### Resolved this session
- Close + successor services — `docs/tickets/2026-07-14-wv2-close-and-successor-rebalance-services.md` **Done**

### Deferred / already tracked
- Capital Activation — See: `docs/tickets/2026-07-09-capital-activation-mcp-telegram.md`  
- Host MCP git-home — See: `docs/tickets/2026-07-13-mcp-winston-source-git-home.md`  
- Version root compose.yml — See: `docs/tickets/2026-07-17-version-workspace-compose-yml.md`  
- Reverse smoke cash Orange/Rust — See: `docs/tickets/2026-07-17-reverse-session-smoke-cash-events.md`  

### Filed this wrap (demo epic matrix)
- See §14 and new tickets under `docs/tickets/2026-07-17-ops-daily-*`

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Close + successor services | rspec 10 ex | ✅ |
| Live disposable smoke | rails runner #193–#195 | ✅ |
| Readiness skip closed | rails runner | ✅ |
| Ops shell help + already_closed | rails runner | ✅ |
| MCP Telegram live | image rebuild not run this session | ⚠️ |

**Test command(s):**

```bash
bin/compose exec -T winston_v2 bash -lc \
  'TEST_DB_HOST=wv2_postgres TEST_DB_USER=sawtooth TEST_DB_PASSWORD=sawtooth \
   TEST_DB_NAME=winston_v2_test RAILS_ENV=test bundle exec rspec \
   spec/services/operations/portfolio_close_service_spec.rb \
   spec/services/operations/portfolio_successor_service_spec.rb'
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new  
- **Services:** used running `winston_v2` container  
- **Migrations:** None (schema columns already from Phase 3)  
- **Data:** Disposable OPs #193–#195 closed; journals #57 on #194  

---

## 9. Risks & Technical Debt

- MCP tools not live until `winston_mcp` rebuild.  
- Force close on real leaves open residue without broker flatten path.  
- Ecosystem repo still has unrelated pre-session dirty files — do not stage blindly.  

---

## 10. Open Questions

- _None blocking._ Operator still chooses demo order for essential desk tickets.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Close/successor shipped; demo matrix tickets filed at wrap.  
- **Next concrete step:** Rebuild MCP image; smoke `close_portfolio` / `successor` in Ops UI; then demo checklist ticket 0.  
- **Files to read first:**  
  1. `winston_v2/app/services/operations/portfolio_close_service.rb`  
  2. `winston_v2/app/services/operations/portfolio_successor_service.rb`  
  3. `ecosystem/docs/tickets/2026-07-17-ops-daily-demo-epic.md`  

---

## 12. Stakeholder Communications

- _None formal._  

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report, record (tickets)  
- **What worked well:** Matching CashEventService / ActivationService result shapes  
- **Friction points:** ecosystem dirty tree from prior sessions  
- **Subagent usage:** none  

---

## 14. Follow-up Actions

- [ ] Rebuild/restart `winston_mcp` for close/successor tools  
- [ ] Demo smoke checklist (Ops UI + Telegram) — See: `docs/tickets/2026-07-17-ops-daily-demo-smoke-checklist.md`  
- [ ] DAR open-book blotter appendix — See: `docs/tickets/2026-07-17-ops-daily-dar-positions-blotter.md`  
- [ ] Ops shell cash parity — See: `docs/tickets/2026-07-17-ops-daily-shell-cash-parity.md`  
- [ ] External stop exit packaging — See: `docs/tickets/2026-07-17-ops-daily-external-stop-exit.md`  
- [ ] Bulk risk actions — See: `docs/tickets/2026-07-17-ops-daily-bulk-risk-actions.md`  
- [ ] Signal→related instrument fill — See: `docs/tickets/2026-07-17-ops-daily-related-instrument-fill.md`  
- [ ] Journal draft edit — See: `docs/tickets/2026-07-17-ops-daily-journal-draft-edit.md`  
- [ ] Telegram equity compare charts — See: `docs/tickets/2026-07-17-ops-daily-telegram-equity-compare.md`  
- [ ] Capital Activation (already tracked)  
- [ ] Host MCP git-home + compose versioning (already tracked)  

---

## 15. Appendix

### Rake examples

```bash
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:close[12]
SYMBOLS=AMZN,MSFT,GLD INITIAL_CAPITAL=12000 \
  bin/compose exec -T winston_v2 bin/rails wv2:portfolios:successor[12]
```

### Ops shell

```
close_portfolio Orange notes=hygiene
successor Orange symbols=AMZN,MSFT,GLD capital=12000
```
