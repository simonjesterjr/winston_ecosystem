# ADR-018: Plan A preferred packaging / Plan B suboptimal fallback (Mode C LEAP→underlying first)

**Status:** Accepted  
**Date:** 2026-09-19  
**Deciders:** Operator (John) + Architecture / Grok Bot Chief of Staff  
**Builds on:** ADR-009 (Human-Gated desk; dual spines; Desk Workflow), ADR-013 (paper write / HITL extra-modal), ADR-017 (LEAP Model B precalc for IBKR-bound / Desk-Send — **does not govern Mode C paper fulfill**)  
**Domain law:** [`docs/business-context/mode-c-leap-plan-a-plan-b.md`](../business-context/mode-c-leap-plan-a-plan-b.md); [`leap-extra-modal-proxy.md`](../business-context/leap-extra-modal-proxy.md); [`human-gated-desk-and-fulfillment.md`](../business-context/human-gated-desk-and-fulfillment.md)  
**Authoritative plan:** [`plans/wv2-bg-ibkr-leap-fulfillment.md`](../../plans/wv2-bg-ibkr-leap-fulfillment.md) (Mode C paper-eval variant)  
**Tickets:** `2026-09-18-mode-c-leap-preferred-underlying-fallback.md`, `2026-09-18-wv2-workflow-fulfillment-justification.md`  
**Code:** Wv2 PR #7 (Plan B + Justification); follow-ups for form prefill / spine / Plan B callout  
**Glossary:** `CONTEXT.md` — Plan A, Plan B, LEAP-preferred, untradeable, Justification, Signal Spine, Booked Capital Spine, `signal_share_units`, Mode C

## Context

**Plan A is policy-defined**, not instrument-defined. Mode C paper OPs use `leap_fulfillment=all` (**LEAP as Plan A**): IBKR real chain for ATM long-dated packaging; journals/cash stay **Wv2 paper** (no IBKR bind, no OPT Desk-Send). ADR-017 Model B governs **IBKR-bound** LEAP packaging / Desk-Send — Mode C must not be confused with that path.

Operators hit cases where Plan A LEAP cannot be packaged honestly:

- No listed expiry ≥ min LEAP horizon (`no_expiry_ge_min`) — e.g. BITQ / Indigo #1583 journal #1946  
- Affordability floor: `floor(signal_share_units/100) == 0` (`zero_contracts` / `zero_contracts_floor`) — e.g. SMH / Orange #1576 journal #1941 (17 shares)

Without a desk rule, the workflow left **units=0**, `fulfillment_type=leap`, and no first-class confirm path — looking like an error rather than **suboptimal packaging so we still enter**. Auth/session/CPGW failures are a different class and must not silently become Plan B.

## Decision

We choose a **general Plan A / Plan B packaging law**, with Mode C LEAP→underlying as the first concrete instance:

### General law

1. **Plan A** = whatever **preferred fulfillment packaging** the Trading Strategy / OP **Fulfillment Packaging Policy** says for this signal (shares, LEAP, other extra-modal). It is **not** hard-coded to LEAPs.  
2. **Plan B** = when Plan A cannot be fulfilled honestly (**untradeable** / unavailable — not auth-blocked), the desk may still **enter the market** with a **suboptimal but valid** packaging choice that preserves the **Signal Spine** (methodology size, direction, Working Stop on the underlying). Plan B is explicitly second-best packaging, not a different signal.  
3. **Hard stop** = auth / session / broker-connectivity failures for the path Plan A needs — **no** silent Plan B; restore the path first.  
4. **Justification** is mandatory when Plan B is active: what Plan A was, why it failed, what Plan B is, and that the operator is confirming suboptimal packaging on purpose.  
5. **Confirm form defaults to Plan B** when Plan A failed untradeable — prefilled packaging + size for Plan B, with a callout pointing at Justification.  
6. **Signal Spine stays on the underlying Market.** TS entry/pyramid/exit and Working Stop geometry are unchanged by Plan A vs Plan B. Enter remains enter.

