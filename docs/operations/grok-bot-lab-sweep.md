# Lab Sweep — Grok Bot brief

Paste into a Grok Bot custom instruction. Host is **Grok Bot / Grok CLI on sawtooth** (Builder plane). **Not** Cromwell Telegram. **Not** Lab Scout execute.

**Job:** Create and list lab experiment cells for `strategy77_rst_heat_risk_v1` via Shell hop.

**Do not duplicate** hop / Model Context Protocol (MCP) / recreate details. Point, then stop:

| What | Path |
|------|------|
| Shell hop | [`grok-bot-shell-lab-eval.md`](grok-bot-shell-lab-eval.md) |
| Plan | [`winston-lab-eval-grok-cli.md`](../../plans/winston-lab-eval-grok-cli.md) |
| MCP contract | [`winston-mcp-tools.md`](../../interfaces/winston-mcp-tools.md) **v0.5** |

**Skill:** `lab-sweep` (`/lab-sweep`)

## Fences

- Report only — no pack promotion.
- No Broker Gateway `order_write`.
- No Cromwell cron. Mutating MCP needs `authorization: lab_geometry_report_only`.
- Shell-only (no Funnel, no Tailscale Serve `/mcp`).
- Do **not** execute Portfolio Backtest Run (PBR) **#596** unless the operator explicitly says execute.

## Default (safe) — smoke only

Mint × turtle × 1% × `resting_stop_touch`, cell_key `mint_rst_turtle_r01`. Pending PBR **#596** may already exist; **reuse is success**.

```bash
cd /home/johnkoisch/Documents/com/sawtooth
./bin/lab-eval list
./bin/lab-eval get 596
./bin/lab-eval create-smoke
```

## UAT (32 cells) — opt-in

Only when the operator explicitly says **UAT** / `FULL=1`. Do **not** start execute unless the operator says to execute. Do **not** execute #596 in the same breath as “write the brief.”

1. Create pending cells:

   ```bash
   ./bin/compose exec -T -e FULL=1 winston_unit_test \
     bin/rails runner lib/scripts/strategy_fill_heat_risk_matrix_setup.rb
   ```

2. Execute is **serial, hours of CPU**. Per cell (or the execute runner):

   ```bash
   ./bin/lab-eval execute <id> --i-mean-it
   ```

3. Then hand off to **Edge Scorecard**. Do not score, promote packs, or call Broker Gateway from this skill.
