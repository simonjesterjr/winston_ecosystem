# Wv2 + Broker Gateway + IBKR LEAP extra-modal fulfillment — detailed inventory

**Date:** 2026-09-15  
**Status:** Detailed inventory; authoritative plan is [`plans/wv2-bg-ibkr-leap-fulfillment.md`](../../plans/wv2-bg-ibkr-leap-fulfillment.md) (no code; no PBR stamps)  
**Mode:** contractor pickup  
**ADR:** [`ADR-017-leap-packaging-precalc-occ.md`](../adr/ADR-017-leap-packaging-precalc-occ.md) (Proposed — Model B)  
**Monoliths:** Winston v2 (Wv2), Broker Gateway (BG), Client Portal Gateway (CPGW) via IBKR adapter; WUT only as sizing skeleton  
**Desk law:** [`docs/business-context/leap-extra-modal-proxy.md`](../business-context/leap-extra-modal-proxy.md); sticky 20D_BO in [`turtle-s2-pyramid-and-working-stop.md`](../business-context/turtle-s2-pyramid-and-working-stop.md)  
**Parent plans / tickets:** [`plans/spending-capacity-and-leap-fulfillment.md`](../../plans/spending-capacity-and-leap-fulfillment.md); ticket [`2026-09-09-extra-modal-leap-unit-evaluation.md`](../tickets/2026-09-09-extra-modal-leap-unit-evaluation.md); analysis [`2026-09-09-extra-modal-leap-unit-vs-shares.md`](2026-09-09-extra-modal-leap-unit-vs-shares.md); ADR-009; ADR-013  
**Human gates:** paper DUT only; no option Desk Send until SC Check + tradable 1×1 + grill locks below  

---

## 0. One-sentence outcome

Paper DUT can **Desk Send one LEAP** as the fulfillment command for an underlying Trend Following signal, with Working Stop / sticky 20D_BO still evaluated on the **underlying**, sell-to-close of the option as **HITL** on stop-out, and Accept-Fill at the **option print**.

---

## 1. Inventory (what already exists — do not re-derive)

### 1.1 Desk / domain law

| Artifact | Locked |
|----------|--------|
| `leap-extra-modal-proxy.md` | TS owns exits / Working Stop on **underlying**; packaging is fulfillment; HITL sell LEAP on stop unless policy says otherwise; dual spines; Exit Capital Reconcile |
| `human-gated-desk-and-fulfillment.md` | Confirm may change packaging; Extra-Modal Guardrail = HITL on related fill; non-goal: multi-leg OMS |
| `turtle-s2-pyramid-and-working-stop.md` | Sticky 20D_BO (not doctrine A); under-max silence; pierce = flatten-all |
| ADR-009 | DA never opens/closes Positions; Human-Gated; dual spines |
| ADR-013 | Paper DUT `order_write`; Confirm≠Send default (WQ/Walnut carve-outs); Order Intent types MKT/LMT/STP/STPLMT on adapter; §7 Guardrail extra-modal = HITL |

### 1.2 LEAP / packaging tickets & plans

| Artifact | Role / gap |
|----------|------------|
| Ticket `2026-09-09-extra-modal-leap-unit-evaluation.md` | Read-only 1×1 unblocked; **option Desk Send still blocked** until SC + matrix + grill |
| Analysis `2026-09-09-extra-modal-leap-unit-vs-shares.md` | CPGW can MKT/LMT OPT; `resolve_conid` stock-biased; geometry **B** (LEAP is Desk-Sent command) default; three-metric matrix |
| Plan `spending-capacity-and-leap-fulfillment.md` | SC before LEAP send; prefer LEAP cash outlay; Part 2f = one paper LEAP send (not authorized by plan alone) |
| Ticket `2026-09-01-fulfillment-packaging-policy-ops-ui.md` | OP policy home for “prefer LEAP on entry” — not BG |
| Ticket `2026-08-05-…-exit-reconcile.md` | Required before LEAP lot is capital-honest |
| Grill ticket `2026-07-22-grill-fulfillment-schwab-extra-modal.md` | Older Schwab/extra-modal grill trail |

