# Session Report — Walnut paper Session Order Slate (STP) first DUT round

**Date:** 2026-09-09
**Time:** ~09:40–14:44 MDT (continued from compacted session `01a07f1b`)
**Duration:** ~5h (this wrap turn; prior compaction covered morning wiring)
**Project:** sawtooth Winston ecosystem (winston_v2 + broker_gateway + ecosystem)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `winston_v2` main; `broker_gateway` main; `ecosystem` main (all dirty vs origin)
**Model:** Grok 4.6 (xAI)
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Wire Portfolio Walnut paper Trend Following (TF) to Interactive Brokers (IBKR) paper DUT through Winston v2 (Wv2) + Broker Gateway (BG): Session Order Slate of stop-market (STP) parks, Approve then per-leg Confirm = Desk Send. Operator clicks Confirm. Paper DUT only.

**Outcome:** Delivered (first round). Operator confirmed a full Walnut slate of STPs on DUT after several fail-closed loops.

**One-line summary:** Walnut slate Approve → Confirm now parks real DUT stop-market tickets; we fail closed without a broker order id, round to a 0.01 tick, initialize CPGW brokerage with `compete: true` after browser SSO, and stop lying about “needs login” from a stale poll.

---

## 2. Work Completed

- Session Order Slate UI on Walnut (`/wv2/operations/slate?portfolio_id=1428`): Approve then per-leg Confirm (send STP). Link next to the OP, Pending, portfolio detail — not the ops-shell header. Tailscale public URLs.
- Confirm in-flight UX: button → **Sending…** (gold); siblings disable; working legs show **sent** / protective **stop in place GTC**.
- Fail-closed: HTTP 200 without an IBKR `order_id` is **not** submitted. Journals stay draft. Evidence is not `order.upserted`.
- CPGW STP ticket: `{orders:[ticket]}`, stop on **`price` and `auxPrice`**, integer whole-share qty, walk confirmation **arrays and hashes**, recover id from DUT book by `cOID` if POST body empty.
- CPGW brokerage init: `ssodh/init` **`compete: true`** (SSO-connected ≠ iserver authenticated; `compete: false` returned “Force compete capability must be used together with compete flag”).
- Login banner: live DUT **snapshot**, not `last_refresh_status`. Successful place/snapshot stamps binding `ok`.
- Tick size: US stock STP rounded to **$0.01**. DD BUY 148.7655 was rejected by CPGW (“minimum price variation of 0.01”); send 148.77.
- False-working journals (working, no DUT id) voided on slate rebuild. Slate #1 cancelled; draft #12 approved and parked.
- Operator completed one round of Walnut STPs on DUT. DBC 282 long remains the booked lot; protective GTC verified on the IBKR blotter after the STP ticket fix.

**Standing constraint honored:** agent never Desk-Sent. Operator clicked Confirm.

---

## 3. Code Delivered

### Files changed (this session — not other dirty-tree work)

Winston v2:

| File | Change | Notes |
|------|--------|-------|
| `app/controllers/operations/slates_controller.rb` | added | rebuild / approve / confirm; live login probe |
| `app/views/operations/slates/*` | added | slate show + legs table + Sending… |
| `app/models/session_order_slate.rb` | added | draft/approved desk |
| `app/services/operations/session_order_slate/` | added | Builder, Approve; 2dp entry stops |
| `db/migrate/20260909180000_create_session_order_slates.rb` | added | |
| `app/services/operations/ibkr_session_probe.rb` | added | live snapshot = needs_login |
| `app/services/quiver_tracking/wq_confirm_send.rb` | modified | require broker_order_id; 0.01 tick; re-send unparked working |
| `app/services/operations/journal_confirmation_service.rb` | modified | TF send; re-send working-without-oid |
| `app/services/broker_gateway/client.rb` | modified | 422+order 401 → auth_failed |
| `app/services/operations/fulfillment_catalog.rb` | modified | 15s TTL |
| `app/services/operations/fulfillment_desk.rb` | modified | compete=true ritual |
| `app/assets/stylesheets/ops_shell.css` | modified | Sending… / disabled Confirm |
| `app/controllers/operations/portfolios_controller.rb` | modified | OpsPath.join slate |
| `config/routes.rb` | modified | slate routes |
| `spec/requests/operations_slate_spec.rb` | added | rebuild/approve/sent/banner |
| `spec/services/quiver_tracking/wq_confirm_send_spec.rb` | modified | fail-closed, tick, re-send |
| `spec/services/broker_gateway/client_spec.rb` | modified | 422→auth_failed |
| `spec/services/operations/ibkr_session_probe_spec.rb` | added | |

Broker Gateway:

| File | Change | Notes |
|------|--------|-------|
| `app/services/adapters/ibkr_adapter.rb` | modified | STP ticket, confirm hops, fail-closed, 0.01 tick, CPGW error text |
| `app/services/adapters/ibkr/session.rb` | modified | `ssodh/init` compete: true |
| `app/services/evidence/place_order_service.rb` | modified | no upsert without order id; stamp auth |
| `app/services/evidence/account_snapshot_service.rb` | modified | stamp last_refresh_status from live snap |
| matching specs | modified | |

