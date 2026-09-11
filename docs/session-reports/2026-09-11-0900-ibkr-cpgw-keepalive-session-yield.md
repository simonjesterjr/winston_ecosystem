# Session Report — IBKR CPGW keep-alive window + Session Yield

**Date:** 2026-09-11
**Time:** ~08:12–09:00 MDT
**Duration:** ~50m
**Project:** Winston ecosystem — Broker Gateway (BG), Winston v2 (Wv2), ecosystem contractor docs
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on `ecosystem`, `broker_gateway`, `winston_v2` (each dirty with other grains; this session’s files listed in §3)
**Model:** Grok 4.6 (xAI)
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** (1) Status of the Interactive Brokers (IBKR) Client Portal Gateway (CPGW) session and the turn-up / keep-alive / turn-down protocol. (2) Programmatic and non-programmatic up/down; stop 24×7 401 tickle; explain duration of Thursday’s DAY-order updates. (3) Override so Winston yields the paper session to IBKR Desktop; fix ops-shell **All adapters** header.

**Outcome:** Delivered (ops-shell click not browser-verified).

**One-line summary:** One paper Single Sign-On (SSO) on 9 Sep held ~44.5 hours via CPGW self-tickle; keep-alive is now an explicit window; Session Yield on the Fulfillment Desk binding page stops compete so Desktop can hold the same paper username.

---

## 2. Work Completed

- Probed live CPGW: Java up since 31 Aug on `:5000`; brokerage session **401** after DNS `api.ibkr.com` at **04:57–04:58 MDT**; keep-alive later **off**. IBKR Desktop also running (compete risk).
- Log reconstruction: paper SSO **Wed 9 Sep 08:26:28 MT**; **Thu 10 Sep zero browser logins**; `tickle,200` all 24 hours; DAY-order polls were leftover keep-alive, not a stealth re-login. Hold **09-09 08:26 → 09-11 04:56 (~44.5h)**. Idle ~6 min is without tickle; logged-in CPGW self-tickles ~30s.
- Lifecycle CLI `ecosystem/deployment/bin/run-ibkr-cpgw` (`status|start|stop|up|down|keepalive on|off`). Eclipse Temurin 17 = vendored OpenJDK 17 JRE, not IBKR software.
- BG `TickleJob` gated on `broker_gateway/tmp/ibkr_keepalive.on`; 401/error **closes** the window. Sidekiq restarted.
- **Session Yield** on Adapter Binding: `operator_holds_session` / `operator_holds_until`; API `POST /api/v1/bindings/:id/session_yield`; TickleJob, live poll, Desk Send fail closed; keep-alive off; best-effort CPGW logout.
- Wv2 Fulfillment Desk: yield form on IBKR binding detail; glance tag **Desktop holds session**; adapter-class rows link to binding details.
- Ops-shell header: desktop `pointer-events: none` on `<summary>` only re-enabled Quiver Tracking + Refresh — **All adapters** / **Ecosystem** were unclickable. CSS now enables all header `a`/`button`.
- Glossary: **Session Yield**; Fulfillment Ritual / Desk updated. Runbook `docs/operations/ibkr-cpgw.md`. Skill `ibkr-cpgw`. Ticket `2026-09-06-ibkr-cpgw-unattended-session.md` In progress (spike done; Winston-owned window still open).

---

## 3. Code Delivered

### Files changed (this session only)

**ecosystem**

| File | Change | Notes |
|------|--------|-------|
| `CONTEXT.md` | modified | Session Yield; ritual; Desk exception |
| `AGENTS.md` | modified | `/ibkr-cpgw` skill |
| `deployment/bin/run-ibkr-cpgw` | modified | lifecycle CLI |
| `deployment/ibkr-webapi-template.txt` | modified | keep-alive window comments |
| `docs/operations/ibkr-cpgw.md` | added | SOT runbook |
| `docs/operations/README.md` | modified | index row |
| `docs/tickets/2026-09-06-ibkr-cpgw-unattended-session.md` | modified | spike + remaining scope |
| `docs/tickets/2026-09-06-wv2-fulfillment-label-and-desk.md` | modified | Session Yield write |
| `docs/tickets/INDEX.md` | modified | ticket status |
| `.gitignore` | modified | `gw.pid` |
| `.grok/skills/ibkr-cpgw/SKILL.md` | added | |
| `docs/session-reports/2026-09-11-0900-ibkr-cpgw-keepalive-session-yield.md` | added | this report |

**broker_gateway**