### 1.3 Code pointers (verified read)

| Layer | Path | Fact |
|-------|------|------|
| Wv2 book packaging | `winston_v2/.../related_instrument_fulfillment.rb` | Types `leap\|option\|…`; strike/expiry/right required; flow = contracts × premium × 100; journals stay on **underlying** Market |
| Wv2 Desk Send (stock) | `winston_v2/.../quiver_tracking/wq_confirm_send.rb` `#build_intent` | Intent: `symbol`, `side`, `quantity`, `order_type`, `tif`, `client_order_key` (+ stop/limit). **No `conid`, no OPT fields** |
| Wv2 slate | `session_order_slate/builder.rb` | Parks **stock** STP/GTC on underlying symbol; no option legs today |
| BG place | `broker_gateway/.../evidence/place_order_service.rb` | Pass-through Hash intent; basket refused |
| BG IBKR | `ibkr_adapter.rb` | `ORDER_TYPES = MKT LMT STP STPLMT`; `place_order` posts `{orders:[{conid,…}]}`; **`resolve_conid` prefers NYSE/NASDAQ stock** unless `intent["conid"]` present |
| BG normalizer | `ibkr/normalizer.rb` | OPT lots → `asset_class: option` + `extra_modal_note` |
| WUT | `leap_purchase_service.rb` | Strike = last ± ATR offset (0 = ATM); contracts = floor(shares/100); BS premium — **lab only** |

### 1.4 IBKR / CPGW capability (from docs + adapter)

**Supported for options (Campus / analysis + code shape):**

- Resolve OPT conid: `secdef/search` → strikes → `secdef/info` (must search first).
- Snapshot quotes: `marketdata/snapshot?conids=` (first poll often empty; Greeks lag; paper options MD may be empty / paid).
- Place **MKT** and **LMT** on an OPT conid via the same `place_order` path as stock — **if** `intent.conid` is explicit.
- STP/STPLMT on OPT conid is API-possible; **law forbids** silent option protective STP for v1 (Guardrail = HITL).

**Limitations:**

- Stock-biased `resolve_conid` will not pick LEAPs from a ticker alone.
- Sequential per-strike `secdef/info` — fine for 1–3 ATM candidates, not a full chain watcher.
- No continuous option streaming on CPGW; tickle ≠ login; `compete:true` kicks Desktop/TWS on same paper username.
- Replace still CapabilityGate-refused; cancel-all refused.
- DUT option permissions, multiplier 100, option tick ($0.05/$0.10) must be verified on first spike.

**Answer to operator question:** Yes — IBKR/CPGW **supports market (and limit) orders on LEAPs** when given an OPT conid. Workflow is monitor **underlying** signal → choose ATM (or ATR-offset) LEAP → Desk Send OPT MKT/LMT. Broker stop on the option is **not** v1.

---

## 2. Two fulfillment models (contract timing)

Both assume **geometry B from the 2026-09-09 analysis**: the Desk-Sent command **is** the LEAP (no stock STP that “fills as LEAP”). The fork below is only **when** strike/expiry/conid are chosen.

### Model A — Live resolve at Confirm/Send

```
DA / slate signal on UNDERLYING
  → Handoff: share-unit size, direction, Working Stop (underlying)
  → At Confirm/Send: CPGW resolve ATM (± leap_atr_offset) ≥2y expiry
       → build call/put → place MKT/LMT on OPT conid
```

| Dimension | Effect |
|-----------|--------|
| Latency | Secdef dance on the critical Send path (search → strikes → info → optional snapshot) |
| Moment of Truth | Strike matches fill-time underlying; good vs overnight drift |
| Slate rebuild | Simple (underlying only); no stale OCC rows |
| Wrong-strike risk | Low at send; high **HITL surprise** if Confirm UI never showed the contract |
| HITL | Must preview resolved contract on Confirm **before** Send, or Approve is blind |

