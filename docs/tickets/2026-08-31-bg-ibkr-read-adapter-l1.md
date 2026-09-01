# Ticket: Broker Gateway — Interactive Brokers L1 read adapter

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-08-31  
**Mode:** contractor  
**Graph nodes:** broker_gateway, ecosystem  
**Edges:** `interfaces/winston-broker-evidence-standard.md`; Client Portal Web API REST  
**Human gates:** paper username SSO in Client Portal Gateway; no credentials in git  
**DoD:** `interactive_broker_trader_api` registered; fixtures → evidence; `order_write` false; live GET gated  
**Series:** `production-ready-wq`  
**Plan:** [`plans/production-ready-wq.md`](../../plans/production-ready-wq.md) (paper broker rehearsal; Schwab Phase 2 remains)  
**Monoliths:** **broker_gateway**  

## Problem

WQ paper rehearsal against a **real broker paper account** should not wait on Schwab Individual sandbox. The operator has an Interactive Brokers paper account. BG had no IBKR adapter.

## Scope

1. Adapter key `interactive_broker_trader_api`, L1: `auth` + `order_read` + `txn_read`; **`order_write: false`**.  
2. Ruby/Rails REST client (no Python/C# SDK).  
3. Fixtures first (Client Portal-shaped orders + trades JSON).  
4. Live path: Client Portal Gateway session (`BG_IBKR_LIVE_READ`); username/password never in repo. Secrets only in gitignored `ecosystem/deployment/ibkr.env`.  
5. CapabilityGate refuse place/cancel/replace.

## Non-goals

- Desk Send / `place_order`  
- Binding WQ #1372 (still dummy_sim)  
- OAuth 1.0a key ceremony (later; CPGW is the individual paper path)  
- Positions/balances as capital SoT  

## Acceptance

- [x] Registry registered; L1 read only  
- [x] Fixture refresh produces evidence events  
- [x] Live off by default; fail closed without gateway session  
- [x] Env template + gitignore; no tokens in code  
- [x] CPGW vendored at `ecosystem/vendor/ibkr-clientportal-gw`; wrapper `ecosystem/deployment/bin/run-ibkr-cpgw`; paper account id `DUT070450` in gitignored `ibkr.env`  
- [x] `BG_IBKR_LIVE_READ` live GET path proved against CPGW (`host.docker.internal`); binding `bnd_3d6a5020d839c315583277d2`  
- [x] **2026-09-01 paper session:** CPGW paper username SSO; `GET /iserver/accounts` → `DUT070450`, `isPaper: true`, portfolio `type: DEMO`. Refresh `auth.status` ok (empty orders/trades/positions; paper cash ~$12k). `order_write` false. WQ #1372 stays `dummy_sim`.  

## Keep-alive / next

CPGW paper SSO is session-based (~6 min idle unless `/tickle`). Re-login at https://localhost:5000 with the **paper username** if `auth/status` is 401. Do not log into CPGW with the live username. WQ #1372 stays `dummy_sim`. `order_write` stays false. Remaining: orders/trades appear on paper book → refresh produces `trade.executed` / order events.

## Auth note (not a blocker for fixtures)

IBKR Web API **is** REST, but individuals do not get a simple long-lived API key. Standard path: run Client Portal Gateway, browser-login with the **paper username**, then BG GETs `https://host.docker.internal:5000/v1/api/...`. OAuth 2.0 (beta) / OAuth 1.0a are later alternatives. One brokerage session per username — do not leave TWS logged in as the paper user while CPGW holds the session.
