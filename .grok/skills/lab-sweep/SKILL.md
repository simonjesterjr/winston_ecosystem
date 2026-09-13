---
name: lab-sweep
description: >
  Create and list lab experiment cells for strategy77_rst_heat_risk_v1 via
  Grok Bot / Grok CLI Shell on sawtooth. Default is smoke only. Triggers:
  /lab-sweep, lab sweep, 32-cell UAT setup.
metadata:
  short-description: "Lab sweep: list/get/create-smoke; UAT opt-in"
---

# Lab Sweep

Brief (source of truth): `ecosystem/docs/operations/grok-bot-lab-sweep.md`

Host: Grok Bot / Grok CLI on sawtooth (Builder). **Not** Cromwell Telegram. **Not** Lab Scout execute.

Default (safe) — smoke only. Pending PBR #596 reuse is success. Do not execute unless asked.

```bash
cd /home/johnkoisch/Documents/com/sawtooth
./bin/lab-eval list
./bin/lab-eval get 596
./bin/lab-eval create-smoke
```

UAT / `FULL=1` (32 cells) is **opt-in** — only when the operator says UAT. Execute is serial hours of CPU (`./bin/lab-eval execute <id> --i-mean-it`). Then hand off to Edge Scorecard.

Hop / MCP / fences: `ecosystem/docs/operations/grok-bot-shell-lab-eval.md`, `ecosystem/plans/winston-lab-eval-grok-cli.md`, MCP v0.5. Do not duplicate those runbooks.
