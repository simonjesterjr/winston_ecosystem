# Ticket: Pulse emit from WUT / Wv2 / BG jobs (after DM)

**Status:** In progress
**Priority:** P2
**Mode:** contractor
**Program:** Winston Ecosystem View
**Parent:** [`2026-09-07-winston-ecosystem-view.md`](2026-09-07-winston-ecosystem-view.md)
**Graph nodes:** winston_unit_test, winston_v2, broker_gateway, data_manager, ecosystem
**Depends on:** DM Pulse emit — shipped 2026-09-08
**DoD:** Pulse Work tablet shows operator titles (`Daily Analysis · {date}` / `Portfolio Backtest Run {id} · {name}`) while those jobs run, including MCP `perform_now`. Tickle / health / expected_returns stay silent. No shared Pulse DB. Contract: `wev:pulse:work` HASH on the owner Redis DB.

## Why

data_manager now writes `DownloadTask` while a symbol is in flight. Winston Unit Test (WUT) backtests, Winston v2 Daily Analysis, and Broker Gateway tickle still only show as Sidekiq `busy` counts / queue depth. Fine for “is the worker awake”; not “Daily Analysis on Mint” or “PBR 550 running.”

## Work (when someone stares at Pulse during those jobs)

- [x] Contract: Pulse Work Record on `winston-ecosystem-view-pulse/v1` (`wev:pulse:work` HASH, `PUBLISH wev:pulse`). Poll and future Cable are both readers.
- [x] WUT: PBR / single backtest / optimization / daily ops / PCS / Quiver lab / data sync / backup. Silent: expected_returns, Cable broadcast.
- [x] Wv2: Daily Analysis (`subject` walks Operational Portfolios) / MMS / Intake (only when it worked) / WQ fill+ingest / Congress LS / hourly radar aggregate.
- [x] DM: orchestrators + acquire rows beside `DownloadTask`. Silent: health check.
- [x] BG: refresh / place order / sandbox fills. Silent: tickle.

Until named HASH is empty, projector falls back to Sidekiq `busy` / queued args.
