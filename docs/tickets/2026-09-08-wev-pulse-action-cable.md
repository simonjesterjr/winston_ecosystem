# Ticket: Pulse push via Action Cable (after DM emit)

**Status:** Proposed
**Program:** Winston Ecosystem View
**Parent:** [`2026-09-07-winston-ecosystem-view.md`](2026-09-07-winston-ecosystem-view.md)
**Priority:** P2
**Mode:** contractor
**Graph nodes:** winston_v2, data_manager, ecosystem
**Edges:** `interfaces/winston-ecosystem-view-v1.md`, Tailscale Serve `/wv2`
**Depends on:** DM Pulse emit (DownloadTask) — shipped 2026-09-08; prefer Turbo Frame ticket first
**Human gates:** Tailscale Serve WebSocket path must work on phone `/wv2`
**DoD:** Pulse map updates on job start without a 3s client poll; Cable URL works behind Tailscale Serve; no PnL on the Pulse channel

## Why

Operators asked for live isometric Pulse (e.g. IBM moving while data_manager pulls). The **data** is now a running `DownloadTask`. Push delivery is optional: a desk that can wait 3s should keep polling or use the Turbo Frame ticket.

This ticket is the **2–4 day** stack, not the emit.

## Blocked until

1. DM `DownloadTask` start/finish is in production compose and visible on `GET /internal/pulse` during a real sync (verify on the 15:30 MT window).
2. Decide Cable is worth Tailscale Serve breakage vs 3s poll.

## Work

1. Uncomment Action Cable in Winston v2 (`config/application.rb`); add `cable.yml` on Redis DB `/2` (or a dedicated index — do not collide with Sidekiq).
2. Mount `/cable` under `RAILS_RELATIVE_URL_ROOT=/wv2`. Confirm Tailscale Serve forwards WebSocket upgrades.
3. Channel `EcosystemPulseChannel`; broadcast a fingerprint of `EcosystemPulse.call` when DM Pulse rows change (or a 1–2s server poller **if** no emit hook in Wv2).
4. Client: subscribe only on the Pulse tab; apply `flowing` / `busy`; tablets from the same payload.
5. Copy WUT’s `turbo_stream_from` / cable consumer as the reference — do not invent a second bus.
6. Spec + phone smoke: open `https://sawtooth-ai.tail944ffb.ts.net/wv2/operations/ecosystem` Pulse tab.

## Not this ticket

- Instrumenting WUT/Wv2 jobs the same way (separate if needed)
- OpenTelemetry traces
- Faking motion when idle
