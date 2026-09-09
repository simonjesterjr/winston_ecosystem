# Winston Ecosystem View — contracts v1

**Owner:** `ecosystem/`  
**Consumers:** inventory CLI, static console, Wv2 `/operations/ecosystem`  
**Status:** draft (tournament synthesis 2026-09-07)  
**Related:** `plans/winston-ecosystem-view.md`, ADR-005, ADR-006, ADR-007

Read-only. Does not book, activate, or Capital-Activate.

Every projected field is either a value with `source`, or `{ "status": "UNKNOWN", "reason": "..." }`. Never coerce missing to `0`.

Forbidden keys on Pulse documents: `return_pct`, `sharpe`, `pcs`, `pbr`, `equity`.  
Forbidden keys on Book Board documents: `queue_depth`, `cpu`, `restart_count`.

---

## Envelope

```json
{
  "schema": "winston-ecosystem-view/v1",
  "generated_at": "2026-09-07T22:00:00Z",
  "planes": {
    "poster": {},
    "pulse": {},
    "book_board": {},
    "codebase": { "status": "UNKNOWN", "reason": "no CodeScene/CodeCity in repo" }
  }
}
```

---

## ComponentStatus (Pulse + Poster legend)

```json
{
  "id": "winston_v2_sidekiq",
  "plane": "pulse",
  "parent": "wv2",
  "health": "ok | degraded | down | UNKNOWN",
  "lag": null,
  "error_budget": null,
  "note": "compose has no healthcheck; podman often stays starting",
  "live": true,
  "status": "Up 24 minutes (starting)"
}
```

`parent` ∈ `wv2 | wut | dm | bg | ai | infra | host`.  
IBKR CPGW: `id=ibkr_cpgw`, `parent=host`, `live=UNKNOWN` unless separately probed.

---

## QueueSnapshot (Pulse)

```json
{
  "name": "expected_returns",
  "owning_monolith": "wut",
  "redis_db": 1,
  "depth": 227000,
  "retry": null,
  "dead": null,
  "p50_wait": { "status": "UNKNOWN", "reason": "not stored" },
  "p95_wait": { "status": "UNKNOWN", "reason": "not stored" },
  "oldest_job_age": { "status": "UNKNOWN", "reason": "not stored" },
  "last_error_class": { "status": "UNKNOWN", "reason": "not stored" },
  "slo": null,
  "health": "degraded",
  "alerts": ["depth>=100", "worker -q subscription UNKNOWN"]
}
```

`slo` is null until a documented product SLO exists. Inventory may still **flag** depth≥100 / dead≥10. Those flags are not `health` and not a product SLO. `health` on a queue snapshot means Redis was reachable. `expected_returns` is a producer-only graveyard unless a worker `-q` exists (`discard_on StandardError` — those jobs do not become the dead set).

---

## CronSnapshot (Pulse)

```json
{
  "id": "daily_analysis",
  "owner": "wv2",
  "schedule": "30 16 * * 1-5 America/Denver",
  "class": "DailyAnalysisJob",
  "last_ok": { "status": "UNKNOWN", "reason": "sidekiq-cron last-ok not read" },
  "last_duration": { "status": "UNKNOWN" },
  "next_run": { "status": "UNKNOWN" },
  "overdue": { "status": "UNKNOWN" },
  "watermark": "DAR scored session"
}
```

---

## DataWatermark (Pulse)

```json
{
  "dataset": "winston_eod_parquet",
  "symbol": "AAPL",
  "asof": "2026-09-05",
  "expected_asof": "2026-09-05",
  "lag_days": 0,
  "blocking_books": { "status": "UNKNOWN", "reason": "OP block list not wired" },
  "source": "DataCoverage.latest vs CompletedNySession.date"
}
```

`feature_asof` per universe: UNKNOWN (not implemented in DM Ruby).  
`roll_calendar`: absent.  
`corporate_actions`: no cron (rake only).

---

## OperationalPortfolioRow (Book Board world)

Not a CONTEXT **Book**. `execution_mode` is `paper` \| `real`.

