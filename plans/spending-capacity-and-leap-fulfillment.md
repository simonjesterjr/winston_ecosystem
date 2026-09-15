# Plan: Spending Capacity, then LEAP fulfillment preference

**Status:** Draft for operator lock  
**Date:** 2026-09-11  
**Mode:** contractor  
**Monoliths:** Winston v2 (Wv2) primary; Winston Unit Test (WUT) Portfolio Backtest Run (PBR) impact; Broker Gateway (BG) poll fields only  
**Durable home:** this file. Session draft: Grok session `01a09295` plan.md  
**Discovery that forced this:** DUT (Interactive Brokers paper) auto-liquidated 612 DBC @ 33.15 (`liquidation_trade`, order 17891562871). Session low 32.99 — Working Stop 32.56 was **not** hit. Gross ~2.94× on ~$25k. After sale: Special Memorandum Account (SMA) ~$113, Regulation T (Reg T) margin $26.6k vs net liquidation $25.0k, buying power still ~$37k.

This is two sequenced parts in **one** plan. Part 2 does **not** invent a competing LEAP design; it **updates** the parked analysis and blocked ticket with this discovery.

**Operator comments folded in (2026-09-11):**

1. **@plan.md:20** — The plan must lock a **firm dual-spine model**: signal on the **underlying Market** (e.g. IBM); fulfillment on the **LEAP / derived vehicle** (preferred over the underlying when listed); **capital adjustment** from that packaging; **profitability / equity curves / Edge (R)** measured on the reconciled book; **then** size the next unit from **refined SC** after LEAP preference (premium cash, not share notional).
2. **Original ask (second note; no second `@plan.md:N` arrived in-session)** — Part 2 is LEAP fulfillment as entry preference on DUT; if a plan already exists, **update it** (do not fork). That is `docs/analysis/2026-09-09-extra-modal-leap-unit-vs-shares.md` + ticket `2026-09-09-extra-modal-leap-unit-evaluation.md` + pointer on `plans/trade-fulfillment-engine.md`.

Assumed locks (questions declined): Walnut keeps stored `max_leverage=3` and SMA still binds; WUT `leverage_accounting=gross` is **opt-in**; LEAP read-only matrix runs **in parallel** with Part 1; no option Desk Send until SC Check + 1×1 + grill.


**Related (2026-09-14/15):** Domain law [`docs/business-context/leap-extra-modal-proxy.md`](../docs/business-context/leap-extra-modal-proxy.md); Proposed ADR [`docs/adr/ADR-017-leap-packaging-precalc-occ.md`](../docs/adr/ADR-017-leap-packaging-precalc-occ.md) (Model B); authoritative Wv2+BG+IBKR plan [`wv2-bg-ibkr-leap-fulfillment.md`](wv2-bg-ibkr-leap-fulfillment.md); detailed inventory [`docs/analysis/2026-09-15-wv2-bg-ibkr-leap-fulfillment-plan.md`](../docs/analysis/2026-09-15-wv2-bg-ibkr-leap-fulfillment-plan.md). Part 1/2 below unchanged.


---

## What this plan is for

1. Make **Spending Capacity (SC)** real Ruby and a **slate refuse**, not glossary.
2. Show SC on the Operational Portfolio (OP) in Wv2.
3. Say exactly how PBRs in WUT change (and what must **not** silently change).
4. Lock the **signal → LEAP fulfillment → capital reconcile → Edge / equity → SC** loop (comment 1), by **updating** the existing extra-modal artifacts (comment 2) — not a third design.

### Firm model (comment 1) — one IBM lot

```
DA / slate signal     Market IBM  (55-day, 1% share-equivalent unit, Working Stop on parquet)
        │
        ├─ Signal Spine / Books / Unit Heat / 20-day gate     stay on IBM
        │
        └─ Fulfillment Packaging Policy: prefer LEAP on entry
              Order Intent on OPT conid (geometry B)
              Accept-Fill at option print (premium × 100 × contracts)
              Fulfillment Link + indicated ±$D
              Exit Capital Reconcile applies ±$D so Booked Capital / equity / Edge use LEAP cash
              Protective: HITL sell-to-close when IBM 2N would fire (until packaging says else)
        │
        └─ Next unit: 1% of Risk Capital, then SC Check on remaining
              SC after LEAP uses premium outlay, not IBM share notional
```

