# Ticket: WQ Phase 3 analog — bind paper WQ to IBKR DUT (evidence, not send)

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-09-01  
**Mode:** contractor  
**Graph nodes:** winston_v2, broker_gateway  
**Edges:** `broker_binding_id`; Confirmation Intake; `interactive_broker_trader_api`  
**Human gates:** CPGW paper username SSO; Desk Confirm books; no `place_order`  
**DoD:** #1372 paper; BG binding `bnd_3d6a5020d839c315583277d2`; tickle keep-alive; DummySimFills skipped; Confirm ≠ Send  
**Series:** `production-ready-wq`  
**Plan:** [`plans/production-ready-wq.md`](../../plans/production-ready-wq.md) §7 (2026-09-01 operator lock)  
**Monoliths:** winston_v2, broker_gateway  

## Problem

Schwab Individual sandbox is not the rehearsal broker. IBKR paper `DUT070450` is authenticated on Client Portal Gateway. WQ must not call IBKR; Broker Gateway is the adapter surface (paper and live IBKR bindings + Schwab).

## Scope

1. CPGW **tickle** every minute while `BG_IBKR_LIVE_READ=true`.  
2. One adapter class `interactive_broker_trader_api`; paper vs live = binding `env`.  
3. Persist #1372 `fulfillment_adapter_key` + `broker_binding_id` to the IBKR **paper** binding.  
4. Do **not** POST `sandbox_fills` to IBKR.  
5. `order_write` false. Monday re-alignment still **Desk Confirm** in Wv2. Hand-placed DUT fill → BG refresh → Confirmation Intake → Confirm.

## Non-goals

- Desk Send / `place_order` (Phase 4 + write ADR)  
- Auto-send of the Monday basket  
- Binding Mint / TF to this CPGW session  
- Treating DUT cash as `capital_base`

## Acceptance

- [x] Tickle job + nested `/tickle` authStatus parse  
- [x] WQ OP may use `interactive_broker_trader_api`  
- [x] DummySimFills no-ops for IBKR-bound OPs  
- [x] #1372 bound to IBKR paper binding on compose (`bnd_3d6a5020d839c315583277d2`)  
- [x] One hand-placed DUT fill → evidence: SPCX 1.06 (two execs 1.0+0.06 @ 143.38)  
- [x] Paper spike next WQ lot BRK.B: search `BRK B` conid 72063691; qty 0.571485 rejected (min 0.0001); 0.5715 MKT filled @ 503.78 after o354 reply; BG `trade.executed` appended. `order_write` still false (CPGW spike, not Desk Send).  
- [x] TickerRemap: `BRK B` / `BRK.B` / `BRK-B` canonical `BRK-B`; intake matches class-share; partial execs not qty-mismatch  
- [x] HUBB paper spike: 0.3907 (from 0.390724) @ 442.99; command/evidence pattern in `docs/analysis/2026-09-01-fulfillment-command-vs-broker-executions.md`