```json
{
  "object_type": "operational_portfolio",
  "id": 11,
  "name": "Mint · a1b2c3d4",
  "seed_name": "Mint",
  "fingerprint": "a1b2c3d4…",
  "execution_mode": "real",
  "export_kind": "trade_ready",
  "active": true,
  "closed": false,
  "attention_band": "real",
  "markets": ["TLT", "GLD"],
  "trading_strategy": "FastBO5",
  "fulfillment_adapter_key": "dummy_sim",
  "monolith_owner": "wv2",
  "scores": { "pcs": {}, "pbr": {}, "equity": {}, "mms": {}, "dar": {} }
}
```

`attention_band` = `Operations::AttentionBands.band_for` (`real` \| `paper` \| `inactive`).

Lab objects, if ever shown: `"object_type": "lab_pbr"` — never mixed silently.

---

## ScoreProjection

Each inner object:

```json
{ "status": "ok", "value": 12.4, "unit": "pct", "source": "Operations::PortfolioEquitySeries" }
```

or `{ "status": "UNKNOWN", "reason": "not stored on OP" }`.

Allowed sources only: PBR columns, PCS snapshot (`books_key`), ops equity series, MMS scorer, DAR scored-session status.  
**No composite.** `vol`, `expectancy`, `signal_idle_bars`, `paper_live_hash_ok`, `expression_rev` default UNKNOWN.

---

## ExpressionProjection

```json
{
  "trading_strategy": "FastBO5",
  "fingerprint": "…",
  "universe": { "markets": ["TLT", "GLD"] },
  "features": { "standard": "winston_eod", "owner": "dm" },
  "signal": { "primary": "Breakout20DayStrategy" },
  "filter": { "confirmational": [] },
  "sizer": { "status": "UNKNOWN", "reason": "PositionSizer path not projected" },
  "risk": { "evaluation": "static" },
  "execution": { "fulfillment_adapter_key": "dummy_sim" },
  "ledger": { "kind": "cash_event_plus_journal" }
}
```

This is a **view** of TradingStrategy + OP. Not a pipeline engine.

---

## Book Board projection (C math, CSS/SVG)

World right-handed: +x along shelf, +z away (depth), +y up.

```
depth_plane(op):
  closed or not active → 2 (far)
  else if execution_mode == "real" → 0 (near)
  else → 1 (mid)
```

`export_kind` does not change shelf.

Isometric 2:1:

```
sx = OX + (x - z) * (TILE_W / 2)
sy = OY + (x + z) * (TILE_H / 2) - y * ELEV
```

Default `TILE_W=72`, `TILE_H=36`, `ELEV=36`.  
Table row id = slab id. Pick either → same detail pane.

Tint: ops current drawdown when series present; else `--ops-muted` + UNKNOWN chip.  
Badge: integrity/pulse boolean only — not decoration.

On `prefers-reduced-motion` or viewport `<900px`: table only.

---

## Navigation

Poster node → runtime containers for that parent → queues it produces/consumes → OPs it owns → TradingStrategy in repo.  
Reverse: OP → fingerprint → wv2 → last jobs (UNKNOWN if not stored) → watermarks.

---

## Pulse live document (`GET /operations/ecosystem/pulse`)

Polled by the Pulse plane (3s). Not first-paint HTML. Forbidden keys: `return_pct`, `sharpe`, `pcs`, `pbr`, `equity`.

```json
{
  "schema": "winston-ecosystem-view-pulse/v1",
  "generated_at": "2026-09-08T01:00:00Z",
  "owners": { "dm": { "queues": {}, "busy": 0, "cron": [], "jobs": [] } },
  "dm": { "status": "ok", "running_symbols": ["IBM"], "events": [] },
  "flows": [{ "from": "eodhd", "to": "data_manager", "kind": "http", "label": "IBM", "state": "live" }],
  "nodes_busy": ["eodhd", "data_manager", "data_manager_sidekiq"]
}
```

`state` is `live` (Sidekiq busy or DM running task) or `recent` (Cromwell `symbol_updated` within 15 minutes). UI must not animate idle edges.
