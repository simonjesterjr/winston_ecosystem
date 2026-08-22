# Ticket: Resting session stop-market orders (entry / pyramid / protect)

**Status:** Blocked  
**Priority:** P1  
**Date:** 2026-08-20  
**Series:** `trade-fulfillment-engine` (L3+; not an L1 child)  
**Domain:** methodology fill cadence, Order Intent, Working Stop, Broker Gateway, Desk Send  
**Monoliths:** winston_unit_test (lab cadence), winston_v2 (slate / Daily Analysis / desk), broker_gateway (transport when `order_write` exists)  
**Do not start (this ticket):** Broker Gateway (BG) is L1 (`auth` + `txn_read` + `order_read` only). Live slates wait on write-capable fulfillment.  
**Lab child (unblocked):** [`2026-08-20-wut-resting-stop-touch-fill-cadence.md`](2026-08-20-wut-resting-stop-touch-fill-cadence.md) — WUT `resting_stop_touch` geometry; start now.

**Origin:** Operator session 2026-08-20 — next-open fill vs “would-have-been” 2× Average True Range (ATR) stop (signal 110, 2 ATR stop 102, next open 100). That tape is a **contra-indicator only under next-open**. Resting breakout stops dissolve it.

---

## Problem

Winston’s canonical End of Day (EOD) story is: **Signal Date** T → **Fill Date** T+1 **next session open** (ADR-009, lab `next_bar_open`). That delay creates a class of tapes the original Turtles never had:

- Breakout prints ~110 on T.
- Planned 2 ATR stop *if filled at 110* would be 102.
- T+1 opens at 100 — through the counterfactual stop — before any order was live.

Next-open Trend Following (TF) still enters at 100 and hangs a **fill-relative** stop at 92. Turtle **stop-entry** never fills (buy-stop at 110 never trades). Mixing the two (enter at 100, keep stop 102) is the rejected hybrid.

When fulfillment automates through **Broker Gateway**, next-open market-on-open on a *close-based* signal will bake that gap into live books. The methodology-correct Turtle / Donchian loop is **rest orders at known prices before the session**, not “signal last night, buy the open.”

---

## Intended session cycle (operator sketch, refined)

After T’s bar is final and Daily Analysis (DA) / lab levels are known, **before session T+1**:

1. Build a **session order slate** per Active Operational Portfolio (OP) + Trading Strategy (TS).
2. Park **stop-market** orders (not limits — see below) for:
   - **Initial entry** — buy-stop / sell-stop at the current breakout (e.g. 20-day or 55-day high/low).
   - **Pyramid** — buy-stop / sell-stop at `last_fill ± pyramid_atr_multiplier × N` (N = ATR used by the TS; **not** hardcoded 1 ATR).
   - **Protective** — stop-market on every open lot at the **Working Stop**.
3. During T+1, fills happen if price **touches** the parked level (gap through → fill at open / auction).
4. **After the session:**
   - Unfilled **entry** and **pyramid** day orders → cancel.
   - Fills → Confirmation Intake → Human-Gated book (until a later accept-fill ADR).
   - Recompute levels (new Donchian, new N, new heat / cash).
   - Park the **next** session’s slate.

Unfilled entry orders dying at the close is correct. **Protective stops are not in that cancel set.**

---

## Evaluation — what the sketch is missing

The loop is the right *shape*. These are the holes that will hurt when BG can write.

### 1. Order type: stop-market, not limit

Breakouts need **buy-stop / sell-stop** (stop-market): *if last ≥ 110, buy at market*.

A **limit** buy at 110 only fills if price is at or *better than* 110 — that is a fade, not a breakout. “Limit buy/sell market” is not a broker type.

Optional later: **stop-limit** with a slippage band (can **miss** on a fast gap). Default for Turtle geometry is stop-market. Name the Order Intent `stop_market` / `stop_limit`, never “breakout limit.”

### 2. Three slates — cancel-all is a capital bug

