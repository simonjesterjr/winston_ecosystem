# Hints & Gotchas

Quick cues for the Winston ecosystem. Add a new file when something bites you twice.

## How to use

- One topic per file: `YYYY-MM-DD-short-topic.md` or a standing name like `parquet-reconciliation.md`.
- Link back to principles, interfaces, or WUT reference code — don't duplicate long explanations.
- If a hint becomes a durable decision, promote it to `docs/adr/` (Wave 2) or update `principles/`.

## Starter hints (expand as you learn)

### Always read ecosystem first

Before touching DM, WUT, Wv2, or Cromwell: `ecosystem/principles/`, `ecosystem/plans/`, `ecosystem/interfaces/`.

### WUT is the mature reference

`winston_unit_test/` has the comprehensive patterns for data sync, portfolios, Sidekiq daily ops, and parquet consumption. Do not model after `winston/` (v1 legacy).

### Compose port map

| Service | Host port | Internal |
|---------|-----------|----------|
| WUT | 3000 | 3000 |
| DM | 3001 | 3000 |
| Wv2 | 3002 | 3000 |

Use `bin/compose` from the sawtooth root.

### Session discipline

End every substantive session with `/wrap` or `/session-report`. Lessons learned go in session report §13.

### Cromwell skills ≠ developer skills

Runtime bot skills live in `ecosystem/ai/skills/`. Developer session skills live in `ecosystem/.grok/skills/`.

### ADR vs business-context vs CONTEXT.md

- **CONTEXT.md** — glossary terms only
- **docs/business-context/** — domain rules ("what" and "why")
- **docs/adr/** — irreversible engineering decisions ("we chose X over Y")
- Use `/grill-with-docs` to stress-test plans against all three