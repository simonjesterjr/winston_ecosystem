---
name: grill-with-docs
description: >
  Socratic design interview that challenges your plan against the ecosystem
  domain model, sharpens terminology, and updates CONTEXT.md and ADRs inline
  as decisions crystallise. Use when stress-testing a plan, design doc, or
  feature proposal against documented language and decisions.
metadata:
  short-description: "Stress-test plans against domain docs"
---

# Grill with Docs

Interview the user relentlessly about every aspect of the plan until you reach shared understanding. Walk down each branch of the design tree, resolving dependencies one-by-one. For each question, provide your recommended answer.

**Ask one question at a time.** Wait for feedback before continuing.

If a question can be answered by exploring the codebase or docs, explore instead of asking.

## Read first

Before grilling, load:

1. `ecosystem/CONTEXT.md` — canonical glossary
2. `ecosystem/docs/adr/` — accepted architecture decisions
3. `ecosystem/docs/business-context/` — domain rules
4. `ecosystem/principles/` and `ecosystem/interfaces/` — invariants and contracts
5. Relevant monolith `AGENTS.md` if the plan touches a specific app

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with `CONTEXT.md`, call it out immediately.

> "Your glossary defines **Reconciliation** as parquet→PG metadata sync, but you seem to mean downloading new bars — which is it?"

### Sharpen fuzzy language

Propose precise canonical terms.

> "You said 'account' — do you mean **Portfolio**, **Cromwell principal**, or broker account?"

### Stress-test with scenarios

Invent concrete scenarios that probe edge cases.

> "Portfolio A imports from WUT with MSFT and IBM. DM has parquet for MSFT only. What happens at first daily analysis?"

### Cross-reference with code

When the user states how something works, check the code. Surface contradictions.

> "You said Wv2 recalculates ATR, but ADR-003 says DM owns derivatives — which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `ecosystem/CONTEXT.md` immediately. Use [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md). Do not batch updates.

`CONTEXT.md` is glossary only — no implementation, no specs.

### Offer ADRs sparingly

Only when all three are true (see [ADR-FORMAT.md](./ADR-FORMAT.md)):

1. Hard to reverse
2. Surprising without context
3. Real trade-off

Write to `ecosystem/docs/adr/ADR-NNN-slug.md` for cross-monolith decisions, or `{monolith}/docs/adr/` for app-only.

### Offer business-context when teaching domain

If the session clarifies a **domain rule** (not an architecture choice), offer to write or update `ecosystem/docs/business-context/`.

## After the session

Summarize:
- Terms added/changed in CONTEXT.md
- ADRs created or proposed
- Business-context updates
- Open questions → suggest `/record ticket` for each

## Usage

```
/grill-with-docs
/grill-with-docs the MCP daily analysis design
```