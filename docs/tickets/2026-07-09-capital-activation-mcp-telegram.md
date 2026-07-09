# Ticket: Capital Activation (MCP / Telegram)

**Status:** Proposed

**Date:** 2026-07-09

**Context:** Session [`2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill`](../session-reports/2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill.md). **ADR-006**. Operator speech: “Activate Portfolio Red + Ts10 with initial capital of $13,986”.

## Problem

Paper→real must open a **new** OP series with stated capital — not rewrite paper equity. Telegram “Activate” is overloaded with the Active attention flag.

## Scope

1. Domain service: Capital Activation from seed + TS fingerprint + initial capital $X.
2. Defaults: new OP `execution_mode=real`, Active true; new initial CashEvent = $X only.
3. Paper A not auto-closed or auto-deactivated.
4. Dual Active same seed/Books → require `FORCE_DUAL_ACTIVE` (or equivalent).
5. Real requires trade_ready provenance or `FORCE_REAL`.
6. MCP tool + Cromwell skill/docs phrasing; rake for smoke.
7. Clear operator errors distinguishing set-Active vs Capital Activation.

## Acceptance

- New OP capital_base starts at $X independent of paper terminal equity
- Paper series journals unchanged
- Force flags required for dual Active and observation→real
- Documented in lifecycle business-context / portfolio_configs README

## Related

- `wv2-operational-portfolio-lifecycle.md`
- Active mutex: `2026-07-09-wv2-active-mutex-seed-books.md`
- export_kind: `2026-07-08-wv2-importer-honor-export-kind.md`
