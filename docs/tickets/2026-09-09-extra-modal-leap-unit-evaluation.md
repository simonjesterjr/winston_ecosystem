# Ticket: Extra-modal LEAP vs share-unit evaluation (Walnut, after grain automation)

**Status:** Proposed — read-only unblocked (2026-09-11)  
**Priority:** P1  
**Date:** 2026-09-09  
**Mode:** contractor  
**Graph nodes:** winston_v2, broker_gateway, winston_unit_test (sizing skeleton only)  
**Human gates:** paper DUT only; no Desk Send of an option until the read-only matrix says tradable; agent never Desk-Sends  
**DoD:** A limited evaluation matrix can compare one Winston risk unit in shares vs an at-the-money (ATM) ~3-year Long-term Equity Anticipation Security (LEAP) on Interactive Brokers (IBKR) paper DUT using live (or snapshot) quotes — not Winston Unit Test (WUT) Black-Scholes — and a later slice can Desk-Send that LEAP as the fulfillment command if the grill locks geometry B  
**Origin:** Operator lock 2026-09-09 after Walnut STP slate — Direction 1 first; Direction 2 parked for pickup when Walnut’s session grain is automated so the book can run on its own  
**Related:** analysis [`docs/analysis/2026-09-09-extra-modal-leap-unit-vs-shares.md`](../analysis/2026-09-09-extra-modal-leap-unit-vs-shares.md) (**read this first — do not re-derive**); parent grain [`2026-09-09-walnut-paper-session-order-slate.md`](2026-09-09-walnut-paper-session-order-slate.md); Accept-Fill [`2026-09-09-walnut-stp-accept-fill-day-entry.md`](2026-09-09-walnut-stp-accept-fill-day-entry.md); close reconcile [`2026-09-09-walnut-day-stp-close-reconcile.md`](2026-09-09-walnut-day-stp-close-reconcile.md); CPGW session [`2026-09-06-ibkr-cpgw-unattended-session.md`](2026-09-06-ibkr-cpgw-unattended-session.md); packaging UI [`2026-09-01-fulfillment-packaging-policy-ops-ui.md`](2026-09-01-fulfillment-packaging-policy-ops-ui.md); Exit Capital Reconcile [`2026-08-05-signal-path-truth-fulfillment-link-exit-reconcile.md`](2026-08-05-signal-path-truth-fulfillment-link-exit-reconcile.md); ADR-013 §7; `CONTEXT.md` Extra-Modal Fulfillment / Protective Stop Guardrail

## Pickup (amended 2026-09-11)

**Read-only 1×1 may start now** in parallel with Spending Capacity (`plans/spending-capacity-and-leap-fulfillment.md`). DUT SMA liquidation (612 DBC @ 33.15, stop never hit) is the cash-outlay reason.

**Option Desk Send still blocked** until:

- [ ] Part 1 SC Check live on Walnut
- [ ] 1×1 matrix row tradable (live CPGW quote, not Black-Scholes)
- [ ] Grill: cash flip, geometry B, stop HITL vs sell-to-close

Do **not** send options until Walnut paper can run the session cycle without a human babysitting every repark:

- [ ] Broker Gateway cancel + replace on paper DUT (parent slate ticket)
- [ ] One Walnut DAY stop-market Accept-Fills at the DUT print
- [ ] Fill-driven parks: new protective Good-Til-Cancelled (GTC) after a print; DAY add exists for the next pyramid
- [ ] After cash close: unfilled DAY gone; protective GTC still live if the lot is open

“Walnut running on its own” here means park → print → book → repark is automated on the stock Session Order Slate. It is **not** permission to skip the LEAP human gates below, and it is **not** Slate Automation of unsent entry legs (still refused for Walnut unless a later grill).

## Problem

Trend Following (TF) sizes a **share** unit (example: 2% of capital, stop 2N). Operators often want the **same unit** with less cash at risk via a listed ATM ~3-year LEAP call. WUT can synthesize a premium; Winston v2 (Wv2) can **book** extra-modal packaging; neither can **evaluate or send** a live IBKR LEAP. Client Portal Gateway (CPGW) can resolve option contract identifiers and place limit/market on them, but is a poor continuous-eval engine. Trader Workstation (TWS) / IB Gateway is the better eval engine and **cannot** share the paper username with CPGW `compete: true`.

Without a parked analysis, the next session will re-litigate geometry (stock STP then LEAP vs LEAP-as-command), the three-metric compare, and whether TWS replaces CPGW.

## Scope (when unblocked)

Follow the analysis first slice; do not expand until that row exists.

1. Read-only 1×1 matrix: one underlying (IBM or next Walnut name with a listed LEAP), nearest expiry **≥ 2 years**, strike nearest last.
2. CPGW `secdef/search` → strikes → `secdef/info` → marketdata snapshot. Reuse WUT contract-count math; **replace** Black-Scholes with the snapshot.
3. Emit cash outlay, risk-unit match, residual (delta / bid-ask / untradeable).
4. Grill before any option `place_order`: flip threshold (cash vs risk unit vs delta); geometry A vs B (analysis default: **B** — the Desk-Sent command is the LEAP); extra-modal stop (HITL vs sell-to-close).
5. Only then: one paper LEAP LMT or MKT via CPGW on an explicit OPT conid (adapter `resolve_conid` is stock-biased today).
6. IB Gateway eval sidecar on a **second paper username** only if the 1×1 matrix proves CPGW polling is the bottleneck. Not a second fulfillment adapter in the first slice.

## Non-goals

- Replacing CPGW as the Walnut **stock** STP adapter
- TWS and CPGW on the same paper username
- Silent option STP / spreads
- Treating WUT Black-Scholes as live cheap/expensive
- Slate Automation of unsent stock entries
- Packaging Policy ops UI (separate ticket)
- Exit Capital Reconcile implementation (separate ticket — must exist before a LEAP-packaged lot is treated as capital-honest)
- Live IBKR / Schwab write

## Acceptance

- [ ] Analysis still matches code (conid, snapshot, RelatedInstrumentFulfillment) at pickup — amend the analysis if not
- [ ] Read-only matrix row for one name with the three metrics and a tradable/untradeable flag
- [ ] Grill answers recorded (threshold, geometry, stop law) before OPT send
- [ ] If sending: one paper LEAP order id; journal stays working until Accept-Fill at the option print; signal Market remains the Book
- [ ] No TWS adapter in the first slice unless the matrix documents CPGW as insufficient **and** a second username exists

## First slice

**Read-only CPGW 1×1.** No option Desk Send. No TWS.