**Edge (R)** (ADR-015): glance number stays \(E=(W\times\overline{W}_R)-(L\times\overline{L}_R)\). **1R** for methodology comparability is still signal-path initial risk (`|entry−original_stop|×share units`). **Win/loss dollars** after reconcile are **booked LEAP P&L**. Do not plot a fake 210-share equity curve as if the calls were stock. Score Projection already forbids inventing a composite; two strips are allowed: signal-path occupancy vs booked Edge.

**Equity curve:** Booked Capital Spine after reconcile is what the household (and DUT NLV when authority is broker) sees. Signal-path lot count is for DA / heat, not for “we made 210 × ΔIBM.”

---

## Canonical terms (already in `CONTEXT.md`)

Do not invent parallel names.

| Term | Law today | Gap this plan closes |
|------|-----------|----------------------|
| **Risk unit** | 1% of **Risk Capital** / (ATR × `atr_multiplier`) | Unchanged. DBC 841 was a *correct* 1% unit and a *fatal* notional. |
| **Capital Authority** | Notional vs Broker Account Capital | Persist on OP; IBKR-paper Walnut = broker. |
| **Risk Capital** | Notional ledger **or** polled net liquidation | PositionSizer still uses `RiskEquity` (journal spine), not DUT net liquidation. |
| **Leverage Guardrail** | Gross long+short vs Risk Capital; default **2×**; per-OP | Walnut stores `max_leverage=3.00`; **PositionSizer does not read it**. |
| **Broker Buying Power** | IBKR `buyingPower` | Too loose overnight. DUT still showed ~$37k after SMA was dead. |
| **Spending Capacity** | min(buying power, remaining guardrail) | **Incomplete.** Must include **overnight margin capacity** (SMA / excess). |
| **Moment of Truth** | Size at fill instant from remaining SC | Fill-driven repark still sizes from last close + 1% only. |
| **Extra-Modal Fulfillment** | Signal Market stays the Book; packaging may be LEAP | No live eval/send; Exit Capital Reconcile not built. |

**Glossary amendment (Part 1, required):** Spending Capacity becomes the **least** of:

1. Remaining **Broker Buying Power** (hard broker ceiling).
2. Remaining **Leverage Guardrail** room: `max_leverage × Risk Capital − gross(long MV + short MV)`.
3. Remaining **Overnight Margin Capacity** — when Capital Authority is Broker Account Capital: IBKR **SMA** (and/or `excessliquidity` if SMA missing). When Notional: WUT-style `equity × max_leverage − gross`.

Do **not** treat short-credited cash (`capital_base` / DUT `cashbalance` $63k) as room for another long. That is how 841 DBC landed.

Human override: per-ticket, may exceed Winston guardrail, **never** a broker reject / SMA 0.

---

## Artifacts this plan consumes (read, do not re-derive)

### Part 1 — SC / capital authority

