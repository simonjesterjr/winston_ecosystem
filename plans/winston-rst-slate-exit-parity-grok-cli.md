# Plan: RST → desk overnight slate + last-unit exit supersession (lab parity)

**Status:** In progress — Grok CLI shipped WUT **A0–A4 + B0–B4** (2026-09-13/14). Remaining: Grok Bot fixture UAT; **A5/B5** narrow Edge (R) panel (operator-gated).  
**Type:** Lab geometry / methodology parity (**WUT only** this program; Wv2 DA / Session Order Slate are consumers later, not this pass)  
**Mode:** contractor  
**UAT owner:** Grok Bot (report-only; no pack promotion without operator lock)  
**Bot brief (verify B1–B4):** [`docs/operations/grok-bot-rst-s2-working-stop-verify.md`](../docs/operations/grok-bot-rst-s2-working-stop-verify.md)  
**Sibling:** [`winston-lab-eval-grok-cli.md`](winston-lab-eval-grok-cli.md) (RST fill geometry shipped; this plan closes what RST v1 deliberately left out)  
**Follow-on program:** [`winston-strategy-slate-to-wv2-paper.md`](winston-strategy-slate-to-wv2-paper.md)

### Operator locks (2026-09-13 grill)

| Topic | Lock |
|-------|------|
| Scope | **WUT lab only.** No Wv2 DA rewrite, no Broker Gateway write, no pack default. |
| Overnight contest (A) | One arm list in the existing ticket queue — **not** a Session Order Slate product. Entries **and** pyramids. Higher Average True Range (ATR), `market_id` tie-break. Overflow **not armed**. Lab does **not** fake intra-bar first-to-touch. **Shipped 2026-09-14 (WUT RST).** |
| Exit phases (B) | Turtle System 2 (S2) recipes only (55/20 + `move_to_last_entry`). System 1 (S1) 20/10 unchanged. |
| Fill for this pass | `resting_stop_touch` (RST). |
| Fingerprint / handoff | **Unchanged.** Lab geometry is not a new Trading Strategy (TS) identity. |
| Workstream C | **Out.** No Wv2 ticket edits this program. |

---

## Problem (operator)

`resting_stop_touch` (RST) is the honest ops-parity **fill** model for Wv2-style parked day-order stops (entry / pyramid / protective). It captures signal→T+1-open slippage that hybrid/next-open hid.

It is **not yet** a full simulation of the desk’s overnight cycle:

1. **Pre-session stack ranking / day-order slate** — which names get parks when heat/cash/units cannot take every breakout.
2. **Last-unit exit supersession** — once a name is **maxed**, Working Stop can become the **20-day** (when it has passed 2N in the trade’s favor); pierce is still a **stop-out**, not a next-open channel exit. While lots &lt; max, 20-day must **not** fire.

Until both land in WUT under RST, Edge (R) on TS#77 (and cousins) is **not** indicative of the live Turtle EOD TF system we intend to run on paper / Walnut / Wv2.

**Doctrine lock (2026-09-13):** Prefer RST for Donchian/stop-entry recipes. Do **not** “fix” Edge by switching back to hybrid/next-open. Fair fill A/B holds the recipe fixed and varies only `hybrid` vs `resting_stop_touch`.

---

## Evidence (do not re-derive)

| Claim | Source | What it establishes |
|-------|--------|---------------------|
| Overnight cycle: build slate → park stop-markets → touch fills → cancel unfilled DAY; replace protective GTC | `docs/tickets/2026-08-20-resting-session-stop-orders.md` §Intended session cycle | Product shape RST is aiming at |
| Over-subscription needs **pre-session ranked slate** + **reserved units**; names that do not fit are **not parked** | Same ticket §Evaluation #4 | Ranking gap is named, not new |
| Lab already ranks competing entries by higher ATR (then market_id) | `winston_unit_test/.../entry_decision_maker.rb` | Seed ranking rule for T+1 ticket queue |
| Unit heat + slate contest (buy-strength / sell-weakness; first-to-touch once parks exist); no ER menu | `docs/tickets/2026-09-01-wv2-unit-heat-slate-contest.md`; WUT `HeatCapacityGate` | Live contest law to port / mirror in lab |
| Turtle S2: 20-day **not evaluated** while lots &lt; max; after maxed, switch Working Stop to 20d when it has **passed** 2N; one Working Stop; pierce = stop-out flatten-all | `docs/business-context/turtle-s2-pyramid-and-working-stop.md` | Exit supersession law |
| Wv2 DA today skips Working Stop; fires 20-day under max (AMCR); silence on 2N pierce (WEAT) | `winston_v2/docs/issues/2026-09-09-da-20day-exit-under-max-lots.md` | Same gap on ops DA — lab must not diverge |
| Walnut paper is already Session Order Slate STP path for TurtleV1 S2 | `docs/tickets/2026-09-09-walnut-paper-session-order-slate.md` | Consumer of correct Working Stop + parks |
| RST v1 matches entry/pyramid/stop **fill geometry** mostly; **not** pre-open 7–20 market ranking slate or last-pyramid 20d-BO exit supersession | Operator lock 2026-09-13 (memory / prior RST note) | Scope boundary of this plan |
| FULL UAT 32-cell TS#77×RST: only 3/32 positive Edge(R); best Yellow×1% ≈ +0.075 | `docs/analysis/2026-09-13-strategy77-rst-heat-risk-matrix.{md,json}` | Current Edge is RST-incomplete chassis — do not treat as TS death sentence |
| #590 fat Edge ≠ TS#77 — different recipe + hybrid fill | `docs/analysis/2026-09-13-pbr590-vs-blue-601-604.{md,json}` | Do not promote hybrid Edge as Turtle ops truth |

