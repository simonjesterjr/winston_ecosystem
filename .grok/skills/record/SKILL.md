---
name: record
description: >
  Record the current finding in the right docs bucket (issue, ticket, plan,
  analysis) with naming and banner conventions. Use when the user says "/record",
  "file this finding", or wants to capture a defect, backlog item, or reference
  doc. Auto-routes if type is omitted.
metadata:
  short-description: "Route finding to the right docs bucket"
---

# /record — File a Finding

Capture what we just worked out as a docs artifact. Read `docs/README.md` before creating anything.

## Auto-routing (if type not specified)

| Situation | Bucket | One-line test |
|-----------|--------|---------------|
| Multi-subsystem defect, business trade-off, worth re-reading | `docs/issues/` | "Something is wrong; here's the trace." |
| Durable technical reference, not tied to one defect | `docs/analysis/` | "Future work will consult this." |
| Scoped work item driving a PR | `docs/tickets/` | "This is backlog work." |
| Design or implementation plan | `docs/plans/` or `../plans/` | "Work not yet built." |
| Architecture decision (irreversible) | `docs/adr/` | "We decided X over Y." |
| Domain rule or explainer | `docs/business-context/` | "This teaches the domain." |

**Ecosystem-level** (cross-monolith): use `ecosystem/docs/{issues,tickets,analysis}/`.

**Monolith-level** (single app): use `{monolith}/docs/{issues,tickets,analysis}/`.

**Plans** for cross-monolith work stay in `ecosystem/plans/` (existing convention). New dated plans can also go in `ecosystem/docs/plans/` when the filing guide applies.

## Naming

- `YYYY-MM-DD-<kebab-slug>.md` for dated docs.
- Issues lead with a status banner: `Open` / `Under investigation` / `Decision pending` / `Fixed in <sha>` / `Won't fix`.
- Tickets lead with `Status:` (`Proposed` / `In progress` / `Done` / `Blocked`).

## Rules

- Cross-link related artifacts; don't duplicate content.
- Skip `docs/issues/` for trivial one-commit fixes — the commit message is enough.
- Verify claims in code or running systems, not from memory.
- Confirm the path and bucket chosen with the user before saving.

## Usage

```
/record issue DM reconciliation drift on boot
/record ticket add MCP portfolio snapshot tool
/record analysis parquet column semantics for ATR-17
/record plan winston-mcp phase 2 design
```