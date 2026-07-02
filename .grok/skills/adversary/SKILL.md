---
name: adversary
description: >
  Spawn an adversarial subagent to challenge the current plan, conclusion, or
  code change before committing to it. Use when the user says "/adversary",
  "challenge this", "red team", or before merging a significant change.
metadata:
  short-description: "Hostile review before committing"
---

# /adversary — Hostile Review

Spawn ONE fresh general-purpose subagent as a hostile reviewer.

**Target:** the argument after `/adversary`, or default to the most recent conclusion, plan, or diff from this turn.

## Subagent standing orders

- Assume the conclusion is **WRONG** until proven otherwise. Break it; do not bless it.
- List every load-bearing assumption. For each, find evidence that would **disconfirm** it — read code at file:line, check tests, verify against `ecosystem/interfaces/` and `ecosystem/principles/`.
- Trust executable code, not comments or stale docs.
- Re-derive numbers independently. Do not trust counts or totals stated in conversation.
- Check against: ecosystem principles, parquet standard, monolith boundaries, compose service contracts.
- Write scratch notes to `/tmp/adversarial-<slug>.md`.
- Return: **VERDICT** (`holds` / `holds-with-caveats` / `broken`), findings with evidence, concrete corrections.

## After the subagent reports

Summarize what survived and what did not. Apply corrections — no agreement theater.

## When to use

- Before committing to an architectural decision (promote survivors to ADR in Wave 2).
- Before merging a cross-monolith change.
- When a conclusion feels too clean or was reached without running tests.

## Usage

```
/adversary
/adversary the WUT-to-Wv2 portfolio handoff design
/adversary this reconciliation fix
```