---

## Goals

1. **WUT under RST** simulates overnight **slate build + rank + reserve** so competing breakouts contest heat/cash the way the desk will park DAY stops.
2. **WUT under RST** implements Turtle S2 **Working Stop phases** (2N while adding; 20d supersession after max when channel has passed 2N; stop-out on pierce).
3. Fingerprint + Edge panels re-run so TS#77 (and other candidates) are scored on **ops-parity geometry**, not fill-only RST.
4. Spec / fixtures Grok Bot can UAT; **no** silent pack promotion.

## Non-goals

- Broker Gateway `order_write` / live Desk Send (parent still gated).
- Preferring hybrid fill to juice Edge.
- Expected-return ranking or human nightly pick-list (forbidden by heat-slate contest ticket).
- Close-confirm / Accept-Fill product work (ops; out of RST v1 by design).
- Rewriting ADR-009 wholesale (use addendum ticket `2026-09-01-adr-009-resting-slate-addendum.md` if language drifts).

---

## Workstreams

### A — Pre-session stack ranking (lab slate)

**Intent:** Before session T+1 bars are applied, given T’s signals + open book + heat/cash, emit an ordered **park list** (entry / pyramid roles) with unit sizes reserved. Overflow = not parked (or documented overflow policy — default: **not parked**).

**Phases**

| Phase | Deliverable | Notes |
|-------|-------------|-------|
| A0 | Spec note: `docs/business-context/wut-rst-session-slate.md` | **Done 2026-09-14.** |
| A1 | Lab object: session slate / ticket queue under RST | Roles `entry_stop` \| `pyramid_stop` on `LabFillTicketQueue`. **Done.** |
| A2 | Rank: higher ATR first, stable tie-break (`market_id`); heat refuse before park | Mirror `EntryDecisionMaker.rank`; Faith unit-heat refuse where turtle heat on. **Done.** |
| A3 | Reserve units at **park time** from risk_equity + N; gap fill still sizes stop from **actual fill** | `units_override` + fill-relative stop. **Done.** |
| A4 | Golden fixtures (over-subscribed morning: 8 signals, capacity for 3) | Fingerprint **unchanged** (operator lock). Spec: `portfolio_backtest_rst_overnight_arm_spec.rb`. **Done.** |
| A5 | Edge panel delta: same TS#77 cells with slate-rank on vs off | Report-only; Grok Bot after fixture UAT. |

**Acceptance (A)**

- [x] Over-subscription fixture: parks ≤ heat/cash capacity; ranking deterministic.
- [x] RST path only (no hybrid sneak).
- [ ] Artifact: analysis note comparing Edge with/without slate contest on one book (Yellow or Blue).

### B — Last-unit exit supersession (Working Stop phases)

**Intent:** Align WUT exit evaluation with `turtle-s2-pyramid-and-working-stop.md` and ISSUE-20260909 expected methodology (fulfillment mode still RST touch / gap→open on the Working Stop).

**Phases**

| Phase | Deliverable | Notes |
|-------|-------------|-------|
| B0 | Gap inventory: current `evaluate_exit` / stop path vs S2 law | Filed: `docs/business-context/wut-s2-working-stop-lab.md` |
| B1 | While lots &lt; max: **suppress** Breakout20 (and do not park 20d protective) | Fixture: 3/4 long, 20d prints — no exit; only 2N + next pyramid. **Done 2026-09-13 (WUT RST).** |
| B2 | On max fill: Working Stop = last±2N; begin **watching** 20d | No dual protective stops. **Done 2026-09-13 (WUT RST).** |
| B3 | When 20d has **passed** 2N in trade’s favor: Working Stop **becomes** 20d; nightly ratchet | Replace, never cancel-all semantics in lab state. **Done 2026-09-13 (WUT RST).** |
| B4 | Pierce of current Working Stop → one `:stop_out` flatten-all (move-together); same-session RST fill; **no** parallel Donchian exit that bar | Priority rule from ISSUE-20260909. **Done 2026-09-13 (WUT RST).** |
| B5 | Fingerprint + Edge panel on TS#77 S2 books | Report-only |

