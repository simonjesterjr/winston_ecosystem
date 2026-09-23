# Ticket: BG OPT Order Intent + IBKR paper 1×1 prove

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-09-15 (checklist refresh 2026-09-23)  
**Mode:** contractor  
**Lane:** B (Operator human-gated paper Desk-Send; agents never Send options — CoS drafts grill/SC only)  
**Graph nodes:** broker_gateway (primary); winston_v2 (client intent builder later); IBKR CPGW  
**Human gates:** **paper DUT only**; **no live** IBKR/Schwab write; **agent never Desk-Sends**; operator-only first OPT Send after grill + SC + tradable matrix; no pack promotion  
**DoD:** BG accepts an OPT Order Intent with **required** `conid` (no stock-biased resolve); read path can resolve/snapshot candidates; one **human-gated** paper **long-call (standard call, not LEAP)** Day LMT Submit → working → print evidence on DUT; Accept-Fill at option print; Book stays underlying. LEAP specimen deferred while LEAP strategy access remains unavailable / Operator path is long calls only for this prove.  
**Origin:** Plan [`plans/wv2-bg-ibkr-leap-fulfillment.md`](../../plans/wv2-bg-ibkr-leap-fulfillment.md) Phases 2–3; ADR-017 Proposed; analysis [`2026-09-15-wv2-bg-ibkr-leap-fulfillment-plan.md`](../analysis/2026-09-15-wv2-bg-ibkr-leap-fulfillment-plan.md)  
**Related:** domain law [`leap-extra-modal-proxy.md`](../business-context/leap-extra-modal-proxy.md); Wv2 fields [`2026-09-15-wv2-leap-packaging-fields.md`](2026-09-15-wv2-leap-packaging-fields.md); standard-call rung [`2026-09-19-standard-call-fulfillment-packaging-rung.md`](2026-09-19-standard-call-fulfillment-packaging-rung.md); read-only matrix [`2026-09-09-extra-modal-leap-unit-evaluation.md`](2026-09-09-extra-modal-leap-unit-evaluation.md); parent [`spending-capacity-and-leap-fulfillment.md`](../../plans/spending-capacity-and-leap-fulfillment.md); ADR-009; ADR-013; ADR-017  
**Prior cancel evidence:** [`../session-reports/2026-09-15-1643-leap-pipeline-dut-flatten-opt-permissions.md`](../session-reports/2026-09-15-1643-leap-pipeline-dut-flatten-opt-permissions.md) — IBM DEC28 250 Call LEAP conid `858327949` Day MKT/LMT/STP oids `31927252`/`31927253`/`31927254` system-cancelled (*no trading permissions for this options strategy*).

## Progress notes (2026-09-23)

- **Paper DUT long-call (non-LEAP) options permission:** Operator confirmed **Done** 2026-09-23. Permission gate is no longer blocking the next Desk-Send path.
- **LEAP strategy access:** still unavailable / not the next Operator path — use a **standard long call** specimen for the capability-matrix prove (Day LMT preferred).
- **Code surface (BG OPT intent / fixture / read resolve):** largely landed in prior sessions (see session report + standard-call ticket note that BG refuses option intent without `conid`). Re-verify acceptance boxes below before marking Done; do **not** invent accepted live order ids.
- **Still open for Done:** live human-gated Day LMT print on paper DUT + Accept-Fill at option print + Book on underlying + grill/SC/1×1 checked. STP/GTC probes remain **logged probes** (may refuse) — do not block Done if Day LMT accept is recorded.

## Evidence — Day LMT probe rejected (2026-09-23 12:19 MT)

- **Binding:** `bnd_3d6a5020d839c315583277d2`
- **Instrument:** IBM SEP17'27 240 Call, conid `911969657`, limit `35.55`
- **Client order key:** `opt-prove-ibm-911969657-20260923121940`
- **Result:** BG returned `rejected` with HTTP status `200`.
- **Accept-Fill:** not reached; no accepted order id or print evidence exists.
- **Ticket:** remains **In progress**. No order was placed by this documentation update.

Full BG error JSON:

