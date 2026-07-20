# Ticket: Loop engineering + Evolution Mode (return to design)

**Status:** Proposed  
**Date:** 2026-07-19 (updated 2026-07-20)  
**Priority:** Low (roadmap capture — do not start Evolution until V1–V2 A/B is designed/run)  
**Plan:** `ecosystem/plans/loop-engineering-and-evolution-mode.md`  
**Source:** Design session mapping [@RohOnChain loop-engineering](https://x.com/RohOnChain/status/2069056530960490835) onto Winston/DAR/Wv2

## Problem

We are close to "architect the loop" (Cromwell skills, cron, MCP, DAR, paper journals, fingerprint succession) but missing an explicit product path for:

1. Completing the Roan six-piece loop on **existing** paper ops (STATE, maker–checker verifier, lesson write-back).
2. **Closed-system verification:** one paper OP Winston alone trades (auto paper fills) vs a HITL twin with the same frozen fingerprint — so we can measure whether loops improve *realized* returns before claiming Evolution Mode value.
3. A later **Evolution Mode**: set-aside paper OPs + controlled TS modification via successor fingerprints (not silent Engaged mutation), with AI verify → paper fills → scorecard → mutation proposals.

Without a parked plan + ticket, future sessions will re-derive this from the tweet or invent a black-box autotrader that violates ADR-006 / `winston-plus-llm` non-goals.

## Scope (when we return)

Work from the plan's phases; **do not jump to L3+ Evolution**. **Prefer V1–V2 before Evolution.**

| Phase | Work | Done when |
|-------|------|-----------|
| **L0** | Plan accepted; open decisions resolved or deferred in writing | Principal marks plan Ready / Blocked with notes |
| **V1** | Closed **Auto** paper OP + **auto-confirm** DAR drafts (frozen TS; paper only; kill switch + audit) | One OP fills without human; never real |
| **V2** | **HITL twin** (same books/fingerprint/capital, different seed) + equity_compare scorecard | Pre-registered metrics after ≥40 closed trades or ≥60 sessions |
| **L1** | Daily STATE discipline + signal verifier skill (shadow on HITL, or later arm B2) | Skill + STATE template; human still confirms HITL |
| **L2** | Tag `ops_lane=evolution` (or equivalent) + scorecard on 1–2 set-aside paper OPs | Metrics visible; no auto-mutate |
| **L3+** | Mutation Proposal schema, successor apply, optional broader auto-paper, WUT micro-backtest, promote path | Separate tickets spawned from plan |

**Non-goals (always):**

- LLM invents entry indicators or replaces DAR signal math
- In-place edit of Engaged OP Books/TS
- Capital Activation / real fills from Auto or evolution equity
- Open-ended "mutate until Sharpe > X" on live capital
- Confounding auto-execution with methodology mutation in the first A/B

## Open decisions (resolve at L0 / before V1)

See plan § Open decisions — including:

- Auto paper-confirm on **one closed OP only** (recommended) vs global
- Auto **price policy** (current paper convention vs next open) — freeze before V1
- Champion fingerprint + capital for HITL/Auto twins
- Evolution as paper subtype vs third lane
- Micro-backtest home (WUT vs Wv2)
- Mutation approver; L1 shadow before EP class

## Acceptance (this ticket)

- [x] Design plan filed at `ecosystem/plans/loop-engineering-and-evolution-mode.md`
- [x] Backlog ticket exists with status Proposed and plan link
- [x] Closed-system Auto vs HITL verification section synced into plan (2026-07-20)
- [ ] Principal reviewed plan and set next phase (**V1** vs park longer)
- [ ] Cross-link from `plans/winston-plus-llm.md` (Phase 2–4 alignment) when next LLM roadmap edit happens
- [ ] When **V1** starts: spawn implementation ticket (auto_paper_confirm flag + post-DAR job); close or re-scope this umbrella ticket
- [ ] When L1 starts: spawn implementation tickets (verifier skill, STATE template)

## See also

- `ecosystem/plans/loop-engineering-and-evolution-mode.md` — full design (incl. § Verification first)
- `ecosystem/plans/winston-plus-llm.md` — Phases 1–4 (notes → ranking → Cromwell workflow → self-improvement)
- `ecosystem/docs/adr/ADR-006-operational-portfolio-lineage-and-lifecycle.md` — fingerprint / successor law
- `ecosystem/docs/adr/ADR-008-confirmational-entry-and-risk-scale.md` — lab confirm path twin to evolution
- `ecosystem/CONTEXT.md` — optional paper autofill as later explicit decision; human-gated fills default
- `ecosystem/ai/skills/winston-confirmation-loop/SKILL.md` — current human maker–checker surface
- `ecosystem/docs/tickets/2026-07-15-winston-model-specialization-plan.md` — related LLM roadmap parking
- `ecosystem/docs/session-reports/2026-07-20-1624-loop-engineering-evolution-mode.md` — this design session
