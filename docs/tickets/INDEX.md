# Active tickets index

Backlog view for `ecosystem/docs/tickets/`. **Done / Completed / Superseded** → [`archive/`](archive/).

## Priority convention

```markdown
**Status:** Proposed
**Priority:** P1
```

| Priority | Meaning |
|----------|---------|
| **P0** | Blocking capital safety, data corruption, or live Telegram/ops failure — work now |
| **P1** | Near-term product/ops path (current epic or paper desk) |
| **P2** | Important but can wait a cycle |
| **P3** | Nice-to-have / cleanup |
| **unset** | Not yet ranked |

## How to triage

1. Serious defects → `docs/issues/` via `manage-issue-ticket`; link from ticket.
2. **Done** → move file to `archive/`.
3. Prefer few **In progress**.

## Program trackers (not a substitute for the table)

| Program | File |
|---------|------|
| Winston Ecosystem View (four-plane console) | [`2026-09-07-winston-ecosystem-view.md`](2026-09-07-winston-ecosystem-view.md) |
| Trend Following six-principles competency | [`2026-09-04-tf-foundations-INDEX.md`](2026-09-04-tf-foundations-INDEX.md) |
| DM ponytail cleanup (2026-09-13) | [`../../../data_manager/docs/tickets/INDEX.md`](../../../data_manager/docs/tickets/INDEX.md) |

## Active tickets

