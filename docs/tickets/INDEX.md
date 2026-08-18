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

## Active tickets

| Priority | Status | File | Title |
|----------|--------|------|-------|
| P1 | Proposed | [`2026-08-18-rust-11-drafts-937-938-desk.md`](2026-08-18-rust-11-drafts-937-938-desk.md) | Desk decision — Rust #11 drafts 937 (GOOGL) and 938 (RXT) |
| P3 | Proposed | [`2026-08-18-mcp-list-journals-for-portfolio.md`](2026-08-18-mcp-list-journals-for-portfolio.md) | MCP list-journals for a portfolio |
| P0 | Done | [`2026-08-18-after-close-eod-session-contract.md`](2026-08-18-after-close-eod-session-contract.md) | After-close EOD session contract (DM to-date + Wv2 exact bar) |
| P1 | Proposed | [`2026-08-18-observe-tuesday-unattended-eod-cycle.md`](2026-08-18-observe-tuesday-unattended-eod-cycle.md) | Observe Tuesday unattended EOD cycle (DM 15:30 MT → DAR 16:30 MT) |
| P2 | Proposed | [`2026-08-18-verify-ops-shell-pending-grouped-live.md`](2026-08-18-verify-ops-shell-pending-grouped-live.md) | Verify ops-shell Pending grouping on a live multi-OP mint |
| P1 | Done | [`2026-08-18-work-monday-catchup-desk-tasks.md`](2026-08-18-work-monday-catchup-desk-tasks.md) | Work Monday 2026-08-17 catch-up desk tasks (12 pending) |
| P2 | Proposed | [`2026-08-18-eodhd-lag-retry-after-close.md`](2026-08-18-eodhd-lag-retry-after-close.md) | EODHD lag retry when 15:30 MT pull misses today’s print |
| P2 | Proposed | [`2026-08-18-persist-dm-download-runs.md`](2026-08-18-persist-dm-download-runs.md) | Persist DM download_runs / download_tasks for after-close sync |
| P3 | Done | [`archive/2026-08-18-commit-wv2-signal-inspect-legend-sheet.md`](archive/2026-08-18-commit-wv2-signal-inspect-legend-sheet.md) | Commit leftover Wv2 signal-inspect legend sheet (`2d86e7a`) |
| P2 | Proposed | [`2026-08-17-exit-at-stop-classic-desk-and-ops-shell.md`](2026-08-17-exit-at-stop-classic-desk-and-ops-shell.md) | Ticket: Exit-at-stop on classic desk and ops shell |
| P2 | Proposed | [`2026-08-17-preserve-winston-signal-on-dar-stop-confirm.md`](2026-08-17-preserve-winston-signal-on-dar-stop-confirm.md) | Ticket: Preserve winston_signal when confirming a DAR exit at stop |
| P3 | Proposed | [`2026-08-17-archive-bg-l1-done-tickets.md`](2026-08-17-archive-bg-l1-done-tickets.md) | Ticket: Archive Broker Gateway L1 Done tickets |
| P3 | Proposed | [`2026-08-17-wut-position-swap-spec-activity-atr.md`](2026-08-17-wut-position-swap-spec-activity-atr.md) | Ticket: WUT PositionSwapEvaluator spec sets Activity.atr as a column |
| P1 | Done | [`2026-08-17-wv2-equity-wut-parity-flow-dar-shell.md`](2026-08-17-wv2-equity-wut-parity-flow-dar-shell.md) | Ticket: Wv2 equity WUT-parity — short flow + DAR + shell |
| P1 | In progress | [`2026-08-12-turtle-systems-eval-and-ops-alignment.md`](2026-08-12-turtle-systems-eval-and-ops-alignment.md) | Ticket: Turtle systems eval + heat + capital + ops voice |
| P1 | Proposed | [`2026-08-12-dar-next-steps-portfolio-name-truncation.md`](2026-08-12-dar-next-steps-portfolio-name-truncation.md) | Ticket: DAR Next Steps — portfolio column truncates to “Portfolio” |
| P1 | Done | [`2026-08-12-ops-shell-next-steps-by-portfolio.md`](2026-08-12-ops-shell-next-steps-by-portfolio.md) | Ticket: Ops shell — pending/next steps grouped by portfolio |
| P1 | Done | [`2026-08-13-handoff-mint-s2-yellow-s1-observation.md`](2026-08-13-handoff-mint-s2-yellow-s1-observation.md) | Ticket: Handoff Mint+TS#77 and Yellow+TS#75 observation OPs |
| P1 | Done | [`2026-08-13-importer-risk-percentage-one-percent.md`](2026-08-13-importer-risk-percentage-one-percent.md) | Ticket: Importer treats risk_percentage 1.0 as 100% |
| P1 | Proposed | [`2026-08-13-evaluate-turtle-mint-s2-yellow-s1.md`](2026-08-13-evaluate-turtle-mint-s2-yellow-s1.md) | Ticket: First Daily Analysis on Turtle Mint S2 + Yellow S1 |
| P3 | Proposed | [`2026-08-13-hygiene-close-unused-inactive-ops.md`](2026-08-13-hygiene-close-unused-inactive-ops.md) | Ticket: Hygiene-close unused inactive Mint/Yellow/Blue leftovers |
| P3 | Proposed | [`2026-08-13-closed-paper-residue-cleanup.md`](2026-08-13-closed-paper-residue-cleanup.md) | Ticket: Human cleanup of open residue on closed paper OPs #6 and #383 |
| P2 | Proposed | [`2026-08-13-rebuild-winston-mcp-snapshot-timeout.md`](2026-08-13-rebuild-winston-mcp-snapshot-timeout.md) | Ticket: Rebuild winston_mcp after snapshot timeout + tool description |
| P2 | Proposed | [`2026-08-13-observe-shuffled-hourly-snapshot.md`](2026-08-13-observe-shuffled-hourly-snapshot.md) | Ticket: Observe shuffled hourly snapshot on Telegram |
| P2 | Proposed | [`2026-08-13-snapshot-universe-active-vs-parquet.md`](2026-08-13-snapshot-universe-active-vs-parquet.md) | Ticket: Snapshot shuffle universe — Active books vs full parquet |
| P3 | Proposed | [`2026-08-13-reseed-cromwell-snapshot-skill.md`](2026-08-13-reseed-cromwell-snapshot-skill.md) | Ticket: Re-seed Cromwell workspace snapshot skill |
| P2 | Proposed | [`2026-08-13-walnut-turtle-hybrid-smoke.md`](2026-08-13-walnut-turtle-hybrid-smoke.md) | Ticket: Portfolio Walnut — Turtle hybrid-price smoke (S1/S2) |
| P2 | Superseded by 2026-08-17 equity parity | [`2026-08-13-investigate-negative-risk-equity-active-ops.md`](2026-08-13-investigate-negative-risk-equity-active-ops.md) | Ticket: Investigate negative risk_equity on Active OPs |
| P2 | Proposed | [`2026-08-12-desk-fill-stop-js-browser-verify.md`](2026-08-12-desk-fill-stop-js-browser-verify.md) | Ticket: Browser-verify desk fill-stop JavaScript |
| P2 | Proposed | [`2026-08-12-dar-risk-equity-live-render.md`](2026-08-12-dar-risk-equity-live-render.md) | Ticket: Live DAR render — free cash + risk equity + over-deployed |
| P1 | Done — Phases 0–4 | [`2026-07-25-ts-portfolio-heat-unit-limits.md`](2026-07-25-ts-portfolio-heat-unit-limits.md) | Ticket: TS creation — multi-level portfolio heat (Turtle unit limits + correlations) |
| P1 | In progress | [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md) | Epic: L1 Confirmation Intake + Broker Gateway build |
| P1 | Done | [`2026-08-09-winston-broker-evidence-standard-interface.md`](2026-08-09-winston-broker-evidence-standard-interface.md) | Ticket: Winston Broker Evidence Standard — interface doc |
| P1 | Ready (scaffold landed; formal close optional) | [`2026-08-09-broker-gateway-rails-scaffold.md`](2026-08-09-broker-gateway-rails-scaffold.md) | Ticket: Broker Gateway — Rails monolith scaffold |
| P1 | Done | [`2026-08-09-bg-adapter-registry-and-capability-profile.md`](2026-08-09-bg-adapter-registry-and-capability-profile.md) | Ticket: Broker Gateway — adapter registry + CapabilityProfile |
| P1 | Done | [`2026-08-09-bg-dummy-sim-adapter.md`](2026-08-09-bg-dummy-sim-adapter.md) | Ticket: Broker Gateway — dummy/sim adapter (paper path + contracts) |
| P3 | Proposed | [`2026-08-12-bg-evidence-volume-name.md`](2026-08-12-bg-evidence-volume-name.md) | Ticket: BG evidence volume — avoid double project prefix |
| P3 | Proposed | [`2026-08-12-bg-compose-first-time-up-docs.md`](2026-08-12-bg-compose-first-time-up-docs.md) | Ticket: Document first-time Broker Gateway compose bring-up |
| P1 | Done | [`2026-08-09-bg-evidence-store-jsonl-and-cursors.md`](2026-08-09-bg-evidence-store-jsonl-and-cursors.md) | Ticket: Broker Gateway — evidence store JSONL + cursors |
| P1 | Done | [`2026-08-09-bg-internal-api-refresh-events.md`](2026-08-09-bg-internal-api-refresh-events.md) | Ticket: Broker Gateway — internal API refresh + events |
| P1 | Ready | [`2026-08-09-bg-schwab-read-adapter-l1.md`](2026-08-09-bg-schwab-read-adapter-l1.md) | Ticket: Broker Gateway — Schwab read adapter (L1) |
| P1 | Ready | [`2026-08-09-wv2-bg-client-and-event-cursor.md`](2026-08-09-wv2-bg-client-and-event-cursor.md) | Ticket: Wv2 — BG client + event cursor |
| P1 | Ready | [`2026-08-09-wv2-trade-notification-store-and-normalize.md`](2026-08-09-wv2-trade-notification-store-and-normalize.md) | Ticket: Wv2 — TradeNotification store + normalize |
| P1 | Ready | [`2026-08-09-wv2-match-prefill-confirmation-intake.md`](2026-08-09-wv2-match-prefill-confirmation-intake.md) | Ticket: Wv2 — match + prefill Confirmation Intake |
| P1 | Ready | [`2026-08-09-wv2-desk-workflow-hitl-evidence-ui.md`](2026-08-09-wv2-desk-workflow-hitl-evidence-ui.md) | Ticket: Wv2 — desk workflow HITL evidence UI |
| P1 | Ready | [`2026-08-09-wv2-confirmation-intake-integration-specs.md`](2026-08-09-wv2-confirmation-intake-integration-specs.md) | Ticket: Wv2 — Confirmation Intake integration specs |
| P1 | Ready | [`2026-08-09-l1-contract-fixtures-and-test-harness.md`](2026-08-09-l1-contract-fixtures-and-test-harness.md) | Ticket: L1 contract fixtures + test harness |
| P1 | Proposed | [`2026-08-07-schwab-trader-api-sandbox-spike.md`](2026-08-07-schwab-trader-api-sandbox-spike.md) | Ticket: Schwab Trader API sandbox / integration-test spike |
| P2 | In progress | [`2026-08-04-stack-arr-mer-risk-scale-chart.md`](2026-08-04-stack-arr-mer-risk-scale-chart.md) | Ticket: Stack ARR + MER on trade timeline; risk-scale path chart |
| P3 | Proposed | [`2026-08-03-portfolio-color-edit-ui.md`](2026-08-03-portfolio-color-edit-ui.md) | Ticket: Portfolio color edit UI (WUT + Wv2) |
| P3 | Proposed | [`2026-08-03-align-portfolio-color-fallback.md`](2026-08-03-align-portfolio-color-fallback.md) | Ticket: Align WUT/Wv2 PortfolioColor fallback + from_name |
| P3 | Proposed | [`2026-08-03-version-portfolio-configs-in-git.md`](2026-08-03-version-portfolio-configs-in-git.md) | Ticket: Version primary portfolio_configs JSON in git |
| P2 | Proposed | [`2026-07-31-am-m-forced-step-smoke.md`](2026-07-31-am-m-forced-step-smoke.md) | Ticket: AM/M forced-step smoke (risk scale knobs that move) |
| P2 | Proposed | [`2026-07-31-adr-risk-scale-orthogonality.md`](2026-07-31-adr-risk-scale-orthogonality.md) | Ticket: ADR — risk_scale_policy orthogonal to base geometry |
| P2 | Proposed | [`2026-07-31-business-analysis-risk-scale-matrix-345-356.md`](2026-07-31-business-analysis-risk-scale-matrix-345-356.md) | Ticket: Business analysis scorecard — matrix PBRs 345–356 |
| P2 | Proposed | [`2026-07-31-kelly-scale-not-global-default.md`](2026-07-31-kelly-scale-not-global-default.md) | Ticket: Kelly scale — not global default |
| P2 | Proposed | [`2026-07-31-yellow-owdc-none-paper-candidate.md`](2026-07-31-yellow-owdc-none-paper-candidate.md) | Ticket: Yellow OWDC + scale=none paper candidate |
| P2 | In progress — Yellow S/M/K scored | [`2026-07-30-kelly-martingale-sizing-portfolio-management.md`](2026-07-30-kelly-martingale-sizing-portfolio-management.md) | Ticket: Kelly / Martingale sizing in portfolio management (WUT lab → Wv2 daily managers) |
| P2 | Proposed | [`2026-07-30-parallel-trading-system-swing-options-intraday.md`](2026-07-30-parallel-trading-system-swing-options-intraday.md) | Ticket: Parallel trading system (swing / options / intraday) reusing Winston rails |
| P1 | In progress | [`2026-07-25-strategy-bakeoff-v1-phase1.md`](2026-07-25-strategy-bakeoff-v1-phase1.md) | Ticket: Strategy bake-off V1 — Phase 1 (cross-portfolio TS selection) |
| P1 | Transferred paper inactive — activate when ready | [`2026-07-26-s4-recipe-transfer-mint-yellow-blue.md`](2026-07-26-s4-recipe-transfer-mint-yellow-blue.md) | Ticket: Promote S4 FastBO5 pack — transfer Mint / Yellow / Blue |
| P2 | Proposed | [`2026-07-26-s4-op-max-markets-book-count.md`](2026-07-26-s4-op-max-markets-book-count.md) | Ticket: S4 pack OPs — set max_markets_per_portfolio to book size |
| P1 | Scored — keep pure next_bar pyramids | [`2026-07-26-hybrid-fill-entry-next-pyramid-same-day.md`](2026-07-26-hybrid-fill-entry-next-pyramid-same-day.md) | Ticket: Hybrid fill — next-bar entry, same-day pyramid (lab + broker priority) |
| P1 | Scored — reject price-level pyramids | [`2026-07-26-hybrid-fill-price-level-pyramid.md`](2026-07-26-hybrid-fill-price-level-pyramid.md) | Ticket: Pyramid price-level fills (resting stop at last±N×ATR) |
| P2 | Scored — keep ladder A (B/C null) | [`2026-07-26-s4-phase2-ladder-mildness.md`](2026-07-26-s4-phase2-ladder-mildness.md) | Ticket: Phase 2 step 3b — S4 milder OWD ladder at frozen heat |
| P2 | Scored — keep $10k ($20k hurts) | [`2026-07-26-s4-capital-20k-survivability.md`](2026-07-26-s4-capital-20k-survivability.md) | Ticket: S4 — does 2× initial capital ($20k) improve survivability? |
| P3 | Proposed | [`2026-07-26-bakeoff-scorecard-cagr-calmar.md`](2026-07-26-bakeoff-scorecard-cagr-calmar.md) | Ticket: Bake-off scorecards — CAGR and Calmar metrics |
| P2 | Proposed | [`2026-07-25-owdc-owd-four-cell-matrix.md`](2026-07-25-owdc-owd-four-cell-matrix.md) | Ticket: OWDC / OWD 4-cell lab matrix (trust close-out) |
| P3 | Proposed | [`2026-07-25-pbr-cash-ledger-return-scorecard.md`](2026-07-25-pbr-cash-ledger-return-scorecard.md) | Ticket: PBR free-cash ledger — total-return scorecard |
| P3 | Proposed | [`2026-07-25-pbr-status-poll-missing-run-ux.md`](2026-07-25-pbr-status-poll-missing-run-ux.md) | Ticket: PBR status-poll UX when run HTML is missing (404) |
| P2 | Proposed | [`2026-07-24-dar-telegram-force-republish-runbook.md`](2026-07-24-dar-telegram-force-republish-runbook.md) | Ticket: DAR Telegram force re-publish runbook |
| P2 | Proposed (follow-on after close-trigger / one_way_dynamic_close) | [`2026-07-24-opposite-entry-signal-on-signal.md`](2026-07-24-opposite-entry-signal-on-signal.md) | Ticket: Opposite-entry “signal-on-signal” (exit vs reverse) — WUT experiment |
| P2 | Proposed | [`2026-07-24-audit-wv2-multi-exit-truncation.md`](2026-07-24-audit-wv2-multi-exit-truncation.md) | Ticket: Audit Wv2 TradingStrategies for truncated multi-exit |
| P2 | Proposed | [`2026-07-24-handoff-paths-singular-exit-only.md`](2026-07-24-handoff-paths-singular-exit-only.md) | Ticket: Confirm no handoff path still uses singular exit only |
| P3 | Proposed | [`2026-07-23-game-theory-analysis-winston-stack.md`](2026-07-23-game-theory-analysis-winston-stack.md) | Ticket: Game-theory analysis of the Winston stack (portfolio → EOD → signal → execution; EOD trend vs intraday swing) |
| P1 | Proposed | [`2026-07-23-pbr-results-json-must-be-json.md`](2026-07-23-pbr-results-json-must-be-json.md) | Ticket: PBR `results_json` must be valid JSON (not Hash#inspect) |
| P1 | Proposed | [`2026-07-23-cromwell-telegram-ops-fastpath-empty-response.md`](2026-07-23-cromwell-telegram-ops-fastpath-empty-response.md) | Ticket: Cromwell Telegram ops fast-path (sidestep empty-response hangs) |
| P1 | Proposed | [`2026-07-23-wv2-add-single-market-to-portfolio.md`](2026-07-23-wv2-add-single-market-to-portfolio.md) | Ticket: Add a single market to a single Operational Portfolio (Wv2) — e.g. SPCX → Yellow |
| P1 | Proposed | [`2026-07-23-mcp-transfer-activate-flow-smooth.md`](2026-07-23-mcp-transfer-activate-flow-smooth.md) | Ticket: Smooth MCP transfer + activate flow (errors, timeouts, reply contract) — includes run-121 false 500 |
| P1 | Proposed | [`2026-07-23-wut-puma-large-pbr-results-json.md`](2026-07-23-wut-puma-large-pbr-results-json.md) | Ticket: WUT puma timeouts under large multi-market PBR results_json |
| P2 | Proposed | [`2026-07-23-reexport-mint-yellow-vet-winners.md`](2026-07-23-reexport-mint-yellow-vet-winners.md) | Ticket: Re-export Mint/Yellow first-pass vet winners (opt #47/#48) |
| P2 | Proposed | [`2026-07-23-mint-yellow-risk-transfer-matrix.md`](2026-07-23-mint-yellow-risk-transfer-matrix.md) | Ticket: Mint/Yellow risk-transfer matrix (R1 ladder + capacity) |
| P2 | Proposed | [`2026-07-23-dm-lookback-exclusive-overlap-specs.md`](2026-07-23-dm-lookback-exclusive-overlap-specs.md) | Ticket: Specs for DM lookback/date-range and exclusive MAX_OVERLAP=0 |
| P1 | In progress (membership still open; **strategy/risk rescu… | [`2026-07-07-revisit-portfolio-blue-membership-strategy.md`](2026-07-07-revisit-portfolio-blue-membership-strategy.md) | Ticket: Revisit Portfolio Blue membership and strategy viability |
| P1 | In progress (mitigations landed 2026-07-09; await natural… | [`2026-07-09-cromwell-cron-llm-timeout.md`](2026-07-09-cromwell-cron-llm-timeout.md) | Ticket: Harden Cromwell cron LLM path (timeouts on scheduled Telegram) |
| P1 | In progress (ops fixes applied host-side; remaining work … | [`2026-07-15-cromwell-llm-cpu-reliability.md`](2026-07-15-cromwell-llm-cpu-reliability.md) | Ticket: Cromwell LLM CPU reliability (timeouts, think, cron isolation) |
| P1 | Proposed | [`2026-07-15-cromwell-thin-cron-and-priority.md`](2026-07-15-cromwell-thin-cron-and-priority.md) | Ticket: Thin / LLM-light Cromwell cron + user priority (Tier 2) — elevated 2026-07-23 |
| P1 | Proposed | [`2026-07-04-operational-data-backup-and-dr.md`](2026-07-04-operational-data-backup-and-dr.md) | Ticket: Operational data backup and disaster recovery |
| P1 | Proposed (Phase 3 follow-on — after ADR-006 minimum) | [`2026-07-09-capital-activation-mcp-telegram.md`](2026-07-09-capital-activation-mcp-telegram.md) | Ticket: Capital Activation (MCP / Telegram) |
| P1 | Proposed | [`2026-07-09-confirm-cromwell-hourly-telegram.md`](2026-07-09-confirm-cromwell-hourly-telegram.md) | Ticket: Confirm natural Cromwell hourly Telegram after CPU tuning |
| P1 | Proposed | [`2026-07-13-cromwell-scrub-placeholder-path-memory.md`](2026-07-13-cromwell-scrub-placeholder-path-memory.md) | Ticket: Scrub Cromwell permanent memory of `path/to/file.txt` hallucination |
| P1 | Proposed | [`2026-07-13-observe-cromwell-market-snapshot-hourlies.md`](2026-07-13-observe-cromwell-market-snapshot-hourlies.md) | Ticket: Observe Cromwell market-snapshot hourlies for real MCP + clean Telegram |
| P1 | Proposed | [`2026-07-21-cromwell-hourly-telegram-attention-discipline.md`](2026-07-21-cromwell-hourly-telegram-attention-discipline.md) | Ticket: Cromwell hourly Telegram — attention discipline (quiet = one line) |
| P1 | Proposed | [`2026-07-13-stale-parquet-prior-close-active-symbols.md`](2026-07-13-stale-parquet-prior-close-active-symbols.md) | Ticket: Stale DM parquet last-dates for some Active symbols |
| P1 | Proposed | [`2026-07-15-journal-ledger-stop-on-confirm-and-update.md`](2026-07-15-journal-ledger-stop-on-confirm-and-update.md) | Ticket: Human stop on confirm/book + stop update path |
| P1 | Proposed | [`2026-07-18-ops-mcp-recreate-after-demo-tools.md`](2026-07-18-ops-mcp-recreate-after-demo-tools.md) | Ticket: Recreate winston_mcp after ops demo tool surface changes |
| P1 | Proposed | [`2026-07-20-dar-real-process-miss-attention.md`](2026-07-20-dar-real-process-miss-attention.md) | Ticket: DAR attention for Active real process-miss Passed Signals |
| P2 | Proposed | [`2026-07-22-cromwell-snapshot-open-empty-response-artifact.md`](2026-07-22-cromwell-snapshot-open-empty-response-artifact.md) | Ticket: Cromwell market-snapshot-open — empty run `response` vs Telegram `message` |
| P2 | Proposed | [`2026-07-21-cromwell-activate-id-or-name.md`](2026-07-21-cromwell-activate-id-or-name.md) | Ticket: Cromwell must always pass `id_or_name` on portfolio activate |
| P2 | Proposed | [`2026-07-21-portfolio-id-or-name-fingerprint-resolution.md`](2026-07-21-portfolio-id-or-name-fingerprint-resolution.md) | Ticket: Portfolio `id_or_name` fingerprint / short-fp resolution + multi-match error |
| P2 | Proposed | [`2026-07-02-compose-orchestrator-unification.md`](2026-07-02-compose-orchestrator-unification.md) | Ticket: Unify compose orchestration (podman-compose vs podman compose) |
| P2 | Proposed | [`2026-07-02-dm-integration-audit-mirror.md`](2026-07-02-dm-integration-audit-mirror.md) | Ticket: DM integration audit mirror to ecosystem hub (fast follow) |
| P2 | Proposed | [`2026-07-02-wv2-integration-audit-correlation.md`](2026-07-02-wv2-integration-audit-correlation.md) | Ticket: Wv2 integration audit + correlation ID echo (fast follow) |
| P2 | Proposed | [`2026-07-04-tailscale-serve-ecosystem-deployment.md`](2026-07-04-tailscale-serve-ecosystem-deployment.md) | Ticket: Tailscale Serve deployment docs + Wv2/DM subpath parity |
| P2 | Proposed | [`2026-07-06-dm-wut-registry-metadata-sync-followups.md`](2026-07-06-dm-wut-registry-metadata-sync-followups.md) | Ticket: DM ↔ WUT registry metadata mirror follow-ups |
| P2 | Proposed (see main plan) | [`2026-07-07-wut-activities-compatibility-shim-dm-stubs.md`](2026-07-07-wut-activities-compatibility-shim-dm-stubs.md) | Ticket: WUT — Remove belongs_to :activity for DM data; refactor creation + usage sites + result rows to composite (market_id, date) + DM Bar loader |
| P2 | Proposed (see main ticket) | [`2026-07-07-wut-dm-data-sets-ui-dm-truth-no-load-sync-buttons.md`](2026-07-07-wut-dm-data-sets-ui-dm-truth-no-load-sync-buttons.md) | Ticket: data_sets UI — DM as source of truth; pure registry view using DataCoverage; remove all "Load Full Data", "Sync", hydration actions and language; columns reflect DM metadata |
| P2 | Proposed | [`2026-07-08-correlation-close-only-parquet-load.md`](2026-07-08-correlation-close-only-parquet-load.md) | Ticket: Close-only parquet load for correlation builder |
| P2 | Proposed | [`2026-07-08-wut-dm-parquet-controller-cleanup.md`](2026-07-08-wut-dm-parquet-controller-cleanup.md) | Ticket: WUT DM parquet: clean up remaining Activity queries in controllers |
| P2 | Proposed | [`2026-07-08-wut-dm-parquet-remaining-services.md`](2026-07-08-wut-dm-parquet-remaining-services.md) | Ticket: WUT DM parquet: refactor remaining services for direct DM loader usage |
| P2 | Proposed | [`2026-07-08-wut-dm-parquet-result-views-repull.md`](2026-07-08-wut-dm-parquet-result-views-repull.md) | Ticket: WUT DM parquet: implement full bar re-pull + rendering in all backtest result views and charts |
| P2 | Proposed | [`2026-07-09-first-pass-doctrine-gates-review.md`](2026-07-09-first-pass-doctrine-gates-review.md) | Ticket: First-pass trend doctrine and viability gates review |
| P2 | Proposed | [`2026-07-09-link-validation-pbr-to-optimization.md`](2026-07-09-link-validation-pbr-to-optimization.md) | Ticket: Link validation PortfolioBacktestRun to PortfolioSignalOptimization |
| P2 | Proposed | [`2026-07-09-telegram-agent-reply-visibility.md`](2026-07-09-telegram-agent-reply-visibility.md) | Ticket: Telegram agent reply visibility (inbound OK, human may not see) |
| P2 | Proposed | [`2026-07-09-track-ai-runtime-config-in-git.md`](2026-07-09-track-ai-runtime-config-in-git.md) | Ticket: Track AI runtime Containerfile + example config in git |
| P2 | Proposed | [`2026-07-09-use-saved-trading-strategy-in-backtest-workflow.md`](2026-07-09-use-saved-trading-strategy-in-backtest-workflow.md) | Ticket: Use saved TradingStrategy in backtest workflow (slice B) |
| P2 | Proposed | [`2026-07-09-validation-pbr-day-by-day-perf.md`](2026-07-09-validation-pbr-day-by-day-perf.md) | Ticket: Speed up full validation PortfolioBacktestRun after vet_trend |
| P2 | Proposed | [`2026-07-09-wut-active-account-id-sidekiq-failures.md`](2026-07-09-wut-active-account-id-sidekiq-failures.md) | Ticket: WUT Sidekiq jobs failing on missing active_account_id columns |
| P2 | Proposed | [`2026-07-10-promote-wv2-daily-ops-smoke-scripts.md`](2026-07-10-promote-wv2-daily-ops-smoke-scripts.md) | Ticket: Promote Wv2 daily-ops smoke scripts out of tmp/ |
| P2 | Proposed | [`2026-07-10-watch-sidekiq-eod-daily-analysis-path.md`](2026-07-10-watch-sidekiq-eod-daily-analysis-path.md) | Ticket: Watch Sidekiq EOD path (DM sync → Wv2 analysis → Cromwell) |
| P2 | Proposed | [`2026-07-12-re-vet-mango-rust-trade-ready.md`](2026-07-12-re-vet-mango-rust-trade-ready.md) | Ticket: Re-vet Portfolio Mango and Rust for trade-ready gates |
| P2 | Proposed | [`2026-07-13-cromwell-dream-memory-path-hygiene.md`](2026-07-13-cromwell-dream-memory-path-hygiene.md) | Ticket: Fix Cromwell dream routing for MEMORY.md and skill status paths |
| P2 | Proposed | [`2026-07-13-extend-cron-llm-timeout-acceptance.md`](2026-07-13-extend-cron-llm-timeout-acceptance.md) | Ticket: Extend Jul 9 cron LLM timeout ticket with post-truncation acceptance |
| P2 | Proposed | [`2026-07-13-market-radar-core-portfolio-scope.md`](2026-07-13-market-radar-core-portfolio-scope.md) | Ticket: Limit intraday market radar to core Active portfolios |
| P2 | Proposed | [`2026-07-13-pbr-level2-remaining-experiments.md`](2026-07-13-pbr-level2-remaining-experiments.md) | Ticket: PBR Level 2 remaining experiments (anti-overfit matrix) |
| P2 | Proposed | [`2026-07-14-refresh-remaining-color-portfolio-json-fingerprints.md`](2026-07-14-refresh-remaining-color-portfolio-json-fingerprints.md) | Ticket: Refresh remaining color portfolio_configs with fingerprints |
| P2 | Proposed | [`2026-07-14-workspace-compose-portfolio-configs-tracking.md`](2026-07-14-workspace-compose-portfolio-configs-tracking.md) | Ticket: Track host compose.yml + portfolio_configs outside monolith gits |
| P2 | Proposed | [`2026-07-15-cromwell-parallel-capacity-dual-runtime.md`](2026-07-15-cromwell-parallel-capacity-dual-runtime.md) | Ticket: Cromwell parallel capacity — dual runtime (Tier 1) |
| P2 | Proposed | [`2026-07-15-journal-ledger-export-csv-pdf.md`](2026-07-15-journal-ledger-export-csv-pdf.md) | Ticket: Operational portfolio journal ledger export (CSV → PDF) |
| P2 | Proposed | [`2026-07-15-journal-ledger-wut-ops-schema-alignment.md`](2026-07-15-journal-ledger-wut-ops-schema-alignment.md) | Ticket: WUT operations journal schema alignment |
| P2 | Proposed | [`2026-07-15-journal-ledger-wv2-journals-ui-or-route-cleanup.md`](2026-07-15-journal-ledger-wv2-journals-ui-or-route-cleanup.md) | Ticket: Wv2 journals browse UI or remove dead route |
| P2 | Proposed / blocked on runtime | [`2026-07-16-bonsai-27b-lab-eval-when-runnable.md`](2026-07-16-bonsai-27b-lab-eval-when-runnable.md) | Ticket: Lab-eval Bonsai 27B (ternary) when runtime is viable |
| P2 | Proposed | [`2026-07-16-bonsai-8b-cromwell-ab-eval.md`](2026-07-16-bonsai-8b-cromwell-ab-eval.md) | Ticket: Bonsai 8B vs cromwell-qwen3:8b A/B for Cromwell |
| P2 | Proposed | [`2026-07-16-cromwell-core-model-promotion-policy.md`](2026-07-16-cromwell-core-model-promotion-policy.md) | Ticket: Cromwell core model promotion policy (checklist) |
| P2 | Proposed | [`2026-07-17-ops-live-telegram-confirm-phrase-smoke.md`](2026-07-17-ops-live-telegram-confirm-phrase-smoke.md) | Ticket: Live Telegram confirm-phrase smoke (when draft exists) |
| P2 | Proposed | [`2026-07-17-version-workspace-compose-yml.md`](2026-07-17-version-workspace-compose-yml.md) | Ticket: Version workspace root `compose.yml` in git |
| P2 | Proposed | [`2026-07-18-ops-telegram-demo-tools-smoke.md`](2026-07-18-ops-telegram-demo-tools-smoke.md) | Ticket: Live Telegram smoke — ops demo tools (#5–#7 + bulk/exit_reason) |
| P2 | Proposed | [`2026-07-20-rails-code-review-wut-baseline.md`](2026-07-20-rails-code-review-wut-baseline.md) | Ticket: First rails-code-review baseline (WUT) |
| P2 | Proposed | [`2026-07-20-safe-bug-fix-harness-multi-repo.md`](2026-07-20-safe-bug-fix-harness-multi-repo.md) | Ticket: Multi-repo isolation policy + optional full safe-bug-fix harness |
| P2 | Proposed | [`2026-07-20-wv2-capacity-swap-desk-packages.md`](2026-07-20-wv2-capacity-swap-desk-packages.md) | Ticket: Wv2 capacity swap → ordered Desk Handoff packages |
| P1 | Proposed (Phase 1 D10) | [`2026-08-05-signal-path-truth-fulfillment-link-exit-reconcile.md`](2026-08-05-signal-path-truth-fulfillment-link-exit-reconcile.md) | Ticket: Signal-path operational truth + fulfillment link + exit capital reconcile |
| P2 | Superseded by L1 implement tickets (discovery closed via Grill A/B) | [`2026-07-21-broker-confirmation-email-api-intake.md`](2026-07-21-broker-confirmation-email-api-intake.md) | Ticket: Broker confirmation intake (email / API) for desk fulfillment |
| P2 | Done (Grill A 2026-08-06; parent + L1 tickets closed 2026-08-09) | [`2026-07-22-grill-fulfillment-schwab-extra-modal.md`](2026-07-22-grill-fulfillment-schwab-extra-modal.md) | Ticket: Grill-with-docs — fulfillment ownership, Schwab intake, extra-modal |
| P3 | Proposed | [`2026-07-22-cromwell-snapshot-watcher-queued-false-positive.md`](2026-07-22-cromwell-snapshot-watcher-queued-false-positive.md) | Ticket: Fix market-snapshot overnight watcher — race on `queued` / empty response |
| P3 | Proposed | [`2026-07-21-blue-241-successor-cleanup.md`](2026-07-21-blue-241-successor-cleanup.md) | Ticket: Decide fate of Blue successor OP #241 |
| P3 | Proposed | [`2026-07-21-ops-speech-prefer-portfolio-numeric-id.md`](2026-07-21-ops-speech-prefer-portfolio-numeric-id.md) | Ticket: Prefer numeric portfolio `#id` in ops speech and skill examples |
| P3 | Proposed (largely delivered; residual compose smoke) | [`2026-07-04-daily-report-pdf-redesign.md`](2026-07-04-daily-report-pdf-redesign.md) | Ticket: Redesign Wv2 daily activity report PDF layout |
| P3 | Proposed | [`2026-07-06-propagate-ecosystem-log-hygiene.md`](2026-07-06-propagate-ecosystem-log-hygiene.md) | Ticket: Propagate ecosystem log hygiene patterns to top-level and monoliths |
| P3 | Proposed | [`2026-07-07-update-portfolio-overlap-tasks-red-vet-complete.md`](2026-07-07-update-portfolio-overlap-tasks-red-vet-complete.md) | Ticket: Update portfolio-overlap-rebuild.md.tasks.json after rich TradingStrategy export alignment |
| P3 | Proposed | [`2026-07-07-update-wut-to-wv2-handoff-richer-trading-strategy-shape.md`](2026-07-07-update-wut-to-wv2-handoff-richer-trading-strategy-shape.md) | Ticket: Update wut-to-wv2-handoff.md to document richer TradingStrategy export shape |
| P3 | Proposed (Phase B/C deferred; planning done) | [`2026-07-08-schema-cleanup-activity-id-columns.md`](2026-07-08-schema-cleanup-activity-id-columns.md) | Ticket: Eventual schema cleanup for activity_id columns (post DM SoT) |
| P3 | Proposed | [`2026-07-09-thelio-discrete-gpu-for-ollama.md`](2026-07-09-thelio-discrete-gpu-for-ollama.md) | Ticket: Optional discrete GPU for Cromwell Ollama (Thelio Mira) |
| P3 | Proposed | [`2026-07-09-trading-strategy-fingerprint-versioning.md`](2026-07-09-trading-strategy-fingerprint-versioning.md) | Ticket: TradingStrategy fingerprint payload versioning |
| P3 | Proposed | [`2026-07-09-wut-development-log-rotation.md`](2026-07-09-wut-development-log-rotation.md) | Ticket: Rotate / truncate WUT development.log |
| P3 | Proposed | [`2026-07-09-wut-loader-context-perf-specs.md`](2026-07-09-wut-loader-context-perf-specs.md) | Ticket: Specs for DM loader and optimization context perf fixes |
| P3 | Proposed | [`2026-07-09-wv2-observation-import-orange-white.md`](2026-07-09-wv2-observation-import-orange-white.md) | Ticket: Optional Wv2 import of Orange/White observation portfolios |
| P3 | Proposed | [`2026-07-12-pcs-business-context-doc.md`](2026-07-12-pcs-business-context-doc.md) | Ticket: Business-context doc for Portfolio Correlation Score |
| P3 | Proposed | [`2026-07-13-correlation-deep-dive-yaml-refresh.md`](2026-07-13-correlation-deep-dive-yaml-refresh.md) | Ticket: Refresh process for correlation deep-dive YAML |
| P3 | Proposed | [`2026-07-13-pcs-deep-dive-mcp-tool.md`](2026-07-13-pcs-deep-dive-mcp-tool.md) | Ticket: Optional MCP tool for portfolio PCS deep dive |
| P3 | Proposed | [`2026-07-13-wut-expose-business-analysis-link.md`](2026-07-13-wut-expose-business-analysis-link.md) | Ticket: Expose ecosystem business analysis from WUT UI |
| P3 | Proposed | [`2026-07-15-cromwell-analyst-adapter-future.md`](2026-07-15-cromwell-analyst-adapter-future.md) | Ticket: Second LoRA adapter for Winston analysis (future) |
| P3 | Proposed | [`2026-07-15-cromwell-qlora-ollama-ab.md`](2026-07-15-cromwell-qlora-ollama-ab.md) | Ticket: Offline QLoRA recipe + Ollama tag A/B for Cromwell |
| P3 | Proposed | [`2026-07-15-cromwell-trace-harvest-gold-sft.md`](2026-07-15-cromwell-trace-harvest-gold-sft.md) | Ticket: Cromwell trace harvest → gold SFT dataset |
| P3 | Proposed (reference / anti-scope) | [`2026-07-15-telegram-handoff-non-goals.md`](2026-07-15-telegram-handoff-non-goals.md) | Ticket: Telegram handoff — explicit non-goals (E) |
| P3 | Proposed | [`2026-07-15-winston-model-specialization-plan.md`](2026-07-15-winston-model-specialization-plan.md) | Ticket: Draft Winston model specialization plan (or ADR) |
| P3 | Proposed (watch active via scheduler) | [`2026-07-16-bonsai-ollama-availability-watch.md`](2026-07-16-bonsai-ollama-availability-watch.md) | Ticket: Watch for Bonsai 27B (and 8B) Ollama availability |
| P3 | Proposed | [`2026-07-17-mcp-recreate-hint.md`](2026-07-17-mcp-recreate-hint.md) | Ticket: Document winston_mcp Podman recreate pattern as ecosystem hint |
| P3 | Proposed | [`2026-07-17-reverse-session-smoke-cash-events.md`](2026-07-17-reverse-session-smoke-cash-events.md) | Ticket: Reverse session smoke cash on Orange / Rust |
| P3 | Proposed | [`2026-07-19-loop-engineering-evolution-mode.md`](2026-07-19-loop-engineering-evolution-mode.md) | Ticket: Loop engineering + Evolution Mode (return to design) |
| P3 | Proposed | [`2026-07-20-evaluate-agent-skill-cromwell.md`](2026-07-20-evaluate-agent-skill-cromwell.md) | Ticket: evaluate-agent-skill for Cromwell skill changes |
| P3 | Deferred | [`2026-07-15-journal-ledger-order-vs-fill-deferred.md`](2026-07-15-journal-ledger-order-vs-fill-deferred.md) | Ticket: Order vs fill semantics (resting stops) — deferred |

## Archive

77 closed tickets in [`archive/`](archive/) — includes 2026-07-24 multi-cohort evaluate smoke (Mint #311 + Yellow #330).

_Updated 2026-08-18 MDT (filed live Pending-grouping verify ticket)._