| Artifact | What it already locked | This plan does |
|----------|------------------------|----------------|
| `CONTEXT.md` Capital Authority … Spending Capacity; Grill 2026-09-01 Q2 / D | Names, 2× gross default, buying power ceiling | **Amend SC** to include overnight SMA; persist authority |
| Ticket [`2026-09-04-tf-p3-live-sizing-and-capital-authority.md`](ecosystem/docs/tickets/2026-09-04-tf-p3-live-sizing-and-capital-authority.md) | Entire desired outcome 1–6; `max_leverage` unused | **This is the implementation plan.** Close the ticket when Part 1 ships. |
| ADR-008 | Confirmational entry ⊥ OWD ladder | Preserve. Pass `pyramid_position_number` into ProposedSize **or** refuse OWD OPs (P3 item 4). |
| ADR-010 | Kelly/AM/M meta layer; not a global default | **Out of SC scope.** Do not promote Kelly. |
| ADR-006 | Paper vs real series; CashEvent | Capital Activation still new series; SC is ops sizing |
| ADR-013 §7 | Walnut slate STP; Broker Account Capital named; “CashEvent align until Broker Account Capital wired” | Wire Risk Capital from polled NLV for Walnut; keep slate STP |
| ADR-009 | DA does not open lots; Human-Gated | SC refuse is a **park/send refuse**, not DA inventing fills |
| Session [`2026-09-10-1532-walnut-unit-risk-inspect-layout.md`](winston_v2/docs/session-reports/2026-09-10-1532-walnut-unit-risk-inspect-layout.md) | Operator: 3× gross OK for paper; DBC 108% notional is 1% risk; `max_leverage` unused | **Revoke “3× is OK” as a live-relevant assumption.** 3× stored still loses to SMA. |
| Issue [`2026-09-11-slate-atr-trails-working-stop.md`](winston_v2/docs/issues/2026-09-11-slate-atr-trails-working-stop.md) | ATR trail ≠ stop-out; DUT liquidation 612 @ 33.15 | Evidence pack for SC. P0 stop-freeze stays a **separate** code commit. |
| WUT `PositionManager#check_leverage_constraint` | `max_leverage` default **3.0**; total long+short vs `max_leverage × equity`; **long buying power subtracts longs only** | Align to **gross**; version so old PBRs do not silently change |
| Paper import caps (`PortfolioConfigImporter::PAPER_MAX_LEVERAGE = 1`) | Default paper import 1× | Walnut is **3.00** (explicit). SC will still bind via SMA. Do not force Walnut to 1× in this plan unless operator says so. |
| Ticket `2026-07-26-s4-capital-20k-survivability.md` | $20k vs $10k does not save S4; share floors change paths | Lab capital ≠ broker SMA. Do not “fix” Walnut by minting $20k notional. |
| Ticket `2026-08-13-importer-risk-percentage-one-percent.md` | `1.0` means 1% | Preserve (P3 item 5 already listed). |
| Ticket `2026-09-01-wv2-unit-heat-slate-contest.md` | Unit Heat then first-to-touch consumes cash | Contest consumes **SC**, not cashbalance. |
| ADR-015 + ticket `2026-09-11-measuring-edge-scoreboard.md` | Edge (R) WUT lab / Wv2 ops; 1R = entry risk $; no BookScore | After LEAP preference: 1R stays signal-path; booked P&L after Exit Capital Reconcile feeds Lot R. Do not display WUT PBR Edge as Walnut live Edge. |

### Part 2 — LEAP (update, do not fork)

| Artifact | Role | This plan does |
|----------|------|----------------|
| Analysis [`2026-09-09-extra-modal-leap-unit-vs-shares.md`](ecosystem/docs/analysis/2026-09-09-extra-modal-leap-unit-vs-shares.md) | Parked technical reference; geometry **B** default; three metrics | **Amend** with DUT 2026-09-11 liquidation: stock 1% unit can be 100%+ notional; SMA is the reason to prefer LEAP **cash outlay**, not “options are cheaper.” |
| Ticket [`2026-09-09-extra-modal-leap-unit-evaluation.md`](ecosystem/docs/tickets/2026-09-09-extra-modal-leap-unit-evaluation.md) | P1 blocked until Walnut grain babysits itself | **Unstick priority:** start **read-only 1×1** in parallel with Part 1. Keep **no option Desk Send** until grill + SC live. |
| Ticket [`2026-08-05-signal-path-truth-fulfillment-link-exit-reconcile.md`](ecosystem/docs/tickets/2026-08-05-signal-path-truth-fulfillment-link-exit-reconcile.md) | Dual spine; ±$D at exit | **Prerequisite** before a LEAP-packaged lot is capital-honest. Part 2 implement after or with first LEAP book, not after first send. |
| Ticket [`2026-09-01-fulfillment-packaging-policy-ops-ui.md`](ecosystem/docs/tickets/2026-09-01-fulfillment-packaging-policy-ops-ui.md) | Policy on OP, not BG | Needed for “prefer LEAP on entry” as a **rule**, not a fingerprint. |
| Plan [`trade-fulfillment-engine.md`](ecosystem/plans/trade-fulfillment-engine.md) | Configurable fulfillment; extra-modal already in CONTEXT | Add a pointer section; do not rewrite L1–L3. |
| ADR-013 §7.6–7.7 | Extra-modal stop = HITL; contest consumes cash | Addendum when geometry B sends OPT: Order Intent may be MKT/LMT on option conid; Guardrail stays HITL-on-underlying unless packaging says sell-to-close. |
| WUT `LeapPurchaseService` / `BlackScholesCalculator` | Lab contract count / synthetic premium | Reuse **count** math; **replace** premium with CPGW snapshot. |

