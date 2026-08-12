# Session Report — BG registry + dummy_sim + compose bring-up

**Date:** 2026-08-12  
**Time:** ~2026-08-10 session work; wrap 11:52 MDT  
**Duration:** multi-day gap between implement and wrap  
**Project:** sawtooth Winston ecosystem + broker_gateway  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `main` (broker_gateway, ecosystem)  
**Model:** Grok 4.5  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** (1) Explain why Broker Gateway (BG) was missing from `c ps` / compose vs data_manager; (2) finish L1 step #1 — formalize adapter registry + CapabilityProfile and complete `dummy_sim`.

**Outcome:** Delivered

**One-line summary:** BG Rails services were never started (only `bg_postgres` was up); brought up `broker_gateway` + Sidekiq on :3003; formalized registry/CapabilityGate/`dummy_sim` scenarios with 51 green specs and live refresh smoke.

---

## 2. Work Completed

- Diagnosed compose: `broker_gateway` / `broker_gateway_sidekiq` defined in root `compose.yml` but not running; only `bg_postgres` had been started.
- Built image, `compose up -d bg_postgres broker_gateway broker_gateway_sidekiq`, `db:prepare` + seed.
- Fixed Sidekiq boot: comment-only `sidekiq_schedule.yml` loaded as `false` → `Sidekiq::Cron::Job.load_from_hash!` crash; guard for Hash-with-keys.
- Formalized `Adapters::CapabilityProfile`, `Adapters::Registry` (MAP + PROFILES), `Adapters::CapabilityGate` (fail-closed `order_write`).
- Binding model: `env` (sandbox|live), `secrets_pointer`, Q8 deferred notes, registry defaults, L1 reject `cap_order_write`.
- `DummyAdapter` scenarios: auth / exact / partial / orphan / cancel / reject; `force` ⇒ orphan.
- API: `GET /api/v1/adapters`; refresh accepts `scenario=`; serialize `env` / `secrets_pointer`.
- Tickets: registry + dummy_sim **Done**; epic progress updated; INDEX updated.
- Restarted WUT after redis recreate side-effect during compose up.

---

## 3. Code Delivered

### Files changed (this session focus)

#### broker_gateway

| File | Change | Notes |
|------|--------|-------|
| `app/services/adapters/capability_profile.rb` | added | L1 profile value object |
| `app/services/adapters/capability_gate.rb` | added | fail-closed write gate |
| `app/services/adapters/registry.rb` | added/rewritten | MAP + PROFILES + catalog |
| `app/services/adapters/dummy_adapter.rb` | modified | scenarios + gate on place_order |
| `app/models/adapter_binding.rb` | modified | env, secrets_pointer, Q8 notes, defaults |
| `db/migrate/20260810120000_binding_env_and_secrets_pointer.rb` | added | env + secrets_pointer |
| `app/controllers/api/v1/adapters_controller.rb` | added | registry catalog API |
| `app/controllers/api/v1/bindings_controller.rb` | modified | scenario + serialize |
| `app/services/evidence/refresh_service.rb` | modified | scenario kwarg; refuse order_write |
| `config/routes.rb` | modified | adapters#index |
| `config/initializers/sidekiq.rb` | modified | safe empty schedule |
| `config/sidekiq_schedule.yml` | modified | `{}` + comments |
| `db/seeds.rb` | modified | paper dummy_sim + env |
| `db/schema.rb` | modified | new columns |
| `AGENTS.md` | modified | smoke with adapters/scenarios |
| specs (registry, gate, dummy, binding, refresh, request) | added/modified | 51 examples |

Also present uncommitted on disk from **prior L1 sessions** (evidence JSONL store, MG1 refresh/events API, migrations, base_controller): needed for a coherent working BG commit — include in wrap commit as one L1 foundation ship.

#### ecosystem

| File | Change | Notes |
|------|--------|-------|
| `docs/tickets/2026-08-09-bg-adapter-registry-and-capability-profile.md` | Done | acceptance checked |
| `docs/tickets/2026-08-09-bg-dummy-sim-adapter.md` | Done | Wv2 pull deferred to client ticket |
| `docs/tickets/2026-08-09-l1-confirmation-intake-bg-build.md` | progress | step 4 Done; next = Wv2 client |
| `docs/tickets/INDEX.md` | updated | registry/dummy Done |
| `docs/session-reports/2026-08-12-1152-bg-registry-dummy-sim-compose.md` | added | this report |

### Commits

- broker_gateway `934dd93` — feat(L1): evidence store, registry, CapabilityProfile, dummy_sim scenarios  
- ecosystem `97ced04` — docs: close BG registry + dummy_sim; wrap session; optional compose tickets  

### Branch / PR state at sign-off

- broker_gateway `main` — clean (except local `tmp/pids`, `vendor/`) — **pushed**  
- ecosystem `main` — wrap files clean; **other** unstaged ticket/analysis dirt left for other sessions — **pushed**  
- WUT / Wv2 dirty from **other** sessions — **not** committed by this wrap  
- PR: not opened (direct main)

**Monoliths touched this session:** `broker_gateway`, `ecosystem` (docs). Workspace root `compose.yml` already had BG services (not git-versioned at root).

---

## 4. Decisions Made

### Decision 1: Registry without per-vendor migration
- **Choice:** String keys + in-code `Adapters::Registry` MAP/PROFILES  
- **Why:** Ticket acceptance; no schema churn per vendor  
- **Reversibility:** easy  
- **Promote to ADR?** No  

### Decision 2: schwab_trader_api profile-only until adapter ticket
- **Choice:** PROFILES entry, not MAP class  
- **Why:** Capability visibility without fake poll  
- **Reversibility:** easy  