### Model B — Precalc at Signal / slate time

```
DA / slate signal on UNDERLYING
  → At Signal/slate: compute candidate OCC (strike, expiry, right)
       optional conid if CPGW up; attach to handoff / fulfillment_details
  → Fulfillment: “send this contract” (MKT/LMT)
  → At Send: verify conid (refresh if missing); warn if underlying moved past strike class
```

| Dimension | Effect |
|-----------|--------|
| Latency | Send is thin (conid already known or one verify hop) |
| Moment of Truth | Contract chosen when signal/slate minted; may stale overnight |
| Slate rebuild | Nightly rebuild refreshes candidates (same as DAY stock parks die/rebuild) |
| Wrong-strike risk | Real if last moved a full strike class; mitigated by Send recheck + HITL warn |
| HITL | Approve sees exact instrument_label / OCC / conid on the handoff |

### Recommendation for **v1 paper: Model B** (precalc) + Send-time verify

**Rationale (ordered):**

1. **HITL / ADR-009** — Desk Approve must see the packaged instrument, not only “IBM long 1 unit.” Model A without a Confirm preview is blind; with preview it becomes B-at-Confirm anyway.
2. **Geometry B + WQ-like send** — Intent already carries what DUT should print; OPT conid belongs on the intent the same way `client_order_key` does.
3. **CPGW latency** — Secdef on Send fights MKT urgency and session tickle; precalc at slate/Signal (or Confirm packaging step) keeps Send fail-closed and fast.
4. **Slate rebuild** — DAY rebuild culture already refreshes parks; refresh candidate LEAP with the same cadence.
5. **Wrong-strike** — Accept residual risk; **Send-time verify**: if last is >½ strike increment from packaged strike, refuse or force HITL re-pick (do not silently re-ATM).
6. **Model A remains the fallback** when CPGW was down at slate mint and `conid` is blank — resolve once at Confirm packaging, then stamp details (converges to B).

**Not recommended for v1:** Model A as silent resolve-inside-`place_order` with no stamped packaging fields.

---

## 3. Phased build plan

Gates between phases: paper DUT only; kill switch / `cap_order_write`; no live IBKR/Schwab; no agent Desk-Send of options.

### Phase 0 — Prerequisites (parallel, already named)

- [ ] Spending Capacity Check live on Walnut (Part 1 of spending-capacity plan) — LEAP SC uses **premium cash**, not share notional.
- [ ] Read-only CPGW 1×1 matrix row tradable (live quote, not Black-Scholes).
- [ ] Grill answers recorded (§5).
- [ ] Exit Capital Reconcile path available before treating a LEAP lot as capital-honest (may ship with first Accept-Fill, not after).

### Phase 1 — Wv2 handoff packaging fields

**Owner:** Wv2  
**Goal:** Signal spine stays underlying; handoff carries LEAP packaging for fulfillment.

Extend `fulfillment_details` / Desk Handoff (and slate leg metadata when used) with:

| Field | Purpose |
|-------|---------|
| `fulfillment_type: leap` | Existing RelatedInstrumentFulfillment |
| `option_type` / `strike` / `expiry` | Existing package validators |
| `leap_atr_offset`, `leap_expiration_days` | Policy knobs (same meanings as WUT lab) |
| `contracts` | Floor(share_units/100); refuse if 0 |
| `ibkr_conid` (optional until resolved) | Explicit OPT conid for BG |
| `occ_symbol` or `instrument_label` | HITL display |
| `packaging_resolved_at`, `underlying_last_at_resolve` | Stale-strike audit |
| `signal_market` | Underlying Book symbol (must not equal OCC) |

Work items:

1. Packaging Policy on OP: `prefer_leap_on_entry` (shares on pyramid unless policy says `leap_fulfillment=all`) — ticket `2026-09-01-…-ops-ui`.
2. At Signal / slate mint (or Confirm packaging step): call a **LeapCandidateResolver** (new Wv2 service) that:
   - Reuses WUT **contract-count** math (`desired_shares/100` floor).
   - Asks BG for OPT search/snapshot (new read endpoints or extend binding API) — **not** BS for live/paper eval.
   - Stamps fields above; leaves journal Market = underlying.
