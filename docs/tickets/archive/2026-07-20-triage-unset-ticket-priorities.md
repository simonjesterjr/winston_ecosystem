# Ticket: Triage remaining unset ticket priorities

**Status:** Done
**Priority:** P2  
**Source:** Session [`docs/session-reports/2026-07-20-2214-ai-workflow-skills-high-roi-install.md`](../session-reports/2026-07-20-2214-ai-workflow-skills-high-roi-install.md)

## Problem

Active backlog has Priority convention and INDEX, but many tickets remain `**Priority:** unset` after bulk hygiene.

## Acceptance criteria

- [x] Walk `docs/tickets/INDEX.md` active list
- [x] Assign P0–P3 (or archive/supersede) for every `unset` ticket worth keeping
- [x] Regenerate INDEX
- [x] Prefer few concurrent In progress items

## Related

- [`docs/tickets/INDEX.md`](../INDEX.md)


## Outcome (2026-07-20)

Triage pass completed:

- **Archived** 4 Completed Jul-08 tickets (`audit-outside-ui-callers`, `dm-bind-mount-decision`, `dm-reconcile-full-e2e-smoke`, `review-manual-registry-symbols`).
- **Assigned** P1/P2/P3 to all remaining previously-`unset` tickets (no P0; no residual `unset` on active backlog).
- **Regenerated** `INDEX.md`.
- **In progress** left alone (already ranked): Blue membership, Cromwell cron timeout, Cromwell CPU reliability.

### Ranking heuristics used

| Band | Rationale |
|------|-----------|
| **P1** | Paper desk correctness (ATR/sizer, journal fill/stop fields), live Cromwell Telegram quality (hallucination hardening, hourlies observation, confirm hourly), stale Active parquet |
| **P2** | Lab SoT follow-through, registry/audit mirrors, ops ergonomics, Phase 3 fingerprint/handoff polish, journal export |
| **P3** | Docs/hygiene, optional GPU, deferred order-vs-fill, residual PDF smoke, PCS niceties |

Prefer few concurrent In progress: no new items moved to In progress this pass.
