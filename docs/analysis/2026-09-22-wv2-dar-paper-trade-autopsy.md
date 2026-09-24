# Wv2 DAR paper-trade autopsy — 2026-09-22

**Date:** 2026-09-22 (America/Denver)  
**From:** Forensics (Operator ask via CoS)  
**Sources:** `winston_v2/storage/cromwell_notifications/wv2_20260922.json`, Journal DB (`status=executed`, updated/confirmed that evening), Position stops.  
**Scope:** Evidence math only. No sizing-rule code changes.  
**Rows:** `ecosystem/docs/analysis/_dar_20260922_rows.json`

---

## Verdict

| Area | Result |
|------|--------|
| Cash/notional arithmetic (a) | **PASS** on formula for all 21 executed journals once short **covers** are treated as buy-to-cover **debits** (AMGN J1990/J2030). Stock: `flow = ±shares×price`. Options: `flow = −contracts×premium×100`. |
| LEAP packaging (b) | **PASS packaging math** for J2015,2019,2020,2022,2026 (conid + expiry + strike + premium + cash_outlay). Paper desk_workflow — **no live BG Order/Fill** found in this probe. |
| Standard calls (c) | **PASS math** J2021 SEF, J2027 BITQ (Plan B after `no_expiry_ge_min`). |
| Stock (d) | **PASS math**; **FAIL smell** on Teal J2029 / Indigo J2028 USDU Plan-C stock (tiny N → huge share count vs equity). |
| Teal 2872 USDU | Sizing **arithmetically correct** under 2% / 2N; capital consumption **~266% of risk equity** — Turtle-spirit fail (plan-only ticket belongs to CoS). |

**Hold promote language** that “workflow smooth = books healthy.” Packaging UX can be fine while Plan-C stock on low-ATR names overdrafts paper cash (`capital_base` Teal → **−47648.8** after J2029).

---

## Verdict table (executed journals confirmed ~22:35–22:57 UTC)

| journal | portfolio | symbol | kind | a cash | b/c/d | notes |
|--------:|-----------|--------|------|--------|-------|-------|
| 1989 | Mint | USO | stock short | PASS | d PASS | credit 18×142.67 |
| 1990 | Yellow | AMGN | stock cover | PASS* | d PASS | exit short → debit; sibling flatten J2030 |
| 1991 | Yellow | ANET | stock | PASS | d PASS | |
| 1992 | Yellow | AKAM | stock pyr | PASS | d PASS | |
| 2013 | Blue | TSM | stock pyr | PASS | d PASS | leap fail `zero_contracts` → stock |
| 2014 | Blue | GOOGL | stock | PASS | d PASS | large notional vs free cash |
| 2015 | Blue | RXT | **LEAP** | PASS | **b PASS** | conid 923585415 C4 2029-01-19 prem 2.30 ×8×100 |
| 2016 | Red | VXX | stock short | PASS | d PASS | Plan C after `no_atm_leap` |
| 2018 | Orange | AAPL | stock pyr | PASS | d PASS | |
| 2019 | Orange | XLK | **LEAP** | PASS | **b PASS** | conid 923652926 C196 2029-01-19 prem 43.125 |
| 2020 | Mango | SVXY | **LEAP** | PASS | **b PASS** | conid 923650611 C64 2029-01-19 prem 13.45 |
| 2021 | Mango | SEF | **call** | PASS | **c PASS** | conid 893744520 C30 2027-02-19; Plan B |
| 2022 | Mango | RXT | **LEAP** | PASS | **b PASS** | same conid as 2015; 4 contracts |
| 2023 | Copper | TSM | stock pyr | PASS | d PASS | |
| 2024 | Copper | GOOGL | stock | PASS | d PASS | |
| 2025 | Slate | TSM | stock pyr | PASS | d PASS | |
| 2026 | Slate | WMT | **LEAP** | PASS | **b PASS** | conid 923658468 C110 2029-01-19 prem 22.90 |
| 2027 | Indigo | BITQ | **call** | PASS | **c PASS** | conid 912464575 C28 2027-04-16; Plan B |
| 2028 | Indigo | USDU | stock | PASS | **d SMELL** | Plan C; 2809 sh; ~206% of run_cap |
| 2029 | Teal | USDU | stock | PASS | **d SMELL** | Plan C; **2872** sh; ~265% of run_cap |
| 2030 | Yellow | AMGN | stock cover | PASS* | d PASS | flatten sibling of 1990 |

\*Initial automated sign check marked FAIL until exit convention applied; `cash_impact` field matches debit cover.