| File | Change | Notes |
|------|--------|-------|
| `app/services/adapters/ibkr/keepalive.rb` | added | flag file |
| `app/services/adapters/ibkr/session_yield.rb` | added | yield + expire |
| `app/jobs/adapters/ibkr/tickle_job.rb` | modified | keepalive + yield gates |
| `app/services/adapters/ibkr/session.rb` | modified | keepalive, logout |
| `app/services/adapters/ibkr_adapter.rb` | modified | refuse when yielded |
| `app/models/adapter_binding.rb` | modified | `session_yielded?` |
| `app/controllers/api/v1/bindings_controller.rb` | modified | `session_yield` |
| `config/routes.rb` | modified | member POST |
| `config/sidekiq_schedule.yml` | modified | comment |
| `db/migrate/20260911140000_adapter_binding_session_yield.rb` | added | |
| `db/schema.rb` | modified | two columns |
| `README.md` | modified | `up`/`down` |
| `AGENTS.md` | modified | skill |
| `spec/jobs/adapters/ibkr/tickle_job_spec.rb` | modified | |
| `spec/requests/api_v1_bindings_spec.rb` | modified | session_yield |
| `spec/services/adapters/ibkr/keepalive_spec.rb` | added | |
| `spec/services/adapters/ibkr/session_yield_spec.rb` | added | |
| `.grok/skills/ibkr-cpgw/SKILL.md` | added | |

**winston_v2**

| File | Change | Notes |
|------|--------|-------|
| `app/assets/stylesheets/ops_shell.css` | modified | header pointer-events |
| `app/controllers/operations/fulfillments_controller.rb` | modified | `session_yield` |
| `config/routes.rb` | modified | POST session_yield |
| `app/services/broker_gateway/client.rb` | modified | `session_yield` (`until_at`) |
| `app/services/operations/fulfillment_{desk,label,catalog}.rb` | modified | yield fields |
| `app/services/operations/ops_shell_panels.rb` | modified | glance thread |
| `app/views/operations/fulfillments/{index,show}.html.erb` | modified | links + form |
| `app/views/operations/shared/_fulfillment_glance.html.erb` | modified | Desktop tag |
| `app/views/operations/home/_panels.html.erb` | modified | |
| `app/views/operations/portfolios/show.html.erb` | modified | |
| `app/views/operations/slates/show.html.erb` | modified | |
| `app/views/quiver_tracking/home/index.html.erb` | modified | |
| `spec/requests/operations_fulfillment_spec.rb` | modified | |
| `spec/services/operations/fulfillment_{desk,label}_spec.rb` | modified | |

Not this session (leave dirty): Wv2 WEV/graphify/WQ files; BG cancel_order specs; skill-mirror churn; `ecosystem/deployment/ibkr.env` (gitignored). Workspace-root `AGENTS.md` / `.grok/skills/ibkr-cpgw` have **no git**.

### Commits

- _Pending wrap commit._

### Branch / PR state at sign-off

- Branch: `main` on each repo — dirty
- Pushed: no
- PR: not opened (direct `main`)

---

## 4. Decisions Made

### Decision 1: Keep-alive is an explicit window
- **Choice:** `TickleJob` no-ops unless `tmp/ibkr_keepalive.on`; 401 deletes the flag. `down` stops Java (real off switch — CPGW self-tickles while logged in).
- **Why:** Minute 401s 24×7; leftover SSO held 44.5h and competed with Desktop.
- **Alternatives considered:** Market-hours cron; auto-tickle whenever `BG_IBKR_LIVE_READ`.
- **Reversibility:** easy
- **Promote to ADR?** no — ritual in CONTEXT + runbook

### Decision 2: Human paper SSO stays law
- **Choice:** tickle + `ssodh/init` cannot recover 401. Unattended login remains open on the P2 ticket.
- **Why:** log spike 2026-09-11
- **Alternatives considered:** headless SSO / OAuth (non-goals)
- **Reversibility:** easy if IBKR later offers a key
- **Promote to ADR?** no

### Decision 3: Session Yield is the one Fulfillment Desk write
- **Choice:** binding-wide hold for same-username Desktop; not rebind.
- **Why:** CPGW tickle/`compete=true` disconnects Desktop.
- **Alternatives considered:** only `keepalive off` (Java still self-tickles); kill CPGW from Wv2 (no host SIGTERM from compose).
- **Reversibility:** easy (Resume + `run-ibkr-cpgw up`)
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- Idle timeout ~6 min ≠ max session. Logged-in CPGW self-tickle ~30s held **~44.5 hours** until DNS.
- Thursday DAY-order updates needed **no** Thursday login.
- `down` ends keep-alive; `keepalive off` only stops BG’s minute job.
- Ops-shell header links inside `<summary>` need explicit `pointer-events: auto` on desktop.
- Pulse `ibkr_cpgw` still lights from tickle **cron freshness**, not HTTP 200.

---

## 6. Issues & Tickets

### Resolved this session
- 24×7 401 TickleJob — gated + auto-off
- All adapters header unclickable — CSS
- Desktop compete — Session Yield