| Role | Lives overnight? | EOD if unfilled |
|------|------------------|-----------------|
| Entry breakout | No (day) | **Cancel** |
| Pyramid scale-in | Usually no (day) | **Cancel** |
| Protective Working Stop | **Yes** | **Replace in place** if the stop moved; never flatten the overnight book |

Cancel-all-then-replace on live protective stops leaves the account **naked** between cancel-ack and new-ack. Replace, or two-phase (new working → then cancel old). Failed cancel of a **stale entry** stop (yesterday’s 55-day high still live) is the other disaster.

Winston today does **not** assume broker stop = Working Stop. This program would make matching them a product invariant, with Stop-Out Reconciliation still catching gap fills.

### 3. This is a methodology change, not “just BG wiring”

ADR-009 locks next-open as the default EOD fill story. Winston Unit Test (WUT) `next_bar_open` sizes `stop = fill ± multiplier × ATR_T`. Lab already scored **price-level pyramids** (`hybrid_entry_next_pyramid_price_level`) and **rejected** them as the S4 pack default (ticket `2026-07-26-hybrid-fill-price-level-pyramid.md`).

Resting **entry** stops were not that experiment. Do **not** automate live resting entries against a lab that still fills next open. Either:

- add a WUT cadence that **touches** parked levels (OHLC high/low vs stop price; gap → open), fingerprint it, and only then hand off OPs that used it, or
- keep next-open as the recipe and treat resting stops as a **new** TS family.

Live ≠ lab is how you get a silent strategy change at the broker.

### 4. Over-subscription (heat / cash / units)

Parking a breakout on **every** flat book can fill eight names the same morning. Turtle heat (L1–L4), `max_positions_per_symbol` / portfolio, and free cash will not survive that.

Need a **pre-session ranked slate** with **reserved units** (same idea as the lab T+1 ticket queue). Names that do not fit heat/cash are **not parked**, or are parked only as a documented overflow policy (in-flight cancel of lower-rank working orders is hard and broker-specific).

Size units from **risk_equity** and **N at park time**. A gap through the entry stop fills worse (110 parked, open 115 → fill 115). Turtle stop is **2N from actual fill**, not from 110.

### 5. Direction and already-in-market

- Flat: may rest **both** buy-stop and sell-stop (System 2). Same-session both-trigger needs a rule (one-cancels-other, or first fill wins + cancel opposite).
- Long: rest protective sell-stop + pyramid buy-stop. Do **not** rest a short entry unless `always_in_market` / reverse is on.
- Reverse: exit + opposite entry same session is its own orchestrator, not “park both and hope.”

### 6. Filters that are not a price

**Confirmational Entry**, skip-after-winner, and other non-price gates cannot be a resting stop. Either they disable the park, or they stay a T+1 human/policy filter (which reintroduces next-open).

### 7. Product / ADR gates (not BG-only)

- BG L1 **must not** grow `order_write` on this ticket. Desk Send is L3. The fulfillment write ADR is **not** current **ADR-010** (that number is Risk Scale Meta-Layer). Use the next free ADR id when L3 is grilled.
- First automation is **confirm the day’s slate** (Human-Gated park), not Daily Analysis silently `place_order`.
- Paper path: `dummy_sim` can rehearse slate → synthetic fills → Confirmation Intake before any live broker.
- Evidence Standard needs an **order role** (`entry_stop` | `pyramid_stop` | `protective_stop`) so intake can match the right journal/lot.
- Related deferred ledger work: [`2026-07-15-journal-ledger-order-vs-fill-deferred.md`](2026-07-15-journal-ledger-order-vs-fill-deferred.md) (orders vs fills). This ticket is the **methodology + session cycle**; that one is journal/OMS rows. Activate together when L3 is real.

### 8. Broker / venue (equities ≠ Turtle futures)

