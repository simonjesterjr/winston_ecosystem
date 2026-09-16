# Ticket: Wv2 paper Blue — IBKR-eval LEAP, paper-only fulfill (from WUT #685)

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-09-16  
**Mode:** contractor / CoS enablement  
**Graph nodes:** winston_v2 (primary); broker_gateway / IBKR (quotes·conid·packaging **eval only**); winston_unit_test (fingerprint source PBR **#685**)  
**Human gates:** no IBKR option Desk Send for this portfolio; agent never Desk-Sends; no pack promotion  
**Origin:** John → Chief of Staff 2026-09-16; Scribe filing  
**DoD:** Ops portfolio **381** (Blue) deactivated; new Blue **$30k** + TS from WUT PBR **#685** fingerprint is **LEAP-only**, **paper-only**, **not IBKR-bound for fulfillment**; IBKR used only to evaluate option strategy (quotes / conid / simple LEAP packaging). Fills, journals, and cash stay in Wv2 paper.  
**Contrast:** Walnut remains **IBKR-bound fulfillment**.  
**Related:** autopsy [`../analysis/2026-09-16-pbr685-blue-leap-s1-2pct.md`](../analysis/2026-09-16-pbr685-blue-leap-s1-2pct.md) · wrap [`../session-reports/2026-09-16-1538-pbr685-blue-leap-s1-2pct-autopsy.md`](../session-reports/2026-09-16-1538-pbr685-blue-leap-s1-2pct-autopsy.md) · plan [`../../plans/wv2-bg-ibkr-leap-fulfillment.md`](../../plans/wv2-bg-ibkr-leap-fulfillment.md) · packaging ticket [`2026-09-15-wv2-leap-packaging-fields.md`](2026-09-15-wv2-leap-packaging-fields.md) · ADR-017 (Proposed) · domain [`../business-context/leap-extra-modal-proxy.md`](../business-context/leap-extra-modal-proxy.md) · desk law [`../business-context/exit-and-protective-stop-desk-law.md`](../business-context/exit-and-protective-stop-desk-law.md)

## Problem

Wv2 paper portfolios need to **evaluate** LEAP substitution using IBKR connectivity (quotes, conid, simple packaging) without **fulfilling** through IBKR. Today’s mental model conflates IBKR eval with IBKR-bound fulfillment (Walnut path). John wants a new Blue paper book cloned from lab winner **#685** that is explicitly paper-fulfillment while still able to price/package LEAPs via IBKR reads.

## Scope

1. **Policy note (session/ticket trail):** Wv2 paper = IBKR-eval allowed; IBKR fulfill **forbidden**. Walnut = IBKR-bound fulfillment (unchanged).
2. **Deactivate** Wv2 ops portfolio **381** (current Blue).
3. **Create** new Blue ops portfolio: **$30k** capital, Trading Strategy / fingerprint from WUT PBR **#685** (`blue_rst_turtle_r02_leap30k_ts75`, TS75, leap_fulfillment=all, risk 2%, RST, turtle heat).
4. Stamp portfolio as **LEAP-only**, **paper-only**, **no IBKR bind** for order write / Desk Send path; wire IBKR (or BG read) only for option-strategy evaluation / packaging candidate resolution.
5. CoS investigates enablement path (which knobs / fulfillment_label / packaging_policy / broker bind flags); implement once path is clear.

## Non-goals

- Changing ADR-017 / Model B packaging law (no ADR unless packaging law changes)
- Option Desk Send on IBKR for this Blue
- Pack promotion / Capital Activation
- Replacing Walnut IBKR fulfillment
- Treating `cash_vs_journal_delta` as fake equity (root cause: short-LEAP entry journals always debit — see analysis § Journal gap; trust final_cash/OA; WUT ticket `2026-09-16-leap-short-entry-journal-direction.md`)

## Acceptance

- [ ] Written desk contrast: paper Blue (IBKR-eval, Wv2 paper fulfill) vs Walnut (IBKR fulfill) is in ticket + session note
- [ ] Ops portfolio 381 deactivated (evidence: id + timestamp / UI or rails note)
- [ ] New Blue $30k exists with #685-derived TS/fingerprint; LEAP-only; paper-only; not IBKR-bound for fulfillment
- [ ] IBKR path used for quotes/conid/simple packaging eval only — no OPT `place_order` from this portfolio
- [ ] Links to #685 analysis + wrap; journal-gap caveat retained
- [ ] INDEX updated; no ADR opened unless packaging law changes





## Mode C packaging locks (John via CoS, 2026-09-16) — grill complete · build enablement

**Discarded:** auto re-ATM / re-resolve at paper-fill for stale stamped strike (interim grill note; not desk lock).

**Locked:**

1. **No Black-Scholes** for packaging. Use the **IBKR real chain** for the ATM LEAP package (IBKR-eval only — still **no IBKR fulfill** for this Blue).
2. **Staleness OK:** EOD TS75 signal → resolve ATM LEAP; HITL paper Desk-Approve may lag many hours. Essential is a **correct ATM notional package**, not freshness-at-Approve.
3. **Stop-out:** when underlying Working Stop pierces → **auto journal sell-to-close** the LEAP on paper (**no HITL on exit**). **Entry stays HITL.**
4. **Spending:** `premium × 100 × contracts` vs paper cash.
5. **Fingerprint locked:** WUT **#685** / **TS75** — `$30k`, **2%**, leap all, S1 (`blue_rst_turtle_r02_leap30k_ts75`).

**Cutover (after enablement):** deactivate ops **381** → stand up new Blue from that fingerprint.

**Plan:** Mode C section in [`../../plans/wv2-bg-ibkr-leap-fulfillment.md`](../../plans/wv2-bg-ibkr-leap-fulfillment.md). **ADR:** none unless Mode C conflicts with ADR-017 (paper-eval variant; Walnut/IBKR-bound path stays Model B).

CoS launching cloud agents for code.

## Open questions (implementation)

- Exact enablement knobs (fulfillment_label, packaging_policy, broker account bind, Session Order Slate off, etc.) — CoS/cloud agents
- Paper LEAP fill path (dummy_sim / internal journal) and how protective WS maps to auto STC without IBKR GTC

## Notes

- #685 autopsy: high cash/OA return at 2% but worse risk-adjusted than Blue 1% #684 / Red 1% #692; investigate journal delta before any promote narrative.