**Will not close:** Kelly tickets, Unit Heat redesign, 20-day-after-max (ISSUE-20260909), parked-GTC vs row stop P2, CPGW unattended login.

---

## Part 1 — Spending Capacity

### 1.1 Problem (one sentence)

Winston sizes **risk units**; IBKR overnight-liquidates **notional**. Walnut ran a correct 1% DBC stack into a 2.9× gross book and DUT sold 612 shares that were never at 2N.

### 1.2 Product rules

1. **SC Check** runs before a DAY entry/pyramid is **minted onto a slate** and again at **Desk Send** / fill-driven repark (Moment of Truth). Protective GTC **replace at same units** does not consume SC. Size-up or new risk does.
2. A leg that fails SC is **not parked**. Status `sc_refused` + reason (`guardrail` / `sma` / `buying_power`). Slate Approve cannot send it without an explicit per-leg override; override still cannot beat a broker reject.
3. **Slate Contest:** Unit Heat first; remaining first-to-touch **consumes SC** (not journal cash). A fill that would overflow remaining SC is skipped, not partially invented.
4. **Risk unit is computed first** (always share-equivalent on the signal Market), then **packaging** chooses LEAP vs shares, then **SC Check** on the **cash that packaging will actually spend** (LEAP premium × 100 × contracts, or share notional). Clamp/refuse that cash. If clamp → 0, refuse. Do not silently take a 50-share “unit” that is no longer 1% without labeling `sc_clamped`. After a LEAP enter, remaining SC is recomputed from SMA / guardrail / buying power — that is the “refined SC” in comment 1.
5. **Capital Authority** column on OP: `notional` \| `broker`. Walnut paper IBKR = `broker`. dummy_sim / Schwab-as-fulfillment-only paper = `notional`.
6. **Risk Capital** for the 1% math: broker NLV when authority is broker; else `RiskEquity` (unchanged).
7. Over-deployed (cash < 25% of equity) stays an **attention flag**. It is not SC.

### 1.3 Wv2 implementation (smallest honest surface)

| Piece | Owner | Notes |
|-------|--------|------|
| `portfolios.capital_authority` | migration | `notional` \| `broker`; default from binding (IBKR paper/real → broker) |
| Persist last broker snapshot on OP | Wv2, from BG `snapshot` | NLV, buyingPower, SMA, excessliquidity, grossPositionValue, maintMargin — **hints** if authority is notional |
| `Operations::SpendingCapacity` | new service | Returns remaining $, components, `ok` / `tight` / `refused` |
| `PositionSizer.units_for` | extend | After 1% floor, clamp to SC; pass `pyramid_position_number` from DA |
| Session Order Slate Builder + FillDrivenRepark | SC Check | Skip/refuse DAY entry/pyramid; keep aligned GTC |
| AutoSend | second check | Fail closed on `sc_refused` |
| Ops UI | OP header + slate rows | See 1.4 |
| DAR / Telegram | attention | `SMA dead` / `SC refused N legs` — not a send |

BG: **read** existing snapshot/ledger fields. No new write API. If SMA is missing from the normalizer, add the field to the L2 snapshot mapping only.

