# Ticket: Winston Ecosystem View (four-plane operator console)

**Status:** In progress
**Priority:** P2
**Mode:** contractor + tournament
**Program:** Winston Ecosystem View
**Graph nodes:** ecosystem, winston_v2, data_manager, winston_unit_test, broker_gateway
**Edges:** `interfaces/winston-ecosystem-view-v1.md`, root `compose.yml`, ADR-005/006/007
**Human gates:** no new compose service; no docker.sock; no Capital Activation chrome; no invented BookScore
**Scorecard:** glossary; no invented services; four planes; inventory-first; Pulse ≠ PnL; paper|real same schema
**DoD:** plan + contracts + poster + inventory CLI + ops-shell link; first paint ADR-005-safe

## Why

Operators cannot see Winston as it actually runs: four monoliths, containers, jobs, watermarks, and every paper/real Operational Portfolio.

## This session

- Tournament A/B/C judged. Synthesis: A ownership + B entry + C board math.
- Plan: `ecosystem/plans/winston-ecosystem-view.md`
- Inventory CLI: `ecosystem/ecosystem_view/bin/inventory`
- Wv2 door: `GET /operations/ecosystem`
- **Done 2026-09-08:** Isoflow poster; Pulse 3s poll + DM emit; Book Board Active-only stacked cubes; Code cuboids + work catalog.
- **Done 2026-09-08 (Code v2):** ADRs / tickets·issues / plans sub-tabs; cuboid metadata pane; document reader under the diagram (`public/ecosystem/work.json`).

## Follow-ons

- **Done 2026-09-08:** DM Pulse emit — `DownloadTask` running while a symbol is acquired (`DmPulseProgress`).
- **Done 2026-09-08:** Code plane work catalog (docs, not git/CI health).
- Near-term: [`2026-09-08-wev-pulse-turbo-frame.md`](2026-09-08-wev-pulse-turbo-frame.md), [`2026-09-08-wev-pulse-action-cable.md`](2026-09-08-wev-pulse-action-cable.md) (WebSockets after emit; skip until a desk needs ≪3s).
- [`2026-09-09-wev-code-plane-visual-qa.md`](2026-09-09-wev-code-plane-visual-qa.md) — operator clickthrough of Code tabs / metadata / reader
- [`2026-09-09-wev-index-work-owner-heuristic.md`](2026-09-09-wev-index-work-owner-heuristic.md) — catalog owner tags
- [`2026-09-09-wev-index-work-refresh-hook.md`](2026-09-09-wev-index-work-refresh-hook.md) — regenerate `work.json` when docs change
- [`2026-09-09-wev-work-json-split-bodies.md`](2026-09-09-wev-work-json-split-bodies.md) — split index vs bodies if Tailscale is slow
- Copy host inventory JSON onto the Tailscale page without lying
- Consume Score Projection sources after first paint (timeout-bounded)
- Code-health catalog when a real tool exists (git/CI — not the docs tablet)
- OTel traces if a collector is added
- Promotion gate after Capital Activation ships
- Drain/explain WUT `expected_returns` depth (Pulse finding, not this UI)
