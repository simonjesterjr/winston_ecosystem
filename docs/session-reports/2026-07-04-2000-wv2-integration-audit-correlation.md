# Session Report — Wv2 Integration Audit + Correlation Echo

**Date:** 2026-07-04
**Time:** ~19:45–20:00 UTC
**Duration:** ~45m
**Project:** Sawtooth / Winston ecosystem (Wv2 + ecosystem docs)
**Working directory:** /home/johnkoisch/Documents/com/sawtooth
**Branch:** main (ecosystem, winston_v2)
**Model:** Grok
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Implement fast-follow ticket `docs/tickets/2026-07-02-wv2-integration-audit-correlation.md` — Wv2 reads MCP correlation headers, writes Integration Log JSONL, and echoes IDs in `daily_complete` notifications.

**Outcome:** Delivered

**One-line summary:** Wv2 now mirrors MCP correlation IDs into `ecosystem/logs/audit/wv2/` and embeds them in Cromwell notifications (schema v1.1) when analysis is MCP-triggered.

---

## 2. Work Completed

- Added thread-local `IntegrationCorrelation` context and `IntegrationAuditTracking` concern on `InternalController`
- Added `IntegrationAuditLogger` appending `internal_request` and `webhook_delivery` events to `integration_YYYYMMDD.jsonl`
- Updated `CromwellNotifier` to attach `correlation_id` / `parent_correlation_id` and bump `schema_version` to `1.1` when headers present
- Mounted audit partition on `winston_v2` + `winston_v2_sidekiq` in root `compose.yml` (`WV2_INTEGRATION_AUDIT_DIR=/audit/wv2`)
- Documented v1.1 additive fields in `interfaces/cromwell-notification-v1.md`
- Added `bin/test-wv2-integration-audit-smoke` and RSpec coverage
- Fixed `Invalid next` syntax error in concern `ensure` block (live 500 on first deploy)

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `winston_v2/app/models/integration_correlation.rb` | added | Thread-local correlation store |
| `winston_v2/app/services/integration_audit_logger.rb` | added | JSONL writer |
| `winston_v2/app/controllers/concerns/integration_audit_tracking.rb` | added | Header capture + request audit |
| `winston_v2/app/controllers/internal_controller.rb` | modified | `include IntegrationAuditTracking` (+ prior uncommitted Phase 2 endpoints bundled in same file) |
| `winston_v2/app/services/cromwell_notifier.rb` | modified | Correlation echo + webhook audit log |
| `winston_v2/spec/services/integration_audit_logger_spec.rb` | added | Unit tests |
| `winston_v2/spec/services/cromwell_notifier_correlation_spec.rb` | added | Correlation helper tests |
| `ecosystem/interfaces/cromwell-notification-v1.md` | added/modified | v1.1 correlation fields |
| `ecosystem/logs/audit/wv2/.gitkeep` | added | Partition scaffold |
| `compose.yml` | modified | Audit mount + env for Wv2 services |
| `bin/test-wv2-integration-audit-smoke` | added | Cross-partition smoke |

### Commits

- _(pending /wrap commit)_

### Branch / PR state at sign-off

- Branch: `main` — dirty (selective commit in progress)
- Pushed: pending
- PR: not opened

---

## 4. Decisions Made

### Decision 1: Thread-local correlation vs CurrentAttributes
- **Choice:** Plain `Thread.current` store (`IntegrationCorrelation`) instead of `ActiveSupport::CurrentAttributes`
- **Why:** Lightweight specs run without full Rails boot; Puma request threading is sufficient
- **Alternatives considered:** `CurrentAttributes` (rejected for spec friction)
- **Reversibility:** easy
- **Promote to ADR?** no — follows ADR-004

