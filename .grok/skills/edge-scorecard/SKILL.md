---
name: edge-scorecard
description: >
  After lab experiment cells complete, score and rank by Edge (R) (`edge_r`).
  Triggers: /edge-scorecard, lab eval scorecard, best Edge (R).
metadata:
  short-description: "Score completed lab cells by Edge (R)"
---

# Edge Scorecard

Runbook (source of truth): `ecosystem/docs/operations/grok-bot-edge-scorecard.md`

```bash
cd /home/johnkoisch/Documents/com/sawtooth
./bin/lab-eval list
./bin/lab-eval get <pbr_id>
./bin/lab-eval score
```

**Banner:** report only — no pack promotion.

- Rank by `edge_r` (ADR-015 / `winston-edge-v1`). Not Cromwell. Not a second Edge formula.
- If the only cell is pending (#596), say so — no winner. Do not execute PBRs.