```json
{"binding_id":"bnd_3d6a5020d839c315583277d2","status":"rejected","error":"You are submitting an order without market data. We strongly recommend against this as it may result in erroneous and unexpected trades.\nAre you sure you want to submit this order? | \"BUY 1 IBM SEP 17 '27 240 Call @ 35.55\"\nYou are not able to submit this order because you do not have trading permissions for this options strategy.","order":{"ok":false,"mode":"live","order_type":"LMT","client_order_key":"opt-prove-ibm-911969657-20260923121940","conid":"911969657","asset_class":"option","symbol":"IBM","side":"BUY","quantity":"1","status":"rejected","error":"...same...","http_status":200}}
```

## Problem

`PlaceOrderService` pass-through + IBKR adapter `resolve_conid` prefers NYSE/NASDAQ **stock** unless `intent["conid"]` is present. OPT Desk Send cannot be honest until OPT intents **require** conid, evidence records `asset_class`/conid, and paper prove shows one OPT print.

## Scope

1. Intent schema (backward compatible): `asset_class` / `sec_type`, required `conid` when option, optional OCC audit fields (`right`, `strike`, `expiry`), `quantity` = contracts, `order_type` MKT|LMT for v1 entry.  
2. Adapter: if option, **require** `conid`; never fall through to stock search.  
3. Read API: thin `secdef/search` → strikes → `secdef/info` → snapshot (1–3 conids); empty quote → `untradeable`.  
4. Evidence: `order.upserted` records conid + asset_class + underlying symbol.  
5. CapabilityGate: option write behind same paper + `cap_order_write` + kill; no Schwab OPT write.  
6. Fixture path for OPT place without network.  
7. **Prove:** capability matrix, not a single print — operator on explicit OPT conid: **Day LMT** (preferred specimen for this refresh), optionally Day MKT; then probe STP/GTC. Record accept/fill/reject. Journal working until Accept-Fill at option print; Book stays underlying. Verify DUT option permission, multiplier 100, tick, paper MD.

## Non-goals

- Silent option protective STP / STPLMT for open LEAP/call lots  
- Geometry A / stock STP filled as LEAP  
- Live write  
- Agent Desk-Send  
- Multi-leg OMS  
- Replacing CPGW as Walnut **stock** STP adapter  
- TWS + CPGW on same paper username  
- Requiring a LEAP specimen while LEAP strategy permission is unavailable

## Acceptance

- [ ] Specs: option intent without conid refuses; stock path unchanged  
- [ ] Read resolve returns tradable/untradeable with live/snapshot quote (not BS)  
- [ ] Fixture OPT place_order green offline  
- [ ] Grill + SC + 1×1 gates checked before any OPT write *(use checklist below)*  
- [ ] Capability matrix row(s): at least one accepted OPT order id (**Day LMT** preferred; Day MKT OK); probes of STP/GTC logged even if refused; agent did not Send options  
- [ ] No live / no pack promotion

## Human gates (repeat)

| Gate | Rule |
|------|------|
| Environment | Paper DUT only |
| Live | Forbidden |
| Agent | Never Desk-Sends options |
| Grill | `/grill-with-docs` before first OPT Send |
| SC / matrix | Parent Part 1 SC Check + tradable 1×1 row |

## System One harness

**State:** Paste (1) this ticket's Grill + SC checklist filled for the chosen long-call specimen, (2) CPGW/BG evidence for the Day LMT (order id + status: working/filled/cancelled — no invented ids), (3) journal/Book note: Accept-Fill at option print vs Book Market = underlying.

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| paper_only | Noul | Prove used live IBKR/Schwab write or non-DUT paper | noul ≥ 0.85 → FAIL |
| agent_no_send | Noul | An agent Desk-Sent the OPT (vs Operator Send) | noul ≥ 0.85 → FAIL |
| conid_explicit | Noul | Order Intent lacked explicit OPT `conid` / fell through to stock resolve | noul ≥ 0.85 → FAIL |
| sc_premium | Noul | SC used share notional instead of `premium × 100 × contracts` | noul ≥ 0.85 → FAIL |
| accept_fill_print | Noul | Accept-Fill claimed at underlying print rather than option print | noul ≥ 0.85 → FAIL |
| book_underlying | Noul | Book Market retargeted to OCC / option root | noul ≥ 0.85 → FAIL |
| long_call_specimen | Noul | Specimen is a standard long call (non-LEAP) for this prove path, or LEAP only if Operator re-opens LEAP permission | noul ≥ 0.85 → PASS |

