# Session Report — ADR-013 paper DUT WQ Confirm-Send

**Date:** 2026-09-06
**Time:** wrap 19:07 MDT (session continued from compacted WQ/IBKR realignment → grill → implement)
**Duration:** ~same-day continuation (law accepted, then implementation authorized and shipped)
**Project:** Winston ecosystem — Broker Gateway (BG), Winston v2 (Wv2), Winston Quiver (WQ) paper
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on `ecosystem`, `winston_v2`, `broker_gateway` (started from `origin/main`; **dirty, uncommitted** at wrap)
**Model:** Grok 4.6 (xAI)
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Implement ADR-013 this session: paper DUT write behind the kill switch; WQ Confirm Desk Sends one regular-hours market order; journal stays working until Accept-Fill at the print. Dummy-sim Confirm still books immediately. Do not concretize the IBKR adapter as market-only.

**Outcome:** Delivered. Paper DUT `place_order` is live on binding `bnd_3d6a5020d839c315583277d2` (`cap_order_write` true, `BG_IBKR_ORDER_WRITE=true`, live write still false). No live paper order was sent from this session — Confirm on the tracking desk is the send click.

**One-line summary:** WQ Confirm on the IBKR-paper Shadow Portfolio now sends one market order to paper DUT and books only when the fill prints.

---

## 2. Work Completed

### Law (prior segment of this session, accepted)

- ADR-013 accepted: first write is IBKR **paper DUT**, not live Schwab. WQ Confirm = Desk Send of one regular-hours MKT. Journal **working** until matched print Accept-Fills. Market-only is WQ packaging policy, not the IBKR adapter. dummy_sim Confirm still books. Mint/TF Confirm stays book-only.

### Broker Gateway write path

- `Adapters::WritePolicy`: sandbox IBKR + `BG_IBKR_ORDER_WRITE=true` only; live IBKR / dummy_sim / Schwab refuse.
- Binding may persist `cap_order_write` only when WritePolicy allows; otherwise forced false.
- `IbkrAdapter#place_order` transports **MKT, LMT, STP, STPLMT**. Fixture path when `BG_IBKR_LIVE_READ` is off; live POST `/iserver/account/{acct}/orders` + reply-confirm loop when live-read is on.
- `Evidence::PlaceOrderService` + `POST /api/v1/bindings/:id/orders`. Basket (`orders` / `intents` array) refused.
- `cancel_order` / `replace_order` still CapabilityGate-refused.
- Recreated `broker_gateway` + `broker_gateway_sidekiq` so `ibkr.env` kill switch loaded. Enabled `cap_order_write` on DUT binding.

### Winston v2 Confirm-Send