| Priority | Status | File | Title |
|----------|--------|------|-------|
| P1 | In progress | [`2026-09-18-cpgw-host-lifecycle-in-ecosystem.md`](2026-09-18-cpgw-host-lifecycle-in-ecosystem.md) | CPGW host lifecycle (restart / systemd / HTTP helper) — CLI restart + control service for Desk/BG/Wv2 |
| P1 | In progress | [`2026-09-17-mode-c-new-books-pcs-60-90.md`](2026-09-17-mode-c-new-books-pcs-60-90.md) | Mode C new books Indigo/Teal/Copper/Slate — PCS 60–90 compile + TS75 stamp |
| P2 | In progress | [`2026-09-08-wev-pulse-other-monolith-emits.md`](2026-09-08-wev-pulse-other-monolith-emits.md) | WEV Pulse emit from WUT/Wv2/BG + **remaining nanobot_cromwell DAR** — [parent](2026-09-07-winston-ecosystem-view.md) · correlated PR #4/#5 archived |
| P1 | In progress | [`2026-09-17-cromwell-daily-state-verifier.md`](2026-09-17-cromwell-daily-state-verifier.md) | Cromwell daily STATE + stop/skip + verifier skill on 8b — [loop L1](2026-07-19-loop-engineering-evolution-mode.md) |
| P1 | Proposed | [`2026-09-17-eod-pending-15-human-confirm.md`](2026-09-17-eod-pending-15-human-confirm.md) | Human confirm 2026-09-17 pending drafts (EOD verifier skipped) |
| P2 | Proposed | [`2026-09-17-compose-nanobot-recreate-cascade.md`](2026-09-17-compose-nanobot-recreate-cascade.md) | podman-compose nanobot recreate cascades Redis/Wv2/Ollama |
| P2 | Proposed | [`2026-09-17-leap-aware-dar-narrative.md`](2026-09-17-leap-aware-dar-narrative.md) | LEAP-aware DAR/EOD narrative from MCP facts |
| P3 | Proposed | [`2026-09-17-cromwell-cron-dual-route-3b.md`](2026-09-17-cromwell-cron-dual-route-3b.md) | Dual-route Cromwell cron to 3b (sessionKey model routing) |
| P1 | In progress | [`2026-09-17-promote-screen-yellow-rust-walnut-mint.md`](2026-09-17-promote-screen-yellow-rust-walnut-mint.md) | Promote screen Y/Rust/Walnut/Mint — multi-TS ×1%/2%; else new books |
| P1 | Proposed | [`2026-09-16-wv2-paper-leap-eval-red-from-692.md`](2026-09-16-wv2-paper-leap-eval-red-from-692.md) | Wv2 paper Red from WUT #692 — $30k Mode C; replace existing Red OPs (after Blue) |
| P3 | Proposed | [`2026-09-16-podman-nvidia-cdi-cleanup.md`](2026-09-16-podman-nvidia-cdi-cleanup.md) | Rootless Podman NVIDIA CDI cleanup (ollama still on classic `/dev/nvidia*` + lib binds) |
| P1 | In progress | [`2026-09-16-wv2-paper-leap-eval-blue-from-685.md`](2026-09-16-wv2-paper-leap-eval-blue-from-685.md) | Wv2 paper Blue from WUT #685 — IBKR-eval LEAP, paper-only fulfill (deactivate ops 381) — [analysis](../analysis/2026-09-16-pbr685-blue-leap-s1-2pct.md) |
| P1 | Proposed | [`2026-09-15-wv2-leap-packaging-fields.md`](2026-09-15-wv2-leap-packaging-fields.md) | Wv2 Model B — stamp OCC packaging on handoff/slate — [plan](../../plans/wv2-bg-ibkr-leap-fulfillment.md) · [ADR-017](../adr/ADR-017-leap-packaging-precalc-occ.md) |
| P1 | Proposed | [`2026-09-15-bg-ibkr-opt-order-intent-prove.md`](2026-09-15-bg-ibkr-opt-order-intent-prove.md) | BG OPT Order Intent + IBKR paper 1×1 prove — [plan](../../plans/wv2-bg-ibkr-leap-fulfillment.md) · [ADR-017](../adr/ADR-017-leap-packaging-precalc-occ.md) |
| P1 | In progress | [`2026-09-04-tf-p3-live-sizing-and-capital-authority.md`](2026-09-04-tf-p3-live-sizing-and-capital-authority.md) | Spending Capacity + Capital Authority into sizer/slate — [plan](../../plans/spending-capacity-and-leap-fulfillment.md) |
| P1 | Proposed | [`2026-09-09-extra-modal-leap-unit-evaluation.md`](2026-09-09-extra-modal-leap-unit-evaluation.md) | Extra-modal LEAP vs share unit — read-only 1×1 unblocked — [plan](../../plans/wv2-bg-ibkr-leap-fulfillment.md) · [ADR-017](../adr/ADR-017-leap-packaging-precalc-occ.md) · [law](../business-context/leap-extra-modal-proxy.md) |
| P1 | In progress | [`../../../winston_unit_test/docs/tickets/2026-09-14-wut-leap-packaged-pbr-faithful-sim.md`](../../../winston_unit_test/docs/tickets/2026-09-14-wut-leap-packaged-pbr-faithful-sim.md) | WUT LEAP-packaged PBR sim (lab Black-Scholes; #666 was hybrid shares) |
| P2 | Proposed | [`../../../data_manager/docs/tickets/2026-09-13-dm-ponytail-delete-dead-skeleton.md`](../../../data_manager/docs/tickets/2026-09-13-dm-ponytail-delete-dead-skeleton.md) | DM ponytail 1/5 — delete dead skeleton surface |
| P2 | Proposed | [`../../../data_manager/docs/tickets/2026-09-13-dm-ponytail-stop-persisting-bars-json.md`](../../../data_manager/docs/tickets/2026-09-13-dm-ponytail-stop-persisting-bars-json.md) | DM ponytail 4/5 — stop persisting `bars.json` |
| P3 | Proposed | [`../../../data_manager/docs/tickets/2026-09-13-dm-ponytail-drop-unused-gems.md`](../../../data_manager/docs/tickets/2026-09-13-dm-ponytail-drop-unused-gems.md) | DM ponytail 2/5 — drop unused gems |
| P3 | Proposed | [`../../../data_manager/docs/tickets/2026-09-13-dm-ponytail-drop-unused-frontend.md`](../../../data_manager/docs/tickets/2026-09-13-dm-ponytail-drop-unused-frontend.md) | DM ponytail 3/5 — drop unused frontend stack |
| P3 | Proposed | [`../../../data_manager/docs/tickets/2026-09-13-dm-ponytail-shrink-standardizer.md`](../../../data_manager/docs/tickets/2026-09-13-dm-ponytail-shrink-standardizer.md) | DM ponytail 5/5 — shrink standardizer |
| P2 | In progress | [`2026-09-11-measuring-edge-scoreboard.md`](2026-09-11-measuring-edge-scoreboard.md) | Edge (R) + E-ratio scoreboard — WUT PBR + Wv2 live/DAR/MMS |
| P3 | Proposed | [`2026-09-11-fulfillment-desk-adapters-yield-browser-verify.md`](2026-09-11-fulfillment-desk-adapters-yield-browser-verify.md) | Browser-verify All adapters header + Session Yield |
| P2 | Proposed | [`2026-09-10-unit-risk-vs-parked-gtc.md`](2026-09-10-unit-risk-vs-parked-gtc.md) | Remaining unit risk vs parked GTC when the row stop differs |
| P3 | Proposed | [`2026-09-10-signal-inspect-first-paint-eval-card.md`](2026-09-10-signal-inspect-first-paint-eval-card.md) | Browser-verify Signal Inspect first-paint Evaluation card |
| P3 | Proposed | [`2026-09-10-dar-wq-open-lots-unit-risk.md`](2026-09-10-dar-wq-open-lots-unit-risk.md) | Unit-risk column on DAR and Winston Quiver open-lot tables |
| P3 | Proposed | [`2026-09-09-wut-dataset-dm-sync-dead-jobs.md`](2026-09-09-wut-dataset-dm-sync-dead-jobs.md) | WUT DataSetDmSyncJob dead-lettered on unacquirable / unmapped symbols |
| P1 | In progress | [`2026-09-13-cpgw-force-true-empty-open-orders.md`](2026-09-13-cpgw-force-true-empty-open-orders.md) | BG `open_orders` empty while DUT still holds live Day/GTC — [issue](../issues/2026-09-13-cpgw-force-true-empty-open-orders.md) |
