# Ticket: First Daily Analysis on Turtle Mint S2 + Yellow S1

**Status:** Done — verified on live DA 2026-09-04 (ops had already run)  
**Priority:** P1  
**Date:** 2026-08-13  
**Monolith:** winston_v2  
**See:** handoff [`2026-08-13-handoff-mint-s2-yellow-s1-observation.md`](2026-08-13-handoff-mint-s2-yellow-s1-observation.md); session [`2026-08-13-1528-turtle-paper-handoff.md`](../session-reports/2026-08-13-1528-turtle-paper-handoff.md)

## Problem

#797 Mint · 85730621 (Turtle S2) and #798 Yellow · 7aa73357 (Turtle S1) are Active paper but have **not** been through Daily Analysis (DA). No drafts, tasks, or Daily Activity Report (DAR) rows yet.

## Scope

1. Run `wv2:portfolios:evaluate` (or wait for scheduled DA) covering the current Active set.  
2. Confirm #797 / #798 / #384 all appear (dual-Active Mint must stay distinct).  
3. Spot-check sizing is **1%** of risk equity on the Turtle OPs, **2%** on #384.  
4. Note any `missing_data` / `unsupported_strategy` skips (Breakout10 / Breakout55 must resolve).

## Acceptance

- [x] DA result rows for #797 and #798 (evaluated or explicit skip reason)  
- [x] DAR / ops shell lists both new OPs under paper band  
- [x] No 100% unit-size on Turtle drafts  

## Non-goals

- Desk confirm / fills  
- Real capital

---

## Close-out (2026-09-04)

Did **not** re-run `wv2:portfolios:evaluate` (Friday session still open). Live ops already scored these OPs.

Verified against 2026-09-03 Daily Analysis Report (DAR) (`storage/cromwell_notifications/wv2_20260903.json`) and Winston v2 (Wv2) rows:

| OP | Seed | Fingerprint | risk_percentage | Entry / exit | 2026-09-03 |
|----|------|-------------|-----------------|--------------|------------|
| **#797** | Mint Turtle S2 | `85730621` | **1.0** (1%) | Breakout55 / Breakout20 | chapter present; pyramid OIH 4 units |
| **#798** | Yellow Turtle S1 | `7aa73357` | **1.0** (1%) | Breakout20 / Breakout10 | chapter present; enter ANET 5 units; pyramid BNO 28 |
| **#384** | Mint FastBO5 | `0478e0ea` | **2.0** (2%) | Breakout5 / VolatilityExit | chapter present; pyramid OIH 8, UNG 337 |

- `skipped_portfolios` = [] — Breakout10 / Breakout55 resolved (not `unsupported_strategy` / `missing_data`).
- Attention band **paper** on the DAR. Dual-Active Mint #797 and #384 both listed.
- Passed signals: #797=8, #798=34, #384=23. Tasks: #797=19, #798=32, #384=42 (through 3 Sep).
- Turtle max journal units 87 / 66 — not the 100% importer bug. #384 UNG 337 at 2% is FastBO5, not Turtle.

First DA happened in unattended EOD after the 13 August handoff. Ticket was stale Proposed.  
