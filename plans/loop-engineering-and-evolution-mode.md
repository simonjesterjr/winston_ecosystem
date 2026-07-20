# Plan: Loop Engineering for Winston + Evolution Mode (DAR/Wv2)

**Status:** Proposed design (not scheduled for build)  
**Date:** 2026-07-19 (updated 2026-07-20)  
**Type:** Design exploration / long-horizon roadmap slice  
**Source:** [@RohOnChain loop-engineering article](https://x.com/RohOnChain/status/2069056530960490835) (2026-06-22)  
**Ticket:** `docs/tickets/2026-07-19-loop-engineering-evolution-mode.md`  
**Maps to:** ADR-006, ADR-008, `plans/winston-plus-llm.md`, Cromwell skills, paper-first ops  

---

## Source idea (what the post claims)

Roan’s thesis: stop being *inside* the prompt loop; become the architect who designs **loops** that prompt, verify, decide next steps, and persist memory after the laptop closes.

**Six pieces of every working loop**

| # | Piece | Role |
|---|--------|------|
| 1 | Automation | Heartbeat (`/loop` cadence vs `/goal` until condition) |
| 2 | Skill | Durable procedure manual (SKILL.md) so runs don’t start from zero |
| 3 | State file | Memory that survives agent amnesia (STATE.md / PROGRESS.md; also audit log) |
| 4 | Verifier | Separate agent/model grades work (maker–checker) |
| 5 | Worktrees | Isolation so parallel agents don’t collide |
| 6 | Connectors | MCP/API hands into real systems |

**Five quant stages (each a sub-loop):** data → signal gen → verification → execution → risk monitoring. Lessons write back into skills/state so the system “self-improves.”

**Hard stop rule:** stop conditions must be checkable by something other than the agent’s claim (“Sharpe > 1.5 over last 30 trades,” not “I think we’re done”).

**Critique we keep in mind:** pure LLM-generated alpha is not what Winston is; Roan’s framing is strongest as **orchestration + verification + memory**, not as “Claude invents signals that print money.”

---

## Where Winston already is (honest map)

Winston is **closer than retail quant stacks** on several pieces — and deliberately **farther** on full auto-execution (by design: ADR-006 “observation post that tasks humans”).

| Roan piece | Winston today | Gap |
|------------|---------------|-----|
| Automation | DM download jobs; Sidekiq; Cromwell cron (`schedule/manifest.yaml`); DAR daily path | Goal-oriented loops rare; mostly fixed cadence |
| Skills | Rich Cromwell skill set (`winston-daily-ops`, `winston-confirmation-loop`, lifecycle, audit, …) | Skills document **ops**, not yet **signal-science lessons** that compound after losses |
| State | Journals, MCP audit JSONL, MEMORY templates, session reports, equity series | No single per-campaign STATE with bounded size + debugability (~400 lines advice) |
| Verifier | Human is checker; `/adversary` for code; deterministic risk rules | No first-class **signal verifier agent** separate from DAR generator |
| Isolation | Fingerprint + OP series (auto-fork); paper vs real bands; worktrees for **code** agents | No named **evolution lane** distinct from paper observation |
| Connectors | MCP tools (Wv2/WUT/DM), Telegram, journals | Strong; no broker auto-fill (intentional) |

**Deterministic core (non-negotiable):** signal math stays in Ruby StrategyRegistry / risk evaluators. LLM augments, grades, proposes, explains — it does **not** become the entry engine (`winston-plus-llm` non-goals). That is a feature relative to Roan’s “agent generates alpha” framing.

**Fingerprint law (ADR-006):** a different methodology is a **different fingerprint** → successor OP, never silent in-place edit of an Engaged series. Any “modify TS in a loop” **must** be successor/fork, not mutation.

---

## 1) How to leverage the idea in Winston (near-term, no new mode)

These are high leverage **without** inventing a new portfolio class. They complete Roan’s six pieces on the infrastructure we already have.

### 1A. Make the daily ops loop explicit (architect, don’t re-prompt)

Codify one **Cromwell daily loop** as a skill + state machine, not ad-hoc chat:

```
DM ready? → sync if stale → DAR Active band → pending list →
  (optional) AI draft notes / risk commentary →
  human confirm fills → status → write lessons to MEMORY/audit
```

- **Automation:** already cron; add explicit **stop/skip conditions** (no trading day, missing coverage, DAR failed) so the loop doesn’t “complete” on partial work.
- **State:** per trading day `STATE-YYYY-MM-DD.md` (or structured PG row + markdown export) with: portfolios touched, signals taken/passed, confirms, errors, open questions. Bound size; treat as audit when a paper series loses.
- **Verifier (light):** separate skill/prompt path for “should we **take** this draft?” that only sees: signal facts, open risk, recent similar journals — **not** the narrative the generator would invent. Human remains final fill gate.

### 1B. Maker–checker on *decisions*, not on signal math

| Maker | Checker | Outcome |
|-------|---------|---------|
| DAR + PositionSizer (deterministic) | AI verifier + human | Confirm / size-down / skip / pass-with-reason |
| AI proposes journal note | Schema + human glance | Stored draft notes only |
| AI proposes config tweak | WUT backtest gate + human | New fingerprint export or reject |

Aligns with Jane Street-style separation and with existing confirmation-loop skill.

### 1C. Self-improving *skills*, not self-rewriting strategies (first)

After material paper/real outcomes (stop-out, skipped breakout that ran, pyramid that failed):

1. Agent appends a **Lesson** to a living skill or `ecosystem/ai/memory` section (capped, reviewed).
2. Lesson is **operator doctrine** (“don’t pyramid energy names into FOMC week without…”) not a free rewrite of ATR multipliers.
3. Second-time ritual → promote to skill (existing workspace discipline).

This is Roan’s “every loss writes a rule” without violating fingerprint immutability.

### 1D. Parallel isolation = Active bands + inactive archive

We already have paper band / real band / inactive. Treat **each fingerprint series as a worktree analog**. Risk monitor is parallel: attention bands + kill hygiene (close paper, force-flatten real) — not a second agent inventing exits outside VolExit rules.

### 1E. Goal loops in the lab (WUT), cadence loops in ops (Wv2)

| Flavor | Where | Example stop condition |
|--------|--------|-------------------------|
| `/goal` | WUT PBR / confirm matrices | Sharpe / DD / trade-count gates on fixed window; cell matrix complete |
| `/loop` | Wv2 DAR + Cromwell | Every RTH day after data ready |

Do **not** put open-ended “keep mutating TS until Sharpe > X” on live capital.

### 1F. Wire to existing roadmap

| Phase in `winston-plus-llm` | Roan alignment |
|-----------------------------|----------------|
| Phase 1 notes / explain | Skill growth + state narrative |
| Phase 2 signal ranking + safe config suggestion | Verifier + propose-only |
| Phase 3 Cromwell workflow | Full daily loop owner |
| Phase 4 self-improvement | Only via WUT backtest + human promote |

**Recommended order of leverage:** 1A daily STATE + stop conditions → 1B verifier skill for pending journals → 1C lesson write-back → later 1E goal loops for lab campaigns.

---

## 2) Evolution Mode: set-aside portfolios + controlled TS modification loop

### Product intent

A **third attention lane** (alongside Active real and Active paper observation):

> **Evolution lane:** paper-only series whose purpose is *not* regime observation of a frozen recipe, but *controlled methodology search* under live market path — signals from DAR, paper fills, AI-assisted validation of outcomes, then **successor fingerprints** when evidence supports a change.

This is **paper science in ops time**, not capital-at-risk automation, and not silent rewrites of Engaged OPs.

### Glossary candidates (for later CONTEXT.md if adopted)

| Term | Meaning |
|------|---------|
| **Evolution Portfolio (EP)** | Wv2 OP with `execution_mode=paper` and a new flag e.g. `ops_lane: evolution` (or `purpose: evolution`). Set-aside capital; never Capital Activation path without explicit exit from evolution + trade-ready provenance. |
| **Evolution TradingStrategy (ETS)** | Fingerprinted methodology marked `class: evolution` / `export_kind` sibling (e.g. `evolution_candidate`). Same StrategyRegistry primitives only — **no free-form LLM strategy code**. |
| **Mutation Proposal** | Structured delta (add confirmational strategy, change ladder step, tighten ATR stop mult, change max_markets, etc.) proposed by AI or human after N paper outcomes. |
| **Evolution Cycle** | One full: DAR signals → paper confirm policy → hold/exit outcomes → scorecard → propose/reject → optional successor fork. |
| **Promotion out of evolution** | EP series closed or frozen; winning ETS re-exported via WUT validation gates as Observation or Trade-Ready — never jump to real on EP equity alone. |

### What it looks like end-to-end

```
┌─────────────────────────────────────────────────────────────────┐
│  EVOLUTION LOOP (paper only, set-aside OP band)                  │
│                                                                   │
│  1. HEARTBEAT (cadence)                                           │
│     DM coverage OK → DAR for Active evolution OPs only             │
│                                                                   │
│  2. SIGNAL (maker — deterministic)                                │
│     Same DAR engines as normal paper; journals draft as today     │
│                                                                   │
│  3. VERIFY (checker — AI + rules)                                 │
│     Separate prompt/skill: regime notes, correlation, recent      │
│     lessons, open risk. Output: TAKE | SIZE_DOWN | SKIP | HOLD    │
│     + structured reason. Never invents new entry indicators.      │
│                                                                   │
│  4. PAPER EXECUTE (policy)                                        │
│     Modes: human-gated (v1) | auto-paper-confirm if TAKE (v2)     │
│     Auto only on evolution lane; never real. Journals still SoT.  │
│                                                                   │
│  5. SCORECARD (objective stops — not agent opinion)               │
│     Rolling N trades / M days: hit rate, expectancy, max DD,      │
│     pass rate, confirm-override rate, time-in-trade vs plan.      │
│                                                                   │
│  6. MUTATION PROPOSAL (AI or human)                               │
│     Delta within approved knobs only (StrategyRegistry params,    │
│     confirm set, ladder, risk %, max_markets, books add/drop).    │
│     Requires evidence refs (journal ids, scorecard cells).        │
│                                                                   │
│  7. CONTROLLED APPLY (fingerprint law)                            │
│     Never mutate Engaged EP in place.                             │
│     Path: soft-close or end-signals A → open successor A′ with    │
│     new ETS fingerprint (lineage: parent_fingerprint + delta).    │
│     Optional: WUT micro-backtest of delta on same books first.    │
│                                                                   │
│  8. LESSON WRITE-BACK                                             │
│     STATE + skill appendix; rejected proposals also recorded.      │
│                                                                   │
│  9. EXIT GATES                                                    │
│     Kill: DD > X, proposal thrash > Y/week, N consecutive loses.  │
│     Promote: scorecard passes observation thresholds → freeze ETS │
│     → WUT re-validate → Observation/Trade-Ready handoff.          │
└─────────────────────────────────────────────────────────────────┘
```

### Separation from existing paper OPs

| | Observation paper (today) | Evolution paper (proposed) |
|--|---------------------------|----------------------------|
| Intent | Regime sample of **frozen** fingerprint | **Search** under live path |
| TS change | Successor only for deliberate rebalance | Successor is the *point* of the loop |
| Auto-confirm | No (human) | Optional later, paper-only |
| Attention | Active paper band | Separate band / tag so DAR desk doesn’t mix |
| Real capital | Capital Activation after trade-ready | **Forbidden** from EP equity path |
| AI role | Explain / confirm assist | Verifier + mutation proposer |

### “New class of TS” — precise meaning

Not a new Ruby strategy language. Prefer:

1. **Same primitives** (Breakout*, VolExit*, confirmational set, one_way_dynamic ladders, etc.).
2. **Provenance metadata:** `lineage.parent_fingerprint`, `evolution_generation`, `mutation_summary`, `scorecard_snapshot_id`.
3. **Allowed knob catalog** (closed set) for AI proposals — anything outside catalog is rejected without WUT code change.
4. Optional later: new registry strategies only via normal lab code path (human PR), never LLM-authored code in the loop.

### Controlled loop guardrails (non-negotiable)

1. **Fingerprint immutability** — mutations = successor A′ only (ADR-006).
2. **Paper-only** until normal promotion path.
3. **Human gates by phase:**
   - Phase E0: all confirms + all mutations human-approved.
   - Phase E1: auto paper-confirm on TAKE when scorecard green; mutations still human.
   - Phase E2: auto-apply mutation only if WUT micro-backtest gate passes + human weekly review.
4. **Checkable stop conditions** (Roan’s warning): kill/promote metrics in PG, not “agent says done.”
5. **No silent Books churn** — book adds/drops are shape rebalance with successor + correlation flag (ADR-007).
6. **Attention hygiene** — evolution OPs do not steal Active real slots; mutex rules still apply per seed unless force.
7. **Audit** — every cycle writes STATE + MCP audit + proposal JSON; state is the debug log when money (paper) is lost.

### Cromwell / MCP surface (sketch)

**Skills**

- `winston-evolution-cycle` — daily: list evolution OPs → pending → verify → (confirm policy) → update STATE.
- `winston-evolution-propose` — after scorecard trigger: draft Mutation Proposal JSON.
- `winston-evolution-apply` — human says apply → successor fork via existing lifecycle tools (+ new MCP if needed).

**Possible new tools (later)**

- `wv2_list_evolution_portfolios`
- `wv2_get_evolution_scorecard`
- `wv2_propose_ts_mutation` (draft only)
- `wv2_apply_ts_mutation` (successor create; human token)
- WUT: `wut_micro_backtest_delta` for pre-apply gate

**State files**

- Per EP: `evolution/STATE-{seed}-{fp-short}.md` (rolling ~400 lines) + durable PG tables for scorecard/proposals.

### Fit with confirmational entry experiment (ADR-008)

Evolution mode is the **ops-time twin** of WUT confirm matrices:

- Lab: grid on historical path (PBR 78/80 style).
- Evolution: live path stress of one confirm/ladder recipe, then propose next delta (e.g. Penetration25 vs EMA20) with paper evidence.
- Winning generation still must re-enter WUT for full validation before Trade-Ready.

### What we deliberately do *not* build

- LLM invents new indicator formulas and deploys them to real books.
- In-place edit of Engaged OP methodology.
- Auto-fill real capital from evolution scorecards.
- Open-ended `/goal` that runs forever without DD/thrash kills.
- Replacing DAR with a chat model.

---

## Verification first: closed-system Auto vs HITL paper A/B

**Principal direction (2026-07-20):** before Evolution Mode or broad loop claims, run a **closed paper system** where Winston alone may trade one OP (loop + auto execution), and compare it to a **HITL** twin. Optional convenience: automate fills on the closed book so the loop is complete without desk latency.

This is the right experiment shape. It answers a cleaner question than “does AI invent alpha?”:

> Holding methodology fixed, does **closing the loop** (always take system signals, no human delay/skip) change realized paper equity vs **human-gated** fills?

`CONTEXT.md` already carves this out: *optional paper autofill is a later, explicit decision; not implied by draft creation.* Real capital stays human-gated.

### Twin portfolio design

| | **HITL control** | **Closed auto (treatment)** |
|--|------------------|-----------------------------|
| Intent | Today’s desk path | “Only Winston trades this” |
| Seed naming | e.g. `Blue HITL · {fp}` | e.g. `Blue Auto · {fp}` — **different seed_name** so Active mutex is clean without force |
| Books + TS fingerprint | Identical | Identical (same methodology) |
| Initial capital | Same CashEvent | Same CashEvent |
| Execution mode | `paper` | `paper` only (hard forbid real / Capital Activation) |
| Active | Yes (attention + DAR) | Yes (separate seed → dual Active OK) |
| Fills | Human confirm (Telegram / shell / MCP) | **Auto-confirm** DAR drafts under a fixed policy |
| TS mutation | None (frozen fingerprint) | **None in v1 of this experiment** — auto *execution* only, not evolution |
| AI role (optional later arm) | None, or shadow notes only | Optional arm B2: auto-confirm only if verifier says TAKE |

**Why freeze TS for the first A/B:** otherwise you confound “automation of fills” with “methodology search.” Evolution is a **second** experiment after Auto vs HITL is measured.

**Why separate seed names:** ADR-006 mutex is one Active per `seed_name` and per identical Books set (unless force). Identical Books + dual Active needs force and confuses attention hygiene. Prefer distinct seeds that still share books/fingerprint content so equity compare is fair.

### Auto fill policy (closed book only)

Keep the policy **boring and checkable** — no agent discretion on price inventing:

1. **Eligible journals only:** draft enter/exit/pyramid from DAR for the Auto OP; never ad-hoc free-form unless policy says so.  
2. **When:** after DAR completes for that OP (same Signal Date T).  
3. **Price:** use existing paper convention (signal / next-open rule as implemented today for paper confirms — do not invent a new pricing model in v1).  
4. **Units:** PositionSizer output; if zero units → log fail, do not invent size.  
5. **Kill switch:** OP flag `auto_paper_confirm=false` or global env; max daily confirms; halt on error rate.  
6. **Audit:** every auto-confirm writes journal notes + MCP/audit trail (`source: auto_paper_loop`).  
7. **Never:** real mode, Capital Activation, other OPs, or books outside the closed OP.

Optional **arm B2** (after B1 baseline): auto-confirm only on verifier TAKE; SKIP → Passed Signal with reason `verifier_skip` (not process miss). Compare B1 (always take) vs B2 (AI gate) vs HITL.

### What the A/B measures

Pre-register metrics (example — freeze before go-live):

| Metric | HITL | Auto | Notes |
|--------|------|------|-------|
| Terminal equity / return | | | Primary |
| Max DD | | | Risk |
| Trade count | | | HITL often fewer (skips/delay) |
| Process-miss rate | | | Auto should be ~0 on drafted signals |
| Mean R / expectancy | | | Quality of taken set |
| Confirm lag (signal → fill) | | | HITL latency cost |
| Equity path correlation | | | Same markets → high corr; gaps = behavior |

**Interpretation guide:**

- Auto **beats** HITL mainly via higher trade count / less lag → automation recovers *process* drag, not new alpha. Still valuable.  
- Auto **matches** HITL → loops don’t buy return; invest in lab recipes instead.  
- Auto **loses** → humans were adding positive discretion (or auto priced worse); do not expand auto.  
- B2 beats B1 → verifier has edge; invest in L1 verifier.  
- B2 loses to B1 → verifier destroys opportunity; keep AI out of the fill gate.

Use existing `equity_compare` / PortfolioEquitySeries tooling for side-by-side charts when available.

### Minimum run length

Not “until it looks good.” Pre-commit e.g.:

- **≥ 40 closed round-trips** on each arm, **or**  
- **≥ 60 trading days** with both Active,  

whichever comes first; then scorecard + optional holdout week. Kill early only on infra failure or DD circuit breaker (e.g. Auto DD > X% absolute).

### Scope vs full Evolution Mode

```
Phase V0  Design A/B (this section)
Phase V1  Closed Auto paper OP + auto-confirm service (no TS mutation)
Phase V2  HITL twin + equity_compare dashboard / report
Phase V3  Optional verifier-gated auto arm (B2)
Phase V4  Only if V1–V2 justify: Evolution (mutate via successor) on a *third* closed book
```

V1 is **much smaller** than Evolution Mode: one flag + Sidekiq/job after DAR + hard paper-only guardrails. That is the “for convenience, let trade executions happen with automation” path — and it is exactly the right convenience for a closed system.

### Explicit non-goals for the closed A/B

- No real broker, no real Capital Activation from Auto equity  
- No silent dual-use of the HITL OP for “sometimes auto”  
- No methodology mutation mid-experiment on either arm  
- No claiming “loops improve alpha” if the only gain is fill rate  

---

## Phased adoption (if product yes)

| Phase | Scope | Outcome |
|-------|--------|---------|
| **L0** | Design only (this doc) | Shared language; optional ADR draft |
| **V1–V2** | **Closed Auto vs HITL paper A/B** (frozen TS; auto paper fills) | Measured automation / process effect on returns |
| **L1** | Daily STATE + signal verifier skill (shadow or B2 arm) | Roan pieces 3–4 without new OP class |
| **L2** | Tag `ops_lane=evolution` + scorecard on 1–2 set-aside OPs | Measure without auto-mutate |
| **L3** | Mutation Proposal schema + human successor apply | Controlled TS loop with fingerprint law |
| **L4** | Optional auto paper-confirm + WUT micro-backtest gate | Broader than V1 closed book |
| **L5** | Promote path into Observation/Trade-Ready | Closes loop into existing handoff |

**Order change:** run **V1–V2 before L2+ evolution**. L1 shadow verifier can run in parallel on HITL without auto fills.

No broad Evolution build until V1–V2 scorecard is interpreted.

---

## Open decisions (need principal input)

1. **Is evolution a third lane or a subtype of paper?** (Recommend: subtype flag on paper OP — fewer lifecycle branches.)
2. **Auto paper-confirm:** closed A/B only first (Recommend: **yes for one Auto OP**; not global).  
3. **Where does micro-backtest live?** WUT-only (pure) vs Wv2 shadow runner (faster, risk of dual engines).
4. **Who may approve mutations?** John only vs Telegram policy vs weekly batch.
5. **Capital for closed A/B:** fixed toy book ($5–20k) both arms — recommend same number both sides.  
6. **Should L1 verifier ship before any EP class?** (Recommend yes as shadow; B2 auto-gated after B1 baseline.)  
7. **Auto price policy:** stick to current paper fill convention vs always next open — freeze before V1.  
8. **HITL seed vs Auto seed naming** and whether both stay in DAR attention band long-term.

---

## Risks

| Risk | Mitigation |
|------|------------|
| Overfit to last 10 paper trades | Require WUT re-validate; minimum trade count; thrash kill |
| Attention overload (too many fingerprints) | Cap Active evolution OPs (e.g. 1–2); archive aggressively |
| AI rubber-stamps every signal | Separate verifier prompt; track SKIP rate; blind to maker prose |
| Violating engagement lock | Only successor path; tests on import/rebalance |
| Confusion with Capital Activation | Explicit forbid + UI/Telegram copy |
| Complexity explosion | V1–V2 closed A/B first; no L3 until V1–V2 interpreted; no L3 until L2 scorecards used for 2+ weeks |

---

## Suggested next artifacts (when leaving design)

1. Optional ADR-009: **Evolution lane / controlled methodology loop** (builds on ADR-006, LLM plan).
2. CONTEXT.md terms if lane adopted.
3. Skill stubs under `ecosystem/ai/skills/` for L1 verifier + STATE discipline.
4. Spawn V1 implementation ticket when ready: closed Auto paper auto-confirm + HITL twin.
5. Ticket: scorecard metrics definition (objective stops) — spawn when L2 starts.

---

## Summary answers

### 1) Leverage in Winston now

Treat Cromwell + DAR + journals + MCP as an incomplete Roan loop: **finish automation stop conditions, durable daily STATE, maker–checker verification, and lesson write-back into skills** — while keeping deterministic signals and human real-capital gates. Map goal loops to WUT science and cadence loops to Wv2 ops. Do not chase auto-broker execution as the definition of success.

### 2) Evolution mode shape

Set-aside **paper** OPs with an evolution tag; same signal engines; AI as **verifier + mutation proposer**; paper fills with staged autonomy; **mutations only via successor fingerprints** and closed knob catalogs; objective scorecards for kill/promote; exit only through WUT → Observation/Trade-Ready. That is “self-improving quant loop” compatible with Winston’s majestic-monolith and lineage laws — not a black-box autotrader.

### 3) Verify before Evolution (principal direction 2026-07-20)

Run a **closed-system Auto vs HITL paper A/B** with frozen methodology and optional paper auto-confirm on the Auto arm only. Measure process/automation effects on realized equity before any self-mutating TS loop. See § Verification first.

