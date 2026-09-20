# Mode C — LEAP Plan A / Plan B fulfillment

**Type:** Domain / fulfillment packaging (Mode C paper)  
**Status:** Desk lock 2026-09-19 — **Accepted as [ADR-018](../adr/ADR-018-mode-c-leap-plan-a-plan-b.md)**  
**Applies to:** Operational Portfolios with `leap_fulfillment=all` (LEAP-preferred Mode C paper); Wv2 desk workflow confirm path  
**Does not apply to:** Auth/session/CPGW failures (hard stop); IBKR-bound Desk-Send / ADR-017 Model B live OPT (separate law)  
**Glossary:** Plan A, Plan B, LEAP-preferred, untradeable, Justification, Signal Spine, Booked Capital Spine, `signal_share_units`  
**Related:** [`leap-extra-modal-proxy.md`](leap-extra-modal-proxy.md); [`human-gated-desk-and-fulfillment.md`](human-gated-desk-and-fulfillment.md); plan [`../../plans/wv2-bg-ibkr-leap-fulfillment.md`](../../plans/wv2-bg-ibkr-leap-fulfillment.md); tickets `2026-09-18-mode-c-leap-preferred-underlying-fallback.md`, `2026-09-18-wv2-workflow-fulfillment-justification.md`; Wv2 PR #7 (behavior + Justification), follow-ups #8 (Justification ERB), Plan B form prefill (in flight)

## One-sentence law

**Plan A is whatever preferred packaging the TS / Fulfillment Packaging Policy says; when that packaging is untradeable (not auth-blocked), Plan B lets the desk still enter with suboptimal fulfillment. Mode C’s first instance: LEAP → underlying at `signal_share_units`, with Justification; confirm form is Plan B by default.**

## Definitions

| Term | Meaning |
|------|---------|
| **Plan A** | Preferred fulfillment packaging per TS / OP **Fulfillment Packaging Policy** (not hard-coded to LEAPs). Mode C instance: ATM long-dated LEAP under `leap_fulfillment=all`. |
| **Plan B** | **Suboptimal but valid** packaging so we still **enter the market** when Plan A is untradeable. Mode C default instance: **stock / underlying** at **`signal_share_units`**. When `packaging_preference` includes `standard_call`, that listed-call rung may be Plan A or Plan B (ADR-018 addendum 2026-09-19). |
| **Untradeable** | LEAP cannot be packaged honestly from the chain / affordability floor — e.g. `no_expiry_ge_min`, empty/thin chain, `no_atm_leap`, `no_candidates`, **zero contracts after floor(`signal_share_units`/100)** (codes may appear as `zero_contracts` or `zero_contracts_floor`). |
| **Hard stop** | Auth / session / CPGW / binding failures — **no** silent stock fallback. Operator must restore session (Initiate / login) before packaging. |
| **Justification** | Desk workflow panel: Signal → Risk units → Fulfillment preference → Why Plan A won’t work → Why Plan B will. |

## Rules (non-negotiable)

1. **Signal stays on the underlying.** TS entry/pyramid/exit and Working Stop geometry are unchanged by Plan A vs Plan B. Packaging does not invent a second signal. See [`leap-extra-modal-proxy.md`](leap-extra-modal-proxy.md).
2. **Plan A is preference, not a hard refuse.** Untradeable Plan A **must not** leave the operator with nowhere to go — Plan B is an explicit suboptimal enter, not a failed signal.
3. **Plan B size = `signal_share_units`.** Never confirm 0 shares because LEAP floor’d to 0 contracts. Task/journal meta that stamped `units: 0` for LEAP refuse must not win over `signal_share_units` on the confirm form.
4. **Confirm form is Plan B when Plan A failed untradeable.** Prefill: `fulfillment_type=stock`, units = `signal_share_units`, ATR/stop suggestion for **stock enter** kept. Callout: Plan A not adopted (see Justification); this is Plan B.
5. **Justification is mandatory when Plan B is active** (or any `leap_failure_code` is present). Five beats; no ad-hoc force+note as the only path.
6. **Auth remains a hard stop.** `auth_failed` / session yield / CPGW down → no Plan B auto-path.
7. **Spine truth.** Enter tasks show **enter** (not exit). Do not infer exit solely from `debit_credit=credit` on a draft enter — packaging mistakes must not relabel the signal.
8. **Human-gated.** Plan B is still Desk Confirm on paper; never Desk-Send; never silent autofill into real.

## Evidence cases (canon)

| Case | Market / OP | Plan A fail | Plan B |
|------|-------------|-------------|--------|
| BITQ / Indigo evolved #1583 | journal #1946 | `no_expiry_ge_min` | stock @ `signal_share_units` (e.g. 247) |
| SMH / Orange #1576 | journal #1941 / task #1794 | `zero_contracts` (17 shares → 0 LEAP contracts) | stock @ **17** |

## Implementation map (Wv2)

| Concern | Where |
|---------|--------|
| Classify untradeable vs hard stop | `LeapCandidateResolver` (`untradeable:` flag) |
| Persist Plan B on confirm path | `DeskWorkflowsController#related_details` (`fulfillment_plan_a/b`, reason, `signal_share_units`) |
| Justification UI | `desk_workflows/_justification.html.erb` |
| Form prefill + Plan B callout | Desk workflow show / handoff / `form_fields` (prefer `signal_share_units` when Plan B / leap failure + units 0) — **product fix in flight 2026-09-19** |
| WUT lab parallel | Separate: WUT historically refuses LEAP when contracts floor to 0; Mode C live desk law above is Wv2 paper — do not silently assume WUT already Plan-B’s |

## Anti-patterns

- Leaving Units=0 on the confirm form while “proposed N” shows underneath.
- Spine labeling an enter as **exit** because draft `debit_credit` was wrong.
- Treating Justification as enough while the form still looks like a blocked LEAP.
- Silent stock fallback on auth failure.
- Rewriting Book / DA / PCS onto the OCC symbol when Plan A succeeds.

## Open / follow-ups

- Align packaging/daily_analysis emit codes (`zero_contracts` vs `zero_contracts_floor`) so resolver and drafts share one untradeable vocabulary.
- ~~Promote to ADR~~ → **ADR-018 Accepted** (2026-09-19). ADR-017 live packaging unchanged.
- WUT: decide whether lab PBRs should Plan-B to shares when LEAP floor is 0 (today they refuse) — separate ticket if John wants parity.

## Change log

| Date | Change |
|------|--------|
| 2026-09-19 | Initial desk lock from QA on #1941 + tickets A/B + PR #7. |
| 2026-09-19 | Promoted to **ADR-018** (Accepted). |
| 2026-09-19 | Operator: Plan A = TS/policy preference; Plan B = suboptimal enter (LEAP→stock is Mode C instance). |
