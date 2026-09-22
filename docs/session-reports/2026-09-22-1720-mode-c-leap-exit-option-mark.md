# Session Report — Mode C LEAP stop-out at option mark

**Date:** 2026-09-22
**Time:** ended 17:20 MDT
**Duration:** one sitting
**Project:** Winston v2 (Wv2) + ecosystem ticket
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth/winston_v2`
**Branch:** `main` (started from `main`)
**Model:** Grok 4.7
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Mode C paper Long-term Equity Anticipation Security (LEAP) and `standard_call` stop-outs must sell-to-close at the option mark, not the underlying Working Stop.

**Outcome:** Delivered

**One-line summary:** Stop-out cash is contracts × option mark × 100. The Working Stop stays on the underlying as the signal.

---

## 2. Work Completed

- Confirmed the ad-hoc stamped-premium path already on `main` (`d302fdc`) passes the original Exit sell-to-close examples.
- Taught `OptionMark.for_position(live: true)` to prefer a Client Portal Gateway (CPGW) snapshot: mid of bid and ask (`cpgw_mid`), else last (`cpgw_last`), else the stamped premium (`stamped`). No Black–Scholes.
- `ExitAtStopService#exit_one` uses that live mark for both the no-draft `AdHocExitService` path and the draft Confirm path, and still stamps `exit_at_stop`.
- Locked CPGW mid, CPGW last, and draft-confirm in `mode_c_paper_leap_spec`. Stock exit-at-stop spec stayed green.
- Closed the P0 ticket and removed it from the active index.

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `winston_v2/app/services/operations/option_mark.rb` | modified | Live snapshot before stamped premium |
| `winston_v2/app/services/operations/exit_at_stop_service.rb` | modified | `for_position(position, live: true)` |
| `winston_v2/spec/integration/mode_c_paper_leap_spec.rb` | modified | Mid, last, and draft-confirm examples |
| `ecosystem/docs/tickets/archive/2026-09-20-mode-c-leap-exit-at-stop-option-mark.md` | moved | Status Done, acceptance checked |
| `ecosystem/docs/tickets/INDEX.md` | modified | Row removed |
| `ecosystem/docs/session-reports/2026-09-22-1720-mode-c-leap-exit-option-mark.md` | added | This report |

### Commits

- `2551984` on `winston_v2` `main` — fix(ops): book Mode C option stop-outs at the option mark (pushed)
- ecosystem `main` — commit that archives the ticket and adds this report (same wrap)

### Branch / PR state at sign-off

- Branch: `main` on both repos
- Pushed: Winston v2 yes; ecosystem with this report
- PR: not opened

---

## 4. Decisions Made

### Decision 1: Snapshot fields, not a bare premium
- **Choice:** A candidate counts as a CPGW snapshot only when it has bid and ask (mid) or last (`31` / `84` / `86` accepted too). A packaging `premium` alone stays `stamped`.
- **Why:** The Mode C spec's chain stub carries `premium` without a quote. Treating that as a live print would relabel the stamped fallback.
- **Alternatives considered:** New Broker Gateway quote-by-conid route.
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 2: Reuse `option_candidates` instead of a new quote route
- **Choice:** Read the desk binding (`LEAP_READ_BINDING_ID`) and match the open contract on Contract Identity, else strike + expiry + right.
- **Why:** Broker Gateway has no public snapshot-by-conid route. This session was authorized to push Winston v2 `main`, not a new gateway API.
- **Alternatives considered:** Call the gateway account snapshot (that payload is lots and cash, not an option print).
- **Reversibility:** easy — replace `cpgw_quote` when a conid snapshot exists
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- `d302fdc` had already stopped booking `units × Working Stop × 100` for the stamped-premium case. The ticket was still In progress because the CPGW branch and the draft-confirm lock were not in the spec.
- Workspace Graphify Graph did not index the Ruby services (documentation nodes only). `winston_v2/graphify-out/graph.json` is absent. The services were read from disk.

---

