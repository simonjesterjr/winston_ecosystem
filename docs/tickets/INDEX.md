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
| P1 | In progress (membership still open; **strategy/risk res | [`2026-07-07-revisit-portfolio-blue-membership-strategy.md`](2026-07-07-revisit-portfolio-blue-membership-strategy.md) | Ticket: Revisit Portfolio Blue membership and strategy viability |
| P1 | In progress (mitigations landed 2026-07-09; await natur | [`2026-07-09-cromwell-cron-llm-timeout.md`](2026-07-09-cromwell-cron-llm-timeout.md) | Ticket: Harden Cromwell cron LLM path (timeouts on scheduled Telegram) |
| P1 | In progress (ops fixes applied host-side; remaining wor | [`2026-07-15-cromwell-llm-cpu-reliability.md`](2026-07-15-cromwell-llm-cpu-reliability.md) | Ticket: Cromwell LLM CPU reliability (timeouts, think, cron isolation) |
| P1 | Proposed | [`2026-07-04-operational-data-backup-and-dr.md`](2026-07-04-operational-data-backup-and-dr.md) | Ticket: Operational data backup and disaster recovery |
| P1 | Proposed   | [`2026-07-13-cromwell-scrub-placeholder-path-memory.md`](2026-07-13-cromwell-scrub-placeholder-path-memory.md) | Ticket: Scrub Cromwell permanent memory of `path/to/file.txt` hallucination |
| P1 | Proposed   | [`2026-07-18-ops-mcp-recreate-after-demo-tools.md`](2026-07-18-ops-mcp-recreate-after-demo-tools.md) | Ticket: Recreate winston_mcp after ops demo tool surface changes |
| P1 | Proposed (Phase 3 follow-on — after ADR-006 minimum) | [`2026-07-09-capital-activation-mcp-telegram.md`](2026-07-09-capital-activation-mcp-telegram.md) | Ticket: Capital Activation (MCP / Telegram) |
| P2 | Proposed | [`2026-07-02-compose-orchestrator-unification.md`](2026-07-02-compose-orchestrator-unification.md) | Ticket: Unify compose orchestration (podman-compose vs podman compose) |
| P2 | Proposed | [`2026-07-04-tailscale-serve-ecosystem-deployment.md`](2026-07-04-tailscale-serve-ecosystem-deployment.md) | Ticket: Tailscale Serve deployment docs + Wv2/DM subpath parity |
| P2 | Proposed   | [`2026-07-13-pbr-level2-remaining-experiments.md`](2026-07-13-pbr-level2-remaining-experiments.md) | Ticket: PBR Level 2 remaining experiments (anti-overfit matrix) |
| P2 | Proposed   | [`2026-07-15-cromwell-parallel-capacity-dual-runtime.md`](2026-07-15-cromwell-parallel-capacity-dual-runtime.md) | Ticket: Cromwell parallel capacity — dual runtime (Tier 1) |
| P2 | Proposed   | [`2026-07-15-cromwell-thin-cron-and-priority.md`](2026-07-15-cromwell-thin-cron-and-priority.md) | Ticket: Thin / LLM-light Cromwell cron + user priority (Tier 2) |
| P2 | Proposed   | [`2026-07-15-journal-ledger-wv2-journals-ui-or-route-cleanup.md`](2026-07-15-journal-ledger-wv2-journals-ui-or-route-cleanup.md) | Ticket: Wv2 journals browse UI or remove dead route |
| P2 | Proposed   | [`2026-07-16-bonsai-8b-cromwell-ab-eval.md`](2026-07-16-bonsai-8b-cromwell-ab-eval.md) | Ticket: Bonsai 8B vs cromwell-qwen3:8b A/B for Cromwell |
| P2 | Proposed   | [`2026-07-16-cromwell-core-model-promotion-policy.md`](2026-07-16-cromwell-core-model-promotion-policy.md) | Ticket: Cromwell core model promotion policy (checklist) |
| P2 | Proposed   | [`2026-07-17-ops-live-telegram-confirm-phrase-smoke.md`](2026-07-17-ops-live-telegram-confirm-phrase-smoke.md) | Ticket: Live Telegram confirm-phrase smoke (when draft exists) |
| P2 | Proposed   | [`2026-07-17-version-workspace-compose-yml.md`](2026-07-17-version-workspace-compose-yml.md) | Ticket: Version workspace root `compose.yml` in git |
| P2 | Proposed   | [`2026-07-18-ops-telegram-demo-tools-smoke.md`](2026-07-18-ops-telegram-demo-tools-smoke.md) | Ticket: Live Telegram smoke — ops demo tools (#5–#7 + bulk/exit_reason) |
| P2 | Proposed   | [`2026-07-19-loop-engineering-evolution-mode.md`](2026-07-19-loop-engineering-evolution-mode.md) | Ticket: Loop engineering + Evolution Mode (return to design) |
| P2 | Proposed   | [`2026-07-20-rails-code-review-wut-baseline.md`](2026-07-20-rails-code-review-wut-baseline.md) | Ticket: First rails-code-review baseline (WUT) |
| P2 | Proposed   | [`2026-07-20-safe-bug-fix-harness-multi-repo.md`](2026-07-20-safe-bug-fix-harness-multi-repo.md) | Ticket: Multi-repo isolation policy + optional full safe-bug-fix harness |
| P2 | Proposed   | [`2026-07-20-triage-unset-ticket-priorities.md`](2026-07-20-triage-unset-ticket-priorities.md) | Ticket: Triage remaining unset ticket priorities |
| P2 | Proposed / blocked on runtime   | [`2026-07-16-bonsai-27b-lab-eval-when-runnable.md`](2026-07-16-bonsai-27b-lab-eval-when-runnable.md) | Ticket: Lab-eval Bonsai 27B (ternary) when runtime is viable |
| P3 | Proposed   | [`2026-07-15-cromwell-analyst-adapter-future.md`](2026-07-15-cromwell-analyst-adapter-future.md) | Ticket: Second LoRA adapter for Winston analysis (future) |
| P3 | Proposed   | [`2026-07-15-cromwell-qlora-ollama-ab.md`](2026-07-15-cromwell-qlora-ollama-ab.md) | Ticket: Offline QLoRA recipe + Ollama tag A/B for Cromwell |
| P3 | Proposed   | [`2026-07-15-cromwell-trace-harvest-gold-sft.md`](2026-07-15-cromwell-trace-harvest-gold-sft.md) | Ticket: Cromwell trace harvest → gold SFT dataset |
| P3 | Proposed   | [`2026-07-15-winston-model-specialization-plan.md`](2026-07-15-winston-model-specialization-plan.md) | Ticket: Draft Winston model specialization plan (or ADR) |
| P3 | Proposed   | [`2026-07-17-mcp-recreate-hint.md`](2026-07-17-mcp-recreate-hint.md) | Ticket: Document winston_mcp Podman recreate pattern as ecosystem hint |
| P3 | Proposed   | [`2026-07-17-reverse-session-smoke-cash-events.md`](2026-07-17-reverse-session-smoke-cash-events.md) | Ticket: Reverse session smoke cash on Orange / Rust |
| P3 | Proposed   | [`2026-07-20-evaluate-agent-skill-cromwell.md`](2026-07-20-evaluate-agent-skill-cromwell.md) | Ticket: evaluate-agent-skill for Cromwell skill changes |
| P3 | Proposed (reference / anti-scope)   | [`2026-07-15-telegram-handoff-non-goals.md`](2026-07-15-telegram-handoff-non-goals.md) | Ticket: Telegram handoff — explicit non-goals (E) |
| P3 | Proposed (watch active via scheduler)   | [`2026-07-16-bonsai-ollama-availability-watch.md`](2026-07-16-bonsai-ollama-availability-watch.md) | Ticket: Watch for Bonsai 27B (and 8B) Ollama availability |
| unset | ? | [`2026-07-08-audit-outside-ui-callers-rakes-jobs.md`](2026-07-08-audit-outside-ui-callers-rakes-jobs.md) | Ticket: Audit outside-UI callers (rakes, jobs, scripts) for legacy activities / duplicatio |
| unset | ? | [`2026-07-08-dm-bind-mount-decision.md`](2026-07-08-dm-bind-mount-decision.md) | Ticket: Decide on bind-mount for data_manager in development (or document rebuild requirem |
| unset | ? | [`2026-07-08-dm-reconcile-full-e2e-smoke.md`](2026-07-08-dm-reconcile-full-e2e-smoke.md) | Ticket: Run full E2E smoke for DM reconcile + PBR after source-of-truth cutover |
| unset | ? | [`2026-07-08-review-manual-registry-symbols.md`](2026-07-08-review-manual-registry-symbols.md) | Ticket: Review the 8 "manual" symbols registered via reconcile (CDE, IBM, JNJ, PG, ROKU, R |
| unset | ? | [`2026-07-08-schema-cleanup-activity-id-columns.md`](2026-07-08-schema-cleanup-activity-id-columns.md) | Ticket: Eventual schema cleanup for activity_id columns (post DM SoT) |
| unset | Deferred   | [`2026-07-15-journal-ledger-order-vs-fill-deferred.md`](2026-07-15-journal-ledger-order-vs-fill-deferred.md) | Ticket: Order vs fill semantics (resting stops) — deferred |
| unset | In progress → largely delivered (2026-07-10 multi-pag | [`2026-07-04-daily-report-pdf-redesign.md`](2026-07-04-daily-report-pdf-redesign.md) | Ticket: Redesign Wv2 daily activity report PDF layout |
| unset | Proposed | [`2026-07-02-dm-integration-audit-mirror.md`](2026-07-02-dm-integration-audit-mirror.md) | Ticket: DM integration audit mirror to ecosystem hub (fast follow) |
| unset | Proposed | [`2026-07-02-wv2-integration-audit-correlation.md`](2026-07-02-wv2-integration-audit-correlation.md) | Ticket: Wv2 integration audit + correlation ID echo (fast follow) |
| unset | Proposed | [`2026-07-06-dm-wut-registry-metadata-sync-followups.md`](2026-07-06-dm-wut-registry-metadata-sync-followups.md) | Ticket: DM ↔ WUT registry metadata mirror follow-ups |
| unset | Proposed | [`2026-07-06-propagate-ecosystem-log-hygiene.md`](2026-07-06-propagate-ecosystem-log-hygiene.md) | Ticket: Propagate ecosystem log hygiene patterns to top-level and monoliths |
| unset | Proposed | [`2026-07-07-update-portfolio-overlap-tasks-red-vet-complete.md`](2026-07-07-update-portfolio-overlap-tasks-red-vet-complete.md) | Ticket: Update portfolio-overlap-rebuild.md.tasks.json after rich TradingStrategy export a |
| unset | Proposed | [`2026-07-07-update-wut-to-wv2-handoff-richer-trading-strategy-shape.md`](2026-07-07-update-wut-to-wv2-handoff-richer-trading-strategy-shape.md) | Ticket: Update wut-to-wv2-handoff.md to document richer TradingStrategy export shape |
| unset | Proposed | [`2026-07-08-correlation-close-only-parquet-load.md`](2026-07-08-correlation-close-only-parquet-load.md) | Ticket: Close-only parquet load for correlation builder |
| unset | Proposed | [`2026-07-08-wut-dm-parquet-controller-cleanup.md`](2026-07-08-wut-dm-parquet-controller-cleanup.md) | Ticket: WUT DM parquet: clean up remaining Activity queries in controllers |
| unset | Proposed | [`2026-07-08-wut-dm-parquet-remaining-services.md`](2026-07-08-wut-dm-parquet-remaining-services.md) | Ticket: WUT DM parquet: refactor remaining services for direct DM loader usage |
| unset | Proposed | [`2026-07-08-wut-dm-parquet-result-views-repull.md`](2026-07-08-wut-dm-parquet-result-views-repull.md) | Ticket: WUT DM parquet: implement full bar re-pull + rendering in all backtest result view |
| unset | Proposed | [`2026-07-09-first-pass-doctrine-gates-review.md`](2026-07-09-first-pass-doctrine-gates-review.md) | Ticket: First-pass trend doctrine and viability gates review |
| unset | Proposed | [`2026-07-09-link-validation-pbr-to-optimization.md`](2026-07-09-link-validation-pbr-to-optimization.md) | Ticket: Link validation PortfolioBacktestRun to PortfolioSignalOptimization |
| unset | Proposed | [`2026-07-09-track-ai-runtime-config-in-git.md`](2026-07-09-track-ai-runtime-config-in-git.md) | Ticket: Track AI runtime Containerfile + example config in git |
| unset | Proposed | [`2026-07-09-trading-strategy-fingerprint-versioning.md`](2026-07-09-trading-strategy-fingerprint-versioning.md) | Ticket: TradingStrategy fingerprint payload versioning |
| unset | Proposed | [`2026-07-09-use-saved-trading-strategy-in-backtest-workflow.md`](2026-07-09-use-saved-trading-strategy-in-backtest-workflow.md) | Ticket: Use saved TradingStrategy in backtest workflow (slice B) |
| unset | Proposed | [`2026-07-09-validation-pbr-day-by-day-perf.md`](2026-07-09-validation-pbr-day-by-day-perf.md) | Ticket: Speed up full validation PortfolioBacktestRun after vet_trend |
| unset | Proposed | [`2026-07-09-wut-active-account-id-sidekiq-failures.md`](2026-07-09-wut-active-account-id-sidekiq-failures.md) | Ticket: WUT Sidekiq jobs failing on missing active_account_id columns |
| unset | Proposed | [`2026-07-09-wut-development-log-rotation.md`](2026-07-09-wut-development-log-rotation.md) | Ticket: Rotate / truncate WUT development.log |
| unset | Proposed | [`2026-07-09-wut-loader-context-perf-specs.md`](2026-07-09-wut-loader-context-perf-specs.md) | Ticket: Specs for DM loader and optimization context perf fixes |
| unset | Proposed | [`2026-07-09-wv2-observation-import-orange-white.md`](2026-07-09-wv2-observation-import-orange-white.md) | Ticket: Optional Wv2 import of Orange/White observation portfolios |
| unset | Proposed   | [`2026-07-09-confirm-cromwell-hourly-telegram.md`](2026-07-09-confirm-cromwell-hourly-telegram.md) | Ticket: Confirm natural Cromwell hourly Telegram after CPU tuning |
| unset | Proposed   | [`2026-07-09-telegram-agent-reply-visibility.md`](2026-07-09-telegram-agent-reply-visibility.md) | Ticket: Telegram agent reply visibility (inbound OK, human may not see) |
| unset | Proposed   | [`2026-07-09-thelio-discrete-gpu-for-ollama.md`](2026-07-09-thelio-discrete-gpu-for-ollama.md) | Ticket: Optional discrete GPU for Cromwell Ollama (Thelio Mira) |
| unset | Proposed   | [`2026-07-10-promote-wv2-daily-ops-smoke-scripts.md`](2026-07-10-promote-wv2-daily-ops-smoke-scripts.md) | Ticket: Promote Wv2 daily-ops smoke scripts out of tmp/ |
| unset | Proposed   | [`2026-07-10-watch-sidekiq-eod-daily-analysis-path.md`](2026-07-10-watch-sidekiq-eod-daily-analysis-path.md) | Ticket: Watch Sidekiq EOD path (DM sync → Wv2 analysis → Cromwell) |
| unset | Proposed   | [`2026-07-12-pcs-business-context-doc.md`](2026-07-12-pcs-business-context-doc.md) | Ticket: Business-context doc for Portfolio Correlation Score |
| unset | Proposed   | [`2026-07-12-re-vet-mango-rust-trade-ready.md`](2026-07-12-re-vet-mango-rust-trade-ready.md) | Ticket: Re-vet Portfolio Mango and Rust for trade-ready gates |
| unset | Proposed   | [`2026-07-13-correlation-deep-dive-yaml-refresh.md`](2026-07-13-correlation-deep-dive-yaml-refresh.md) | Ticket: Refresh process for correlation deep-dive YAML |
| unset | Proposed   | [`2026-07-13-cromwell-cron-hallucination-hardening.md`](2026-07-13-cromwell-cron-hallucination-hardening.md) | Ticket: Harden Cromwell cron against post-truncation hallucination |
| unset | Proposed   | [`2026-07-13-cromwell-dream-memory-path-hygiene.md`](2026-07-13-cromwell-dream-memory-path-hygiene.md) | Ticket: Fix Cromwell dream routing for MEMORY.md and skill status paths |
| unset | Proposed   | [`2026-07-13-extend-cron-llm-timeout-acceptance.md`](2026-07-13-extend-cron-llm-timeout-acceptance.md) | Ticket: Extend Jul 9 cron LLM timeout ticket with post-truncation acceptance |
| unset | Proposed   | [`2026-07-13-market-radar-core-portfolio-scope.md`](2026-07-13-market-radar-core-portfolio-scope.md) | Ticket: Limit intraday market radar to core Active portfolios |
| unset | Proposed   | [`2026-07-13-observe-cromwell-market-snapshot-hourlies.md`](2026-07-13-observe-cromwell-market-snapshot-hourlies.md) | Ticket: Observe Cromwell market-snapshot hourlies for real MCP + clean Telegram |
| unset | Proposed   | [`2026-07-13-pcs-deep-dive-mcp-tool.md`](2026-07-13-pcs-deep-dive-mcp-tool.md) | Ticket: Optional MCP tool for portfolio PCS deep dive |
| unset | Proposed   | [`2026-07-13-stale-parquet-prior-close-active-symbols.md`](2026-07-13-stale-parquet-prior-close-active-symbols.md) | Ticket: Stale DM parquet last-dates for some Active symbols |
| unset | Proposed   | [`2026-07-13-wut-expose-business-analysis-link.md`](2026-07-13-wut-expose-business-analysis-link.md) | Ticket: Expose ecosystem business analysis from WUT UI |
| unset | Proposed   | [`2026-07-14-refresh-remaining-color-portfolio-json-fingerprints.md`](2026-07-14-refresh-remaining-color-portfolio-json-fingerprints.md) | Ticket: Refresh remaining color portfolio_configs with fingerprints |
| unset | Proposed   | [`2026-07-14-workspace-compose-portfolio-configs-tracking.md`](2026-07-14-workspace-compose-portfolio-configs-tracking.md) | Ticket: Track host compose.yml + portfolio_configs outside monolith gits |
| unset | Proposed   | [`2026-07-14-wv2-parquet-atr-position-sizer.md`](2026-07-14-wv2-parquet-atr-position-sizer.md) | Ticket: Fix parquet ATR / PositionSizer zero units |
| unset | Proposed   | [`2026-07-15-journal-ledger-export-csv-pdf.md`](2026-07-15-journal-ledger-export-csv-pdf.md) | Ticket: Operational portfolio journal ledger export (CSV → PDF) |
| unset | Proposed   | [`2026-07-15-journal-ledger-promote-fill-fields.md`](2026-07-15-journal-ledger-promote-fill-fields.md) | Ticket: Promote journal fill fields out of JSON |
| unset | Proposed   | [`2026-07-15-journal-ledger-stop-on-confirm-and-update.md`](2026-07-15-journal-ledger-stop-on-confirm-and-update.md) | Ticket: Human stop on confirm/book + stop update path |
| unset | Proposed   | [`2026-07-15-journal-ledger-wut-ops-schema-alignment.md`](2026-07-15-journal-ledger-wut-ops-schema-alignment.md) | Ticket: WUT operations journal schema alignment |
| unset | Proposed (see main plan) | [`2026-07-07-wut-activities-compatibility-shim-dm-stubs.md`](2026-07-07-wut-activities-compatibility-shim-dm-stubs.md) | Ticket: WUT — Remove belongs_to :activity for DM data; refactor creation + usage sites + |
| unset | Proposed (see main ticket) | [`2026-07-07-wut-dm-data-sets-ui-dm-truth-no-load-sync-buttons.md`](2026-07-07-wut-dm-data-sets-ui-dm-truth-no-load-sync-buttons.md) | Ticket: data_sets UI — DM as source of truth; pure registry view using DataCoverage; rem |

## Archive

64 closed tickets in [`archive/`](archive/).

_Generated 2026-07-20 UTC. Priority lines on tickets are SOT._
