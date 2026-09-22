# Ticket: Sub-100 share packaging — M-band (1 contract vs stock) for long call/LEAP and long put

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-09-21  
**Review by:** 2026-10-01 (Chief of Staff reminder routine)  
**Mode:** design → grill → policy/code  
**Graph nodes:** winston_v2 (fulfillment packaging ladder, Justification, journal stamp); broker_gateway (option candidates); ecosystem ADR-018 / leap law  
**Implementer:** TBD (Winston Dev after Operator locks k / δ)  
**Human gates:** lock risk-overshoot k and δ assumptions before coding; paper Mode C first; no ADR until irreversible desk law  
**DoD (first deliverable):** analysis filed; ticket open; Operator review of M/D bands; decision whether to replace blunt `floor(N/100)=0` with M-band rule  
**Origin:** Operator paper journal [#1984](https://sawtooth-ai.tail944ffb.ts.net/wv2/operations/workflow?journal_id=1984&portfolio_id=1583&task_id=1837) (Indigo IBM short 40 shares → `zero_contracts` → Plan C stock) + CoS analysis 2026-09-21  
**Related:** ADR-018 packaging rung; [`2026-09-19-standard-call-fulfillment-packaging-rung.md`](2026-09-19-standard-call-fulfillment-packaging-rung.md); [`2026-09-18-mode-c-leap-preferred-underlying-fallback.md`](2026-09-18-mode-c-leap-preferred-underlying-fallback.md); [`2026-09-09-extra-modal-leap-unit-evaluation.md`](2026-09-09-extra-modal-leap-unit-evaluation.md); [`../business-context/leap-extra-modal-proxy.md`](../business-context/leap-extra-modal-proxy.md); [`../analysis/2026-09-21-packaging-sub100-share-vs-option-m-band.md`](../analysis/2026-09-21-packaging-sub100-share-vs-option-m-band.md)

## Goal

Replace (or refine) the blunt packaging gate `floor(signal_share_units / 100) == 0 → zero_contracts` with an **M-band** rule so that when Turtle sizing yields **N < 100** shares, the desk can still choose **1 long call / LEAP** (longs) or **1 long put** (shorts) when risk overshoot is acceptable — instead of always falling to stock.

## Specimen (#1984)

| Field | Value |
|-------|-------|
| Portfolio | Indigo evolved `#1583` (from WUT `#724`) |
| Underlying | IBM |
| Direction | short |
| Units (shares) | **40** |
| Signal / exec | ~228.35 |
| Stop | 242.59 |
| 1R (stock) | ~40 × 14.24 ≈ **$570** |
| Ladder | leap → standard_call → stock |
| Outcome | both option rungs `zero_contracts`; Plan C **stock** short |

## Analysis summary (Operator + CoS)

### Lenses

1. **Cash outlay** — capital leaving the account today  
2. **Risk dollars (1R)** — Turtle-relevant  
3. **Oversizing** — 1 contract vs intended N-share unit  

For N < 100 the alternative to N shares is almost always **1 contract** (~100 × δ share-equivalent). Cash-only comparisons mislead.

### Long

- Stock capital ≈ N × S (specimen long-analogue: 40 × 228 ≈ $9.1k)  
- 1 long call/LEAP capital ≈ 100 × D  
- **Cash break-even:** D < (N/100) × S → specimen D < ~$91 (almost always true → not decisive)  
- **Risk gate:** accept 1 contract iff R_opt ≤ k × R_stock with R_opt ≈ 100 × δ × stop_distance:

  **M = (100 × δ) / k**

  | δ | k | M (min shares for 1 contract) |
  |---|---|-------------------------------|
  | 0.7 | 1.0 | 70 |
  | 0.7 | 1.5 | ~47 |
  | 0.5 | 1.5 | ~33 |
  | 0.5 | 2.0 | 25 |

**Proposed band**

- **N < M** → stock (1 contract oversizes 1R too much)  
- **M ≤ N < 100** → allow **1** LEAP / standard long call if D/liquidity OK  
- **N ≥ 100** → `floor(N/100)` contracts as today  

D inside the middle band is a **liquidity/quality** gate (spread, % of S), not the primary vs-stock break-even.

### Short

Symmetric with **long put** (not short call — undefined risk):

- Short stock: credit N×S but margin ≈ m × N × S; borrow/locate  
- 1 long put: debit 100 × D_put; defined risk  
- Margin cash break-even (m≈0.5): D < ~$46 on specimen — again often true, not decisive  
- **Same M = 100 × δ_put / k**  
- Below M → short stock (what #1984 did under k=1.5 / δ≈0.7)  
- M ≤ N < 100 → allow 1 long put when borrow is painful or defined risk wanted  

### Tentative desk default (not locked)

- **k = 1.5**, LEAP δ ≈ 0.65–0.75 → **M ≈ mid-40s to ~50s**  
- Specimen N=40 sits **just under** that → stock was correct under this default  

## Non-goals

- Short calls / credit structures as Turtle short packaging  
- Changing TF signal or stop law  
- Silent Plan B on auth/CPGW failure  
- Shipping code before Operator locks k / δ  

## Work items

- [ ] Operator lock: k, δ assumptions (LEAP vs standard_call), long vs short  
- [ ] Decide: replace `zero_contracts` share-floor with M-band, or keep floor and add M as overlay  
- [ ] Spec Wv2 Justification copy for “1 contract allowed: N≥M, risk overshoot ≤k”  
- [ ] Spec BG option_candidates path when N<100 but M-band passes  
- [ ] Paper walk on Indigo/Teal with N in [M, 99]  
- [ ] If irreversible: ADR addendum to ADR-018 (only after lock)  
- [ ] **Review checkpoint 2026-10-01** — status, locks, next step  

## Open questions

1. One M for LEAP and standard_call, or separate δ (LEAP higher δ → higher M)?  
2. Cap absolute 1R overshoot dollars in addition to k?  
3. Short side: prefer put when borrow fee > X even if N < M?  