3. Desk Workflow UI: show instrument_label, premium snapshot, cash outlay vs share notional, SC remaining.
4. SC Check on **premium × 100 × contracts** before park/send.

**Non-ship:** DA inventing OPT Positions; retargeting Books to OCC.

### Phase 2 — BG option Order Intent

**Owner:** BG (+ Wv2 client)  
**Goal:** One Order Intent can express OPT without stock-biased conid resolution.

Intent schema additions (backward compatible):

```text
symbol            # underlying (Winston signal Market) — audit / remap
broker_symbol     # optional OCC or IBKR ticker string
conid             # REQUIRED for OPT when asset_class=option
asset_class       # stock | option (default stock)
sec_type          # STK | OPT (mirror)
right             # C | P (optional audit)
strike, expiry    # optional audit; conid is SoT for place
order_type        # MKT | LMT (v1 LEAP entry); STP reserved, not used for protective
quantity          # contracts
side, tif, client_order_key, limit_price
```

Work items:

1. `PlaceOrderService` / adapter: if `asset_class=option` (or `sec_type=OPT`), **require** `conid`; never fall through to NYSE/NASDAQ search.
2. Read API for candidate resolve: thin wrapper `secdef/search` → strikes → `secdef/info` → snapshot (1–3 conids). Fail closed on empty quote → `untradeable`.
3. Evidence payload: record `conid`, `asset_class`, underlying `symbol` on `order.upserted`.
4. CapabilityGate: option write still behind same paper + `cap_order_write` + env kill; no Schwab OPT write.

### Phase 3 — IBKR adapter OPT path

**Owner:** BG `IbkrAdapter`  
**Goal:** Prove one paper LEAP MKT (or LMT) Submit → working → print.

Work items:

1. Honor `intent["conid"]` (already partially true); add explicit OPT branch + logging.
2. Do **not** invent option STP protective for open LEAP lots.
3. Fixture path: OPT conid place_order for specs without network.
4. Verify DUT: option trading permission, multiplier 100, tick size, paper MD subscription.
5. First human-gated paper send (operator only): one name, one contract, journal **working** until Accept-Fill at option print; Book stays underlying.

### Phase 4 — Monitoring / reconcile

**Owner:** Wv2 + BG poll  
**Goal:** Honest dual spines after print.

Work items:

1. Accept-Fill matches Single Fulfillment Identity on OPT print (`RelatedInstrumentFulfillment.signed_flow` already purchase-signed).
2. Snapshot/normalizer already tags OPT `extra_modal_note` — join via Fulfillment Link, never retarget Book.
3. Exit Capital Reconcile CashEvent when packaged PnL ≠ signal-path proxy (CONTEXT IBM example).
4. DAR / slate attention: naked LEAP lot (no HITL stop task) when Working Stop exists on underlying.
5. SC remaining recomputed after premium outlay (refined SC).

### Phase 5 — Stop-out HITL

**Owner:** Wv2 desk  
**Goal:** Sticky 20D_BO / 2N pierce on **underlying** → desk task to sell LEAP; no silent option STP.

Work items:

1. DA evaluates Working Stop on underlying (existing Turtle S2 / ADR-009 addendum).
2. On pierce: mint signaled stop-out draft + **HITL sell-to-close** task carrying packaged `ibkr_conid` / contracts from open lot.
3. Desk Send SELL MKT/LMT on that conid (same OPT intent path); Accept-Fill at option print.
4. Optional later policy: auto-send sell-to-close — **grill + ADR-013 addendum**, not v1 default.
5. Protective Stop Guardrail: for extra-modal, “matching GTC at DUT” is **N/A**; attention = missing HITL task / unacked stop-out, not missing option STP.

---

## 4. End-to-end v1 paper workflow (recommended)

