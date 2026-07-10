# Session Report — Deactivate Wv2 Demo Actives (Red Focus)

**Date:** 2026-07-10  
**Time:** ~08:55–09:14 MDT  
**Duration:** ~20m  
**Project:** Sawtooth ecosystem / winston_v2 (ops + docs)  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `ecosystem` `main` (docs only)  
**Model:** Grok 4.5 (xAI)  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Execute ticket `2026-07-10-deactivate-wv2-demo-actives-for-red-focus.md` so Daily Analysis focuses on Portfolio Red paper observation.

**Outcome:** Delivered

**One-line summary:** Deactivated seed demos (B + Sample Trend); only Portfolio Red remains Active; re-evaluated 2026-07-10 and confirmed Red-only notification.

---

## 2. Work Completed

- Listed Wv2 portfolios: three Active (B, Sample Trend, Red).
- Ran `wv2:portfolios:deactivate` for Trading Portfolio B and Sample Trend (name substring).
- Confirmed Active set is Red-only; capital_base $10k and TS#8 unchanged.
- Re-ran `wv2:portfolios:evaluate` (no id_or_name — does not re-activate demos).
- Verified Cromwell notification `wv2_20260710.json`: `portfolios[]` = Red only; summary `portfolios: 1`.
- Documented Active hygiene + deactivate commands in `portfolio_configs/README.md`.
- Marked ticket **Done** with resolution notes.

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `ecosystem/docs/tickets/2026-07-10-deactivate-wv2-demo-actives-for-red-focus.md` | modified | Status Done + resolution |
| `ecosystem/docs/session-reports/2026-07-10-0914-deactivate-wv2-demo-actives-red-focus.md` | added | This report |
| `portfolio_configs/README.md` | modified | Active attention hygiene section |

### Runtime state (DB / storage, not git)

- Portfolio `#2` Trading Portfolio B → `active=false`
- Portfolio `#3` Sample Trend Portfolio (from WUT) → `active=false`
- Portfolio `#5` Portfolio Red → `active=true` (unchanged capital/TS)
- Artifacts: `winston_v2/storage/cromwell_notifications/wv2_20260710.json`, `storage/reports/wv2_20260710.pdf`

### Commits

- `65e4b1f` — docs: deactivate Wv2 demos for Portfolio Red focus  

### Branch / PR state at sign-off

- Branch: `ecosystem` `main` — clean after push  
- Pushed: yes (`origin/main`)  
- PR: not opened (direct main)

**Monoliths touched:** none for application code. `winston_v2` DB active flags only. Docs in `ecosystem/`. Host-only `portfolio_configs/README.md` (workspace volume, not in any monolith git).

---

## 4. Decisions Made

### Decision 1: Deactivate demos now (not wait for ADR-006 Active mutex)
- **Choice:** Immediate operator deactivate of B + Sample Trend via existing rake.
- **Why:** Ticket acceptance; domain wants laser Active attention; no schema required.
- **Alternatives considered:** Leave demos until Active mutex is coded; force-only dual Active later.
- **Reversibility:** Easy — `wv2:portfolios:activate[name]`.
- **Promote to ADR?** No — operational hygiene already in CONTEXT / ADR-006 doctrine.

### Decision 2: Evaluate without id_or_name
- **Choice:** Bare `wv2:portfolios:evaluate` after deactivates.
- **Why:** `evaluate[name]` auto-activates the named portfolio; would re-pollute Active set if used carelessly.
- **Alternatives considered:** N/A.
- **Reversibility:** N/A.
- **Promote to ADR?** No — documented in README.

---

## 5. Insights Surfaced

- `capital_base` is a Portfolio method (from CashEvents), not a DB column — bare `pluck(:capital_base)` fails.
- Cromwell `passed_signals` still lists historical expired demo rows; that does **not** mean demos were re-evaluated today. Trust `portfolios[]` + `summary.portfolios` for Active set.
- `portfolio_configs/` is a compose bind-mount at the workspace root and is **outside** all monolith git repos — README edits are host-local unless separately versioned (see plan task 16 / deployment packaging).

---

## 6. Issues & Tickets

### Resolved this session
- Demo Active dilution → ticket `2026-07-10-deactivate-wv2-demo-actives-for-red-focus.md` **Done**.