### Decision 2: Compose audit mount path
- **Choice:** Shared `./ecosystem/logs/audit:/audit` with `WV2_INTEGRATION_AUDIT_DIR=/audit/wv2`
- **Why:** Matches MCP partition layout (`/audit/mcp`, `/audit/webhook`)
- **Alternatives considered:** Host-path only without container mount (rejected — breaks compose smoke)
- **Reversibility:** easy
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- Root `sawtooth/compose.yml` and `bin/` scripts are **not** in any git repo — only `ecosystem/`, `winston_v2/`, etc. are versioned. Compose/smoke changes live on disk until a repo homes them.
- `winston_v2` working tree bundles prior uncommitted Phase 2 MCP internal API work alongside this session's audit wiring.

---

## 6. Issues & Tickets

### Resolved this session
- `docs/tickets/2026-07-02-wv2-integration-audit-correlation.md` — all acceptance criteria met via smoke + live MCP chain

### Deferred
- `docs/tickets/2026-07-02-dm-integration-audit-mirror.md` — sibling fast follow
- `docs/tickets/2026-07-02-cromwell-audit-trail-skill.md` — depends on wv2 + dm partitions
- Root `compose.yml` / `bin/test-wv2-integration-audit-smoke` versioning — not in git; consider promoting to `ecosystem/deployment/` or a sawtooth meta-repo

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| IntegrationAuditLogger | RSpec | ✅ |
| CromwellNotifier correlation | RSpec | ✅ |
| Live /internal/portfolios + headers | curl in container | ✅ |
| MCP → Wv2 JSONL join | `bin/test-wv2-integration-audit-smoke` | ✅ |

**Test command(s):**
```bash
bin/test-wv2-integration-audit-smoke
cd winston_v2 && bundle exec rspec spec/services/integration_audit_logger_spec.rb spec/services/cromwell_notifier_correlation_spec.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None
- **Services:** Recreated `winston_v2`, `winston_v2_sidekiq` with audit volume mount
- **Migrations:** None

---

## 9. Risks & Technical Debt

- `compose.yml` and `bin/` at workspace root are unversioned — audit mount and smoke script may not travel with git clones of individual monoliths
- `internal_controller.rb` commit may bundle unrelated Phase 2 endpoints if staged whole-file

---

## 10. Open Questions

- **Where should root compose/bin live in git long-term?** — needs answer from: operator; blocks: reproducible deployment from clone-only workflow

---

## 11. Handoff & Resume Notes

- **Where I left off:** Smoke passed; ready to commit/push
- **Next concrete step:** Implement DM integration audit mirror (`docs/tickets/2026-07-02-dm-integration-audit-mirror.md`)
- **Files to read first:**
  1. `ecosystem/docs/business-context/mcp-audit-correlation-design.md`
  2. `winston_v2/app/services/integration_audit_logger.rb` (Wv2 pattern to mirror in DM)
  3. `ecosystem/docs/tickets/2026-07-02-dm-integration-audit-mirror.md`

---

## 12. Stakeholder Communications

_None._

---

## 13. Tools & Workflow Notes

- **Skills used:** session-report, wrap
- **What worked well:** Reusing MCP audit partition layout; live podman exec verification
- **Friction points:** `next` invalid in `ensure` block; root compose not in git
- **Subagent usage:** None

---

## 14. Follow-up Actions

- [ ] DM integration audit mirror — owner: next session — ticket: `docs/tickets/2026-07-02-dm-integration-audit-mirror.md`
- [ ] Cromwell `winston-audit-trail` skill — owner: next session — ticket: `docs/tickets/2026-07-02-cromwell-audit-trail-skill.md`
- [ ] Version root `compose.yml` + `bin/` smoke scripts — owner: operator — **task:** `plans/winston-mcp-next-steps.md.tasks.json` id 16

---

## 15. Appendix

Live wv2 JSONL sample:
```json
{"correlation_id":"live-test-cid-2","parent_correlation_id":"parent-2","event":"internal_request","source":"winston_v2","status":"ok","at":"2026-07-04T19:53:54.554Z","endpoint":"/internal/portfolios","http_method":"GET","http_status":200,"duration_ms":42}
```