```
Underlying signal (DA / RST / Turtle S2)
        │
        ├─ Signal Spine: units, Working Stop, heat, sticky 20D_BO on UNDERLYING
        │
        └─ Packaging (Model B): ATM (±offset) LEAP ≥2y, contracts, conid
              SC Check on premium cash
              Desk Approve sees OCC / cash / SC
              Desk Send → BG Order Intent {conid, OPT, MKT|LMT, contracts}
              Journal working → Accept-Fill at option print
              Fulfillment Link; Book remains underlying
        │
        └─ Exit: underlying Working Stop pierce → HITL sell LEAP
              Exit Capital Reconcile CashEvent
```

IBKR market orders for LEAPs: **yes, supported** via CPGW on OPT conid. Prefer MKT on signal-touch for v1 paper simplicity (WQ-like); LMT allowed when matrix shows wide bid/ask.

---

## 5. Open risks / grill questions (≤6)

1. **Flip threshold:** cash outlay vs risk-unit floor vs delta — which flips shares→LEAP on ~$25k Walnut? (Plan default: cash is operational trigger; risk-unit match is hard floor.)
2. **Stop law:** keep HITL sell-to-close (current law) vs policy-automatic sell-to-close when underlying Working Stop would fire?
3. **Stale strike:** on Send, if underlying moved past packaged strike class — refuse, HITL re-pick, or auto re-ATM (Model A escape)?
4. **Entry order type:** MKT-on-signal vs LMT for first paper LEAP given paper options MD quality?
5. **Second paper username** for IB Gateway eval sidecar — yes/no, or CPGW-only forever for v1?
6. **Pyramid packaging:** LEAP on first unit only (`leap_fulfillment=entry`) vs all adds (`all`) — Unit Heat occupancy must stay one unit either way?

Expect an **ADR-013 addendum** when geometry B + OPT Order Intent + stop HITL are operator-locked.

---

## 6. Explicit non-goals

- Multi-leg OMS / spreads / calendar as first-class Positions (ADR-009).
- Pack promotion / mv2 Capital Activation / paper→real in-place (ADR-006).
- Silent option STP or stock STP “filled as LEAP” (geometry A).
- Treating WUT Black-Scholes as live cheap/expensive.
- TWS + CPGW `compete:true` on the same paper username.
- Live IBKR or Schwab `order_write`.
- Slate Automation of unsent entries (no Approve).
- Replacing CPGW as Walnut **stock** STP adapter.
- New Trading Strategy fingerprint solely for packaging (unless Unit Heat occupancy changes — then grill).
- Continuous rewrite of `capital_base` to LEAP MTM mid-life.

---

## 7. Suggested implementation sequence (contractor slices)

| Slice | Deliverable | Gate |
|-------|-------------|------|
| S0 | SC Check + 1×1 matrix (existing tickets) | Operator |
| S1 | BG OPT read (secdef+snapshot) + intent.conid required for option | Specs green |
| S2 | Wv2 LeapCandidateResolver + stamp fulfillment_details (Model B) | HITL UI shows OCC |
| S3 | Wv2 Desk Send builds OPT intent; one paper LMT/MKT | Operator Desk Send |
| S4 | Accept-Fill + Exit Capital Reconcile on option print | Capital honesty |
| S5 | Stop-out HITL sell-to-close task + optional Send | Guardrail attention |

Do **not** stamp PBRs from this plan. Lab LEAP PBR recipes remain WUT fingerprint work under existing WUT tickets.

---

## 8. Recommendation summary

| Choice | Lock |
|--------|------|
| Fulfillment geometry (analysis) | **B** — Desk-Sent command is the LEAP |
| Contract timing (this plan) | **Model B** — precalc OCC at Signal/slate; Send verifies conid / stale-strike |
| Entry order | MKT (default) or LMT if quote width demands; no option STP protective |
| Stop-out | Underlying Working Stop + sticky 20D_BO; **HITL** sell LEAP |
| IBKR LEAP MKT | **Supported** on CPGW with explicit OPT conid |

