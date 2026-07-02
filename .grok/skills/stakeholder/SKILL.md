---
name: stakeholder
description: >
  Rewrite the current analysis or decision as a stakeholder-ready email or
  document in plain English. Use when the user says "/stakeholder", needs an
  outward-facing summary, or wants to communicate a technical decision to
  non-engineers.
metadata:
  short-description: "Plain-English stakeholder communication"
---

# /stakeholder — Stakeholder Communication

Turn the analysis, issue, or decision we just produced into a stakeholder-facing artifact.

## Style rules

- Plain language. Lead with the decision or bottom line, then the why, then any action needed.
- Introduce abbreviations in full before using them.
- Use canonical names from `ecosystem/CONTEXT.md` when it exists; until Wave 2, use terms from `ecosystem/principles/` and `ecosystem/interfaces/`.
- Illustrate with a concrete example tied to behavior the reader already knows.
- Verify field mappings and numbers in code or data before stating them.

## Format (first argument)

- **`email`** — write to a temp file for copy-paste. Subject + greeting + 3–6 short paragraphs + clear ask. Print the file path.
- **`doc`** — save under `docs/communications/YYYY-MM-DD-<slug>.md` with a one-line summary banner at top. Show draft before saving.

## Audience (optional second argument)

Tune depth: `ops` (default), `trading`, `data`, `exec`. Assume domain knowledge for trading/ops; less engineering jargon.

## Usage

```
/stakeholder email
/stakeholder doc trading
/stakeholder email exec
```