### 1.4 Flags and labels (Wv2)

On the OP (ops shell, portfolio live, slate header), always in this order:

1. **Fulfillment Label** (already).
2. **Capital Authority** chip: `notional` \| `broker NLV $…`.
3. **Gross / Risk Capital** vs **max_leverage** (e.g. `2.13× / 3.00×`).
4. **SC remaining** dollars + binding constraint (`sma` / `guardrail` / `buying_power`).
5. **SMA** (broker authority only). Red when ≈ 0.

Slate leg tags: `sc_ok` · `sc_tight` (would consume >50% remaining) · `sc_clamped` · `sc_refused`.

Do not overload **over-deployed**.

### 1.5 WUT / PBR impact (do not silent-rewrite history)

WUT **already** has `max_leverage` (PBR column default **3.0**) and `PositionManager#check_leverage_constraint`. Gaps vs DUT:

- Long **buying power** subtracts **longs only**, so a fat short book does not reduce room for the next DBC long. That is the lab analogue of “short-credited cash absorbs 800 shares.”
- Constraint is `max_leverage × equity`, **not** overnight 50% / SMA.
- Historical S4 / bake-off paths used this. Changing it in place **changes fill sets** (same lesson as $10k vs $20k).

**PBR rules for this plan:**

1. Add `leverage_accounting`: `legacy_long_bp` (current, default for old recipes) \| `gross` (long+short consume the same cap).
2. **Do not** flip the default on existing fingerprints. New / Walnut-like TF recipes and a named replay use `gross`.
3. Optional `overnight_reg_t_proxy`: treat hold-through-close as **2×** even if `max_leverage` is 3. Replay Walnut-like PBR at $25k with `gross` + 2× proxy to answer “does 1% stock TF survive SMA-like lab?” — **report**, do not silently replace the 3× lab champion.
4. Fingerprint includes `leverage_accounting` when ≠ `legacy_long_bp` (same rule as risk_scale_config).
5. WUT UI: show “leverage constrained” notes that already exist; add gross vs legacy on the PBR.

Lab `max_leverage=3` remains a **research knob**. It is not a claim that IBKR will hold 3× overnight.

### 1.6 Walnut ops while Part 1 ships

Until SC Check is live: **no new stock units** on Walnut (no 4th DBC pyramid, no new names). Keep the 229-share GTC @ 32.56. That is desk policy, not a code freeze.

### 1.7 Verification

- Specs: SpendingCapacity (broker SMA binds before buyingPower; guardrail 2× vs 3×; protective replace same-size does not consume; clamp to 0 → refuse).
- Slate request spec: DBC-like quiet ETF 3rd pyramid `sc_refused` on a $25k / 2.9× fixture.
- WUT: one new PBR fixture `gross` vs `legacy_long_bp` fill-count difference; existing default suite stays green.
- Compose: Walnut slate shows SC chips; WorkingFillJob does not remint a DAY pyramid that fails SC.
- Replay math of 2026-09-11: fixture from DUT snapshot (NLV $25,028, gross ~$73k pre-liq, SMA post-liq $113) refuses the 612-share-equivalent add.

### 1.8 Part 1 done when

Ticket **2026-09-04-tf-p3-live-sizing-and-capital-authority** can move to **Done** with: Capital Authority persisted, Risk Capital from NLV on Walnut, Leverage Guardrail + SC in sizer and slate, Moment of Truth clamp, OWD level passed or OWD refused, 1% convention preserved, Kelly still not default.

---

## Part 2 — LEAP as entry preference (update existing design)

### 2.1 Why now

Part 1 stops IBKR from confiscating stock units. It does **not** make a 1% DBC unit cheap. On ~$25k, that unit is still ~$9k–$28k cash. A listed ATM ~3-year LEAP is **premium × 100 × contracts** — same signal Market, far less SMA burn.

This is **Extra-Modal Fulfillment**, not a new Trading Strategy fingerprint — unless Unit Heat occupancy changes (then grill).

