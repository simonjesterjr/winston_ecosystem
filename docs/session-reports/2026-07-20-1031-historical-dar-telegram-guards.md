# Session Report — Historical DAR morning Telegram leak + guards

**Date:** 2026-07-20  
**Time:** ~07:50–10:31 MDT  
**Duration:** ~2h 40m  
**Project:** sawtooth Winston ecosystem (cross-monolith)  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `ecosystem` `main`; `winston_v2` `main`  
**Model:** Grok 4.5 (xAI)  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Explain morning Telegram DAR for **2023-10-15** (paper); enforce policy that DARs are EOD-only and historical dates never hit Sawtooth Main outside explicit test passes; file issue and implement Wv2/MCP date + Telegram guards.

**Outcome:** Delivered

**One-line summary:** Root-caused the 7:47 AM DAR to a market-snapshot cron LLM calling `perform_daily_analysis` for a recycled test date; hard-blocked non-production evaluate and Telegram auto-delivery unless explicit historical flags.

---

## 2. Work Completed

- Traced incident via MCP audit, webhook `daily_complete`, Cromwell `cron_market-snapshot-open` session, and notification file mtimes
- Confirmed pattern: Jul 15 / Jul 16 / Jul 20 with `parent_correlation_id: abc123` and historical dates
- Filed issue `docs/issues/2026-07-20-historical-dar-morning-telegram-leak.md`
- Implemented production-date policy in `DailyReportSchedule` + evaluate controller + `CromwellNotifier` Telegram path
- Extended MCP tool schemas / evaluate pass-through / 422 guidance
- Updated ecosystem interfaces for DAR date + Telegram policy
- Specs (15 examples green in container); live smoke: historical evaluate **422**, production enqueue **200**
- Rebuilt `winston_mcp` image; restored compose stack after podman recreate churn

---

## 3. Code Delivered

### Files changed

| File | Change | Repo |
|------|--------|------|
| `ecosystem/docs/issues/2026-07-20-historical-dar-morning-telegram-leak.md` | **added** | ecosystem |
| `ecosystem/docs/session-reports/2026-07-20-1031-historical-dar-telegram-guards.md` | **added** | ecosystem |
| `ecosystem/interfaces/winston-mcp-tools.md` | date / allow_historical policy | ecosystem |
| `ecosystem/interfaces/cromwell-notification-v1.md` | Telegram production-date rule | ecosystem |
| `winston_v2/app/services/daily_report_schedule.rb` | production/historical/evaluate/telegram helpers | winston_v2 |
| `winston_v2/app/controllers/internal_controller.rb` | evaluate guards + flags | winston_v2 |
| `winston_v2/app/services/cromwell_notifier.rb` | skip non-production Telegram | winston_v2 |
| `winston_v2/app/jobs/daily_analysis_job.rb` | default date → `default_report_date` | winston_v2 |
| `winston_v2/spec/services/daily_report_schedule_spec.rb` | **added** | winston_v2 |
| `winston_v2/spec/services/cromwell_notifier_telegram_guard_spec.rb` | **added** | winston_v2 |
| `ai/mcp_winston/mcp_winston/server.py` | schema + pass-through + blocked errors | host image (not in git) |
| `ai/mcp_winston/mcp_winston/errors.py` | 422 guidance | host image (not in git) |

### Commits

- _Pending wrap commit (this session)._

### Branch / PR state at sign-off

- `ecosystem` `main` — dirty with **unrelated** prior edits; wrap stages **only this session’s files**
- `winston_v2` `main` — dirty with this session’s guards only
- `ai/mcp_winston` — **no git home** (see existing ticket `docs/tickets/2026-07-13-mcp-winston-source-git-home.md`); image rebuilt live
- Pushed: pending wrap
- PR: not opened (direct main workflow)

---

## 4. Decisions Made

### Decision 1: Hard guards in Wv2, not prompt-only
- **Choice:** Block evaluate for non-`default_report_date` unless `allow_historical=true`; Telegram only for production date unless force
- **Why:** Soft cron FORBIDDEN failed repeatedly; agent still called the tool
- **Alternatives considered:** MCP-only refuse; disable Telegram entirely for all MCP evaluates
- **Reversibility:** easy (flags + ENV)
- **Promote to ADR?** no (operational policy; interfaces updated)

### Decision 2: Historical test pass opt-in split
- **Choice:** `allow_historical` runs analysis without Telegram; `deliver_telegram=true` (with allow) required to post Sawtooth Main
- **Why:** Operators still need demo/historical analysis without channel pollution
- **Alternatives considered:** Single force flag that always Telegrams
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 3: Default evaluate date = production report date
- **Choice:** Omit date → `DailyReportSchedule.default_report_date` (not bare `Date.current`)
- **Why:** Before 4:30 MT, “today” is not a valid EOD target
- **Alternatives considered:** Keep `Date.current` and rely solely on cutoff block
- **Reversibility:** easy
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- **Same class as Jul 13 path hallucination:** truncation / continue turns → agent invents tools and placeholder IDs (`abc123`, old demo dates)
- **`parent_correlation_id: abc123`** is a reliable forensic fingerprint for LLM-invented chains
- **2023-10-15** was first materialised Jul 15 (test/demo), then re-run by cron Jul 20
- **Legitimate EOD path was healthy** (e.g. 2026-07-19 at 16:30 MT); incident was not Sidekiq schedule failure
- **podman-compose `up` recreate** can stop the stack and fail on name conflicts; prefer `podman start` / targeted rebuild over full recreate when only MCP image changed