### Decision 3: dummy_sim scenarios via refresh `scenario=` param
- **Choice:** exact/partial/orphan/cancel/reject; force⇒orphan  
- **Why:** Contract rehearsal without network  
- **Reversibility:** easy  

### Decision 4: L1 order_write fail-closed at model + gate + refresh
- **Choice:** validation + CapabilityGate + refresh refuse  
- **Why:** Domain lock until ADR-010  
- **Promote to ADR?** No (already L1 locks)

---

## 5. Insights Surfaced

- Compose **definitions ≠ running**: operator saw DM because it was up; BG only had Postgres until explicit `up`.
- podman-compose recreate of shared `redis` can bounce dependents (WUT exited once).
- Empty YAML schedule + sidekiq-cron is a footgun (`false.keys`).
- Volume name `sawtooth_bg_evidence` becomes project-prefixed `sawtooth_sawtooth_bg_evidence` — cosmetic debt.

---

## 6. Issues & Tickets

### Resolved this session
- BG not visible in `c ps` — started services  
- Adapter registry + CapabilityProfile ticket → **Done**  
- dummy_sim adapter ticket → **Done** (Wv2 pull remains on client ticket)

### Deferred
- Wv2 BG client + event cursor — already ticketed  
- TradeNotification store / match-prefill / desk UI — already ticketed  
- Schwab read adapter + sandbox spike — already ticketed  
- Optional: rename evidence volume to avoid double project prefix  
- Optional: ensure default full-stack `compose up -d` docs always mention BG trio  

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| BG unit/request specs | `bundle exec rspec` (host) | ✅ 51 examples, 0 failures |
| Compose health | `curl :3003/health` | ✅ |
| Registry API | `GET /api/v1/adapters` | ✅ dummy_sim + schwab profile |
| Refresh smoke | `POST …/refresh?scenario=exact` | ✅ 2 events |
| Events pull | `GET …/events?since_cursor=0` | ✅ auth.status,trade.executed |
| Sidekiq | container logs after fix | ✅ booted Redis /3 |

**Test command(s):**  
`cd broker_gateway && bundle exec rspec`  
`curl -s http://127.0.0.1:3003/health`

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new (gems already in scaffold)  
- **Services:** `bg_postgres`, `broker_gateway` (:3003), `broker_gateway_sidekiq`; WUT restarted  
- **Migrations:** `20260810120000_binding_env_and_secrets_pointer` (+ prior evidence store migration if not applied)  
- **Seed:** paper `dummy_sim` binding `bnd_…` env=sandbox  

---

## 9. Risks & Technical Debt

- Uncommitted prior L1 evidence/API work lived only on disk until this wrap — risk of loss if not committed.  
- Evidence volume double-prefix naming.  
- `apply_registry_capability_defaults` forces L1 caps on create for known keys — intentional but document for operators.  
- No Wv2 consumer yet — BG is write/poll ready but Confirmation Intake path incomplete.

---

## 10. Open Questions

- **Q8** OP↔binding multi-account law — still deferred (documented on model).  
- Whether root compose should be versioned in git (existing P2 ticket space).

---

## 11. Handoff & Resume Notes

- **Where I left off:** Registry + dummy_sim Done; BG up on :3003; wrap pending commit/push.  
- **Next concrete step:** Implement Wv2 ticket `2026-08-09-wv2-bg-client-and-event-cursor.md` (HTTP client + cursor + pull loop).  
- **Files to read first:**  
  1. `ecosystem/docs/tickets/2026-08-09-l1-confirmation-intake-bg-build.md`  
  2. `ecosystem/interfaces/winston-broker-evidence-standard.md` §9  
  3. `broker_gateway/app/controllers/api/v1/bindings_controller.rb`  
  4. `broker_gateway/app/services/adapters/registry.rb`  

---

## 12. Stakeholder Communications

- _None required._ Optional: “Paper path can now poll synthetic broker evidence through BG on port 3003.”

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report (inline), operator-prose  
- **What worked well:** host rspec then compose smoke; ticket acceptance checkboxes as definition of done  
- **Friction points:** compose redis recreate side-effects; empty sidekiq-cron YAML; multi-day gap before wrap  
- **Subagent usage:** none  

---

## 14. Follow-up Actions

- [ ] Wv2 BG client + event cursor — **already ticketed** (`2026-08-09-wv2-bg-client-and-event-cursor.md`)  
- [ ] TradeNotification + match/prefill + desk UI — **already ticketed** (L1 epic children)  
- [x] Optional: rename compose evidence volume — ticketed [`2026-08-12-bg-evidence-volume-name.md`](../tickets/2026-08-12-bg-evidence-volume-name.md)  
- [x] Optional: document “first-time BG up” — ticketed [`2026-08-12-bg-compose-first-time-up-docs.md`](../tickets/2026-08-12-bg-compose-first-time-up-docs.md)  
- [ ] Commit + push broker_gateway + ecosystem L1 docs (this wrap)

---

## 15. Appendix

### Compose bring-up (first time)

```bash
./bin/compose build broker_gateway
./bin/compose up -d bg_postgres broker_gateway broker_gateway_sidekiq
./bin/compose exec -T broker_gateway bin/rails db:prepare db:seed RAILS_ENV=development
curl -s http://localhost:3003/health
curl -s http://localhost:3003/api/v1/adapters
```

### Seeded smoke (example)

```text
BID=bnd_f1feaf2e361799fc3ecd610a
POST refresh?scenario=exact → events_appended=2, head_cursor=2
GET events → auth.status, trade.executed
```
