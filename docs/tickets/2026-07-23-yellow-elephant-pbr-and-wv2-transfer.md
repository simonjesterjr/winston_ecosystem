# Ticket: Yellow + Elephant5+20 PBR and Wv2 transfer

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-07-23  
**Domain:** Portfolio Signal Optimization, TradingStrategy, handoff  
**Monoliths:** winston_unit_test, winston_v2  
**See:** [session report](../session-reports/2026-07-23-1038-mint-yellow-exclusive-pbr-dm-transfer.md)

## Problem

Portfolio Yellow (EEM, 17 exclusive markets) has corr_v2 membership and vet screening winners, but **Elephant5+20** was only proven end-to-end on Mint (PBR 121 → OP#311). Yellow needs the same fixed-runner PBR + export + Wv2 import for smoke-test population balance.

## Desired outcome

1. Create PBR from TS **Elephant5+20** on **Portfolio Yellow** (ladder seeded via factory fix).  
2. Confirm non-zero trades / sensible metrics (runner DM lookback fix required).  
3. Export config (pyramid_risks present) and import to Wv2 (paper, inactive default).  
4. Optional: activate for multi-cohort evaluate smoke.

## Acceptance

- [ ] Yellow Elephant PBR completed with trades > 0  
- [ ] Export passes OneWayDynamicRiskValidator  
- [ ] Wv2 OP exists with Yellow books + fingerprint suffix  
- [ ] Session note or sidecar path recorded under `portfolio_configs/`  

## Prerequisites

- WUT fixes from 2026-07-23 session committed (lookback + ladder provenance).  
- Exclusive Yellow membership locked (0 peer overlap).
