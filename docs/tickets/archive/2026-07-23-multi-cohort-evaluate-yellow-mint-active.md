# Ticket: Multi-cohort evaluate smoke with Yellow #330 + Mint #311 Active

**Status:** Done  
**Priority:** P2  
**Date:** 2026-07-23  
**Closed:** 2026-07-24  
**Domain:** Daily Analysis, paper Active band, smoke  
**Monoliths:** winston_v2  
**See:** [session report](../session-reports/2026-07-23-1158-yellow-122-wv2-activate.md); Mint activate: [`2026-07-23-activate-wv2-mint-op311-smoke.md`](2026-07-23-activate-wv2-mint-op311-smoke.md)

## Problem

Yellow OP **#330** (`Portfolio Yellow · 92776cfd`) and Mint OP **#311** (`Portfolio Mint · 3749c990`) are both **Active paper** after exclusive-cohort handoffs. Multi-cohort Daily Analysis / evaluate has not been re-run as a deliberate smoke since both joined the Active band.

## Desired outcome

1. Run evaluate for the current Active set (or explicit date) without auto-activating extras.  
2. Confirm both #311 and #330 appear in notification / DAR portfolio list.  
3. Note any `missing_data` / skip reasons for Yellow or Mint markets.  
4. Short session note or checklist tick on success.

## Acceptance

- [x] `wv2:portfolios:evaluate` (or internal evaluate) completes for Active band including #311 + #330  
- [x] Operator-visible summary: which OPs evaluated, errors if any  
- [x] No unexpected activation of demos/smoke OPs  

## Smoke evidence (2026-07-24 ~15:50 UTC)

**Command:** `bin/compose exec -T winston_v2 bin/rails wv2:portfolios:evaluate`  
(no `id_or_name` — all Active; no force-activate)

| Check | Result |
|-------|--------|
| Date | `2026-07-24` |
| DM ingest | `ingested=88`, `skipped=3`, `errors=[]` |
| Portfolios evaluated | **7** — status all `evaluated` |
| Skipped | **0** (`skipped_portfolios: []`) |
| #311 Mint | `evaluated` — strategy Elephant window `2019-11-01–2026-07-22 · 3749c990` |
| #330 Yellow | `evaluated` — strategy Elephant window `2019-05-28–2026-07-22 · 92776cfd` |
| Actions / pending | **0** / **0** (quiet day — no new desk drafts) |
| missing_data / skip | **None** for Mint or Yellow |
| PCS (daily_job) | Mint **91.2**; Yellow **73.31** (history + current) |
| DAR artifacts | `storage/reports/wv2_20260724.md` + `.pdf` (9 pages); notif `storage/cromwell_notifications/wv2_20260724.json` |
| Webhook | delivered **200** → MCP audit path |
| Telegram | **skipped** `non_production_date` (eval date 2026-07-24 vs production_date 2026-07-23) — intentional guard, not a smoke fail |
| Active set after | unchanged: #6, #11, #157, #240, #308, **#311**, **#330** — no Smoke* portfolios Active |

### Active paper band (post-smoke)

| Id | Name | Mode |
|----|------|------|
| 6 | Portfolio Orange · 6622b2eb | paper |
| 11 | Portfolio Rust · dd7e7c7a | paper |
| 157 | Portfolio Mango (WUT run 57) | paper |
| 240 | Portfolio Blue · 9cf64e64 | paper |
| 308 | Portfolio Orange · 7ea76741 | paper |
| **311** | **Portfolio Mint · 3749c990** | paper |
| **330** | **Portfolio Yellow · 92776cfd** | paper |

### Notes

- Mint/Yellow equity still at initial $10k (no fills yet) — expected for new paper OPs with zero actions.  
- Market table in DAR lists Mint symbols (AMCR, APLD, ASTS, …) and Yellow symbols (ABBV, AEP, …) with bars and signal-inspect links — data path healthy.  
- Telegram skip is consistent with historical-DAR guards: mid-session calendar date ahead of last settled EOD production date.

## Non-goals

- Real capital activation  
- Changing Active mutex policy  
- Fixing MCP transfer path  

## Ops sketch

```bash
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:list
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:evaluate
# inspect cromwell notification / DAR as usual
```
