# Grok Bot Edge Scorecard

**Banner (every reply):** report only — no pack promotion.

**Host:** Grok Bot / Grok CLI on sawtooth (Builder plane). **Not** Cromwell. **Not** a second Edge formula.

**Job:** After experiment cells **complete**, score and rank by Edge (R) (`edge_r`). Explain “best Edge on portfolio X because …” using per-market contribution + heat skips when present.

**Plan:** [`winston-lab-eval-grok-cli.md`](../../plans/winston-lab-eval-grok-cli.md) (Phase D)  
**Shell hop** (list / get / create / execute): [`grok-bot-shell-lab-eval.md`](grok-bot-shell-lab-eval.md) — point, do not copy.  
**Interface:** [`winston-mcp-tools.md`](../../interfaces/winston-mcp-tools.md) v0.5  
**Edge contract:** ADR-015 / [`winston-edge-v1.md`](../../interfaces/winston-edge-v1.md)  
**Skill:** `edge-scorecard`  
**Companion:** Lab Sweep / Shell owns create and execute. This brief scores completed cells only.

**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Experiment:** `strategy77_rst_heat_risk_v1`

Smoke Portfolio Backtest Run (PBR) **#596** (`mint_rst_turtle_r01`) is **pending**. Do **not** execute it from this skill. Full-window Mint Turtle is hours of CPU.

## Commands

```bash
cd /home/johnkoisch/Documents/com/sawtooth
./bin/lab-eval list
./bin/lab-eval get <pbr_id>
./bin/lab-eval score          # WRITE=1 scorecard → ecosystem/docs/analysis/YYYY-MM-DD-strategy77-rst-heat-risk-matrix.{json,md}
```

`score` ranks completed cells by `edge_r` and writes dated JSON + markdown (Winston Unit Test bind: `ecosystem/docs/analysis/`). Do not call `./bin/lab-eval execute`.

## MCP fallbacks

If the wrapper is missing, read tools on Winston Unit Test (WUT) via Model Context Protocol (MCP) — [`winston-mcp-tools.md`](../../interfaces/winston-mcp-tools.md) v0.5. Copy-paste `podman exec winston_mcp` hop is in the Shell runbook.

- **`wut_get_run_edge_report`** — `{ "pbr_id": int, "include_per_market": true }` → `edge_r`, `profit_factor`, `edge_n`, `edge_components`, heat skips. Not `expectancy_r`. `costs=fill_only`.
- **`wut_compare_runs`** — `{ "experiment": "strategy77_rst_heat_risk_v1" }` or `{ "pbr_ids": [...] }`. Rank by `edge_r`. Thin cells stay listed (`disqualified_reason` is glance, not a drop).

## Rules

- Key is **`edge_r`**, not `expectancy_r`, not Sharpe-as-edge. Formula lives in ADR-015 / `winston-edge-v1` — do not invent another.
- `costs=fill_only`.
- Glance: `n<20` hide value; 20–99 thin; `n≥100` glance. **Do not drop thin cells.**
- Banner on **every** reply: **report only — no pack promotion**.
- If the only cell is pending (#596), say so — **no winner**. Do not invent completed metrics.
- John gates pack promotion. No Broker Gateway. No Cromwell execute.

## Reply shape

1. Banner.
2. Completed vs pending / failed counts.
3. Ranked table: cell_key, book, heat, risk, n, `edge_r`, profit factor, glance. Keep thin rows; hide the glance *value* when `n<20`.
4. Winner: **best Edge on {portfolio} because …** — per-market contribution + heat skips when those fields are present. If they are absent, say so; do not fabricate.
5. Artifact paths when `score` wrote files.

Pending-only (current smoke):

> **report only — no pack promotion.**  
> Experiment `strategy77_rst_heat_risk_v1` has one cell: PBR **#596** `mint_rst_turtle_r01` (Mint × turtle × 1%), **pending**. No completed Edge (R). No winner.

## Out of scope

Create / execute cells, `FULL=1` 32-cell UAT, pack promotion, Broker Gateway `order_write`, Cromwell Telegram execute, a second Edge formula.
