# Winston bot / CLI / AI-DLC operating contract

**Status:** Active desk law (process)  
**Date:** 2026-09-21  
**Owner:** Chief of Staff (orchestrate); Operator (approve discards / lane exceptions)  
**Related:** [`sawtooth-host-ops-dod.md`](sawtooth-host-ops-dod.md); [`../tickets/2026-09-21-probe-before-promote.md`](../tickets/2026-09-21-probe-before-promote.md); ecosystem `AGENTS.md`

Chat is not the record. Git + tickets are the spine.

## Mental model

| Role | Who | Does | Does not |
|------|-----|------|----------|
| **Act** | CoS, Sawtooth Ops, PBR Ops, Forensics | Stamp / probe / queue / host DoD, autopsies, smell-tests, promote gates | Own the durable narrative; invent a second trail; default-code Winston |
| **Code** | **Grok CLI** (default for planned work); **Winston Dev** only for unplanned small/hotfix/issues | Implement against ticket (± plan); push `main`; in-band wrap | Parallel bot + CLI on the same ticket; PR theater as desk default |
| **Remember** | AI-DLC in `ecosystem/` | Plans, tickets, analysis, session reports, ADRs | Out-of-band Scribe as primary wrap owner |
| **Judge** | Jev | Screen / verify / System One checkpoints / overnight compact | Replace tickets or host probes |

## Formal AI-DLC lanes

### Lane A — Planned (new feature or sufficient complexity)

Always:

1. **Ticket** first (INDEX row) before a second bot or any coding session.
2. **Plan** in `ecosystem/plans/` (or ticket-linked plan section) — grill-with-docs against CONTEXT / ADRs / business-context.
3. **Jev System One harness** written into the plan (state + atomic checkpoints + pass rules) — see jev-desk-guardrails (yes/no or noul questions on observable state), e.g. heat intent vs hash, peak open vs portfolio cap, packaging floor contracts, Edge_R present.
4. **Implementer = Grok CLI only.** Winston Dev is **not** used on Lane A.
5. Checkpoints run at plan gates (before code, after implement, before host promote / pull DoD). Fail closed → stop and update ticket.

### Lane B — Unplanned small (hotfix / `docs/issues/` / sufficiently small)

1. Still open or update a **ticket** (or promote a ready issue → ticket) before a second actor.
2. Ticket must list a short **System One harness** (state + checks): what Jev or probe must answer before “done.” Skip only for trivial doc renames.
3. **Winston Dev may implement** Lane B. Grok CLI may also implement Lane B. Never both on the same ticket unless Operator splits scope in writing.
4. No full plan required; still wrap in-band with the coding commit stream.

### Fan-out cap

Smell-test: CoS alone → ticket (+ optional Forensics **evidence only** into `docs/analysis/`).  
Second bot only after the ticket exists.  
Never CoS + Forensics + Dev + Scribe on one smell in the same burst.

## How CoS works with Grok CLI (not paste-only)

Tickets are the **contract**, not the only interface.

### Preferred: shared watchable Grok CLI session on sawtooth

1. CoS files/updates the ticket (± Lane A plan) and writes a **`## CLI seed`** block (cwd, monoliths, acceptance, System One checkpoints, “push `main`, no PR, wrap in this stream”).
2. Operator opens a visible terminal on **sawtooth-ai** in the seed cwd and starts Grok Build TUI, e.g.  
   `cd <cwd> && grok "$(sed -n '/^## CLI seed/,/^## /p' path/to/ticket.md | …)"`  
   or paste the seed once into an interactive `grok` session.
3. **Both watch that TUI** (Operator at the keyboard; CoS follows the session in chat and can feed follow-ups the Operator pastes, or reads `grok export` / session transcript after beats).
4. Session owns implement + wrap + push. Host pull / probe remains Sawtooth Ops or CoS per host DoD.

### Fallback: ticket paste

If no shared pane is available, Operator (or CoS via instruction) pastes the CLI seed into a solo `grok` session. Same ticket remains source of truth.

### Not default

- Cursor Cloud Agent / private worker (PR-oriented, workers often offline) — only when Operator asks.
- CoS inventing Winston patches in chat.
- Scribe opening a parallel wrap commit after the fact.

## Delivery: push / pull (no PR default)

1. Implement on `main` (or short-lived local worktree merged locally) → **push**.
2. Sawtooth Ops / CoS **host-verify**: compose pull, container SHA, probe-before-promote when promote language is at stake.
3. Review = grill-with-docs + Jev verify + host smoke — not GitHub PR review theater.  
   External PRs only when Operator wants an audit trail.

## Wrap (in-band)

Whoever closes the coding session writes the session report and commits it **with** the code/docs push.  
Scribe is **optional hygiene** (nag if ticket has no report path) — not primary wrap owner.

## Overnight ticket triage (Loop)

Overnight Loop evaluates ripe INDEX tickets (and linked issues):

- Propose **discard** (stale / superseded / duplicate) — **Operator approval required in the morning** before archive.
- Propose **prioritize** (P0/P1 bump, next CLI seed, Lane A plan kickoff).
- Jev **screen** claims; attach compact notes under `docs/analysis/` or ticket updates.  
Morning Loop surfaces those proposals in one short block.

## Jev chokepoints (standing)

Full guardrails: [`jev-desk-guardrails.md`](jev-desk-guardrails.md) (API vs `jevctl`, harness shape, anti-oversell).

1. **Screen** — new/updated ticket text; overnight research claims.
2. **Verify** — autopsy conclusions; promote language.
3. **System One** — plan/ticket checkpoints; probe-before-promote state questions.
4. **Compact** — overnight research → ticket deltas.

## Role rewrite

| Actor | Mandate |
|-------|---------|
| Chief of Staff | Orchestrate; open tickets before fan-out; write CLI seeds; host fallback; Jev/probe gates; overnight triage proposals |
| Sawtooth Ops | Host stamps / pulls / DoD |
| Forensics / PBR Ops | Evidence → `docs/analysis/`; link ticket; do not start Dev |
| Winston Dev | **Lane B only** (hotfix / issues / small) unless Operator explicitly expands |
| Grok CLI | **Default implementer**; sole Lane A coder; in-band wrap |
| Scribe | Optional nag only |
| Jev | Judge at chokepoints |

## Definition of Done for this contract

- [x] Filed under business-context
- [ ] Winston AI-DLC / filing skills patched to match
- [ ] Overnight + morning Loop prompts include ticket triage
- [ ] Next planned Winston change uses Lane A with CLI seed + System One checkpoints
