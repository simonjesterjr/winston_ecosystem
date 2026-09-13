# Grok Bot Shell lab eval

**Decision:** Shell-on-sawtooth only. No Tailscale Serve `/mcp`. No Funnel.
Grok Bot cloud cannot reach `winston_mcp`. Transport = operator / Grok Bot
**Shell on sawtooth-ai**. Model Context Protocol (MCP) is the structured API
the hop should invoke.

**Plan:** [`winston-lab-eval-grok-cli.md`](../../plans/winston-lab-eval-grok-cli.md)  
**Interface:** [`winston-mcp-tools.md`](../../interfaces/winston-mcp-tools.md) v0.5

**Banner:** report only — no pack promotion. No Broker Gateway `order_write`.
Cromwell Telegram uses compose-network MCP for **ops** tools only — **not**
`wut_execute_portfolio_backtest_run` (off [cron allowlist](cron-tool-allowlist.md)).

**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`

**Cromwell vs Grok Bot:** Desk plane (Telegram) must not start Portfolio Backtest
Runs (PBRs). Builder / Grok Bot Shell may.

Smoke PBR **#596** (`mint_rst_turtle_r01`) is **pending**. Do **not** execute it
in these examples: full-window Mint Turtle is **hours** of CPU.

## Preferred hop — MCP `call_tool` (Phase B, live)

From sawtooth root. Proven: `podman exec winston_mcp python3` + `call_tool` from
`mcp_winston.server`.

```bash
# list
podman exec winston_mcp python3 -c '
import asyncio
from mcp_winston.server import call_tool
print(asyncio.run(call_tool("wut_list_experiment_cells", {"experiment": "strategy77_rst_heat_risk_v1"}))[0].text)
'

# get PBR 596
podman exec winston_mcp python3 -c '
import asyncio
from mcp_winston.server import call_tool
print(asyncio.run(call_tool("wut_get_portfolio_backtest_run", {"pbr_id": 596}))[0].text)
'

# create — idempotent reuse of mint_rst_turtle_r01
podman exec winston_mcp python3 -c '
import asyncio
from mcp_winston.server import call_tool
print(asyncio.run(call_tool("wut_create_portfolio_backtest_run", {
  "authorization": "lab_geometry_report_only",
  "portfolio_id_or_name": "Portfolio Mint",
  "trading_strategy_name": "TurtleV1 S2 Breakout55/20",
  "parent_pbr_id": 432,
  "experiment": "strategy77_rst_heat_risk_v1",
  "cell_key": "mint_rst_turtle_r01",
  "fill_cadence": "resting_stop_touch",
  "heat_mode": "turtle",
  "risk_percentage": 0.01,
}))[0].text)
'
```

Do **not** call `wut_execute_portfolio_backtest_run` on #596 from this hop.

## Rails-runner hop (Phase A harness)

```bash
./bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/strategy_fill_heat_risk_matrix_{setup,execute,scorecard}.rb
```

Pass env **into the container**: `-e WRITE=1`, `-e FULL=1`, `-e EXECUTE=1`.
Default setup is **smoke** (one Mint cell). `FULL=1` is the 32-cell UAT — do not
run unless operator / Grok Bot is doing UAT.

```bash
# smoke setup (idempotent; pending #596)
./bin/compose exec -T winston_unit_test \
  bin/rails runner lib/scripts/strategy_fill_heat_risk_matrix_setup.rb

# scorecard after completed cells
./bin/compose exec -T -e WRITE=1 winston_unit_test \
  bin/rails runner lib/scripts/strategy_fill_heat_risk_matrix_scorecard.rb

# UAT only — 32 cells
./bin/compose exec -T -e FULL=1 winston_unit_test \
  bin/rails runner lib/scripts/strategy_fill_heat_risk_matrix_setup.rb
```

`EXECUTE=1` on setup (or the `execute` runner) sync-runs pending smoke cells.
**Do not** use it on #596 unless you intend hours of CPU.

## Wrapper

`./bin/lab-eval` (if present; otherwise the copy-paste above still works):

```bash
./bin/lab-eval setup
./bin/lab-eval list
./bin/lab-eval get 596
./bin/lab-eval score
./bin/lab-eval execute 596              # REFUSE without --i-mean-it
./bin/lab-eval execute 596 --i-mean-it  # hours of CPU — do not run on #596 casually
```

`execute` must be gated. Missing wrapper → MCP / rails-runner hops.

## Chief of Staff dispatch (Phase D)

Pasteable briefs (Builder plane — not Cromwell Telegram):

| Role | Brief | Grok CLI skill |
|------|--------|----------------|
| Lab Sweep | [`grok-bot-lab-sweep.md`](grok-bot-lab-sweep.md) | `/lab-sweep` |
| Edge Scorecard | [`grok-bot-edge-scorecard.md`](grok-bot-edge-scorecard.md) | `/edge-scorecard` |

Default: Sweep lists/creates **smoke** only. Scorecard: if #596 is still pending, **no winner**. 32-cell UAT and execute only when the operator says so.

## Artifacts

Winston Unit Test (WUT) bind: `ecosystem/docs/analysis/` → `/ecosystem/docs/analysis`.

| What | Path |
|------|------|
| Setup (exists) | `ecosystem/docs/analysis/2026-09-13-strategy77-rst-heat-risk-setup.json` |
| Scorecard | `ecosystem/docs/analysis/YYYY-MM-DD-strategy77-rst-heat-risk-matrix.{json,md}` |

## Recreate gotchas

MCP image is **not** bind-mounted — rebuild after `mcp_winston/` edits:

```bash
podman-compose build winston_mcp
```

- Recreating `winston_mcp` requires removing `nanobot_cromwell` first (`--requires`).
- Recreating `winston_unit_test` requires removing `winston_mcp` then `nanobot_cromwell`.
- `podman-compose up --no-deps` may still bounce redis / WUT / Winston v2 (Wv2) —
  `podman start` the named containers after.

See [`recreate-winston-mcp.md`](recreate-winston-mcp.md).
