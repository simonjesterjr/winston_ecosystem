# Ticket: Wv2 Operational Portfolio lifecycle schema

**Status:** Proposed

**Date:** 2026-07-09

**Context:** Session [`2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill`](../session-reports/2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill.md). **ADR-006**.

## Problem

ADR-006 needs durable fields that do not exist on Wv2 Portfolio / TradingStrategy today.

## Scope

1. Migrations (or equivalent) for approximately:
   - `portfolios.seed_name`
   - `portfolios.fingerprint` (and/or shared provenance JSON)
   - `portfolios.execution_mode` (`paper` | `real`, default paper)
   - `portfolios.export_kind` (or provenance)
   - `portfolios.closed_at` / lifecycle status
   - `portfolios.successor_of_id` (or bidirectional successor link)
   - `trading_strategies.fingerprint`, `fingerprint_payload` / provenance as needed
2. Model validations and helpers: `engaged?` (journals.any?), `closed?`, display name builder.
3. Backfill strategy for existing rows (seed_name from name; mode paper; no fingerprint).

## Acceptance

- New imports can persist all ADR-006 lineage fields
- Engaged/closed queryable without scanning journals only for closed
- Specs for helpers and constraints

## Related

- Import lineage ticket: `2026-07-09-wv2-import-lineage-fingerprint-adopt-fork.md`
- Capital Activation ticket: `2026-07-09-capital-activation-mcp-telegram.md`
