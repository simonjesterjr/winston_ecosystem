# ADR-011: Alt Filings are DM-owned events, not EOD bars

**Status:** Accepted
**Date:** 2026-08-18
**Deciders:** Architecture (plan: Quiver API in Winston)
**Builds on:** ADR-001, ADR-002, ADR-003, ADR-009
**Domain context:** `CONTEXT.md` — Alt Filing, data_manager, Daily Analysis

## Context

Quiver Quantitative (and similar vendors) sell **event** datasets: U.S. House/Senate trades, Form 4 insider trades, contracts. Winston already has a single bar upstream (EODHD) and a Human-Gated desk. We needed a home for Quiver that does not fork a fourth monolith or poison the bar contract.

Alternatives:

- **A: New `quiver/` monolith** — dataset ≠ domain
- **B: WUT or Wv2 fetch Quiver** — duplicate keys; lab/ops drift; desk request path depends on a paid vendor
- **C: Bake columns into Winston EOD Standard parquet** — events are not OHLCV; ADR-002/003 consumers would break
- **D: DM second adapter, event store + internal read API** — same acquisition owner as EODHD, separate artifact family

## Decision

We chose **D**.

- **DM** holds `QUIVER_API_KEY`, the HTTP client, sync job, and `quiver_filings`.
- Artifacts are **Alt Filings** (PG rows; optional `data/alt/quiver/` parquet later). Not `{SYMBOL}` EOD parquet.
- WUT and Wv2 **read** `GET /internal/alt/quiver`. They do not store the vendor key.
- **Daily Analysis** must not mint enter/pyramid/exit from an Alt Filing. Inspect/DAR footnote only.
- A House Long-Short (or similar) book is a **WUT lab PBR**, not an overlay on existing Operational Portfolios.

## Consequences

### Positive
- One acquisition owner; EODHD bar pipeline stays single-upstream.
- Lab and ops see the same filing set.

### Negative
- New PG tables in DM; another secret and cron.
- Cannot reproduce Quiver’s published CAGR without unpublished lookback/weight details.

### Risks mitigated
- Look-ahead: live/lab entry uses **file date**, not transaction date (STOCK Act ≤45-day lag).
- Desk policy: Congress prints stay context, not signals (ADR-009).
