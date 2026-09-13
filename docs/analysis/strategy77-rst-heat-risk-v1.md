# Strategy 77 × resting stop-touch × heat × risk — lab companion

**Experiment:** `strategy77_rst_heat_risk_v1`  
**Plan:** [`ecosystem/plans/winston-lab-eval-grok-cli.md`](../../plans/winston-lab-eval-grok-cli.md)  
**Config:** [`strategy77-rst-heat-risk-v1.config.json`](strategy77-rst-heat-risk-v1.config.json)  
**Banner:** **report only — no pack promotion**

## Panel

UAT: 8 turtle books × 2 heat (`legacy`, `turtle`) × 2 risk (`0.01`, `0.02`) × `resting_stop_touch` = **32 cells**.

Books: Blue, Mango, Mint, Yellow, Orange, Red, Green, Rust. TS name `TurtleV1 S2 Breakout55/20`. Capital $10k. Chassis freeze in the config.

Parent window: per-book `turtle_systems_v1` cell_key **`B1`** (S2). Inherit overlapping dates from that parent PBR.

Setup default is **smoke** (Mint × turtle × 1%). `FULL=1` is Grok Bot UAT after Phase B+C — **not Phase A**.

## Invoke (compose)

Scripts: WUT `lib/scripts/strategy_fill_heat_risk_matrix_{setup,execute,scorecard}.rb`.

```bash
# Phase A smoke (default): create pending Mint × turtle × 0.01. Idempotent.
./bin/compose exec -T winston_unit_test \
  bin/rails runner lib/scripts/strategy_fill_heat_risk_matrix_setup.rb

# Optional: create then sync-execute the smoke cell only (not the 32).
./bin/compose exec -T -e EXECUTE=1 winston_unit_test \
  bin/rails runner lib/scripts/strategy_fill_heat_risk_matrix_setup.rb

# Or execute pending smoke cells / explicit ids.
./bin/compose exec -T winston_unit_test \
  bin/rails runner lib/scripts/strategy_fill_heat_risk_matrix_execute.rb

# After cells complete: score. Pass WRITE into the container.
./bin/compose exec -T -e WRITE=1 winston_unit_test \
  bin/rails runner lib/scripts/strategy_fill_heat_risk_matrix_scorecard.rb
```

Grok Bot UAT later: same runners (or MCP Wave 1) with `FULL=1` for the 32. Shell hop: [`docs/operations/grok-bot-shell-lab-eval.md`](../operations/grok-bot-shell-lab-eval.md) and `./bin/lab-eval`. Compose bind: `./ecosystem/docs/analysis` → `/ecosystem/docs/analysis` on `winston_unit_test` (+ sidekiq). Recreating WUT requires dropping `winston_mcp` then `nanobot_cromwell` first (`--requires`).

## Scorecard (`WRITE=1`)

- `ecosystem/docs/analysis/YYYY-MM-DD-strategy77-rst-heat-risk-matrix.json`
- sibling `.md`

JSON keys are **`edge_v1`**: `edge_r`, `profit_factor`, `edge_n`, `edge_components`, glance (`n<20` hide / 20–99 thin / ≥100 glance), heat_skips. **Not** `expectancy_r`. `costs=fill_only`. Rank by `edge_r`.