### 2.2 Do not start from zero

Amend, do not rewrite:

1. Analysis `2026-09-09-extra-modal-leap-unit-vs-shares.md` — add a **2026-09-11 DUT** section: liquidation was SMA/Reg T, not 2N; buying power lied; 1% stock unit vs overnight capacity is the flip **reason**. Keep three metrics (cash / risk-unit match / residual delta). Keep geometry **B** as send default (Desk-Sent command **is** the LEAP). Keep Guardrail HITL-on-underlying until packaging says otherwise.
2. Ticket `2026-09-09-extra-modal-leap-unit-evaluation.md` — status: **Proposed, unblocked for read-only**. Block **option Desk Send** until: (a) Part 1 SC Check live, (b) 1×1 matrix row tradable, (c) grill on flip threshold + stop law.
3. `plans/trade-fulfillment-engine.md` — short pointer: packaging preference is OP policy; engine already assumed extra-modal.
4. Ticket `2026-09-01-fulfillment-packaging-policy-ops-ui.md` — implement as the place “prefer LEAP on **entry** (shares on pyramid unless policy says else)” lives.
5. Ticket `2026-08-05-…-exit-reconcile.md` — must run before a LEAP lot is treated as capital-honest (signal 210 IBM vs 2 calls +$D at exit).

### 2.3 Geometry (already parked)

- **A.** Park IBM/DBC stock STP; if it prints, buy LEAP instead — fights “DUT is SoT for the Desk-Sent command”; double-unit risk.
- **B. (default)** No stock STP for that name. DA still evaluates the 55-day on parquet. When touched, **Desk Send MKT or LMT on the option conid**. Journal working until Accept-Fill at the **option** print. Book stays the **signal Market**. Protective: HITL sell-to-close when Working Stop would fire on the underlying (ADR-013 addendum).

A LEAP limit is **not** a breakout stop. Moment of Truth for B is “signal touched,” closer to Winston Quiver market-on-signal than Turtle STP.

### 2.4 DUT / CPGW (already parked)

- Resolve OPT conid: `secdef/search` → strikes → `secdef/info` (BG `resolve_conid` is stock-biased; Order Intent must carry explicit option conid).
- Snapshot bid/ask/delta; first snapshot often empty.
- `place_order` already posts `{orders:[{conid,…}]}` — OPT is a conid, not a new adapter.
- **Do not** run TWS `compete: true` on the same paper username as CPGW.
- Second paper username for eval-only IB Gateway remains optional and later.
- Verify DUT option permissions, multiplier 100, option tick, paid options market data (paper quotes may be empty).

### 2.5 Signals / journals / Books / cash (already locked in CONTEXT)

```
DA signal on Market DBC (55-day, 1% share-equivalent unit)
  → Journal + task (enter) on Book DBC
  → Fulfillment Packaging Policy: leap (entry preference)
  → Order Intent: BUY CALL conid, qty contracts, LMT/MKT
  → Accept-Fill at option print (premium × 100 × qty = flow, purchase-signed)
  → Position: signal DBC, option columns + fulfillment_details
  → Working Stop still on DBC parquet; GTC stock stop is N/A; HITL sell-to-close
  → Pyramid draft still in share units; fill may be more calls or shares per policy
  → Exit: sell-to-close; Exit Capital Reconcile applies ±$D vs signal-path P&L
```

`RelatedInstrumentFulfillment` already does the cash multiplier. Do not retarget Books to the option root.

SC on a LEAP enter consumes **premium cash**, not share notional — that is the point, and it is how comment 1 “evaluate sizing based on the refined SC (after preferring LEAPs)” works. Still run SC Check (SMA can still die if many names take calls).

**Profitability / equity / Edge after packaging** (comment 1, not optional):

| Spine | What it measures | Must not |
|-------|------------------|----------|
| Signal Spine | IBM units, Working Stop, heat, 20-day gate, 1R | Pretend 210 shares were bought |
| Booked Capital Spine | DUT prints, LEAP premium flow, NLV when broker authority, Exit Capital Reconcile ±$D | Ignore the option P&L until someone notices |
| Edge Snapshot | Lot R = booked P&L / signal 1R; ops n is this series | Show WUT PBR Edge as Walnut live Edge (ADR-015) |