**Runner:** Operator checklist + CPGW/BG read evidence; `jev ask` on residual smells only.  
**On fail:** do not mark ticket Done; do not invent order ids.

## Grill + SC checklist (2026-09-23)

Operator-only. Agents never Desk-Send options. Maps **1:1** to Acceptance boxes above. Specimen: **paper DUT long-call (standard call, not LEAP)** Day LMT. Prior LEAP cancels (session 2026-09-15) are evidence of the old permission wall — not reusable order ids.

### Specimen blanks (fill before Send)

| Field | Value |
|-------|--------|
| Binding id | `bnd_3d6a5020d839c315583277d2` (expect still DUT; confirm) |
| DUT label | `DUT070450` (confirm) |
| Underlying symbol | ________ (propose liquid: **IBM** — same underlying as 2026-09-15 probes; Operator may pick another liquid name) |
| Underlying conid | ________ (IBM was `8314` on 2026-09-15 — re-resolve) |
| Option symbol / OCC | ________ (standard call; DTE in standard rung, **not** ≥1y LEAP) |
| Option conid | ________ (**required** on intent; never stock-search) |
| Right / strike / expiry | CALL / ________ / ________ |
| Contracts (qty) | ________ (start **1**) |
| Multiplier | **100** (confirm) |
| Bid / ask / mid (paper MD) | ________ / ________ / ________ |
| Day LMT limit price | ________ (at or inside market; record level) |
| Time-in-force | **DAY** |
| Order type | **LMT** (this prove’s preferred matrix row) |

### A → Acceptance: Specs (conid refuse / stock unchanged)

- [ ] Offline/spec: `asset_class=option` (or OPT) **without** `conid` → refuse  
- [ ] Offline/spec: stock intent path unchanged (NYSE/NASDAQ resolve still works)  
- [ ] Evidence path records `conid` + `asset_class` + underlying symbol on upsert

### B → Acceptance: Read resolve tradable/untradeable

- [ ] Read resolve/snapshot for chosen conid returns live/snapshot quote (**not** Black–Scholes)  
- [ ] Empty / missing MD → marked **untradeable** (do not Send)  
- [ ] Tradable 1×1 row recorded for this underlying/expiry/strike (see D)

### C → Acceptance: Fixture OPT place offline

- [ ] Fixture OPT `place_order` green offline (no network)

### D → Acceptance: Grill + SC + 1×1 before any OPT write

**Grill (`/grill-with-docs` locks — confirm still hold for long-call Day LMT):**

- [ ] Geometry **B**: Desk-Sent command **is** the call (not stock STP “fills as call”)  
- [ ] Model B / stamped OCC+conid at Approve; Send does **not** silent re-ATM  
- [ ] Stop-out remains underlying Working Stop; protective sell-to-close is **HITL** (no silent option STP for this prove)  
- [ ] Paper DUT only; no pack promotion; agent never Sends options  
- [ ] Long-call (non-LEAP) specimen chosen because LEAP strategy access still unavailable / Operator wants long calls for this path  
- [ ] Permission gate: Operator confirmed paper DUT **long-call** options permission **Done** 2026-09-23

**Spending Capacity (SC) math — formula `premium × 100 × contracts` (never share notional):**

| Blank | Value |
|-------|--------|
| Premium used ($) | ________ (mid or limit; say which) |
| Multiplier | 100 |
| Contracts | ________ |
| SC cash outlay ($) | ________ = premium × 100 × contracts |
| Buying power / SMA / guardrail hints | ________ / ________ / ________ |
| SC Check result | `ok` / `tight` / `refused` — ________ |
| If refused | **STOP** — do not Send; iterate gate or shrink contracts (do not fall back to share notional) |

**Tradable 1×1:**

- [ ] One underlying × one expiry class × one strike nearest last (or Operator pick)  
- [ ] Bid/ask present (or honest untradeable)  
- [ ] Multiplier 100 + option tick verified  
- [ ] Row logged before first OPT write

