# Ticket: Smoke daily analysis for six Active color cohorts

**Status:** Done  

**Date:** 2026-07-12  
**Completed:** 2026-07-12  

## Context

Wv2 Active set (post Phase 6 import):

- Portfolio Red, Blue, Green, Pink, Blank, Rust (all Active)  
- Orange deactivated; White not activated  

PCS daily path and DAR correlation section depend on WUT snapshots + WutClient.

## Scope

1. Ensure DM parquet for all Books symbols of the six (sync if missing)  
2. `bin/rails wv2:portfolios:evaluate` (or DailyAnalysisJob) for today  
3. Confirm notification JSON has `correlation_scores.series` for Active OPs  
4. Confirm DAR markdown/PDF include CORRELATION SCORES section (or graceful WUT-down note)  
5. Note any `missing_data` / `unsupported_strategy` skips  

## Acceptance

- [x] Evaluate completes without crash  
- [x] Six portfolios appear in evaluate result or explicit skip reasons  
- [x] `correlation_scores` present when WUT reachable  
- [x] Brief note in session report or ticket checklist  

## Smoke run (2026-07-12)

**Command:** `bin/compose exec -T winston_v2 bin/rails wv2:portfolios:evaluate`  
**Report date:** 2026-07-12  

### Preflight

| Check | Result |
|-------|--------|
| Active set | #5 Red, #7 Blue, #8 Green, #9 Pink, #10 Blank, #11 Rust (Orange #6 inactive) |
| `PortfolioReadiness` | all six `ready=true`, no missing symbols |
| DM ingest (via evaluate) | `{:ingested=>61, :skipped=>0, :errors=>[]}` |
| WUT PCS API | `GET /internal/correlation_scores` healthy (`corr_v2`, six color cohorts + Orange) |

### Evaluate result

| Portfolio | Status | Skip reason | PCS | Max \|r\| |
|-----------|--------|-------------|-----|-----------|
| Green | evaluated | — | 83.39 | 0.311 |
| Pink | evaluated | — | 76.29 | 0.438 |
| Blank | evaluated | — | 71.30 | 0.530 |
| Rust | evaluated | — | 77.25 | 0.419 |
| Red | evaluated | — | 73.01 | 0.478 |
| Blue | evaluated | — | 76.15 | 0.441 |

- **skipped_portfolios:** `[]` (no `missing_data`, no `unsupported_strategy`)  
- **actions_created / pending_tasks:** 0 (quiet day — flat cash, no signals)  
- **correlation_scores.series:** 6 entries, `methodology_version: corr_v2`, `as_of: 2026-07-12`, all `error: null`, no degradation flags  
- **chapters:** each OP carries `correlation.latest` + `history` from WutClient  

### Artifacts

| Artifact | Path / note |
|----------|-------------|
| Notification JSON | `winston_v2/storage/cromwell_notifications/wv2_20260712.json` |
| DAR markdown | `winston_v2/storage/reports/wv2_20260712.md` — section **Correlation scores (Active) — corr_v2** + PCS table for all 6 |
| DAR PDF | `winston_v2/storage/reports/wv2_20260712.pdf` (7 pages) |
| Webhook | delivered (`status: 200` → winston_mcp) |
| Telegram | skipped (`missing_telegram_token`) — not a evaluate failure |

### Notes / non-blockers

- Equity remains at initial capital for all six (paper day-zero / no confirmed journals yet).  
- Historical `passed_signals` on inactive demo portfolios (Sample Trend, Trading Portfolio B) are unrelated to the six cohorts.  
- Telegram token missing in this environment; webhook + on-disk report package sufficient for smoke.

## Related

- ADR-007, Phase 5 DAR enrichment  
- WUT `GET /internal/correlation_scores`  
- Plan: `plans/portfolio-correlation-methodology-and-score.md` Phase 8  