### Deferred
- Winston-owned CPGW window after human SSO (`2026-09-06-ibkr-cpgw-unattended-session.md` scope 3) — still open
- Unattended paper SSO — same ticket; human gate stays
- Pulse `ibkr_cpgw` ≠ brokerage session — [`docs/tickets/2026-09-11-wev-pulse-ibkr-cpgw-session-truth.md`](../tickets/2026-09-11-wev-pulse-ibkr-cpgw-session-truth.md)
- Browser click of All adapters + Yield/Resume — [`docs/tickets/2026-09-11-fulfillment-desk-adapters-yield-browser-verify.md`](../tickets/2026-09-11-fulfillment-desk-adapters-yield-browser-verify.md)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| CPGW live status | curl auth/status + tickle; process/port; logs | ✅ 401 at 08:12; death 04:58 |
| Duration spike | gw.2026-09-09..11.log | ✅ ~44.5h |
| TickleJob / Keepalive / SessionYield | `RAILS_ENV=test` BG rspec (30 examples) | ✅ |
| Fulfillment Desk / yield POST | Wv2 rspec `TEST_DB_HOST=$DB_HOST` (10 examples) | ✅ |
| Ops shell / desk pages | curl 200; digested CSS has `pointer-events: auto` | ✅ HTTP |
| Header click / yield button | real browser | ⚠️ not clicked here |
| CPGW `up` wait-SSO | not run (human SSO) | ⚠️ |

**Test command(s):**

```bash
./bin/compose exec -T -e RAILS_ENV=test broker_gateway bundle exec rspec \
  spec/jobs/adapters/ibkr/tickle_job_spec.rb \
  spec/services/adapters/ibkr/session_yield_spec.rb \
  spec/requests/api_v1_bindings_spec.rb
./bin/compose exec -T winston_v2 bash -lc \
  'RAILS_ENV=test TEST_DB_HOST="${DB_HOST}" bundle exec rspec \
    spec/services/operations/fulfillment_desk_spec.rb \
    spec/services/operations/fulfillment_label_spec.rb \
    spec/requests/operations_fulfillment_spec.rb'
./ecosystem/deployment/bin/run-ibkr-cpgw status
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** none new
- **Services:** restarted `winston_v2`, `broker_gateway`, `broker_gateway_sidekiq`. CPGW Java left **up**, session **401**, keep-alive **off**.
- **Migrations:** `20260911140000_adapter_binding_session_yield` on BG dev + test

---

## 9. Risks & Technical Debt

- Yield **until** expiry resumes automation and may compete with Desktop again if still logged in there.
- Logout is best-effort; CPGW process still self-tickles if logout fails — `down` is the hard stop.
- Pulse still can show CPGW “live” from cron.
- `ibkr.env` local comments updated; gitignored.

---

## 10. Open Questions

- **Should yield until auto-`down` CPGW, not only clear the flag?** — operator; blocks Desktop-safe timers
- **Winston-owned `up` after SSO without storing password?** — ticket scope 3; blocks unattended paper window

---

## 11. Handoff & Resume Notes

- **Where I left off:** Session Yield shipped; CPGW process up, session dead, keep-alive off; Desktop may still be running.
- **Next concrete step:** Operator: Yield if using Desktop; else `run-ibkr-cpgw up` + paper SSO for DUT this cash session. Agent: Winston-owned window on the unattended-session ticket.
- **Files to read first:** `ecosystem/docs/operations/ibkr-cpgw.md`; `broker_gateway/app/services/adapters/ibkr/session_yield.rb`; `winston_v2/app/views/operations/fulfillments/show.html.erb`

---

## 12. Stakeholder Communications

- _None._ Operator-only ritual.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, graphify-ponytail (query then files), ibkr-cpgw (authored), wrap, session-report; impeccable Operate/craft-floor for ops-shell (existing tokens, no new visual world)
- **Graphify Graph:** updated `ecosystem/`, `broker_gateway/`, `winston_v2/` (`graphify update`, AST); workspace merge 22395 nodes / 30791 edges → `graphify-out/graph.json` (not staged)
- **Ponytail flags:** `Keepalive` and `SessionYield` sit next to god node `Adapters::Ibkr::Session` (24 edges) — not a third tickle helper; yield is product law, not a duplicate of keepalive. No harmonize this wrap.
- **What worked well:** CPGW logs answered duration without guessing; header bug was one CSS rule.
- **Friction points:** Wv2 `RAILS_ENV=test` uses `TEST_DB_HOST` default localhost inside compose; `until:` is a Ruby keyword (`until_at`).
- **Subagent usage:** none

---

## 14. Follow-up Actions

- [ ] Winston-owned CPGW window (start → wait SSO → keepalive → BG → down or 15-min DAY wait) — owner: next session — due: when paper DUT automation is wanted unattended after one login — See: `docs/tickets/2026-09-06-ibkr-cpgw-unattended-session.md`
- [ ] Unattended paper SSO (if ever) — kill switch + `needs_reauth` refuse write — same ticket
- [ ] Pulse `ibkr_cpgw` from brokerage HTTP 200, not tickle cron freshness — See: `docs/tickets/2026-09-11-wev-pulse-ibkr-cpgw-session-truth.md`
- [ ] Browser-verify All adapters click + Yield/Resume — See: `docs/tickets/2026-09-11-fulfillment-desk-adapters-yield-browser-verify.md`

---

## 15. Appendix

CPGW death (Mountain Time):

```
04:56:26 tickle,200
04:57:27 api.ibkr.com: Temporary failure in name resolution
04:58:01 tickle,401  tickle cp session failed  CP_LOGIN_FAILED
```

Paper SSO: `2026-09-09 08:26:28 Client login succeeds` (paper username). Binding `bnd_3d6a5020d839c315583277d2`, account `DUT070450`.