---

## 6. Issues & Tickets

### Resolved this session
- Filed + mitigated: `docs/issues/2026-07-20-historical-dar-morning-telegram-leak.md` (status: Fixed in tree; live 422 verified)

### Deferred
- Cromwell **tool allowlists** per cron job — See: [`docs/tickets/2026-07-20-cromwell-cron-tool-allowlist.md`](../tickets/2026-07-20-cromwell-cron-tool-allowlist.md)
- Hygiene: quarantine/archive historical demo DAR artifacts — See: [`docs/tickets/2026-07-20-quarantine-historical-demo-dar-artifacts.md`](../tickets/2026-07-20-quarantine-historical-demo-dar-artifacts.md)
- Git-home for `ai/mcp_winston` — already tracked: [`docs/tickets/2026-07-13-mcp-winston-source-git-home.md`](../tickets/2026-07-13-mcp-winston-source-git-home.md) (reinforced this session)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| `DailyReportSchedule` + Telegram guard specs | `bundle exec rspec` in `winston_v2` container | ✅ 15 examples, 0 failures |
| Historical evaluate live | `POST /internal/portfolios/evaluate` `date=2023-10-15` | ✅ 422 `historical_daily_analysis_requires_force` |
| Production evaluate path | `date=2026-07-19` enqueue | ✅ 200 `production_date: true` |
| MCP image | rebuild + container greps `allow_historical` | ✅ present |
| Agent allowlist | not implemented | ⚠️ still relies on Wv2 refuse |

**Test command(s):**

```bash
./bin/compose exec winston_v2 bundle exec rspec \
  spec/services/daily_report_schedule_spec.rb \
  spec/services/cromwell_notifier_telegram_guard_spec.rb --format documentation

podman exec winston_mcp python3 -c \
  'import httpx; r=httpx.post("http://winston_v2:3000/internal/portfolios/evaluate",json={"date":"2023-10-15","sync":True},timeout=20); print(r.status_code,r.json().get("error"))'
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new
- **Services:** `winston_mcp` image rebuilt; brief stack stop during failed compose recreate; services restarted via `podman start`
- **Migrations:** None
- **Data:** Historical notification `wv2_20231015.json` left on disk (hygiene deferred)

---

## 9. Risks & Technical Debt

- Agent can still *attempt* historical analysis; noise in logs/Telegram agent prose until cron allowlists exist
- MCP source remains outside git — drift risk between host `ai/mcp_winston` and what operators rebuild
- Async `perform_later` for historical dates cannot carry thread-local `force_telegram_historical` (sync path is primary for MCP)

---

## 10. Open Questions

- **Should morning market-snapshot continue to use the same weak model as EOD?** — needs answer from: ops preference; blocks: cron quality
- **Archive vs delete historical demo DARs on disk?** — needs answer from: operator; blocks: hygiene cleanup

---

## 11. Handoff & Resume Notes

- **Where I left off:** Guards live on bind-mounted Wv2 + rebuilt MCP; issue + this report written; wrap commits pending
- **Next concrete step:** Commit/push ecosystem + winston_v2 session files; decide follow-up tickets (allowlist / artifact hygiene)
- **Files to read first:**
  1. `ecosystem/docs/issues/2026-07-20-historical-dar-morning-telegram-leak.md`
  2. `winston_v2/app/services/daily_report_schedule.rb`
  3. `winston_v2/app/services/cromwell_notifier.rb` (`deliver_telegram!`)
  4. `ai/mcp_winston/mcp_winston/server.py` (perform_daily_analysis schema)

---

## 12. Stakeholder Communications

- Principals: morning **2023-10-15** DAR was a bot error, not a real EOD. Ignore it. Real DARs remain end-of-day (~4:30–4:35 MT). System now refuses historical analysis posts unless an explicit test flag is set.

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report, record (issue filing conventions)
- **What worked well:** Audit JSONL + session JSONL gave a complete chain in minutes
- **Friction points:** `bin/compose up` recreate after MCP rebuild disrupted the whole stack; host rspec DB credentials unavailable (container path works)
- **Subagent usage:** None

---

## 14. Follow-up Actions

- [ ] Cromwell cron tool allowlist — See: [`../tickets/2026-07-20-cromwell-cron-tool-allowlist.md`](../tickets/2026-07-20-cromwell-cron-tool-allowlist.md) — owner: next session — due: soon
- [ ] Quarantine/archive demo historical DAR artifacts — See: [`../tickets/2026-07-20-quarantine-historical-demo-dar-artifacts.md`](../tickets/2026-07-20-quarantine-historical-demo-dar-artifacts.md) — owner: ops — due: optional
- [ ] Land MCP sources in a git home — See: [`../tickets/2026-07-13-mcp-winston-source-git-home.md`](../tickets/2026-07-13-mcp-winston-source-git-home.md) — owner: infra — due: backlog

---

## 15. Appendix

### Operator contract

| Intent | Call |
|--------|------|
| Real EOD | Sidekiq 4:30 MT / omit date after cutoff |
| Historical analysis only | `allow_historical=true` |
| Historical + Telegram | `allow_historical=true` **and** `deliver_telegram=true` |

### Incident fingerprint

- Time: 2026-07-20 ~07:47 MT  
- Tool: `wv2_perform_daily_analysis`  
- Args: `date=2023-10-15`, `parent_correlation_id=abc123`  
- Session: `cron_market-snapshot-open`  
- Correlation: `53803f16-6d65-4385-94e5-0c3e1ed37fbc`
