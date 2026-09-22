# Analysis: Sub-100 share packaging — cash D vs risk M-band (2026-09-21)

**Ticket:** [`../tickets/2026-09-21-packaging-sub100-share-vs-option-m-band.md`](../tickets/2026-09-21-packaging-sub100-share-vs-option-m-band.md)  
**Specimen:** Wv2 journal #1984 — Indigo IBM short 40 shares @ ~228.35 / stop 242.59; leap + standard_call `zero_contracts`; Plan C stock.

## Problem

Packaging uses `floor(signal_share_units / 100)` for contract count. Any N < 100 forces option rungs untradeable and falls to stock — even when **1 contract** would be risk-acceptable.

## Framework

See ticket body for tables. Short form:

- **Cash D:** option cheaper on cash when `100×D < N×S` (long) or `100×D < m×N×S` (short vs margin). On the specimen these bars are high (~$91 / ~$46) — **not decisive**.
- **Risk M:** allow 1 contract when `N ≥ M = (100×δ)/k`. Below M → stock; M…99 → one contract; ≥100 → floor(N/100).
- Shorts use **long puts**, never short calls, for Turtle packaging.

## Tentative default

k=1.5, δ≈0.7 → M≈47. Specimen N=40 → stock correct under that default.

## Review

Operator + CoS review by **2026-10-01**.
