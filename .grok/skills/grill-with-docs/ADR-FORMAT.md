# ADR Format (Sawtooth)

ADRs live in `ecosystem/docs/adr/` (cross-monolith) or `{monolith}/docs/adr/` (app-only).

**Naming:** `ADR-NNN-kebab-slug.md` (three-digit, zero-padded). Scan existing files and increment.

## Template (full — use for irreversible cross-monolith decisions)

```md
# ADR-NNN: {Title}

**Status:** Accepted
**Date:** YYYY-MM-DD
**Deciders:** Architecture
**Builds on:** ADR-XXX (if applicable)
**Source design:** plans/... or docs/plans/...
**Domain context:** docs/business-context/...

## Context
{Problem and alternatives considered}

## Decision
{What we chose}

## Rationale
{Why — including why NOT the alternatives}

## Consequences
### Positive
### Negative
### Risks mitigated
```

## Minimal template (acceptable for smaller decisions)

```md
# ADR-NNN: {Title}

**Status:** Accepted
**Date:** YYYY-MM-DD

## Context
## Decision
## Consequences
```

## When to create an ADR

All three must be true:

1. **Hard to reverse** — meaningful cost to change later
2. **Surprising without context** — future reader will wonder "why?"
3. **Real trade-off** — genuine alternatives existed

Skip if easy to reverse, obvious, or no alternative.

## What qualifies in sawtooth

- Monolith boundary decisions (ADR-001 pattern)
- Data format choices (parquet standard)
- Ownership decisions (DM owns derivatives)
- MCP vs internal API boundaries
- Auth/deployment targets with lock-in

## What does NOT need an ADR

- Routine bug fixes
- Adding a rake task
- Choosing a variable name
- Obvious Rails conventions