Turtles were futures. Schwab/IBKR equities add: short locate, pattern-day-trader, LULD / halt, opening auction vs stop trigger, extended hours (usually **do not** arm entry stops in pre-market unless explicit). Partial fills, rejects, and “stop elected but not filled” must round-trip through evidence.

Multiple OPs, same symbol, one underlying broker account: allocation / binding per OP or this slate will collide.

### 9. What this *does* fix

With a buy-stop at 110:

- Open 100 → **no fill**. No 102 object. No contra-indicator overlay required.
- Open 115 (gap through entry) → fill 115, stop 115 − 2N.
- Already long, protective 102, open 100 → stop elected at the open (Stop-Out Reconciliation; loss can exceed 2N).

That is the Turtle tape. The 110 / 102 / 100 next-open conundrum was an artifact of **close signal + market-on-open**.

---

## Scope (when unblocked)

1. **ADR** — second fill story: resting stop-market touch vs ADR-009 next-open. Fingerprint / TS flag. Do not silently replace next-open for existing OPs.
2. **WUT** — **child ticket, unblocked:** [`2026-08-20-wut-resting-stop-touch-fill-cadence.md`](2026-08-20-wut-resting-stop-touch-fill-cadence.md). Same-session Donchian touch (not a T+1 skip filter). Heat/cash **reservation of unfilled parks** stays on this parent.
3. **Wv2** — session slate object (per OP, per role, units frozen, N frozen, cancel/replace plan). DA emits the slate; desk confirms park until policy autofill exists.
4. **BG L3** — `place_order` / `replace_order` / `cancel_order` for stop-market; evidence roles; dummy_sim rehearsal first.
5. **Intake** — fill of a parked stop matches the slate row → journal; unfilled cancel is not a Passed Signal of the next-open kind (it is “level not touched”).

## Non-goals (now)

- Any `order_write` on L1 bindings.
- Changing default S4 / Turtle paper OPs from `next_bar_open` without a scored lab cadence.
- Implementing stop-limit as the default.
- Hardcoding pyramid distance = 1 ATR.
- Cancel-all working orders as the EOD job.

## Activation gates

Unblock only when **all** are true:

- [ ] BG L1 Confirmation Intake is stable in compose (read path, dummy_sim, evidence).
- [ ] Fulfillment **write** ADR exists (new number; not ADR-010 risk-scale) and authorizes Desk Send / `order_write`.
- [ ] Fill-cadence ADR (or ADR-009 amendment) chooses resting-touch vs next-open, and WUT can simulate the chosen story.
- [ ] Operator explicitly authorizes implementation (this ticket is capture, not build auth).

## Acceptance (when activated)

- [ ] Written ADR: order type, three roles, overnight protective replace, over-subscription.
- [ ] WUT spec: open 100 vs parked buy-stop 110 → **no entry**; open 115 → fill 115, stop fill-relative 2N.
- [ ] WUT spec: protective stop 102, next open 100 → stop-out at open, not a new long.
- [ ] dummy_sim: park slate → touch fill → intake → Desk Confirm; unfilled entry cancelled; protective not cancelled.
- [ ] No live capital orders from this ticket alone.

## Related

- ADR-009 EOD next-open default; Working Stop ≠ broker SoT today
- Lab T+1 queue: `docs/adr/2026-07-25-lab-t1-fill-queue.md` (price-level pyramid addendum)
- [`2026-07-26-hybrid-fill-price-level-pyramid.md`](2026-07-26-hybrid-fill-price-level-pyramid.md) — scored, **rejected** as S4 pyramid default
- [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md) — L1 epic; this is L3+ related, not a child
- [`2026-07-15-journal-ledger-order-vs-fill-deferred.md`](2026-07-15-journal-ledger-order-vs-fill-deferred.md) — order vs fill ledger
- `plans/trade-fulfillment-engine.md` — Desk Send / `order_write` still L3
- `business_analysis/2026-08-12-turtle-systems-and-heat.md` — N, 0.5N pyramid, heat 4/6/10/12
