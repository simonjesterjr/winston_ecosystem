# Session Report — Confirmation Intake context, L1 build, and desk rehearsal handoff

**Date:** 2026-08-27
**Time:** 2026-08-19 work session; wrap 17:29 MDT
**Duration:** ~one coding session on 2026-08-19, then later operator “how do I test” (wrap 2026-08-27)
**Project:** Winston v2 (Wv2) Confirmation Intake + ecosystem L1 tickets (Broker Gateway already present)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` (started from `origin/main`; intake already on `main`)
**Model:** Grok 4.6 (xAI)
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Understand Schwab sandbox vs test path; then implement the authorized first coding slice: Wv2 client → Trade Notification → match/prefill → desk UI. Later: step-by-step so the operator can see the pieces integrate.

**Outcome:** Delivered (code already on `main` as of 2026-08-21). This wrap records the original session and the integration-test handoff. No new feature commits remain dirty.

**One-line summary:** Confirmation Intake is on `main`; paper and real share one path through Broker Gateway `dummy_sim`; Schwab has no usable paper API twin; live desk rehearsal still needs a Wv2 recreate so `BROKER_GATEWAY_URL` is set.

---

## 2. Work Completed

- Answered: Charles Schwab Trader API is not a paperMoney twin; Developer Portal “sandbox” is unverified for Individual apps; Winston paper rehearses on Broker Gateway `dummy_sim`.
- Implemented L1 Confirmation Intake in Wv2 against the Winston Broker Evidence Standard.
- Shared fixtures under `ecosystem/interfaces/fixtures/broker-evidence/` (copied into Wv2 specs).
- Desk Workflow evidence panel + `/operations/intake` unmatched queue and dummy_sim pull.
- Marked L1 Wv2 child tickets Done; epic progress updated.
- Wrote operator step-by-step for live dummy_sim rehearsal (chat; also §15 below).
- **Later wrap (2026-08-21)** already committed this code: Wv2 `4f13e3e`, ecosystem `891c737`. See `docs/session-reports/2026-08-21-1707-mms-confirmation-intake-wrap.md`.

---

## 3. Code Delivered

### Files changed (this conversation; now on `main`)

| File | Change | Notes |
|------|--------|-------|
| `winston_v2/app/services/broker_gateway/*` | added | HTTP client; no `place_order` |
| `winston_v2/app/services/confirmation_intake/*` | added | normalize, store, match, prefill, attach, ingest |
| `winston_v2/app/models/trade_notification.rb` | added | store ≠ book |
| `winston_v2/app/models/broker_gateway_cursor.rb` | added | consumer-owned cursor |
| `winston_v2/app/controllers/operations/confirmation_intakes_controller.rb` | added | `/operations/intake` |
| `winston_v2/app/views/operations/desk_workflows/_evidence.html.erb` | added | HITL evidence; no Send |
| `winston_v2/spec/services/{broker_gateway,confirmation_intake}/*` | added | 27 intake examples |
| `ecosystem/interfaces/fixtures/broker-evidence/*` | added | v0.1 contract fixtures |
| `ecosystem/docs/tickets/2026-08-09-wv2-*.md` | modified | Done + acceptance |
| `sawtooth/compose.yml` | modified | `BROKER_GATEWAY_URL` on wv2 + sidekiq (**not in a git repo**) |

Migration on `main` is `20260819121000_create_confirmation_intake.rb` (renamed off `20260819120000` to avoid a copy-book collision).

### Commits

Already on `origin/main` (2026-08-21 wrap, not this wrap):

- `winston_v2` `4f13e3e` — feat(ops): Confirmation Intake L1 and Mid-month Scoreboard
- `ecosystem` `891c737` — docs: MMS MCP/skill and Confirmation Intake L1 ticket status

### Branch / PR state at sign-off

- Branch: `winston_v2` `main` and `ecosystem` `main` — clean for this session’s files
- Pushed: yes (2026-08-21)
- PR: not opened
- Dirty trees **not** from this session: Wv2 `?? app/assets/images/`; ecosystem `M docs/tickets/2026-07-15-journal-ledger-order-vs-fill-deferred.md`

---

## 4. Decisions Made

### Decision 1: Test platform is `dummy_sim`, not Schwab sandbox
- **Choice:** Paper Operational Portfolios default to Broker Gateway adapter `dummy_sim`. Same Confirmation Intake path as live read. Never live credentials / `order_write` on paper.
- **Why:** Schwab paperMoney is UI-only; Individual Trader API is live-account oriented; portal sandbox unverified.
- **Alternatives considered:** Wait on Schwab sandbox; paper Manual zero-IO only.
- **Reversibility:** easy (adapter key).
- **Promote to ADR?** no — already Grill B / CONTEXT / Evidence Standard.

### Decision 2: Match stays in Wv2; v1 Q9 assumptions documented in code
- **Choice:** exact / soft / ambiguous / orphan / mismatch; extra-modal via `underlying_hint` / OCC-ish; dummy_sim never matches real or `manual` OPs.
- **Why:** Grill B Q9 deferred; ship a fail-closed matcher.
- **Alternatives considered:** Symbol-equality only (rejected — extra-modal).
- **Reversibility:** easy (match service).
- **Promote to ADR?** no — Q9 still deferred.

### Decision 3: Do not run live dummy_sim exact against the operator’s desk DB from the agent
- **Choice:** Specs only; operator owns the rehearsal OP + Confirm click.
- **Why:** `exact` emits SPY 10 @ 500 and could prefill an existing SPY draft.
- **Reversibility:** n/a.
- **Promote to ADR?** no.

---

## 5. Insights Surfaced

- Running Wv2 at the time of the 2026-08-19 build still had **`BROKER_GATEWAY_URL` unset** inside the container (`printenv` empty). Default client is `http://localhost:3003`, which is wrong **inside** compose. Recreate `winston_v2` and `winston_v2_sidekiq` is a hard prerequisite for live pull.
- `dummy_sim` daily Sidekiq refresh is **auth heartbeat only**. Fills appear only when an operator (or rake) passes `scenario=exact|partial|orphan|cancel|reject`.
- Root `compose.yml` is **not** in a monolith git. Env wiring can drift from committed docs.

---

## 6. Issues & Tickets

### Resolved this session
- L1 Wv2 slice tickets (client, TradeNotification, match/prefill, desk HITL, integration specs, fixtures harness) — **Done** (filed 2026-08-09; status landed in `891c737`).

### Deferred
- Live dummy_sim desk rehearsal (recreate Wv2, throwaway OP, Confirm) — operator; not filed.
- Schwab portal sandbox spike — already `docs/tickets/2026-08-07-schwab-trader-api-sandbox-spike.md` (**Proposed**).
- Schwab L1 read adapter — already `docs/tickets/2026-08-09-bg-schwab-read-adapter-l1.md` (**Ready**).
- MCP/Telegram “review unmatched fills” — noted as follow-on on the desk UI ticket; not a separate ticket.
- Versioning of root `compose.yml` (`BROKER_GATEWAY_URL`) — workspace file, no git owner.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Client / store / match / prefill / ingest | compose `rspec` 27 examples | ✅ 2026-08-19 |
| Existing Desk Workflow request specs | same run | ✅ |
| Later wrap (MMS + intake) | 50 examples | ✅ 2026-08-21 (`4f13e3e`) |
| Live UI dummy_sim → Confirm | not run (would mutate desk DB) | ⚠️ |
| Schwab sandbox / live read | not in scope | ⚠️ |

**Test command(s):**

```bash
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 \
  bundle exec rspec spec/services/broker_gateway spec/services/confirmation_intake \
  spec/requests/operations_confirmation_intake_spec.rb \
  spec/requests/operations_desk_workflow_evidence_spec.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** `webmock` in Wv2 test group (committed).
- **Services:** `broker_gateway` :3003 was up with seeded `dummy_sim` binding; Wv2 needed `--force-recreate` for `BROKER_GATEWAY_URL`.
- **Migrations:** `trade_notifications`, `broker_gateway_cursors`, `portfolios.fulfillment_adapter_key` default `dummy_sim`. Applied on compose test/dev DBs during the build session.

---

## 9. Risks & Technical Debt

- Live pull will fail closed until Wv2 is recreated with `BROKER_GATEWAY_URL=http://broker_gateway:3000`.
- Two SPY drafts → **ambiguous**; operator rehearsal must use a dedicated OP or a single draft.
- Q8 (OP ↔ binding) still deferred; one dummy_sim binding matches many paper OPs by symbol/side/window.
- Root compose env is not in git.

---

## 10. Open Questions

- **Does our Individual Schwab app even show a Sandbox environment?** — needs operator on `developer.schwab.com`; blocks confident live read (not the dummy_sim path). Spike ticket already exists.
- **Should compose.yml live in a git repo?** — needs operator; blocks durable env wiring.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Intake is on `main`. Operator was given a live rehearsal recipe. Agent did **not** recreate Wv2 or create “Intake Rehearsal” OP.
- **Next concrete step:** Recreate `winston_v2` + `winston_v2_sidekiq`, confirm `printenv BROKER_GATEWAY_URL`, then dummy_sim `exact` pull on a throwaway SPY draft and Desk Confirm.
- **Files to read first:**
  1. This report §15
  2. `winston_v2/app/services/confirmation_intake/match_notification.rb` (Q9 v1 assumptions)
  3. `ecosystem/interfaces/winston-broker-evidence-standard.md`
  4. Epic `ecosystem/docs/tickets/2026-08-09-l1-confirmation-intake-bg-build.md`

---

## 12. Stakeholder Communications

- _None._ Internal desk/ops only. No Telegram, no real-capital Schwab.

---

## 13. Tools & Workflow Notes

- **Skills used:** `operator-prose`, `session-report`, `wrap` (this file). Implementation did not use `lightweight-bug-fix` (feature slice, not a defect).
- **What worked well:** Dummy_sim as the same-path rehearsal plug; Evidence Standard as the Wv2↔BG contract; fail-closed ingest.
- **Friction points:** Host `bundle exec rspec` cannot reach Wv2 Postgres; must `compose exec` with `TEST_DB_HOST=wv2_postgres`. Compose env changes need `--force-recreate`. Session spanned days; code was committed in a later wrap before this report.
- **Subagent usage:** none.

---

## 14. Follow-up Actions

- [ ] Recreate Wv2 containers and run live dummy_sim `exact` → Desk Confirm on a throwaway OP — owner: operator — due: next desk session
- [ ] Schwab Trader API sandbox spike (portal + support) — already `2026-08-07-schwab-trader-api-sandbox-spike.md` — owner: operator + spike session
- [ ] Schwab L1 read adapter (fixtures first) — already `2026-08-09-bg-schwab-read-adapter-l1.md` — owner: next coding session
- [ ] Optional MCP/Telegram “review unmatched fills” — owner: later; desk UI ticket notes it deferred
- [ ] Decide whether root `compose.yml` should be versioned — owner: operator

---

## 15. Appendix — live dummy_sim rehearsal (from operator chat)

Prerequisite: `./bin/compose up -d --force-recreate winston_v2 winston_v2_sidekiq` then `printenv BROKER_GATEWAY_URL` → `http://broker_gateway:3000`.

1. Create throwaway paper OP **Intake Rehearsal** with SPY (+ IWM) and one **draft** SPY enter (do not Confirm).
2. Open `/wv2/operations/intake` and `/wv2/operations/workflow?journal_id=…`.
3. Intake: scenario **exact** → Refresh + pull. Expect Trade Notification matched, journal still draft.
4. Workflow: Submit desk action (Confirm). That is the only book.
5. Optional orphan: scenario **orphan** (IWM 1 @ 200) with no IWM draft → unmatched queue.
6. `dummy_sim` exact payload is always buy 10 SPY @ 500. Two SPY drafts → ambiguous.

UI: `http://localhost:3002/wv2/operations/intake` or Tailscale Serve `/wv2/operations/intake`.

---

*End of session report. Code already on `main` (2026-08-21). This wrap’s remaining git work is this file plus follow-up promotion.*
