# Ticket: Wv2 Active mutex (seed_name + Books set)

**Status:** Proposed

**Date:** 2026-07-09

**Context:** Session [`2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill`](../session-reports/2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill.md). **ADR-006**.

## Problem

Many inactive OPs per seed are desirable (regime archive). Multiple **Active** OPs on the same seed or identical Books dilute attention and risk confusion. Capital Activation defaults Active true while paper may still be Active.

## Scope

1. On activate (rake, internal API, MCP): refuse if another Active OP shares `seed_name` **or** identical Books symbol set, unless force.
2. Clear error message listing the conflicting OP id/name.
3. Apply to Capital Activation when setting new OP Active.
4. Specs for seed conflict, Books conflict, force override, no conflict cases.

## Acceptance

- Second Active same seed blocked without force
- Second Active identical membership blocked without force
- Force documented for short dual-active experiments

## Related

- Capital Activation: `2026-07-09-capital-activation-mcp-telegram.md`
- Schema: `2026-07-09-wv2-op-lifecycle-schema.md` (`seed_name`)