Walnut STP drafts (1993–2012) excluded — not executed.

---

## Failures / smells (expected vs actual)

1. **Teal J2029 / Indigo J2028 USDU Plan C** — cash equation holds (`2872×26.65=76538.8`) but **equity base cannot fund** the notional without implied margin/overdraft. Post-trade Teal `capital_base=−47648.8`.  
2. **AMGN sign (tooling only)** — raw “short ⇒ credit” heuristic wrong on **stop-out cover**; journal debit is correct.  
3. **IBKR live fill** — not evidenced in BG AR models this pass. LEAP/call credibility rests on packaging `conid` + premium + `cash_outlay` identity, not broker execution tickets.  
4. Several Mode C stock fills after leap `zero_contracts` / `no_atm_leap` — packaging path OK; size still stock-path risk units.

---

## Teal 2872-share USDU (one paragraph)

Teal P1584 risk **2%**, `atr_multiplier=2`, LEAP-preferred with Plan C stock fallback after `leap_failure_code=no_candidates` (no listed options). Signal close **26.65**; position `original_stop=26.45` ⇒ stop distance **0.20** = **2N** with **N=0.10**. Using DAR risk equity **28727.88**: risk$ = `28727.88×0.02=574.56`; shares = `floor(574.56/0.20)=2872`. Cash outlay `2872×26.65=76538.80` ≈ **266% of risk equity** / **265% of run_capital 28890**. Journal flow and packaging cash_impact match; heat did not shrink the unit. The smell is **correct Turtle unit math on a tiny-N name + stock fulfillment**, not a broken multiply — capital-consumption / min-ATR inclusion is the CoS plan-only ticket, not a Forensics code fix.

---

## System One blocks

### State
- date: 2026-09-22; executed journals: 21 (desk_workflow confirm)  
- cash identity: stock ±shares×px; option −contracts×premium×100 — matched quoted flows  
- Teal J2029: units=2872, px=26.65, flow=−76538.8, stop=26.45, N=0.10, atr_mult=2, risk%=2, risk_equity=28727.88, capital_base_after=−47648.8  
- Indigo J2028: units=2809, flow=−74859.85, same Plan C path  
- LEAP conids present: 923585415, 923652926, 923650611, 923658468 (+ RXT dup); calls 893744520, 912464575  
- BG live Order/Fill: not found in this probe  
- claim under test: “Pending walk smooth ⇒ paper books/sizing healthy”

### Questions
| id | type | instructions |
|----|------|--------------|
| cash_books_ok | Noul | Journal flow matches shares×price or contracts×premium×100 for today’s executed paper trades (after short covers as debits). |
| teal_sizing_correct_but_spirit_wrong | Noul | Teal USDU 2872 is correctly computed from 2%/2N on low-N USDU, but ~266% equity consumption violates Turtle-spirit capital use. |
| leap_packaging_credible | Noul | LEAP/call journals carry real IBKR conid/expiry/strike/premium and cash_outlay = contracts×premium×100. |
| promote_language_ok | Noul | Today’s paper DAR walk supports saying books/packaging are healthy with no sizing smell. |

### Adjudication (`jev ask`, jev-1.13.0)
| id | noul | band |
|----|------|------|
| cash_books_ok | **0.76** | middle → Operator (exit-convention nuance) |
| teal_sizing_correct_but_spirit_wrong | **0.76** | middle → Operator / plan-only capital rule |
| leap_packaging_credible | **0.39** | fail soft-pass — wants live BG fills |
| promote_language_ok | **0.33** | **do not** soft-pass promote language |

### Recommendation
**Hold** any “all clear” promote wording. **Ship** to CoS: cash arithmetic OK; LEAP/call packaging internally consistent; **escalate** Teal/Indigo USDU Plan-C oversizing to Operator + existing capital-consumption plan ticket. No Forensics code change.

---

## Addendum — Capital Fit locked 2026-09-23

Operator confirmed the Teal share count: `floor(2% × $28,727.88 / $0.20) = 2,872`. The smell is fully paid stock on a $0.10 N, not a broken multiply. Hold “books healthy.”

Capital Fit is the side check. First lot on an empty book is at most 1/portfolio-cap of today’s min(free cash, risk equity). Later lots retire that reserve (a 3rd lot is not still stuck at 1/10; an 11th may consume what is left). A capped stock whose stop-risk is under 0.20% of equity is passed. Winston Unit Test uses the same divisor and the same small-N max, with tradeable cash for longs and `max_leverage` as short capacity only. See `ecosystem/docs/tickets/2026-09-22-min-atr-capital-consumption-guard.md`.

