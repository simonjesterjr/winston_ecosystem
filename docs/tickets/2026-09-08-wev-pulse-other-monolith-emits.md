# Ticket: Pulse emit from WUT / Wv2 / BG jobs (after DM)

**Status:** Proposed
**Priority:** P3
**Mode:** contractor
**Program:** Winston Ecosystem View
**Parent:** [`2026-09-07-winston-ecosystem-view.md`](2026-09-07-winston-ecosystem-view.md)
**Graph nodes:** winston_unit_test, winston_v2, broker_gateway, ecosystem
**Depends on:** DM Pulse emit — shipped 2026-09-08
**DoD:** Pulse Work tablet can name a live WUT/Wv2/BG job the same way it names IBM on DM, without inventing a shared DB

## Why

data_manager now writes `DownloadTask` while a symbol is in flight. Winston Unit Test (WUT) backtests, Winston v2 Daily Analysis, and Broker Gateway tickle still only show as Sidekiq `busy` counts / queue depth. Fine for “is the worker awake”; not “Daily Analysis on Mint” or “PBR 550 running.”

## Work (when someone stares at Pulse during those jobs)

- WUT: emit a cheap row or Redis key at PortfolioBacktestJob / DailyOperationsJob start/finish.
- Wv2: DailyAnalysisJob start (`as_of`, active OP count) / finish.
- BG: optional; tickle every minute should **not** spam the ticker.
- Contract: add optional `jobs[]` on `winston-ecosystem-view-pulse/v1` — no PnL fields.

Until then Pulse already peeks Sidekiq `busy` and queued args when present.