- `QuiverTracking::WqConfirmSend` — IBKR-bound WQ Confirm places one MKT; journal `working`; idempotent `client_order_key` `wq-{plan_id}-{task_id}`.
- `QuiverTracking::WqExitGate` — exits before rebalances/enters.
- `QuiverTracking::WqFillBind` — Accept-Fill at DUT print (qty/price), including `drop_book` close.
- `Population.confirm` intercepts IBKR-bound WQ; dummy_sim path unchanged.
- `JournalConfirmationService` treats `drop_book` as exit (was only `"exit"`; TaskMinter mints `drop_book` — root of ghost journal #1279).
- PrefillFromMatch attaches fill evidence to a **working** journal without DraftEdit (draft-only editor).
- Tracking desk copy: IBKR-bound Confirm button reads **Confirm (send MKT)**.

### Ops

- Dummy_sim `POST …/orders` on compose: HTTP 403 `adapter_key dummy_sim is not IBKR paper write`.
- DUT binding capabilities now include `order_write: true`.
- `compose.yml` comment updated (workspace root; **no git** at sawtooth root).
- Did **not** reverse ghost journal #1279. Did **not** click Confirm against live DUT.

---

## 3. Code Delivered

### Files changed

#### ecosystem (uncommitted at wrap)

| File | Change | Notes |
|------|--------|-------|
| `docs/adr/ADR-013-fulfillment-write-ibkr-paper-wq.md` | added | Accepted law + 2026-09-06 implementation note |
| `docs/adr/ADR-009-human-gated-desk-and-fulfillment.md` | modified | Points at ADR-013 carve-out |
| `CONTEXT.md` | modified | Plan Approve / Working WQ Leg / Confirm-Send |
| `docs/tickets/2026-08-30-wq-phase4-one-at-a-time-send.md` | modified | Status Done; paper DUT not Schwab |
| `docs/tickets/INDEX.md` | modified | Phase 4 Done |
| `plans/production-ready-wq.md` | modified | §8 paper DUT shipped |
| `deployment/ibkr-webapi-template.txt` | modified | `BG_IBKR_ORDER_WRITE` default false |
| `docs/session-reports/2026-09-06-1907-adr-013-wq-confirm-send.md` | added | this report |

Not for this commit: `plans/cromwell-staff-roster.md` (unrelated untracked), `vendor/` (Client Portal Gateway vendor tree).

#### broker_gateway (uncommitted at wrap)

| File | Change | Notes |
|------|--------|-------|
| `app/services/adapters/write_policy.rb` | added | ADR-013 allow/refuse |
| `app/services/evidence/place_order_service.rb` | added | one Order Intent; basket refuse |
| `app/services/evidence/account_snapshot_service.rb` | added | L2 snapshot (prior segment) |
| `app/services/adapters/ibkr_adapter.rb` | modified | `place_order` MKT/LMT/STP/STPLMT |
| `app/services/adapters/ibkr/session.rb` | modified | `post_json_response` |
| `app/services/adapters/ibkr/normalizer.rb` | modified | L2 lots/cash (prior segment) |
| `app/models/adapter_binding.rb` | modified | persist write only if policy allows |
| `app/services/adapters/capability_gate.rb` | modified | cite ADR-013 |
| `app/services/adapters/capability_profile.rb` | modified | registry still default write false |
| `app/controllers/api/v1/bindings_controller.rb` | modified | POST orders + snapshot |
| `config/routes.rb` | modified | `post :orders` |
| `config/environments/development.rb` | modified | `config.hosts << "broker_gateway"` |
| `app/services/evidence/refresh_service.rb` | modified | no longer refuse write-capable bindings |
| `AGENTS.md`, `README.md` | modified | paper DUT write |
| specs listed in git status | added/modified | WritePolicy, place_order, request orders, IBKR fixtures |
| `lib/adapters/ibkr/fixtures/{ledger,positions}.json` | added | L2 fixtures |

Not for this commit: `tmp/pids/`, `vendor/`.

#### winston_v2 (uncommitted at wrap)

| File | Change | Notes |
|------|--------|-------|
| `app/services/quiver_tracking/wq_confirm_send.rb` | added | Confirm = Desk Send MKT |
| `app/services/quiver_tracking/wq_exit_gate.rb` | added | exits first |
| `app/services/quiver_tracking/wq_fill_bind.rb` | added | Accept-Fill at print |
| `app/services/quiver_tracking/ibkr_paper_sync.rb` | added | Pull from IBKR paper (prior segment) |
| `app/services/quiver_tracking/plan_repricer.rb` | added | parquet data_ready (prior) |
| `app/services/quiver_tracking/ensure_markets.rb` | added | catalog names (prior) |
| `app/controllers/quiver_tracking/ibkr_sync_controller.rb` | added | Pull from IBKR paper |
| `app/services/quiver_tracking/population.rb` | modified | IBKR intercept; attach_reweight_journal |
| `app/services/operations/journal_confirmation_service.rb` | modified | `drop_book` as exit |
| `app/models/journal.rb` | modified | `working` status + scope |
| `app/services/broker_gateway/client.rb` | modified | `place_order` |
| `app/services/confirmation_intake/*` | modified | working journals; reweight sides; working prefill |
| `app/views/quiver_tracking/_pending.html.erb` | modified | Confirm (send MKT) |
| plus parquet_demand, plan_builder, ingest, live snapshot, current_upload, routes, specs | modified/added | same session |

#### workspace root (no git)

| File | Change | Notes |
|------|--------|-------|
| `compose.yml` | modified | comment only — paper DUT write is ADR-013 |

Gitignored (not committed): `ecosystem/deployment/ibkr.env` now has `BG_IBKR_ORDER_WRITE=true` / `BG_IBKR_ORDER_WRITE_LIVE=false`.

### Commits

- _None yet — wrap paused at follow-up promotion._

### Branch / PR state at sign-off

- Branch: `main` on all three repos — dirty
- Pushed: no
- PR: not opened

---

## 4. Decisions Made

### Decision 1: ADR-013 is the fulfillment-write law
- **Choice:** `order_write` is governed by ADR-013, not ADR-010 (Risk Scale).
- **Why:** Number collision was blocking write; operator lock was paper DUT first.
- **Alternatives considered:** Hide Confirm until cash session; book last-close now; per-leg limit HITL from day one.
- **Reversibility:** easy — turn `cap_order_write` / `BG_IBKR_ORDER_WRITE` off.
- **Promote to ADR?** Done — ADR-013 Accepted.

### Decision 2: WQ Confirm on IBKR paper is Desk Send MKT
- **Choice:** Confirm sends one regular-hours market order; journal working until print.
- **Why:** Booking last-close on Sunday vs Monday print is the drift just unwound; hiding Confirm fights how the operator works the Monday package.
- **Alternatives considered:** Hide until open; book now / DUT later; always-market adapter.
- **Reversibility:** easy (kill switch). Confirm ≠ Send remains default for TF/live.
- **Promote to ADR?** In ADR-013 §3.

### Decision 3: Adapter keeps LMT/STP/STPLMT
- **Choice:** Market-only is WQ Fulfillment Packaging Policy, not `interactive_broker_trader_api`.
- **Why:** Paper Mint on the same DUT will need Session Order Slate (stops, exits, pyramids).
- **Reversibility:** easy.
- **Promote to ADR?** In ADR-013 §4.

---

## 5. Insights Surfaced

- TaskMinter mints `drop_book`; JournalConfirmationService previously closed lots only on `task_type == "exit"`. Confirm of SPCX stamped journal #1279 executed with flow 0 and left the lot OPEN — ghost desk, not DUT.
- Compose `env_file` is baked at container create. Editing `ibkr.env` does not load until `broker_gateway` is recreated.
- `force-recreate` of BG also bounced redis/bg_postgres and left `winston_unit_test` in a name-in-use state until `podman start`.
- Wv2 specs in compose must use `-e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres` or they hit the development book (#1372, 13 names).
- Confirmation Intake match specs using fixture `occurred_at: 2026-08-19` and `WINDOW_DAYS = 7` are date-fragile as of 2026-09-06 (orphan). Pre-existing; not caused by Accept-Fill.

---

## 6. Issues & Tickets

### Resolved this session
- ADR-013 numbered; CapabilityGate cites it.
- Paper DUT `place_order` behind kill switch + `cap_order_write`.
- WQ Confirm-Send MKT; working until Accept-Fill.
- `drop_book` treated as exit on dummy_sim confirm and on DUT Accept-Fill.
- Ticket `2026-08-30-wq-phase4-one-at-a-time-send.md` marked Done (paper DUT, not live Schwab).

### Deferred
- Ghost journal #1279 — See: [`docs/tickets/2026-09-06-wq-ghost-journal-1279-spcx.md`](../tickets/2026-09-06-wq-ghost-journal-1279-spcx.md)
- First operator Confirm-Send against live paper DUT — See: [`docs/tickets/2026-09-06-wq-first-dut-confirm-send-proof.md`](../tickets/2026-09-06-wq-first-dut-confirm-send-proof.md)
- IBKR overnight/queue of regular-hours MKT when cash is closed — See: [`docs/tickets/2026-09-06-ibkr-day-mkt-closed-cash-queue.md`](../tickets/2026-09-06-ibkr-day-mkt-closed-cash-queue.md)
- `fill_units` / `resolved_units` `to_i` dropping fractional units — See: [`docs/tickets/2026-09-06-fractional-units-toi-confirm.md`](../tickets/2026-09-06-fractional-units-toi-confirm.md)
- Date-fragile Confirmation Intake match specs — See: [`docs/tickets/2026-09-06-intake-match-fixture-window.md`](../tickets/2026-09-06-intake-match-fixture-window.md)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| BG WritePolicy / place_order / request orders | rspec in compose test DB | ✅ 56 examples, 0 failures |
| Wv2 Confirm-Send / FillBind / ExitGate / drop_book / dummy_sim population | rspec in compose test DB | ✅ 44 examples, 0 failures |
| dummy_sim HTTP place_order | `POST /api/v1/bindings/{dummy}/orders` | ✅ 403 refused |
| DUT binding write cap | `GET /api/v1/bindings/bnd_3d6a5020d839c315583277d2` | ✅ `order_write: true`, env sandbox |
| Live paper DUT order | Confirm click / CPGW POST | ❌ not sent |
| Overnight MKT queue | DUT when cash closed | ❌ not verified |
| Confirmation Intake match specs (fixture dates) | rspec isolation | ⚠️ 5 failures, date window |

**Test command(s):**

```bash
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=bg_postgres -e BG_IBKR_LIVE_READ=false broker_gateway \
  bundle exec rspec spec/models/adapter_binding_spec.rb spec/services/adapters/write_policy_spec.rb \
  spec/services/adapters/capability_gate_spec.rb spec/services/adapters/ibkr_adapter_spec.rb \
  spec/services/adapters/dummy_adapter_spec.rb spec/services/evidence/place_order_service_spec.rb \
  spec/requests/api_v1_bindings_spec.rb

./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 \
  bundle exec rspec spec/services/quiver_tracking/wq_confirm_send_spec.rb \
  spec/services/quiver_tracking/wq_fill_bind_spec.rb spec/services/quiver_tracking/wq_exit_gate_spec.rb \
  spec/services/quiver_tracking/population_spec.rb spec/services/broker_gateway/client_spec.rb \
  spec/services/operations/journal_confirmation_service_spec.rb \
  spec/requests/quiver_tracking_population_spec.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None added.
- **Services:** Recreated `broker_gateway`, `broker_gateway_sidekiq`, `bg_postgres`; redis bounced; `winston_unit_test` restarted after name conflict. `BG_IBKR_LIVE_READ=true` still on for CPGW snapshots. Kill switch now loaded in the BG container.
- **Migrations:** None.
- **Runtime flag:** DUT binding `cap_order_write=true` in **development** BG DB (not in git).

---

## 9. Risks & Technical Debt

- Confirm on `/quiver_tracking` now **is** paper DUT IO. Accidental click sends a market order (queued if cash closed).
- Live write uses the same CPGW session as live read (`BG_IBKR_LIVE_READ`). Auth-failed refuses write, but a healthy paper SSO will send.
- Ghost #1279 still on the WQ blotter; a later SPCX exit could double-count if not cleaned.
- Fractional `to_i` on units remains a landmine for BRK-B / MSFT / NVDA-sized lots.
- `compose.yml` change lives only on the workspace filesystem (no root git).

---

## 10. Open Questions

- **Does the operator want ghost journal #1279 reversed / lot left for the Monday IBM+SPCX exit package?** — operator; blocks blotter honesty vs DUT.
- **First Confirm-Send which name?** IBM 5.8377 and SPCX 6.2703 were the Monday exits. — operator; blocks first live paper proof.
- **When cash is closed, does DUT actually queue a DAY MKT until the next regular session?** — DUT observation; blocks weekend Confirm confidence.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Implementation shipped; DUT write cap on; no Confirm click; wrap at follow-up promotion.
- **Next concrete step:** Operator Confirm on one approved **exit** (IBM or SPCX) during or after the cash session; watch journal stay working then Accept-Fill at print. Or reverse #1279 first.
- **Files to read first:**
  1. `ecosystem/docs/adr/ADR-013-fulfillment-write-ibkr-paper-wq.md`
  2. `winston_v2/app/services/quiver_tracking/wq_confirm_send.rb`
  3. `broker_gateway/app/services/adapters/write_policy.rb`
  4. This report §6 / §14

---

## 12. Stakeholder Communications

- Operator (johnkoisch): Confirm on the WQ desk now means paper DUT market send. Say so before the next Monday package.
- AlexKoisch: not in this wrap; prior Schwab 5-long paste overwrite is historical context only.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose; session-report; wrap (this step).
- **What worked well:** kill switch + binding flag as two keys; fixture write specs with `LIVE_READ=false`; dummy_sim population specs still book.
- **Friction points:** compose exec without `RAILS_ENV=test` hits the live WQ book; `env_file` requires recreate; `force-recreate` collateral on redis/WUT.
- **Subagent usage:** _None._

---

## 14. Follow-up Actions

- [ ] Reverse or leave ghost journal #1279 — See: [`docs/tickets/2026-09-06-wq-ghost-journal-1279-spcx.md`](../tickets/2026-09-06-wq-ghost-journal-1279-spcx.md)
- [ ] First paper DUT Confirm-Send on one exit — See: [`docs/tickets/2026-09-06-wq-first-dut-confirm-send-proof.md`](../tickets/2026-09-06-wq-first-dut-confirm-send-proof.md)
- [ ] Observe DUT DAY MKT queue when cash is closed — See: [`docs/tickets/2026-09-06-ibkr-day-mkt-closed-cash-queue.md`](../tickets/2026-09-06-ibkr-day-mkt-closed-cash-queue.md)
- [ ] Fractional units `to_i` on confirm/sizer — See: [`docs/tickets/2026-09-06-fractional-units-toi-confirm.md`](../tickets/2026-09-06-fractional-units-toi-confirm.md)
- [ ] Freeze Confirmation Intake match fixture window — See: [`docs/tickets/2026-09-06-intake-match-fixture-window.md`](../tickets/2026-09-06-intake-match-fixture-window.md)

---

## 15. Appendix

DUT binding at wrap:

```
bnd_3d6a5020d839c315583277d2 interactive_broker_trader_api sandbox write=True
```

Kill switch in BG container: `BG_IBKR_ORDER_WRITE=true`, `BG_IBKR_ORDER_WRITE_LIVE=false`, `BG_IBKR_LIVE_READ=true`.

Client order key shape: `wq-{plan_id|np}-{task_id|journal_id}`.
