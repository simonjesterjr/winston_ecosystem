# Session Report — IBKR paper DUT evidence + slate-automation grill

**Date:** 2026-09-01
**Time:** wrap 16:01 MDT (session continued from Interactive Brokers paper rehearsal through grill-with-docs)
**Duration:** ~full-day continuation (CPGW paper login → DUT fills → WQ book align → grill Q1–Q12)
**Project:** Winston ecosystem — Broker Gateway (BG), Winston v2 (Wv2), Winston Quiver (WQ) paper, domain glossary
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on `ecosystem`, `winston_v2`, `broker_gateway`, `data_manager` (started from `origin/main`; **dirty, uncommitted** at wrap)
**Model:** Grok 4.6 (xAI)
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Rehearse WQ paper (Operational Portfolio #1372) against Interactive Brokers (IBKR) paper `DUT070450` through Broker Gateway — not WQ talking to IBKR. Then grill signal vs fill books, extra-modal packaging, capital authority, leverage, and later automation. Constraints: WQ is not a new monolith; #1372 stays paper; Confirm ≠ Send; `order_write` off at L1; dummy_sim remains Winston-internal paper; credentials never in git.

**Outcome:** Partially delivered. IBKR Client Portal Gateway (CPGW) paper path works; DUT was filled to match the WQ book (13 names); WQ cash/equity was aligned then rebalanced. Grill Q1–Q12 locked product law in `ecosystem/CONTEXT.md`. **Not shipped:** L3 Desk Send, Slate Automation code, packaging-policy UI, Mint bound to DUT, accept-fill of entries.

**One-line summary:** Paper IBKR DUT is a working L1 evidence broker for WQ; glossary now locks Turtle resting-slate automation as discovery law (policy Send + accept-fill stops only) without turning Daily Analysis into an autotrader.

---

## 2. Work Completed

### IBKR paper + Broker Gateway L1

- CPGW paper login (`purtey261` → account `DUT070450`, `isPaper` true) on `https://localhost:5000`. Live SSO leftover opened the wrong account until paper was explicit; `ssodh/init` required.
- Tickle keep-alive (~6 min idle); Sidekiq `TickleJob` cron `* * * * *` while live-read is on.
- `TickerRemap`: `BRK.B` = `BRK-B` = `BRK B` (conid 72063691). Size increment 0.0001 (0.571485 rejected; 0.5715 ok). Split executions are one command.
- Normalizer stores qty at 4 decimal places (was `%.2f` → BRK 0.57).
- Wv2 `FULFILLMENT_ADAPTERS` includes `interactive_broker_trader_api`. #1372 bound `bnd_3d6a5020d839c315583277d2`. DummySimFills skip if adapter is not `dummy_sim`.
- Confirmation Intake: canonical symbol match; partial qty is not a mismatch; PrefillFromMatch does not shrink units on partial exec; `broker_execution_ids` accumulate.

### WQ book vs DUT

- Hand-placed DUT fills (split execs everywhere). Original WQ book prices **not** amended (operator lock).
- WQ cash inflow ~$10,037 to match DUT net liquidation ~$11,997; rebalance plan #19, 13 reweights confirmed.
- DUT after auto-fill: 13 positions matching WQ sizes at 0.0001; NLV ~$11,977 cash ~$293 vs WQ equity ~$11,997 cash ~$160.77.
- Reweight confirm nil.id → treat `task_type` reweight. Reweight journals dated 2026-09-02 so cash did not move same day → backdated to 2026-09-01.
- Over-deployed after scale-up (cash $161 vs 25% buffer) — later ops fix on Wv2 `main` history.

### Grill-with-docs (Q1–Q12)

Locked in `ecosystem/CONTEXT.md`. Discovery/learning mode: product law only; no L3 write this session. After WQ paper setup, intent is reset IBKR paper and bind a paper Trend Following OP (probably Mint) — **not done**.

---

## 3. Code Delivered

Uncommitted at wrap. Do **not** treat wrap as having committed these.

### Files changed (this session’s dirty trees)

**ecosystem** (grill + IBKR/WQ docs)

| File | Change | Notes |
|------|--------|-------|
| `CONTEXT.md` | modified | Capital Authority, packaging, Risk Modality, Session Order Slate, Slate Automation, Accept-Fill, Q1–Q12 flags |
| `docs/analysis/2026-09-01-fulfillment-command-vs-broker-executions.md` | added | Command vs split executions; 2-of-3 witnesses |
| `docs/tickets/2026-08-31-bg-ibkr-read-adapter-l1.md` | added | BG IBKR L1 |
| `docs/tickets/2026-09-01-wq-ibkr-paper-evidence-bind.md` | added | WQ Phase 3 analog DUT bind |
| `docs/tickets/INDEX.md` | modified | New P1 rows |
| `docs/tickets/2026-08-30-production-ready-wq.md` and phase 1–4 tickets | added/modified | Epic + children (some from prior days, still untracked) |
| `plans/production-ready-wq.md` | added | North star Phase 4 not this week |
| `interfaces/fixtures/ibkr/` | added | Paper CPGW fixtures |
| `.gitignore` | modified | CPGW vendor dist / JRE |
| `docs/session-reports/2026-09-01-1601-ibkr-paper-and-slate-grill.md` | added | This report |

Also dirty in ecosystem (account for before commit; some may predate this wrap): `ADR-009` one-line, quiver tickets/plans, Schwab fixtures, `deployment/bin/`, `deployment/ibkr-webapi-template.txt`, `vendor/` (binaries — **do not commit dist**), `plans/cromwell-staff-roster.md`.

**winston_v2**

| File | Change | Notes |
|------|--------|-------|
| `app/models/portfolio.rb` | modified | `interactive_broker_trader_api` in `FULFILLMENT_ADAPTERS` |
| `app/services/confirmation_intake/match_notification.rb` | modified | Canonical symbol; partial qty |
| `app/services/confirmation_intake/prefill_from_match.rb` | modified | Don’t shrink units; `broker_execution_ids` |
| `app/services/quiver_tracking/population.rb` | modified | Reweight confirm without draft journal |
| `app/services/quiver_tracking/plan_approve.rb` | modified | Reweight / IBKR-bound path |
| `app/services/ticker_remap.rb` | added | Class-share space/hyphen/dot |
| Specs for match/prefill, plan_approve, dummy_sim skip, ticker remap | modified/added | |

**broker_gateway**

| File | Change | Notes |
|------|--------|-------|
| `app/services/adapters/ibkr_adapter.rb` + `ibkr/` | added | L1 read adapter |
| `app/jobs/adapters/` | added | TickleJob |
| `app/services/ticker_remap.rb` | added | Same class-share remap |
| `config/sidekiq_schedule.yml` | modified | Minute tickle |
| Registry + refresh specs | modified | |
| `tmp/pids/`, `vendor/` | untracked | **Do not commit** |

**data_manager**

| File | Change | Notes |
|------|--------|-------|
| `app/services/ticker_remap.rb` | modified | BRK.B / class-share |
| `spec/services/ticker_remap_spec.rb` | modified | |

**winston_unit_test:** clean.

### Commits

- _None this wrap._ Trees dirty vs `origin/main`.

### Branch / PR state at sign-off

- Branch: `main` on each repo — **dirty**
- Pushed: no (wrap Step 2 must run before commit)
- PR: not opened

---

## 4. Decisions Made

### Decision 1: Capital Authority by context
- **Choice:** Winston Unit Test and default Wv2 paper (including Schwab-as-fulfillment-only) = **Notional Capital**. Wv2 paper + IBKR paper binding, and live = **Broker Account Capital**.
- **Why:** DUT net liquidation is the risk number when that account is bound; dummy_sim is still a Winston ledger.
- **Alternatives considered:** Always notional; always broker.
- **Reversibility:** costly once live books exist
- **Promote to ADR?** no (glossary lock is enough for now)

### Decision 2: Risk Capital / spending
- **Choice:** Risk Capital = net liquidation value. Enter/pyramid room uses **Broker Buying Power**. **Spending Capacity** = min(buying power, room under **Leverage Guardrail**). Default guardrail **gross** 2× (long MV + short MV) / Risk Capital; per OP/TS; human override per ticket; broker buying power is a hard ceiling.
- **Why:** Settled cash can be negative while buying power remains.
- **Alternatives considered:** Free cash only; net (not gross) leverage.
- **Reversibility:** costly
- **Promote to ADR?** no

### Decision 3: Fulfillment Packaging Policy on the Operational Portfolio
- **Choice:** Winston v2 owns it; Ops UI to set; rule-based (including ask per-share price); later LLM bakeoff of shapes (LEAPs vs calendar) without a new fingerprint. Packaging may differ by Desk Action (entrance LEAPs, pyramid shares). BG classifies evidence only.
- **Why:** Desk default at create-time is not enough; same lot can mix modalities.
- **Alternatives considered:** Policy on TradingStrategy; policy in BG.
- **Reversibility:** easy until UI ships
- **Promote to ADR?** no

### Decision 4: Pyramid size after extra-modal entrance
- **Choice:** Daily Analysis drafts in **Signal-Path Operational Lot** share units. Every **Risk Modality** is shown. Fill shape is policy/human. Do not size from option premium alone. One-Way Dynamic Risk is not the live default (lab: higher drawdown without benefit).
- **Why:** Methodology ladder stays coherent; cash-at-risk of calls must stay visible.
- **Alternatives considered:** Size from LEAP premium; next-action modality owns units.
- **Reversibility:** easy until sizer code
- **Promote to ADR?** no

### Decision 5: Live TF session cycle = resting Session Order Slate
- **Choice:** Park stop-market entry / pyramid / protective Working Stop before the session. Risk at **Moment of Truth**. Unfilled entries/pyramids cancel at close; protective stops replace overnight. Next-open stays lab default until a resting-touch fingerprint. Do not mix enter-at-open-100 with stop-102.
- **Why:** Turtle geometry; ADR-009 next-open creates gap tapes.
- **Alternatives considered:** Next-open forever; dual-write stops only; human parks in broker UI.
- **Reversibility:** costly vs ADR-009 point 3
- **Promote to ADR?** **yes** — ADR-009 addendum (deferred; operator did not ask to write it this turn)

### Decision 6: Slate Contest is Turtle mechanical
- **Choice:** **Unit Heat** refuses correlated overflow. Ties: buy-strength / sell-weakness and first-to-touch. No expected-return ranking in live ops. DAR is a **review** (moved stops/levels, Turtle priorities), not a pick-list.
- **Why:** Faith unit limits + first-to-touch; WUT expected-return swap hurt Blue.
- **Alternatives considered:** Nightly ER menu; live PositionSwapEvaluator.
- **Reversibility:** easy until DA ports heat
- **Promote to ADR?** no

### Decision 7: Slate Automation + policy Send
- **Choice:** Explicit flag on OP + TradingStrategy fingerprint. Policy-automatic **Desk Send** of the mechanical slate. Human may halt or Desk Pass. Not implied by paper, Active, or IBKR bind. WQ stays Plan Approve. Daily Analysis still does not open Positions.
- **Why:** Automated and mechanical instructions; DAR is optional review.
- **Alternatives considered:** Nightly Send click even when enabled; silent DA place_order.
- **Reversibility:** costly once write exists
- **Promote to ADR?** yes when leaving discovery (not now)

### Decision 8: Accept-Fill stops only; whole-slate waits
- **Choice:** Discovery: Accept-Fill matched protective Working Stop prints (Stop-Out Reconciliation, warn on gap) so Unit Heat is not a ghost lot. Entries/pyramids stay Desk Confirm. Whole-slate accept-fill is glossary aspiration only — **no scheduled promotion**; later grill required (Q12 D).
- **Why:** Ghost lots poison the next mechanical slate; auto-booking entries guesses packaging.
- **Alternatives considered:** Evidence-only; accept-fill whole slate now; calendar “soon”.
- **Reversibility:** costly once C is on
- **Promote to ADR?** with Decision 7, later

---

## 5. Insights Surfaced

- IBKR paper CPGW is one session per username; leftover live SSO is a foot-gun. Tickle + `ssodh/init` are operational, not optional.
- Broker executions split constantly; Winston command identity must stay one journal/task. Partial qty is not a mismatch. Prefill must not shrink command units.
- `/iserver/account/trades` and `/positions/0` lag; `portfolio2` was the livelier position witness. Do not book from one witness.
- Paper DUT NLV vs WQ notional ledger will diverge (cash $293 vs $160); when Capital Authority is broker, do not CashEvent-mimic NLV on paper IBKR (already glossary).
- WUT expected-return / position-swap is a lab score, not Turtle live law. PCS is membership quality; Unit Heat is occupancy.
- “Soon” is not a gate. Operator chose to keep whole-slate accept-fill unscheduled.

---

## 6. Issues & Tickets

### Resolved this session
- CPGW “unable to connect” / conf.yaml Stream closed — classpath `--conf` basename (prior in-session).
- BRK.B search fail — remap to `BRK B`.
- Qty 0.571485 min increment — 4 dp / 0.0001.
- Session 401 after idle — tickle + ssodh/init.
- Reweight confirm `nil.id` — treat task_type reweight.
- DummySimFills against IBKR-bound OP — skip.

### Deferred
- ADR-009 addendum — See: [`docs/tickets/2026-09-01-adr-009-resting-slate-addendum.md`](../tickets/2026-09-01-adr-009-resting-slate-addendum.md)
- Slate Automation / Accept-Fill ADR — See: [`docs/tickets/2026-09-01-slate-automation-accept-fill-adr.md`](../tickets/2026-09-01-slate-automation-accept-fill-adr.md)
- Packaging-policy UI on Wv2 Ops — See: [`docs/tickets/2026-09-01-fulfillment-packaging-policy-ops-ui.md`](../tickets/2026-09-01-fulfillment-packaging-policy-ops-ui.md)
- Unit Heat / Slate Contest in Wv2 Daily Analysis — See: [`docs/tickets/2026-09-01-wv2-unit-heat-slate-contest.md`](../tickets/2026-09-01-wv2-unit-heat-slate-contest.md)
- WQ cost-basis Corrective Amend vs DUT — See: [`docs/tickets/2026-09-01-wq-cost-basis-corrective-amend-dut.md`](../tickets/2026-09-01-wq-cost-basis-corrective-amend-dut.md)
- Reset DUT and bind paper Mint — See: [`docs/tickets/2026-09-01-ibkr-paper-reset-bind-mint.md`](../tickets/2026-09-01-ibkr-paper-reset-bind-mint.md)
- L3 `order_write` / Phase 4 Send — already ticketed, blocked: [`2026-08-30-wq-phase4-one-at-a-time-send.md`](../tickets/2026-08-30-wq-phase4-one-at-a-time-send.md)
- Resting-touch WUT fingerprint / live resting loop — already ticketed [`2026-08-20-wut-resting-stop-touch-fill-cadence.md`](../tickets/2026-08-20-wut-resting-stop-touch-fill-cadence.md) / [`2026-08-20-resting-session-stop-orders.md`](../tickets/2026-08-20-resting-session-stop-orders.md)
- Whole-slate accept-fill (Q11-C) — See: [`docs/tickets/2026-09-01-whole-slate-accept-fill-later-grill.md`](../tickets/2026-09-01-whole-slate-accept-fill-later-grill.md)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| CPGW paper login DUT070450 | Manual browser + API | ✅ (prior in-session; not re-verified at wrap) |
| Tickle keep-alive | In-session idle recovery | ✅ then |
| TickerRemap BRK.B | Hand search + fill | ✅ then |
| Split execs → one Confirm | SPCX 1.0+0.06 and others | ✅ then |
| WQ #1372 vs DUT 13 names | Positions vs journals | ⚠️ close (NLV/cash gap remains) |
| Wv2 rspec | Mixed; some runs against development PG | ⚠️ not re-run at wrap |
| Slate Automation / Accept-Fill | Glossary only | _None (no code)_ |
| Grill CONTEXT.md | Read-back of locks | ✅ |

**Test command(s):** not re-run at wrap. Prior: Wv2 request/service specs for quiver tracking and confirmation intake; BG registry/refresh specs.

---

## 8. Environment, Dependencies, Data

- **Dependencies:** IBKR Client Portal Gateway + Java 17 JRE under `ecosystem/vendor/` (gitignored dist). Not a new Ruby gem.
- **Services:** compose `data_manager`, `winston_v2`, `broker_gateway`, Redis, Postgres; CPGW on host `localhost:5000`.
- **Migrations:** none this wrap (WQ plan tables already on compose from prior sessions).
- **Secrets:** paper username used in ops chat; **must not** land in git. CPGW conf is local.

---

## 9. Risks & Technical Debt

- Dirty `main` on four repos — wrap must stage **precise** paths; never `vendor/` dist, `tmp/pids`.
- ADR-009 still says next-open as default EOD story; live TF target now contradicts until addendum.
- Paper DUT vs WQ cash/equity gap will confuse operators if Risk Capital is read from the wrong spine.
- Slate Automation glossary is ahead of write capability (`order_write` off). Easy to over-implement.
- Accept-Fill stops without matching evidence will ghost-close lots — match quality is the hazard.

---

## 10. Open Questions

- **When is WQ paper “setup done” enough to reset DUT and bind Mint?** — operator; blocks Mint rehearsal.
- **Corrective Amend WQ cost basis to DUT?** — operator said do not amend the original three prices; remaining names unspecified.
- **Resting-touch fingerprint for Mint?** — lab; blocks live resting loop (not discovery glossary).
- **Whole-slate accept-fill** — later grill only; does not block discovery.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Grill Q12 locked (D). `/wrap` Step 1 (this report). Step 2 follow-up promotion **not yet answered**. Trees still dirty.
- **Next concrete step:** Operator shortcut on follow-ups (`create all tickets` / `skip all` / `ask`), then commit per-monolith precise paths. Operating resume: finish WQ paper, **not** Mint automation.
- **Files to read first:**
  1. `ecosystem/CONTEXT.md` — flagged ambiguities Capital Authority through Accept-Fill / discovery
  2. `ecosystem/docs/tickets/2026-09-01-wq-ibkr-paper-evidence-bind.md`
  3. `ecosystem/docs/analysis/2026-09-01-fulfillment-command-vs-broker-executions.md`
  4. `ecosystem/docs/tickets/2026-08-20-resting-session-stop-orders.md` (already filed; L3+)
  5. `ecosystem/plans/production-ready-wq.md`

---

## 12. Stakeholder Communications

- _None required._ Internal operator + future agent. No Telegram / capital action.

---

## 13. Tools & Workflow Notes

- **Skills used:** `grill-with-docs`, `operator-prose`, `session-report`, `wrap` (Step 1 only at this file’s write)
- **What worked well:** One grill question at a time; locking CONTEXT inline; calling Q7 vs Q8 auto-park contradiction instead of silently merging.
- **Friction points:** Session compaction lost verbatim IBKR command logs; wrap must not invent SHAs. Four dirty `main`s plus `vendor/` risk a bad `git add`.
- **Subagent usage:** _None._

---

## 14. Follow-up Actions

- [ ] ADR-009 addendum — See: [`docs/tickets/2026-09-01-adr-009-resting-slate-addendum.md`](../tickets/2026-09-01-adr-009-resting-slate-addendum.md)
- [ ] Slate Automation + Accept-Fill ADR — See: [`docs/tickets/2026-09-01-slate-automation-accept-fill-adr.md`](../tickets/2026-09-01-slate-automation-accept-fill-adr.md)
- [ ] Packaging-policy UI on Wv2 Ops — See: [`docs/tickets/2026-09-01-fulfillment-packaging-policy-ops-ui.md`](../tickets/2026-09-01-fulfillment-packaging-policy-ops-ui.md)
- [ ] Port Unit Heat / Slate Contest into Wv2 Daily Analysis — See: [`docs/tickets/2026-09-01-wv2-unit-heat-slate-contest.md`](../tickets/2026-09-01-wv2-unit-heat-slate-contest.md)
- [ ] WQ cost-basis / Corrective Amend vs DUT — See: [`docs/tickets/2026-09-01-wq-cost-basis-corrective-amend-dut.md`](../tickets/2026-09-01-wq-cost-basis-corrective-amend-dut.md)
- [ ] After WQ setup: reset IBKR paper DUT; bind paper Mint — See: [`docs/tickets/2026-09-01-ibkr-paper-reset-bind-mint.md`](../tickets/2026-09-01-ibkr-paper-reset-bind-mint.md)
- [ ] Whole-slate accept-fill later grill only — See: [`docs/tickets/2026-09-01-whole-slate-accept-fill-later-grill.md`](../tickets/2026-09-01-whole-slate-accept-fill-later-grill.md)
- [ ] Already filed: resting-touch lab `2026-08-20-wut-resting-stop-touch-fill-cadence.md`; live resting slate `2026-08-20-resting-session-stop-orders.md` (Blocked L3+); WQ Phase 4 Send `2026-08-30-wq-phase4-one-at-a-time-send.md`

---

## 15. Appendix

- IBKR paper account `DUT070450`; CPGW `https://localhost:5000`.
- WQ OP #1372; binding `bnd_3d6a5020d839c315583277d2`.
- Fingerprint / paper constraint: #1372 stays paper; Confirm ≠ Send; `order_write` off.
- Grill recommended (C) on contest HITL; operator chose Turtle (B). Grill recommended (B) on B→C gate; operator chose (D) stay on stops-only until a later grill.
