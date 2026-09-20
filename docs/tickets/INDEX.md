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
| P0 | Proposed | [`2026-09-20-mode-c-leap-exit-at-stop-option-mark.md`](2026-09-20-mode-c-leap-exit-at-stop-option-mark.md) | Mode C LEAP stop-out books option mark, not underlying Working Stop — [wrap](../session-reports/2026-09-20-1140-standard-call-packaging-rung.md) |
| P1 | In progress | [`2026-09-18-cpgw-host-lifecycle-in-ecosystem.md`](2026-09-18-cpgw-host-lifecycle-in-ecosystem.md) | CPGW host lifecycle (restart / systemd / HTTP helper) — CLI restart + control service for Desk/BG/Wv2 |
| P1 | Proposed | [`2026-09-18-wut-macd-confirm-and-trend-phase-pyramid.md`](2026-09-18-wut-macd-confirm-and-trend-phase-pyramid.md) | WUT MACD confirmational + trend-phase pyramid geometry (new PBR feature) |
| P1 | In progress | [`2026-09-17-mode-c-new-books-pcs-60-90.md`](2026-09-17-mode-c-new-books-pcs-60-90.md) | Mode C new books — Copper/Slate live; Indigo/Teal **evolved** (see 2026-09-18 ticket) |
| P1 | Done — scoreboard open | [`2026-09-18-mode-c-indigo-teal-evolved.md`](2026-09-18-mode-c-indigo-teal-evolved.md) | Mode C evolve Indigo/Teal (Wv2 1583/1584; clones 1579/1580 off) — archive when PBRs 723–728 scoreboard closes |
| P2 | In progress | [`2026-09-08-wev-pulse-other-monolith-emits.md`](2026-09-08-wev-pulse-other-monolith-emits.md) | WEV Pulse emit from WUT/Wv2/BG + **remaining nanobot_cromwell DAR** — [parent](2026-09-07-winston-ecosystem-view.md) · correlated PR #4/#5 archived |
| P1 | Proposed | [`2026-09-18-wev-pulse-glance-ux.md`](2026-09-18-wev-pulse-glance-ux.md) | WEV Pulse glance UX — clear attention, active-work list/focus, desktop wall scale — [issue](../issues/2026-09-18-wev-pulse-glance-attention-and-desktop-scale.md) |
| P1 | In progress | [`2026-09-17-cromwell-daily-state-verifier.md`](2026-09-17-cromwell-daily-state-verifier.md) | Cromwell daily STATE + stop/skip + verifier skill on 8b — [loop L1](2026-07-19-loop-engineering-evolution-mode.md) |
| P2 | Proposed | [`2026-09-18-loop-two-model-checker.md`](2026-09-18-loop-two-model-checker.md) | Two-model checker — 8b STATE then 3b verifier — [loop L1.5](2026-07-19-loop-engineering-evolution-mode.md) |
| P1 | Proposed | [`2026-09-17-eod-pending-15-human-confirm.md`](2026-09-17-eod-pending-15-human-confirm.md) | Human confirm 2026-09-17 pending drafts (EOD verifier skipped) |
| P2 | Proposed | [`2026-09-17-compose-nanobot-recreate-cascade.md`](2026-09-17-compose-nanobot-recreate-cascade.md) | podman-compose nanobot recreate cascades Redis/Wv2/Ollama |
| P2 | Proposed | [`2026-09-17-leap-aware-dar-narrative.md`](2026-09-17-leap-aware-dar-narrative.md) | LEAP-aware DAR/EOD narrative from MCP facts |
| P3 | Proposed | [`2026-09-17-cromwell-cron-dual-route-3b.md`](2026-09-17-cromwell-cron-dual-route-3b.md) | Dual-route Cromwell cron to 3b (sessionKey model routing) |
| P1 | In progress | [`2026-09-17-promote-screen-yellow-rust-walnut-mint.md`](2026-09-17-promote-screen-yellow-rust-walnut-mint.md) | Promote screen Y/Rust/Walnut/Mint — multi-TS ×1%/2%; else new books |
| P1 | In progress | [`2026-09-18-bg-option-candidates-quotes.md`](2026-09-18-bg-option-candidates-quotes.md) | BG option_candidates — real OPT conid + CPGW snapshot quotes — [Mode C prefill](../../plans/wv2-bg-ibkr-leap-fulfillment.md) |
| P3 | Proposed | [`2026-09-19-mirror-ponytail-apply-skill.md`](2026-09-19-mirror-ponytail-apply-skill.md) | Mirror `/ponytail-apply` skill into Rails monoliths — [WUT wrap](../../../winston_unit_test/docs/session-reports/2026-09-19-1233-wut-ponytail-apply.md) |
| P2 | Proposed | [`2026-09-19-leap-instrument-label-occ-vs-ticker.md`](2026-09-19-leap-instrument-label-occ-vs-ticker.md) | LEAP instrument label OCC vs ticker — **needs design session** — [wrap](../session-reports/2026-09-18-1720-mode-c-leap-desk-prefill.md) |
| P3 | Proposed | [`2026-09-16-podman-nvidia-cdi-cleanup.md`](2026-09-16-podman-nvidia-cdi-cleanup.md) | Rootless Podman NVIDIA CDI cleanup (ollama still on classic `/dev/nvidia*` + lib binds) |
| P1 | In progress | [`2026-09-15-wv2-leap-packaging-fields.md`](2026-09-15-wv2-leap-packaging-fields.md) | Wv2 Mode C — DA + desk GET LEAP prefill (premium × 100 × contracts) — [plan](../../plans/wv2-bg-ibkr-leap-fulfillment.md) · [BG quotes](2026-09-18-bg-option-candidates-quotes.md) |
| P1 | In progress | [`2026-09-18-mode-c-leap-preferred-underlying-fallback.md`](2026-09-18-mode-c-leap-preferred-underlying-fallback.md) | Mode C LEAP→underlying fallback — draft Wv2 [#7](https://github.com/simonjesterjr/winston_v2/pull/7) — [UI](2026-09-18-wv2-workflow-fulfillment-justification.md) |
| P1 | In progress | [`2026-09-18-wv2-workflow-fulfillment-justification.md`](2026-09-18-wv2-workflow-fulfillment-justification.md) | Desk Justification panel — draft Wv2 [#7](https://github.com/simonjesterjr/winston_v2/pull/7) — [behavior](2026-09-18-mode-c-leap-preferred-underlying-fallback.md) |
| P1 | In progress | [`2026-09-19-standard-call-fulfillment-packaging-rung.md`](2026-09-19-standard-call-fulfillment-packaging-rung.md) | Standard (non-LEAP) long call as ADR-018 packaging rung — Wv2 selector first; WUT out of scope — [design](../analysis/2026-09-19-standard-call-packaging-rung.md) |
| P1 | Proposed | [`2026-09-20-bg-option-candidates-greeks.md`](2026-09-20-bg-option-candidates-greeks.md) | BG option_candidates delta/OI for standard_call filter — [quotes](2026-09-18-bg-option-candidates-quotes.md) |
| P1 | Proposed | [`2026-09-20-standard-call-flatten-roll-desk.md`](2026-09-20-standard-call-flatten-roll-desk.md) | Wire standard_call flatten/roll DTE to desk tasks — helper exists |
| P2 | Proposed | [`2026-09-01-fulfillment-packaging-policy-ops-ui.md`](2026-09-01-fulfillment-packaging-policy-ops-ui.md) | Fulfillment Packaging Policy ops UI — jsonb store already on OP (2026-09-20) |
| P3 | Proposed | [`2026-09-20-wut-standard-call-plan-b-parity.md`](2026-09-20-wut-standard-call-plan-b-parity.md) | WUT lab parity for standard_call / Plan B — only if operator asks |
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

