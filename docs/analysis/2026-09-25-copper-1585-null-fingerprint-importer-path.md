# Note: Copper #1585 null fingerprint — importer path (not runner stamp)

**Date:** 2026-09-25  
**Related:** plan [`../../plans/copper-1585-fingerprint-importer-adopt.md`](../../plans/copper-1585-fingerprint-importer-adopt.md) · ticket [`../tickets/2026-09-25-copper-1585-fingerprint-importer-adopt.md`](../tickets/2026-09-25-copper-1585-fingerprint-importer-adopt.md) · cutover [`2026-09-24-copper-794-mode-d-cutover.rb`](2026-09-24-copper-794-mode-d-cutover.rb) · paper-send [`../tickets/2026-09-24-mode-d-phase-2-paper-send.md`](../tickets/2026-09-24-mode-d-phase-2-paper-send.md)

## Diagnosis

#1585 (`Portfolio Copper · mode-d-from-wut-794`) was created by rails runner `Portfolio.create!` in the Mode D cutover script. That bypassed `Operations::PortfolioConfigImporter` / `POST /internal/portfolios`, so ADR-006 fingerprint lineage never attached. OP and shared TS **#341** remain null-fingerprint. #341 is also Mode C Copper **#1581**'s strategy — stamping #341 would cross-wire Mode C.

## Operator lock

Fingerprint `d627cd795b410360aff56706dec38759d48f7d32f7cfac4203a29523e2c7c666` (short `d627cd79…`) from WUT PBR #794 heat+RST+window capture. Live WUT `GET /internal/portfolio_config?run_id=794` already returns this hash (2026-09-25). It is not yet a Wv2 TS selection until service-path adopt.

## Preflight risks (seen while drafting)

1. **TST leftover** on #1585 markets (TestDesk residue) — `find_adopt_candidate` requires exact book-symbol match; TST forces **fork** instead of adopt. Clear TST book only when journals=0.
2. **seed_name mismatch** — WUT export seed is `Portfolio Copper`; #1585 seed is the full display name. POST must override `seed_name` to the exact #1585 value.
3. **Paper caps** — export has 11 markets and leverage 3.0; without `force_lab_uncapped: true` the importer normalizes to 4 markets / 1.0× leverage.
4. **Shared TS #341** — adopt must create/find a **new** fingerprinted TS; never `update!` #341.
5. **Import lands inactive** — re-activate with `force=true` (dual-active vs #1581 same markets).

## Doctrine

Desk: never repeat runner mint for OP/TS lineage. Service path only. No SQL fingerprint writes. No Desk Send on this note's ticket.