### Mode C instance (first lock, 2026-09-19)

7. Under Mode C `leap_fulfillment=all`, **Plan A** = ATM long-dated LEAP from IBKR-eval chain (paper fulfill).  
8. **Plan B** = **stock / underlying** at methodology **`signal_share_units`** when LEAP is untradeable: e.g. `no_expiry_ge_min`, empty/thin chain, `no_atm_leap`, `no_candidates`, zero contracts after floor(`signal_share_units`/100).  
9. Confirm form: `fulfillment_type=stock`, units = `signal_share_units`, stock ATR/stop suggestion retained; LEAP-refuse `units: 0` must not win over `signal_share_units`.  
10. **Still Human-Gated.** Plan B is Desk Confirm on paper — never Desk-Send, never silent autofill into real.  
11. **ADR-017 unchanged.** Mode C paper fulfill never IBKR-binds; live OPT Model B remains separate. Future Plan A/B pairs (non-LEAP) need their own ticket; they inherit this ADR’s general law.

## Alternatives considered

| Alt | Why not |
|-----|---------|
| **Hard refuse entry when Plan A untradeable** | Blocks valid methodology size; treats packaging failure as signal failure |
| **Silent stock fallback including auth failures** | Hides session problems; violates fail-closed session truth |
| **Force+note only (no Plan B fields / Justification)** | No auditable Plan A/B story; operator improvisation |
| **Collapse Mode C into ADR-017 Desk-Send Model B** | Mode C is paper-eval; must not IBKR-bind fulfill |
| **Force 1 LEAP contract when shares &lt; 100** | Changes risk vs `signal_share_units`; not this ADR |

## Consequences

### Positive

- Untradeable LEAP is a **packaging branch**, not a dead desk.  
- Audit trail (Justification + `fulfillment_plan_a/b`) for DAR / Forensics.  
- Aligns Mode C paper with dual-spine law: signal size stays share units; booked capital follows chosen packaging.  
- Keeps auth/session as hard stops (WEV attention / Initiate still meaningful).

### Negative / residual

- Drafts minted before Plan B code may need one-time repair (units / `debit_credit` / plan_b fields) until emit paths stamp correctly.  
- Code vocabulary drift (`zero_contracts` vs `zero_contracts_floor`) until packaging and resolver share one untradeable set.  
- WUT lab may still refuse LEAP when contracts floor to 0 — **parity with this ADR is a separate decision**, not implied.

### Risks mitigated

- Units=0 confirm with nowhere to go.  
- Spine mislabeling enter as exit.  
- Silent stock on auth failure.  
- Confusing Mode C paper with ADR-017 live OPT Send.

## Smoke (when fully implemented)

- Untradeable LEAP draft → workflow 200, Justification five beats, form Units = `signal_share_units`, fulfillment stock, Plan B callout, spine **enter**.  
- Auth failure → no Plan B fields; hard stop messaging.  
- Confirm Plan B → journal booked as stock at share units; Book Market remains underlying.

## Related

- Business rules: `docs/business-context/mode-c-leap-plan-a-plan-b.md`  
- Tickets: `2026-09-18-mode-c-leap-preferred-underlying-fallback.md`, `2026-09-18-wv2-workflow-fulfillment-justification.md`  
- Evidence: Orange #1576 / #1941 / SMH; Indigo #1583 / #1946 / BITQ  
- Session / QA: 2026-09-19 CoS pull of Wv2 #7 + form QA

## Addendum — 2026-09-19 (operator)

Plan A is **whatever the TS / Fulfillment Packaging Policy prefers**. Assuming that preference is LEAPs (Mode C), Plan B is the **fallback enter** with suboptimal fulfillment (underlying/stock). Same law later for other Plan A shapes.

## Addendum — 2026-09-19 (`standard_call` packaging rung)

**Does not reopen ADR-017** (Model B OCC/conid timing, no silent re-ATM, OPT intent requires explicit conid).

