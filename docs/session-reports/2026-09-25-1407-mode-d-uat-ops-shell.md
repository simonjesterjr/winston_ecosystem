# Session Report — Mode D user acceptance on the Ops Shell

**Date:** 2026-09-24 to 2026-09-25
**Time:** through 14:07 MDT
**Duration:** multi-hour, across the date change
**Project:** Winston v2, Broker Gateway, ecosystem docs
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` in `winston_v2`, `broker_gateway`, and `ecosystem` (each its own git repo)
**Model:** Grok
**Operator:** John

---

## 1. Goal & Outcome

**Stated goal:** Continue Mode D phase 2, then turn the user-acceptance walk into the real Ops Shell desk against the Interactive Brokers (IBKR) paper account. Finish enough of that walk to know the workflow before full Mode D integration.

**Outcome:** Partially delivered. The desk path, the chain read, the first two XLE lots, one covered call, and a protective stop were exercised. The book was then unwound. The call is closed. The 240 shares are not flat yet because the exchange was closed. A GTC limit sell is resting.

**One-line summary:** Mode D user acceptance is the real desk, not a Winston-only page. Resume next week after order 946212659 fills, then start a fresh 120-share XLE long.

---

## 2. Work Completed

- Replaced the separate Mode D page with a redirect onto the existing desk.
- `GET /internal/portfolios` emits `fulfillment_mode` (`stock`, `mode_c`, `mode_d`). No new column.
- Covered-call chain read on the call step only. Spot is the stock close. Weeklies are skipped in favor of the monthly inside 21–45 days. Open interest and the 8% spread are not gates. A missing bid or ask still refuses the quote.
- After a Mode D stock print books: park the GTC exit stop, and offer `floor(shares/100)` covered-call contracts as an opted-out draft. Neither sends a pyramid buy.
- A pyramid buy and a covered-call confirm are not blocked by a live protective stop. A stop that already has a broker order id is not a pending Ops Shell action. The call card is headed **Mode D Option Workflow**.
- Paper account DUT070450: sold 100 IBM (order 1122372704). Bought 120 XLE at 61.81 and 120 at 62.10. Sold 1 Oct 16 66 call at 0.29 (order 1122372776). Bought that call back at 0.60 (order 946212656). Resting flatten: GTC limit sell 240 XLE at 61.00 (order 946212659, PreSubmitted).
- Rules filed: `docs/business-context/mode-d-ops-shell-uat.md`, ADR-019 (production items Proposed), CONTEXT Mode D paragraph, a short note on the protective-stop desk law.

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `winston_v2` desk, workflow, shell, confirmation, Mode D services | modified/added | Real desk, chain panel, call-after-fill, GTC park, guard, pending label |
| `broker_gateway` `CoveredCallCandidates` | modified | Monthly inside the window; no open-interest or spread gate |
| `broker_gateway` `LeapCandidates` | modified | `listed_contract` hook. Furthest-month pick unchanged |
| `broker_gateway` `IbkrAdapter` | modified | `outside_rth` on the ticket when the intent asks |
| `ecosystem` CONTEXT, ADR-019, business note, resume ticket, this report | added/modified | Handoff |

### Commits

- `winston_v2` `3104fcb` — Mode D user acceptance runs on the real desk.
- `broker_gateway` `f410647` — Mode D covered-call read keeps the monthly inside the window.
- `ecosystem` — this report, the resume ticket, the business note, and ADR-019 (commit at wrap).

### Branch / PR state at sign-off

- Branch: `main` in each repo — dirty until the wrap commit
- Pushed: after wrap push
- PR: not opened (this work stays on `main`)

---

## 4. Decisions Made

### Decision 1: The desk is the user-acceptance surface
- **Choice:** `/operations/mode_d` redirects to the real desk. Confirm sends.
- **Why:** Writing journals never tested the chain or the broker.
- **Alternatives considered:** Keep the unbound `TestDesk` page.
- **Reversibility:** easy
- **Promote to ADR?** Recorded in ADR-019 as user-acceptance, not production.

### Decision 2: Drop Mode C liquidity screens on this walk
- **Choice:** No 200-contract open-interest floor. No 8% spread gate. Missing bid/ask still fails.
- **Why:** Operator. Both screens were copied from Mode C Plan B and blocked names that had a quote.
- **Alternatives considered:** Keep them and switch symbols until one passed.
- **Reversibility:** easy
- **Promote to ADR?** UAT only until the operator says the spread gate stays off.

### Decision 3: Stop and call are both required, and they are not the same thing
- **Choice:** Park the GTC stop when the stock print books. Offer the call separately. A filled call does not clear naked.
- **Why:** Operator, and the blotter. IBKR did not prove that a call fill cancels a stop. Winston must not pretend a cancelled stop is still working.
- **Alternatives considered:** Treat the short call as the hedge and skip the stop.
- **Reversibility:** easy
- **Promote to ADR?** Production auto-send of the stop is Proposed in ADR-019.

### Decision 4: Paper-account cash, not the $30,000 book, decides the fill
- **Choice:** Microsoft was abandoned. XLE at about $62 was used so 120 shares, and three such lots, fit DUT070450 after the IBM sale.
- **Why:** 200 MSFT was about $99,586. The account had about $1,894 cash and $24,544 net liquidation.
- **Alternatives considered:** Force the MSFT order anyway.
- **Reversibility:** easy
- **Promote to ADR?** No. It is account fact.

---

## 5. Insights Surfaced

- Ops Shell **NAKED** means no working protective stop at the broker. It does not mean “no covered call.”
- A parked stop left on the pending list, and a ghost `working` journal after IBKR cancelled the order, both blocked the next confirm.
- Capital Fit’s slot slice booked the second XLE print as 52 shares while the broker filled 120. User-acceptance drafts with `source=mode_d_uat` now skip that slice. The book was corrected to 120.
- The call credit must be the print. Winston had $44.50 (the 0.445 limit) against a 0.29 fill ($29).
- `outsideRTH` is not a valid attribute on this XLE market order. A GTC limit is what rested while the exchange was closed.
- Chain spot must be the stock close. Using the option premium (9.125) picked a strike 5% above $9.

---

## 6. Issues & Tickets

### Resolved this session
- Desk walk, portfolio-list field, and assignment-replace child tickets were already archived. This session did not close phase 2. The paper send and the fingerprint adopt stay blocked on their own tickets.

### Deferred
- Finish the walk after the flatten fills. Filed: `docs/tickets/2026-09-25-mode-d-uat-resume.md`.
- Production locks in ADR-019 (auto-send of the stop, one stop per symbol vs per lot, spread gate after UAT, cancel watcher). Not filed as separate tickets. They are the open section of the business note.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Portfolio list `fulfillment_mode` | request spec + live GET | ✅ |
| Chain monthly pick, no OI gate, no spread gate | `covered_call_candidates_spec` + live XLE read | ✅ |
| Covered call after fill | spec + live journal 2109 / 2112 | ✅ |
| GTC park on fill | spec. Live 120-share stop parked, then both stops showed Cancelled on the blotter | ⚠️ |
| Pyramid confirm while a stop is parked | spec + operator confirm of journal 2111 | ✅ |
| Second call confirm | Operator click. Winston rejected before send. IBKR has no second call | ❌ expected, then the guard was opened |
| Flatten | Call buy filled 0.60. Stock GTC limit 946212659 PreSubmitted, shares still long | ⚠️ exchange closed |
| Ops shell parked-stop filter and Mode D Option Workflow label | code review, not a browser pass after the label change | ⚠️ |

**Test command(s):**

```bash
./bin/compose exec -T -e RAILS_ENV=test broker_gateway bundle exec rspec spec/services/adapters/ibkr/covered_call_candidates_spec.rb
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 bundle exec rspec \
  spec/requests/operations_mode_d_desk_spec.rb \
  spec/services/operations/park_protective_stop_spec.rb \
  spec/services/operations/protective_gtc_guard_spec.rb \
  spec/services/operations/covered_call_after_fill_spec.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None added.