**Acceptance (B)**

- [x] Fixtures for: under-max 20d silent; maxed+20d-passed ratchet; 2N / 20d Working Stop pierce flatten-all (RST S2). Gap-open through stop already in RST fill tapes.
- [x] No 20-day channel exit under S2 recipe (RST) — 20-day is Working Stop after max+passed, never close-priced Donchian.
- [ ] Artifact: before/after Edge on same stamped cells (fill cadence still RST). Needs workstream A first.

### C — Ops handoff — **out**

Operator lock: WUT only. Do not edit Wv2 issues or Walnut tickets in this program.

---

## Grok Bot — verify A + B1–B4

Brief: [`docs/operations/grok-bot-rst-s2-working-stop-verify.md`](../docs/operations/grok-bot-rst-s2-working-stop-verify.md) (B) plus the A spec/fixtures below.

```bash
./bin/compose exec -T winston_unit_test bundle exec rspec \
  spec/services/portfolio_backtest_rst_overnight_arm_spec.rb \
  spec/services/portfolio_backtest_s2_working_stop_spec.rb \
  spec/services/portfolio_backtest_resting_stop_touch_spec.rb \
  --format documentation
```

**Pass:** A arm-list examples green (8→3 heat parks; unarmed no fill; entry+pyramid one list; hybrid unchanged) **and** S2 B1–B4 green **and** RST fill tapes green.

Do **not** execute PBR **#596**, `FULL=1` 32-cell, or `/edge-scorecard` on pre-fix cells. Old `strategy77_rst_heat_risk_v1` journals predate A+B.

---

## Suggested next (after Bot fixture UAT)

1. **A0–A4 + B0–B4** — **done** (Grok CLI). Bot verifies.  
2. **A5 / B5** narrow Edge UAT (Grok Bot): Yellow + Blue × turtle heat × 1% risk × RST — **not** another blind 32. New PBRs only (old cells are pre-gate).  
3. Only then expand books / strategies (see sibling program plan).

## Parallelism / cost

- PBR runtime still ~3–4 min; 4–6 parallel. Prefer **fixture-first** over megamatrix until A+B green.  
- Mutators stay `authorization: lab_geometry_report_only`.  
- Transport: Shell-on-sawtooth / existing lab-eval hop (no Funnel requirement).

## Out of scope reminders for implementers

- Do not park every flat-name breakout “and hope heat holds.”  
- Do not implement “tighter of 2N and 20d” while adding.  
- Do not use ADR-009 Unsignaled Exit Allowance to skip methodology stop evaluation.  
- Close-confirm / Accept-Fill remain ops tickets.

## Definition of done (this plan)

- [x] Specs A0 + B0 filed (`wut-rst-session-slate.md`, `wut-s2-working-stop-lab.md`).
- [x] WUT fixtures green for overnight arm list (A) and S2 Working Stop B1–B4 under RST.  
- [ ] Fingerprinted lab path; Edge delta note filed under `ecosystem/docs/analysis/`  
- [ ] Sibling program plan can start **strategy discovery** on the corrected chassis  
- [ ] No pack promotion; operator lock required to stamp “ops-parity v2”

## References

- Parent: `docs/tickets/2026-08-20-resting-session-stop-orders.md`  
- Lab child (shipped geometry): `docs/tickets/2026-08-20-wut-resting-stop-touch-fill-cadence.md`  
- S2 law: `docs/business-context/turtle-s2-pyramid-and-working-stop.md`  
- DA bug twin: `winston_v2/docs/issues/2026-09-09-da-20day-exit-under-max-lots.md`  
- Heat contest: `docs/tickets/2026-09-01-wv2-unit-heat-slate-contest.md`  
- Walnut consumer: `docs/tickets/2026-09-09-walnut-paper-session-order-slate.md`  
- Prior lab eval plan: `plans/winston-lab-eval-grok-cli.md`  
- Scorecard: `docs/analysis/2026-09-13-strategy77-rst-heat-risk-matrix.md`  
- Bot verify brief: `docs/operations/grok-bot-rst-s2-working-stop-verify.md`  
- A spec: `docs/business-context/wut-rst-session-slate.md`
