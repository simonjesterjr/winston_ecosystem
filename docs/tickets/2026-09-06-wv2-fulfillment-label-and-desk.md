# Ticket: Fulfillment Label + Fulfillment Desk (Wv2 v1)

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-09-06  
**Mode:** contractor  
**Graph nodes:** winston_v2  
**Edges:** Broker Gateway `GET /api/v1/bindings` + `GET /api/v1/adapters` (read-only)  
**Human gates:** none (read-only indication). Rebind is not this page (Q8).  
**DoD:** Ops shell, WQ, DAR, and Telegram show who fills; bound chips link to a Wv2 Fulfillment Desk page with rituals + per-OP rules  
**Origin:** Grill 2026-09-06 — `ecosystem/CONTEXT.md` (**Fulfillment Label**, **Adapter Binding**, **Fulfillment Desk**, **Fulfillment Ritual**)

## Problem

The `paper` / `real` chip on the Winston v2 ops shell is **Execution Mode**, not who fulfills. Winston Quiver (WQ) #1372 can be paper and still bound to Interactive Brokers (IBKR) DUT. Operators need a glance of `{Vendor} {Nickname}` beside paper/real, a link to that binding’s config, and an index of stored adapters.

## Scope (v1)

1. **Fulfillment Label** `{Vendor} {Nickname}` beside Execution Mode. dummy_sim / manual: no extra chip.  
2. Chip links to a **Wv2 Fulfillment Desk** binding page (read-only). **All adapters** → index of stored bindings + `manual`.  
3. Binding page: transport facts; **Fulfillment Rituals** (binding-wide, e.g. IBKR Client Portal login / tickle); per-OP desk rules (Confirm vs Send, Capital Authority, packaging).  
4. Glance surfaces: Active OPs; positions-by-band and pending-by-portfolio headers; WQ header + Tracking OP broker row; portfolio live-eval; ops shell + WQ **All adapters** link.  
5. `needs login` sibling tag on ops shell / WQ only when Broker Gateway reports `needs_reauth` / error.  
6. **DAR** and Telegram: inline Fulfillment Label only — not `needs login`, not ritual steps.

## Non-goals

- Rebind / unbind UI (Q8)  
- Broker Gateway HTML desk  
- Fulfillment Packaging Policy editor (separate ticket)  
- Telegram / DAR auth attention  
- Solving IBKR tickle/login (document the ritual only)

## Acceptance

- [x] dummy_sim OP shows `paper` only; IBKR-bound OP shows `paper` + `IBKR DUT070450` (or binding nickname) linking to the desk page  
- [x] WQ header and Tracking OP broker row use the chip, not raw adapter key / `bnd_…`  
- [x] Fulfillment Desk index lists stored BG bindings + manual; IBKR page states login/tickle ritual and WQ Confirm=Send vs Mint book-only as **per-OP** rows  
- [x] `needs login` on ops shell / WQ when binding auth is dead; absent from DAR/Telegram  
- [x] DAR markdown/PDF and Telegram caption include the inline label for bound chapters  
- [x] BG down fails soft (no 500 on ops shell)

Shipped in Wv2 this session. Restart `winston_v2` to pick up routes/views. Nickname comes from Broker Gateway `AdapterBinding.label` (set DUT070450 / UT there).