- **Services:** Compose `winston_v2` (port 3002) and `broker_gateway` (port 3003). Client Portal Gateway on localhost:5000. Paper account DUT070450.
- **Migrations:** None.
- **Live rows:** Winston portfolio 1585 journals 2105–2114 area. Positions 936 and 937 still open. Orders named in §2.

---

## 9. Risks & Technical Debt

- Resting sell 946212659 can fill next session and must be booked or Winston stays long 240 while the broker goes flat.
- `outside_rth` is on the adapter and was rejected for this XLE market order. It is not a general overnight switch.
- Journal 2109’s strike label was corrected to 66. Earlier reads had said 65 while the conid was already the 66 call.
- Winston v2 has no `graphify-out/graph.json`. This session did not build one.
- Broker Gateway has other uncommitted files (cancel-order service, fixtures, vendor) that this session did not write. They were not included in the wrap commit.

---

## 10. Open Questions

Answered by the operator on 2026-09-25, after the wrap. Recorded in ADR-019 and `docs/business-context/mode-d-ops-shell-uat.md`.

- The 8% spread gate does not return for Mode D. Mode C’s 200-contract and 8% screens need a design session. They were not an operator lock.
- Day orders return to the nightly slate. A lot without a working stop is never acceptable. Covered-call sales stay human confirm.
- Trading Strategy #341 stays `move_to_last_entry`. Earlier lots take the newest lot’s stop. The user-acceptance hour made that look strange.
- Winston must match the broker. A cancelled or filled order leaves `working`. A filled call does not prove the stop was cancelled and does not clear naked.

