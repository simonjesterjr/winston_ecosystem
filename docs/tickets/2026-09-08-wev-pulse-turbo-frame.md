# Ticket: Pulse tablets via Turbo Frame (no WebSockets)

**Status:** Proposed
**Priority:** P2
**Mode:** normal
**Program:** Winston Ecosystem View
**Parent:** [`2026-09-07-winston-ecosystem-view.md`](2026-09-07-winston-ecosystem-view.md)
**Graph nodes:** winston_v2, ecosystem
**Edges:** `interfaces/winston-ecosystem-view-v1.md`, ADR-005
**Depends on:** DM Pulse emit (`DownloadTask` running rows) — shipped 2026-09-08
**Human gates:** none (read-only UI)
**DoD:** Pulse tablets refresh without `setInterval(fetch)` in `wev-live.js`; first paint still metadata-only; no Action Cable

## Why

Winston Ecosystem View Pulse currently polls `GET /operations/ecosystem/pulse` every 3s from inline JS. Architecture Decision Record 005 already names Hotwire (Turbo Frames) as the progressive-fill tool. Replacing the timer with a Turbo Frame (or morph refresh) keeps HTTP, drops custom poller, and does **not** require WebSockets.

## Not this ticket

- Action Cable / `ws://…/wv2/cable` — see [`2026-09-08-wev-pulse-action-cable.md`](2026-09-08-wev-pulse-action-cable.md)
- Per-symbol Telegram lines

## Work

1. Enable Turbo **on this page only** (Wv2 ops-shell still has no importmap/Turbo globally).
2. Wrap queue / cron / work tablets in a Turbo Frame that reloads ~3s while the Pulse tab is open.
3. Keep SVG `flowing` / `busy` class hooks in a tiny Stimulus controller or the existing `wev-live.js` fed by the frame’s JSON/data attributes.
4. Spec: frame request is cheap (no parquet); idle Pulse stays still.