### Deferred
- Watch Sidekiq EOD path — already: `docs/tickets/2026-07-10-watch-sidekiq-eod-daily-analysis-path.md`
- Confirm first Red paper pending action — already: `docs/tickets/2026-07-10-confirm-first-red-paper-pending-action.md`
- Promote tmp smoke scripts — already: `docs/tickets/2026-07-10-promote-wv2-daily-ops-smoke-scripts.md`
- Version workspace-root artifacts (`portfolio_configs/README`, compose) in git — already: plan task 16 / related packaging tickets
- ADR-006 schema/import/export_kind — already ticketed 2026-07-08/09

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Deactivate B | rake deactivate + list | ✅ active=false |
| Deactivate Sample Trend | rake deactivate + list | ✅ active=false |
| Red still Active | list | ✅ #5 active, TS#8, capital $10k |
| Active count | list Total active | ✅ 1 |
| Evaluate Red-only | `wv2:portfolios:evaluate` 2026-07-10 | ✅ portfolios=[Red], skipped=[] |
| Webhook | notification webhook_delivery | ✅ status 200 |

**Test command(s):**

```bash
./bin/compose exec -T winston_v2 bin/rails wv2:portfolios:list
./bin/compose exec -T winston_v2 bin/rails wv2:portfolios:evaluate
# inspect portfolios[] in:
# winston_v2/storage/cromwell_notifications/wv2_20260710.json
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None  
- **Services:** Existing compose stack (winston_v2)  
- **Migrations:** None  
- **Data:** Active flags only; no capital/TS mutation  

---

## 9. Risks & Technical Debt

- Host-local `portfolio_configs/README.md` can drift vs clones that lack the volume tree contents.
- Future imports that leave `active: true` in JSON + activate path could re-add demos if operators re-seed carelessly.
- Sidekiq EOD path still unwatched for unattended Red paper cadence.

---

## 10. Open Questions

- _None new this session._  

---

## 11. Handoff & Resume Notes

- **Where I left off:** Red-only Active; 2026-07-10 evaluate clean; ticket Done; wrap in progress.  
- **Next concrete step:** Leave Sidekiq on; after next trading-day 4:30 PM MT check `wv2_YYYYMMDD.json` for Red-only + any pending_actions (ticket watch EOD). Or when signals appear, confirm first paper action via MCP.  
- **Files to read first:**  
  1. `ecosystem/docs/tickets/2026-07-10-deactivate-wv2-demo-actives-for-red-focus.md`  
  2. `ecosystem/docs/tickets/2026-07-10-watch-sidekiq-eod-daily-analysis-path.md`  
  3. `portfolio_configs/README.md` (Active hygiene)  
  4. This session report  

---

## 12. Stakeholder Communications

- Principals: Daily Analysis attention is now Portfolio Red only (paper/observation). Seed demos B and Sample Trend no longer appear in the daily report evaluation list.

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report  
- **What worked well:** Existing `wv2:portfolios:deactivate` rake; list + evaluate smoke is enough for ops tickets.  
- **Friction points:** `portfolio_configs` not versioned in git — wrap cannot commit README into a monolith.  
- **Subagent usage:** None  

---

## 14. Follow-up Actions

- [ ] Watch Sidekiq EOD path — See: [`../tickets/2026-07-10-watch-sidekiq-eod-daily-analysis-path.md`](../tickets/2026-07-10-watch-sidekiq-eod-daily-analysis-path.md)
- [ ] Confirm first Red paper pending action — See: [`../tickets/2026-07-10-confirm-first-red-paper-pending-action.md`](../tickets/2026-07-10-confirm-first-red-paper-pending-action.md)
- [ ] Promote tmp smoke scripts — See: [`../tickets/2026-07-10-promote-wv2-daily-ops-smoke-scripts.md`](../tickets/2026-07-10-promote-wv2-daily-ops-smoke-scripts.md)
- [ ] ADR-006 lifecycle schema/import — See: 2026-07-09 OP lifecycle tickets
- [ ] Optionally version `portfolio_configs/README` (workspace packaging) — plan task 16

---

## 15. Appendix

### Pre / post Active set

```text
Before: active=3  (#2 B, #3 Sample Trend, #5 Red)
After:  active=1  (#5 Portfolio Red)
```

### Evaluate summary (2026-07-10)

```text
evaluated: Portfolio Red
skipped: []
pending_actions: 0
webhook_delivery: 200
```