A listed **standard long call** (DTE in `[standard.min_dte, leap_min_dte)`) is a **Fulfillment Packaging Policy** rung under this ADR’s general law — not a new Trading Strategy and not a free-floating OMS auto-stock.

1. **Plan A** = first entry in OP `packaging_preference` (e.g. `[leap, standard_call, stock]` or pinned `[standard_call]`).
2. **Plan B** = next **tradeable** entry when Plan A is untradeable (not auth). Justification still mandatory: what Plan A was, why it failed, what Plan B is.
3. **Mode C default (superseded 2026-09-20):** empty policy + `leap_fulfillment=all` now derives `[leap, standard_call, stock]` — see addendum below.
4. **`allow_equity_fallback: false`** ignores a later stock rung: after the last call rung fails → **clean refuse**, no silent stock, no units=0 LEAP cosplay.
5. Call selection (LEAP + `standard_call`) shares one selector; stock is policy, not a side door inside the call picker. Signal Spine / Working Stop stay on the underlying.
6. Standard-call lifecycle knobs (`flatten_below_dte`, optional `roll_window_dte`) are packaging time-handling. Default **do not auto-exercise**; HITL if intrinsic near expiry. Language: avoid worthless expiry and unintended exercise — do not say “assignment” for long calls.
7. Protective stop on the packaged call remains HITL sell-to-close (ADR-013 / leap-proxy law). No silent option STP.

Design note: [`docs/analysis/2026-09-19-standard-call-packaging-rung.md`](../analysis/2026-09-19-standard-call-packaging-rung.md). Ticket: `2026-09-19-standard-call-fulfillment-packaging-rung.md`.

## Addendum — 2026-09-20 (operator lock: Plan A/B/C + Mode C is paper)

1. **LEAP-fulfillment recipe** (`leap_fulfillment=all`, empty policy): Plan A = **LEAP**, Plan B = **standard long call** (no covered puts until the operator says), Plan C = **underlying** at `signal_share_units`. Derived `packaging_preference: [leap, standard_call, stock]`.
2. **Stock-only recipe** (`leap_fulfillment` not `all`): Plan A **is** the underlying — the same instrument as Plan C on the LEAP tree. No extra-modal ladder.
3. **Mode C** is a **testing strategy**: paper Operational Portfolios, fake cash, real signals — to validate workflow, integration, technical implementation, and fulfillment. It is **never** real-capital trading except as a gate for the operator to evaluate those issues.
4. **Winston Unit Test (WUT)** Plan-B / standard-call parity is a fast follow. WUT may keep Black–Scholes as a **lab** mark; Winston v2 never uses Black–Scholes when listed Client Portal Gateway data exists (or is empty — then untradeable, not synthesized).
5. Lane 2 Interactive Brokers option Desk-Send / Session Order Slate of DAY option orders is **not** this ADR slice. TWS is out of scope; Client Portal Web API only.

## Addendum — 2026-09-21 (operator lock: furthest expiry, cash not haircut)

On this extra-modal thread, listed calls exist to **cut cash outlay** versus buying the share signal, while still participating in the trend. They are not a risk substitute and not a risk augment.

1. **Furthest listed expiry** in the rung window wins. Plan A LEAP: furthest month with DTE ≥ `leap_min_dte` (365). Plan B standard long call: furthest month with DTE in `[min_dte, leap_min_dte)`. Do not walk the nearest month. Do not cap standard-call `max_dte` at 120 — that left a gap (e.g. Feb 2027 at ~151d on SEF).
2. **Contract count** is `floor(signal_share_units / 100)` on both call rungs (`risk_mult` 1.0). Do not apply a 0.6 standard-call haircut because the listed call is shorter than a LEAP — pick more tenor instead. Cash reduction is premium × 100 × contracts versus share notional, not fewer contracts.
3. Strike pick inside that furthest month stays ATM / delta-band / quote-quality. Working Stop stays on the underlying.