WUT PBRs that later simulate LEAP packaging are a **new recipe / fingerprint**, not a silent rewrite of share-path bake-offs. First lab slice can stay share-path `gross` SC; LEAP-packaged PBR is after the 1×1 matrix proves tradable contracts.

### 2.6 First slice (read-only, parallel with Part 1)

One underlying with a listed ≥2y LEAP (IBM, or next Walnut name). One expiry class, strike nearest last. CPGW snapshot. Emit: share-unit cash, LEAP cash, contracts after 1% cap, delta if any, bid/ask, tradable flag.

**No option send** in this slice.

### 2.7 Grill before any OPT send (do not skip)

1. Flip threshold: **cash outlay** is the operational trigger on ~$25k; **risk-unit match** is a hard floor (do not take a 100-share-control contract that is 4% risk); delta is residual display.
2. Stop law: HITL sell-to-close vs policy-send sell-to-close when DBC 2N would fire.
3. Geometry B confirmed.
4. Second username for eval sidecar: yes/no.

Expect an **ADR-013 addendum** if B + option Order Intent is locked.

---

## Sequence

```
Part 1a  CONTEXT SC formula + Capital Authority column
Part 1b  SpendingCapacity service + BG snapshot fields (SMA)
Part 1c  PositionSizer clamp + DA pyramid_position_number
Part 1d  Slate / FillDrivenRepark / AutoSend SC Check
Part 1e  OP + slate UI chips
Part 1f  WUT leverage_accounting=gross (opt-in) + Walnut-like $25k replay
Part 1g  Walnut live: refuse stock adds that fail SC
         ── parallel ──
Part 2a  Amend LEAP analysis + unstick read-only ticket
Part 2b  CPGW 1×1 matrix
         ── after 1d + 2b + grill ──
Part 2c  Packaging policy UI (prefer LEAP on entry)
Part 2d  Exit Capital Reconcile (required for honest equity / Edge — comment 1)
Part 2e  Ops Edge Snapshot uses booked P&L / signal 1R on extra-modal lots
Part 2f  One paper LEAP send (explicit operator gate)
```

Part 2f is **not** authorized by accepting this plan. Part 2d–2e are **in** the firm model: without them, LEAP preference would lie about profitability and then size the next unit from a fake SC.

---

## Out of scope

- Kelly as live default (ADR-010).
- Slate Automation (no Approve).
- Live IBKR / Schwab `order_write`.
- Silent option STP / spreads.
- Changing Turtle 1% / 2N geometry.
- Forcing Walnut `max_leverage` to 1× without a separate operator call.
- Rewriting historical WUT bake-off winners.

---

## Risks

- **SMA vs excessliquidity vs availablefunds:** pick SMA for overnight TF; log the other two. If CPGW SMA is stale/zero incorrectly, we over-refuse — fail closed.
- **WUT `gross` replay may look “worse”** than 3× lab — that is the honest $25k book, not a regression to hide.
- **LEAP data:** empty paper option quotes → matrix `untradeable`, not synthetic BS.
- **Compete:true:** never TWS + CPGW same username.

---

## Operator locks assumed (challenge if wrong)

1. SC includes overnight SMA, not only buying power + 2× gross.
2. Walnut stays `max_leverage=3` on the OP **and** still cannot add when SMA is dead.
3. WUT historical PBRs stay `legacy_long_bp`; new TF / Walnut-like use `gross`.
4. LEAP work **updates** the 2026-09-09 analysis/ticket; no third design doc.
5. Option Desk Send waits for SC Check + 1×1 + grill.
6. Firm model (comment 1): signal stays on the underlying; LEAP is preferred fulfillment; Exit Capital Reconcile + Edge (R) use booked P&L / signal 1R; next unit sizes from SC **after** that packaging.