Still open, and not a blocker for resuming the walk: the Mode C design session for those liquidity screens.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Call closed. 240 XLE still long. GTC limit sell 240 at 61.00 is order **946212659** (PreSubmitted). Winston lots 936 and 937 still open. No pending desk task. New long was not minted, so it cannot stack on the shares that are still held.
- **Next concrete step:** Check 946212659. Book it if filled. If the market is open and it is still resting, sell 240 at the market and book that print. Then mint one 120-share XLE enter draft and hand the operator the workflow link.
- **Files to read first:**
  1. `ecosystem/docs/tickets/2026-09-25-mode-d-uat-resume.md`
  2. `ecosystem/docs/business-context/mode-d-ops-shell-uat.md`
  3. `winston_v2/app/services/operations/mode_d/park_protective_stop.rb`
  4. `winston_v2/app/services/operations/mode_d/covered_call_after_fill.rb`
  5. `winston_v2/app/services/operations/protective_gtc_guard.rb`

---

## 12. Stakeholder Communications

- Operator resumes early next week from the ticket above. Full Mode D integration waits on this walk.

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report, operator-prose. Graphify query at the start (workspace graph had no Winston v2 Ruby).
- **Graphify Graph:** updated `broker_gateway/graphify-out` and `ecosystem/graphify-out` (AST only). Merged workspace `graphify-out/graph.json` (19086 nodes). Not committed. Winston v2 has no `graphify-out/graph.json`; no full rebuild.
- **Ponytail flags:** `ParkProtectiveStop` reuses `ProtectiveStatus` and `Levels.working_stop`. `listed_contract` is a hook on `LeapCandidates` so the covered-call walker does not copy the month loop. No second stop calculator.
- **What worked well:** Live snapshot and order-status reads settled what the blotter meant. Specs locked the guard and the chain before the next click.
- **Friction points:** Capital Fit sliced a 120-share print to 52. A ghost working stop blocked the next confirm. Chain spot used the option premium. Exchange closed stopped a market flatten.
- **Subagent usage:** None.

---

## 14. Follow-up Actions

- [x] Resume ticket — `docs/tickets/2026-09-25-mode-d-uat-resume.md` — owner: operator, early next week
- [ ] Book or replace order 946212659, then close Winston lots 936 and 937 — owner: next session — due: when the market is open
- [ ] Fresh 120 XLE long on the desk, then the walk through 3 lots and one short — owner: next session — due: after the book is flat
- [ ] Operator answers the four open questions in §10 — owner: operator — due: before production Mode D

---

## 15. Appendix

Desk links used:

- Ops shell: `https://sawtooth-ai.tail944ffb.ts.net/wv2/operations`
- Workflow: `https://sawtooth-ai.tail944ffb.ts.net/wv2/operations/workflow?journal_id=<id>`
- Gateway login: `https://localhost:5000`

Broker order ids: 1122372704 (IBM sell), 1122372772 (first XLE buy), 1122372776 (66 call sell), 440801976 (120 stop, later cancelled), 440802069 (second XLE buy), 946212656 (call buyback), 946212659 (resting stock sell).