### E → Acceptance: Capability matrix (Day LMT print)

**Pre-Send:**

- [ ] Intent carries explicit OPT `conid` + `asset_class=option`  
- [ ] Kill switch / `cap_order_write` / paper binding confirmed  
- [ ] Agent is **not** the Sender — Operator Desk-Sends

**Day LMT (this prove’s Done path):**

- [ ] Operator Desk-Send **Day LMT** 1 contract at limit ________  
- [ ] Broker **accepted** order id: ________ (**do not invent**; leave blank until live)  
- [ ] Status path: submitted → working → ________ (fill / cancel / reject)  
- [ ] If filled: **Accept-Fill at option print** (premium × 100 × qty cash flow)  
- [ ] **Book Market = underlying** (IBM or chosen symbol) — not OCC root  
- [ ] Agent did not Send

**Optional / deferred probes (log even if refused — do not invent ids):**

- [ ] Day MKT probe — result / oid: ________ (optional if Day LMT already accepted)  
- [ ] STP probe — result / oid: ________ (**deferred OK** if refused or skipped)  
- [ ] GTC probe (or GTC sell-to-close after fill) — result / oid: ________ (**deferred OK**)  
- [ ] Prior LEAP permission-cancels (2026-09-15) cited as history only — oids `31927252`/`31927253`/`31927254` on conid `858327949` — **not** Done evidence

### F → Acceptance: No live / no pack promotion

- [ ] Environment was paper DUT only  
- [ ] No live IBKR/Schwab `order_write`  
- [ ] No pack promotion / Capital Activation / paper→real in-place

### What counts as ticket **Done** vs **deferred**

| Done (required) | Deferred (OK to leave open) |
|-----------------|-------------------------------|
| Specs + fixture + read resolve green (or re-verified) | LEAP specimen / LEAP strategy permission |
| Grill + SC (`premium × 100 × contracts`) + tradable 1×1 checked | STP probe accept (log refuse/skip) |
| ≥1 **accepted** paper OPT order id on **Day LMT** (or Day MKT) | GTC probe accept (log refuse/skip) |
| Accept-Fill at **option** print; Book on **underlying** | Plan F MKT urgency path |
| Agent did not Send; no live; no pack promotion | CPGW price-condition / workflow prove |
| | BG fail-closed on post-accept system-cancel (separate slice) |

**Do not mark Done** until a real accepted order id + print/Accept-Fill evidence exists. Permission Done alone is not ticket Done.

## Evidence — second Day LMT probe rejected (~2026-09-23 12:28 MT)

- **Instrument:** IBM JUN17'27 240 Call, conid `846858414`, limit `30.55`
- **Client order key:** `ibm-opt-prove-jun27-240c-1`
- **Result:** BG rejected the probe with the same dual error: no market-data confirmation and no trading permission for this options strategy.
- **Accept-Fill:** not reached; no accepted order id or print evidence exists.
- **Ticket:** remains **In progress**. No order was placed by this documentation update.

Broker error text:

```text
You are submitting an order without market data. We strongly recommend against this as it may result in erroneous and unexpected trades.
Are you sure you want to submit this order? | "BUY 1 IBM JUN 17 '27 240 Call @ 30.55"
You are not able to submit this order because you do not have trading permissions for this options strategy.
```


## Evidence — third probe: Day MKT rejected (~2026-09-23 12:50 MT)

- **Operator-run order:** Day MKT on paper DUT; the agent did not Send.
- **Instrument:** IBM JUN17'27 240 Call, conid `846858414`
- **Order:** `order_type=MKT`, `tif=DAY`, `qty=1`, `side=BUY`
- **Client order key:** `ibm-opt-prove-jun27-240c-mkt-1`
- **Binding:** `bnd_3d6a5020d839c315583277d2`
- **Result:** rejected with the same dual error: market-data warning plus no trading permissions for this options strategy.
- **Classification:** LMT vs MKT does not matter; the hard blocker is options-strategy permission on paper DUT.
- **Accept-Fill:** not reached; no accepted `oid` exists.
- **Ticket:** remains **In progress**.

Broker error text remained the same: an order-without-market-data warning followed by `You are not able to submit this order because you do not have trading permissions for this options strategy.`
