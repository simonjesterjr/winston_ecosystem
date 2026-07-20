---
name: record
description: >
  Record the current finding in the right docs bucket (issue, ticket, plan,
  analysis, operations) with naming and banner conventions. Use when the user
  says "/record", "file this finding", or wants to capture a defect, backlog
  item, or reference doc. Auto-routes if type is omitted. Prefer manage-issue-ticket
  for full defect intake.
metadata:
  short-description: "Route finding to the right docs bucket"
---

# /record — File a Finding

Capture what we just worked out as a docs artifact. Read `ecosystem/docs/README.md` (or the monolith `docs/` guide) before creating anything.

## Auto-routing (if type not specified)

| Situation | Bucket | One-line test |
|-----------|--------|---------------|
| Unexpected defect / ops failure worth re-reading | `docs/issues/` | "Something is wrong; here's the trace." Prefer `manage-issue-ticket`. |
| Durable technical reference, not tied to one defect | `docs/analysis/` | "Future work will consult this." |
| Scoped work item driving a PR | `docs/tickets/` | "This is backlog work." |
| Design or implementation plan | `ecosystem/plans/` or `docs/plans/` | "Work not yet built." |
| Architecture decision (irreversible) | `docs/adr/` | "We decided X over Y." |
| Domain rule or explainer | `docs/business-context/` | "This teaches the domain." |
| Repeatable procedure (2nd diagnosis or high blast radius) | `docs/operations/` | "Next time, follow this runbook." |

**Ecosystem-level** (cross-monolith): `ecosystem/docs/{issues,tickets,analysis,operations,adr}/`.

**Monolith-level** (single app): `{monolith}/docs/{issues,tickets,analysis}/`.

## Issues vs tickets (important)

- **Defects** (wrong behavior, capital risk, Telegram leaks, data corruption) → **`issues/` first**, then a ticket only for remaining implementation work. Use `issues/_template.md` or `manage-issue-ticket`.
- **Features / chores** → `tickets/` only.
- Do not bury a serious investigation only in a ticket.

## Naming and fields

- `YYYY-MM-DD-<kebab-slug>.md` for dated docs.
- **Issues:** YAML frontmatter (`status`, `type`, `priority`) + human status banner. Ready gate before `lightweight-bug-fix`.
- **Tickets:**
  - `**Status:**` `Proposed` | `In progress` | `Done` | `Blocked`
  - `**Priority:**` `P0` | `P1` | `P2` | `P3` | `unset`
- When a ticket is **Done**, move it to `docs/tickets/archive/` and refresh `docs/tickets/INDEX.md` if practical.

## Rules

- Cross-link related artifacts; don't duplicate content.
- Skip `docs/issues/` for trivial one-commit fixes — the commit message is enough.
- Verify claims in code or running systems, not from memory.
- Confirm the path and bucket chosen with the user before saving (unless they already named the bucket).

## Usage

```
/record issue DM reconciliation drift on boot
/record ticket add MCP portfolio snapshot tool
/record analysis parquet column semantics for ATR-17
/record plan winston-mcp phase 2 design
/record operations recreate winston_mcp after tool schema change
```