## 6. Issues & Tickets

### Resolved this session
- `ecosystem/docs/tickets/archive/2026-09-20-mode-c-leap-exit-at-stop-option-mark.md` — Done

### Deferred
- Quote-by-conid. Filed [`docs/tickets/2026-09-22-bg-option-snapshot-by-conid.md`](../tickets/2026-09-22-bg-option-snapshot-by-conid.md). Until then, an open contract outside the furthest-month at-the-money three keeps the stamped premium.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| LEAP / standard_call Exit sell-to-close | rspec `mode_c_paper_leap_spec` | ✅  file green, including new mid, last, and draft examples |
| Stock exit-at-stop | rspec `exit_at_stop_service_spec` | ✅ 4 examples |
| Jev / Noul harness | not run | ⚠️ deterministic specs were the gate |
| Live paper books | not touched | ✅ no Desk-Send, no journal rewrite |

**Test command(s):**

```
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 \
  bundle exec rspec spec/integration/mode_c_paper_leap_spec.rb \
  spec/services/operations/exit_at_stop_service_spec.rb --format documentation
```

The reported run used `-e Exit`, which still executed the whole Mode C file (parent example group name contains "Exit") and all four stock examples: 14 examples, 0 failures.

---

## 8. Environment, Dependencies, Data

- **Dependencies:** _None._
- **Services:** existing compose `winston_v2` used only to run rspec. No restart.
- **Migrations:** _None._

---

## 9. Risks & Technical Debt

- Stop-out of a contract that is no longer among the three nearest strikes of the furthest month books the last stamped premium even when CPGW could print that conid.
- A quote outage or missing `LEAP_READ_BINDING_ID` falls through to the stamped premium. The exit still books. It does not hard-stop the way an entry chain failure does.
- `AdHocExitService` still trusts the price it is given. Only `ExitAtStopService` swaps in the mark. A discretionary desk exit can still pass an operator price.

---

## 10. Open Questions

- **Should Broker Gateway grow a read-only snapshot by option conid?** — needs answer from: operator; blocks: live marks for contracts that have drifted off the at-the-money three.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Specs green. Ticket archived. Winston v2 `2551984` is on `origin/main`. This report lands with the ecosystem commit.
- **Next concrete step:** Implement [`docs/tickets/2026-09-22-bg-option-snapshot-by-conid.md`](../tickets/2026-09-22-bg-option-snapshot-by-conid.md) when a drifted open contract should mark live.
- **Files to read first:** `winston_v2/app/services/operations/option_mark.rb`, `exit_at_stop_service.rb`, `spec/integration/mode_c_paper_leap_spec.rb`

---

## 12. Stakeholder Communications

- _None._ Paper books were not rewritten. No Telegram.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, graphify-ponytail (query; Winston v2 code graph missing), ponytail, session-report, wrap
- **Graphify Graph:** skipped. `winston_v2/graphify-out/graph.json` is missing and was not rebuilt. Ecosystem `graphify-out/graph.json` exists, but the ecosystem worktree is full of unrelated dirty docs; an incremental update would re-extract that set. `graphify-out/` was not staged.
- **Ponytail flags:** Quote resolution stays on `OptionMark` (the existing mark helper). No new chain-walker class. Ceiling comment names the furthest-month at-the-money three limit.
- **What worked well:** The failing-spec path was already green for stamped premium, so the new work was the snapshot branch plus the draft lock.
- **Friction points:** Workspace graph query returned documentation nodes, not the Ruby call graph.
- **Subagent usage:** _None._

---

## 14. Follow-up Actions

- [x] Broker Gateway quote-by-conid — filed [`docs/tickets/2026-09-22-bg-option-snapshot-by-conid.md`](../tickets/2026-09-22-bg-option-snapshot-by-conid.md) (P2 Proposed)

---

## 15. Appendix (optional)

Law: Working Stop pierce signals the exit. The fill is the option mark. Cash = contracts × mark × 100. Stock lots still fill at the Working Stop.
