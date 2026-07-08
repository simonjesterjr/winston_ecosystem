---
Status: Proposed
---

# Ticket: Review the 8 "manual" symbols registered via reconcile (CDE, IBM, JNJ, PG, ROKU, RXT, WMT, WTI)

**Related to:** ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md

## Context
During the first successful `data:reconcile` run, these 8 symbols had no prior `SymbolRegistryEntry` (or one without `list_source`). The reconcile path now defaults them to `list_source: "manual"`.

They are common / well-known symbols (big caps + a few others). They may have been acquired via direct EODHD calls, manual parquet drops, or older non-registry paths.

## Acceptance Criteria
- [ ] Inspect each symbol's history (how its parquet was originally created, any prior registry attempts).
- [ ] Decide for each whether `manual` is correct, or whether it should be re-classified (e.g. `eodhd_screener`, `catalog`, `seed`).
- [ ] Update the entries (and any related suitability / list_metadata) as needed.
- [ ] Add a note or small migration script if a batch correction is warranted.
- [ ] Confirm they now appear correctly in `awaiting_evaluation` / suitable scopes after reconcile.

## Links
- Session report (error log section): `ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md`
- SymbolRegistryEntry model and LIST_SOURCES
- ReconciliationService registry sync code

**Owner:** human  
**Due:** before treating the full symbol registry as authoritative post-reconcile