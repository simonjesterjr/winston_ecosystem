# Ticket: Wv2 Active mutex (seed_name + Books set)

**Status:** Done (2026-07-14 Phase 3 PR 3)

**Date:** 2026-07-09

**Context:** Session [`2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill`](../session-reports/2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill.md). **ADR-006**.  
**Plan:** [`plans/paper-telegram-phase3-adr006.md`](../../plans/paper-telegram-phase3-adr006.md) PR 3.

## Problem

Many inactive OPs per seed are desirable (regime archive). Multiple **Active** OPs on the same seed or identical Books dilute attention and risk confusion. Capital Activation defaults Active true while paper may still be Active.

## Scope

1. On activate (rake, internal API, MCP): refuse if another Active OP shares `seed_name` **or** identical Books symbol set, unless force.
2. Clear error message listing the conflicting OP id/name.
3. Apply to Capital Activation when setting new OP Active.
4. Specs for seed conflict, Books conflict, force override, no conflict cases.

## Acceptance

- [x] Second Active same seed blocked without force
- [x] Second Active identical membership blocked without force
- [x] Force documented for short dual-active experiments
- [ ] Capital Activation path — deferred (service ready to call; Capital Activation not built)

## Delivered

- `Operations::PortfolioActivationService` — mutex + force
- Wired: `wv2:portfolios:activate` / `deactivate` / evaluate-pre-activate (`FORCE=1`)
- Wired: `POST /internal/portfolios/activate` + evaluate (`force` body/query)
- MCP: `wv2_activate_portfolio` accepts `force`; payload maps through
- Interface: `winston-mcp-tools.md` updated
- Specs: 7 examples green; live smoke vs `#12`

## Related

- Capital Activation: `2026-07-09-capital-activation-mcp-telegram.md`
- Schema: `2026-07-09-wv2-op-lifecycle-schema.md` (Done)