Ecosystem (docs already in tree; report added this wrap):

| File | Change | Notes |
|------|--------|-------|
| `docs/session-reports/2026-09-09-1444-walnut-paper-stp-slate.md` | added | this report |
| `docs/tickets/2026-09-09-walnut-paper-session-order-slate.md` | present | still Proposed; cancel/replace open |
| `CONTEXT.md` / ADR-013 | modified | earlier in compacted stretch |

### Commits

- `winston_v2` `5709942` — feat(slate): Walnut Session Order Slate Confirm=Send STP on paper DUT
- `broker_gateway` `d5b4d3b` — fix(ibkr): fail-closed STP place, compete init, 0.01 tick
- `ecosystem` `df13182` — docs: Walnut first STP slate round + follow-up tickets

### Branch / PR state at sign-off

- Branch: `main` on wv2, BG, ecosystem
- Pushed: this wrap
- PR: not opened (commits on `main`)

**Do not** `git add .`. Other dirty files (Pulse, WEV, quiver jobs, `vendor/`, `tmp/pids`) are **not** this session.

---

## 4. Decisions Made

### Decision 1: Fail closed without DUT order id
- **Choice:** CPGW 200 with no `order_id` is rejected; journal stays draft.
- **Why:** First round marked 20 journals working with empty `external_order_id`; DUT book was empty.
- **Alternatives considered:** Trust HTTP 200; treat confirmation `id` as order id (dangerous).
- **Reversibility:** easy
- **Promote to ADR?** no — operationalization of ADR-013 fail-closed

### Decision 2: STP stop on `price` + `auxPrice`
- **Choice:** IBKR Campus: STP trigger is `price`; STPLMT uses `auxPrice`. Send both for STP.
- **Why:** auxPrice-only POSTs returned 200 empty.
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 3: `ssodh/init` compete true
- **Choice:** After browser SSO, init brokerage with `{publish: true, compete: true}`.
- **Why:** `connected: true, authenticated: false`; compete:false → CPGW fail “Force compete…”. Operator login page ≠ iserver.
- **Alternatives considered:** compete:false to spare TWS (broke the desk).
- **Reversibility:** easy; TWS on the same paper user will get kicked
- **Promote to ADR?** no; note on existing unattended-session ticket

### Decision 4: Login banner = live snapshot
- **Choice:** Slate banner only if live DUT snapshot is `auth_failed`.
- **Why:** Stale `last_refresh_status` lied after a parked stop.
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 5: Stock STP ticks are $0.01
- **Choice:** Round stop to 2 decimals on send (and new slate entry legs).
- **Why:** DD 148.7655 rejected by CPGW min variation 0.01.
- **Alternatives considered:** per-conid IBKR info-and-rules (later).
- **Reversibility:** easy
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- Browser CPGW “logged in” is **SSO**. Trading needs **iserver** (`authenticated` + `established`). Tickle keeps SSO; it does not init brokerage.
- Confirmation dialogs may be a **hash**, not an array; reply `id` is not `order_id`.
- Parquet 55-day highs at 4 decimals are not IBKR stock ticks.
- `already_working` without a broker id made a second Confirm a no-op. Rebuild voids those journals.
- DUT paper Client Portal **web** is statements/reset, not the working-order blotter. Use IBKR Desktop / TWS Pending — but not concurrent with CPGW compete.

---

## 6. Issues & Tickets

### Resolved this session
- False working journals / empty DUT book after STP Confirm — fail-closed + rebuild
- 401 mislabeled as 422 rejected — map CPGW 401 → `auth_failed`
- Stale “needs login” banner — live snapshot
- SSO-up / iserver-down — compete:true init
- DD STP 148.7655 tick reject — round 0.01

### Deferred
- **BG cancel + replace** still refused — already [`2026-09-09-walnut-paper-session-order-slate.md`](../tickets/2026-09-09-walnut-paper-session-order-slate.md) (wrap skip new ticket)
- **Accept-Fill at DUT print** — [`2026-09-09-walnut-stp-accept-fill-day-entry.md`](../tickets/2026-09-09-walnut-stp-accept-fill-day-entry.md)
- **After cash close reconcile** — [`2026-09-09-walnut-day-stp-close-reconcile.md`](../tickets/2026-09-09-walnut-day-stp-close-reconcile.md)
- **Unattended CPGW** — already [`2026-09-06-ibkr-cpgw-unattended-session.md`](../tickets/2026-09-06-ibkr-cpgw-unattended-session.md) (wrap skip new ticket)
- **Per-instrument tick** — [`2026-09-09-ibkr-stp-tick-size.md`](../tickets/2026-09-09-ibkr-stp-tick-size.md)
- Other dirty-tree work (Pulse, WEV, quiver jobs) not in this commit

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| BG adapter STP / fail-closed / tick / compete | `bundle exec rspec spec/services/adapters/ibkr_adapter_spec.rb spec/services/adapters/ibkr/session_spec.rb spec/services/evidence/place_order_service_spec.rb` | ✅ |
| Wv2 slate + Confirm + probe | `podman exec winston_v2 bundle exec rspec spec/requests/operations_slate_spec.rb spec/services/quiver_tracking/wq_confirm_send_spec.rb spec/services/operations/ibkr_session_probe_spec.rb` | ✅ (test DB missing in container; ran against dev with transaction rollback; 2 pre-existing isolation fails on MKT count vs live OP lots — not this change) |
| DUT live | Operator parked STPs including DBC GTC; DD failed then succeeded after tick round | ✅ operator |
| Browser UI (slate Sending / banner) | Operator used Tailscale slate; no agent browser | ⚠️ operator-verified only |

**Test command(s):** see table.

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new
- **Services:** compose `winston_v2`, `broker_gateway`, CPGW `https://localhost:5000` (host), Tailscale Serve `/wv2`
- **Migrations:** `winston_v2` `20260909180000_create_session_order_slates` (apply on any host that does not already have `session_order_slates`)
- **Live objects:** Walnut OP #1428; slate #12 approved; DBC 282 long @ ~32.84 on DUT; DUT account DUT070450

---

## 9. Risks & Technical Debt

- `compete: true` kicks TWS on the same paper username
- 0.01 tick is wrong for some products
- Cancel/replace still off → DAY rebuild cannot honestly cancel unfilled DAY STPs; GTC cannot move
- Wv2 `main` dirty with unrelated Pulse/WEV/quiver files — wrap must not `git add .`
- Confirmation-intake job still polls; can flap `last_refresh_status` even when slate probe is live

---

## 10. Open Questions

- **Did every DAY STP remain working on DUT through the cash close?** — needs operator blotter after 16:00 ET; blocks Accept-Fill proof
- **Should slate rebuild after the close expire unfilled DAY journals?** — blocked on cancel
- **SCHZ 892 units** — still a cash/notional concern if parked

---

## 11. Handoff & Resume Notes

- **Where I left off:** Operator completed one Walnut STP round. Tick round + compete init + fail-closed in bind-mounted code. Wrap report written; commits pending follow-up promotion.
- **Next concrete step:** After cash close, compare DUT working orders vs Walnut working journals; then BG cancel/replace (ticket).
- **Files to read first:**
  1. `ecosystem/docs/tickets/2026-09-09-walnut-paper-session-order-slate.md`
  2. `broker_gateway/app/services/adapters/ibkr_adapter.rb` (`live_place_order`, `confirm_ibkr_replies`)
  3. `broker_gateway/app/services/adapters/ibkr/session.rb` (`authenticate`)
  4. `winston_v2/app/services/quiver_tracking/wq_confirm_send.rb`
  5. `winston_v2/app/services/operations/ibkr_session_probe.rb`

Slate URL: `https://sawtooth-ai.tail944ffb.ts.net/wv2/operations/slate?portfolio_id=1428`

---

## 12. Stakeholder Communications

- Operator (John) is the audience. No outward email.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, wrap, session-report
- **What worked well:** fail-closed + raw CPGW body in BG log (`place_order no broker_order_id … raw=`) made DD tick diagnosis one grep
- **Friction points:** CPGW SSO vs iserver; confirmation shapes; 4-decimal parquet highs; wrap dirty trees mixing sessions
- **Subagent usage:** none this wrap turn

---

## 14. Follow-up Actions

- [ ] BG paper DUT **cancel + replace** — already [`../tickets/2026-09-09-walnut-paper-session-order-slate.md`](../tickets/2026-09-09-walnut-paper-session-order-slate.md)
- [ ] Prove **Accept-Fill** at DUT print for a DAY entry — [`../tickets/2026-09-09-walnut-stp-accept-fill-day-entry.md`](../tickets/2026-09-09-walnut-stp-accept-fill-day-entry.md)
- [ ] After cash close: reconcile DUT working vs Walnut journals — [`../tickets/2026-09-09-walnut-day-stp-close-reconcile.md`](../tickets/2026-09-09-walnut-day-stp-close-reconcile.md)
- [ ] Per-conid tick if a name is not 0.01 — [`../tickets/2026-09-09-ibkr-stp-tick-size.md`](../tickets/2026-09-09-ibkr-stp-tick-size.md)
- [ ] CPGW unattended session — already [`../tickets/2026-09-06-ibkr-cpgw-unattended-session.md`](../tickets/2026-09-06-ibkr-cpgw-unattended-session.md)
- [x] Walnut slate ticket: first STP round done; cancel/replace still open — [`../tickets/2026-09-09-walnut-paper-session-order-slate.md`](../tickets/2026-09-09-walnut-paper-session-order-slate.md) In progress

---

## 15. Appendix

CPGW DD reject (2026-09-09 ~20:13 UTC):

```
The price 148.7655 does not conform to the minimum price variation of 0.01 for this instrument.
```

CPGW SSO-only (before compete init):

```
authenticated: false, established: false, connected: true
fail: "Force compete capability must be used together with compete flag"
```

After `POST /iserver/auth/ssodh/init {"publish":true,"compete":true}`:

```
authenticated: true, established: true, connected: true
```
