# GC Status — L1 Broker Gateway build package (2026-08-09)

**Role:** General contractor (GC) integration monitor  
**Date:** 2026-08-09  
**Mode:** contractor — monitor / integrate / reconcile only (no re-scaffold, no large rewrites)  
**Workspace:** `/home/johnkoisch/Documents/com/sawtooth`  
**Authorization basis:** Grill A + Grill B Q1–Q7 locks; operator parallel work package for tickets + interface + scaffold + work graph  

---

## 1. Executive summary

| Workstream | Status | Path(s) |
|------------|--------|---------|
| **1. L1 tickets + discovery re-scope** | **Done** | Epic + 13 children filed; discovery superseded; INDEX reconciled by GC |
| **2. Evidence Standard interface** | **Done (draft)** | `ecosystem/interfaces/winston-broker-evidence-standard.md` (v0.1 draft) |
| **3. `broker_gateway` Rails + compose** | **Mostly done** | App tree + AGENTS + Containerfile + stubs + specs; **compose wired** (`bg_postgres`, `:3003`, sidekiq, evidence volume) |
| **4. Phase 6/7 work graph** | **Done** | `ecosystem/docs/analysis/2026-08-09-l1-confirmation-intake-work-graph.md` |

**Vertical-slice coding readiness:** **Green for first implement sessions** on the **`dummy_sim` critical path**.  
- **MG0 paper lock:** **done 2026-08-09** — paper defaults to BG `dummy_sim`.  
- **MG1 freezes (GC parent):** registry key **`dummy_sim`**; API **`/api/v1/bindings/{binding_id}/refresh|events`**. Scaffold may still expose flat stubs until the API ticket lands.

Domain law is consistent (Human-Gated, no L3).

---

## 2. Workstream detail

### 2.1 Tickets (workstream 1) — **done**

#### Epic + children (all on disk)

| File | Role |
|------|------|
| `2026-08-09-l1-confirmation-intake-bg-build.md` | Epic; domain locks; paper→`dummy_sim` locked |
| `2026-08-09-winston-broker-evidence-standard-interface.md` | Interface acceptance |
| `2026-08-09-broker-gateway-rails-scaffold.md` | Scaffold + compose |
| `2026-08-09-bg-adapter-registry-and-capability-profile.md` | Registry + CapabilityProfile; Q8 TBD |
| `2026-08-09-bg-dummy-sim-adapter.md` | Dummy/sim paper + contracts |
| `2026-08-09-bg-evidence-store-jsonl-and-cursors.md` | JSONL + PG cursors |
| `2026-08-09-bg-internal-api-refresh-events.md` | Refresh + events API |
| `2026-08-09-bg-schwab-read-adapter-l1.md` | Schwab read (after dummy) |
| `2026-08-09-wv2-bg-client-and-event-cursor.md` | Wv2 pull client |
| `2026-08-09-wv2-trade-notification-store-and-normalize.md` | TradeNotification store |
| `2026-08-09-wv2-match-prefill-confirmation-intake.md` | Match + prefill |
| `2026-08-09-wv2-desk-workflow-hitl-evidence-ui.md` | Desk HITL UI |
| `2026-08-09-wv2-confirmation-intake-integration-specs.md` | Integration specs |
| `2026-08-09-l1-contract-fixtures-and-test-harness.md` | Shared fixtures |

**Location:** `/home/johnkoisch/Documents/com/sawtooth/ecosystem/docs/tickets/`  
**INDEX:** all rows added (GC).

#### Discovery re-scope — **done**

`2026-07-21-broker-confirmation-email-api-intake.md` status: **Superseded by L1 implement tickets**; points at epic + children; discovery acceptance checkboxes updated.

#### Related pre-existing

- `2026-08-07-schwab-trader-api-sandbox-spike.md` — MG4 live-read confidence; not blocking dummy slice

---

### 2.2 Winston Broker Evidence Standard interface (workstream 2) — **done (draft)**

**Path:** `/home/johnkoisch/Documents/com/sawtooth/ecosystem/interfaces/winston-broker-evidence-standard.md`

**Landed:**

- v0.1 envelope (`schema_version`, `event_id`, `idempotency_key`, timestamps, `binding_id`, `adapter_key`, `event_type`, redacted account ref, `raw_payload_ref`, `payload`)
- L1 event types (`auth.status`, `order.*`, `trade.executed`) + reserved L2
- Idempotency + orphans + append-only
- Consumer pull sketch under `/api/v1/bindings/{id}/…` (MG1 freeze)
- CapabilityProfile L1 matrix; no `order_write`
- §11 **`dummy_sim` locked** as paper default
- Q8/Q9 deferred; security/redaction

**MG1 freezes applied by parent GC:** key `dummy_sim`; routes `/api/v1/bindings/{binding_id}/…`. Scaffold flat stubs are temporary.

---

### 2.3 `broker_gateway` scaffold (workstream 3) — **mostly done**

**Tree:** `/home/johnkoisch/Documents/com/sawtooth/broker_gateway/`

| Deliverable | Status |
|-------------|--------|
| Rails 7.0 / Ruby 3.3.6 | Yes |
| `AGENTS.md` + `PROJECT_PROFILE.md` | Yes — ownership boundaries clear |
| `Containerfile` | Yes |
| Sidekiq + Redis DB **/3** | Yes |
| Migration: `adapter_bindings`, `evidence_cursors` | Yes |
| Models + capability flags | Yes |
| API stubs: health, bindings, refresh, events | Yes — **flat** `/api/v1/*` |
| `Adapters::DummyAdapter` (`adapter_key: "dummy"`) | Yes — empty lists; no `place_order` |
| `data/evidence/` README | Yes — no JSONL writer yet |
| RSpec stubs | Yes |
| Root `compose.yml` | **Yes** — `bg_postgres` :5435 host map, `broker_gateway` :3003, sidekiq, `sawtooth_bg_evidence` volume |
| Workspace root `AGENTS.md` map | **Yes** — BG row / 3003 |
| Stock Rails `README.md` | Placeholder remains |
| Boot / migrate / health smoke verified | **Not verified this GC session** (wiring present; operator should `compose build` + migrate) |

Scaffold ticket acceptance (compose boot + health) is **code-complete pending first smoke**.

#### Compose services (observed)

- `bg_postgres` — DB `broker_gateway_dev`, user `sawtooth`
- `broker_gateway` — host **3003**, Redis `/3`, bind-mount `./broker_gateway`, volume `sawtooth_bg_evidence` → `/app/data/evidence`
- `broker_gateway_sidekiq` — same env + evidence volume

---

### 2.4 Phase 6/7 work graph (workstream 4) — **done**

**Path:** `/home/johnkoisch/Documents/com/sawtooth/ecosystem/docs/analysis/2026-08-09-l1-confirmation-intake-work-graph.md`

Goal + OOS, **paper policy PENDING (MG0)**, DAG, swimlanes L0–L11, merge gates MG0–MG4, critical path (dummy E2E before Schwab), agent assignment / forbidden parallel edits, test strategy, risks, vertical-slice DoD.

Safe sequencing SoT for next sessions.

---

## 3. Conflicts and contradictions

### 3.1 Paper / Manual zero-IO vs dummy-BG — **PENDING OPERATOR CONFIRMATION** ⚠️

| Source | Position |
|--------|----------|
| Grill B Q3 / CONTEXT / plan diagram | **Manual stays zero-IO inside Wv2** |
| Operator preference (session, not locked) | Paper OPs should still hit BG via **dummy/sim** so intake workflow is always exercised |
| Work graph §2 | Flags Option A vs B; recommends B for tests + Manual escape; **MG0 = operator** |
| Epic OPEN-paper→dummy | Same open; recommends dummy; Manual fallback |
| Dummy ticket | OPEN; implement dummy; Manual remains valid |
| Interface §11 | Sim must conform if used; preference pending lock |

**GC action:** **Do not invent a lock.** No CONTEXT rewrite this session. Hybrid product matrix is already drafted in the work graph (paper+manual / paper+dummy / real+manual / real+schwab_read).

### 3.2 Dummy adapter registry key — **three names**

| Artifact | Key |
|----------|-----|
| Scaffold `Adapters::DummyAdapter` | `dummy` |
| Tickets (dummy + registry + fixtures) | `dummy_sim` |
| Interface §11 example | `sim_dummy` |

**MG2 / MG1 joint freeze:** pick one. **GC recommendation:** freeze **`dummy_sim`** (matches tickets); rename scaffold constant + seed.

### 3.3 Internal API path shape — scaffold vs interface

| Concern | Interface v0.1 | Scaffold stubs |
|---------|----------------|----------------|
| Prefix | `/internal/v1` | `/api/v1` |
| Refresh | `POST /bindings/{binding_id}/refresh` | `POST /refresh` (flat) |
| Events | `GET /bindings/{binding_id}/events?since_cursor=` | `GET /events?cursor=` |
| Cursor | `since_cursor` / `next_cursor` | `cursor` |

**MG1 must freeze** before Wv2 client ticket implement. Prefer **per-binding routes** (interface) + opaque cursor; choose one prefix and stick (align with DM internal style in implement ticket if needed). Scaffold stubs are temporary smoke only.

### 3.4 Evidence path layout

| Source | Layout |
|--------|--------|
| Interface (provisional) | `data/evidence/{binding_id}/events.jsonl` |
| Scaffold evidence README | `data/evidence/<adapter_key>/<stream>/…` (comment) |

Freeze under MG1 with interface as authority unless store ticket documents a deliberate change.

### 3.5 Resolved / non-conflicts

| Topic | Outcome |
|-------|---------|
| Discovery vs epic | **Resolved** — discovery marked Superseded |
| Human-Gated book / no L3 | **Consistent** across all agents |
| No shared PG | **Consistent** (compose dedicated `bg_postgres`) |
| Compose claims vs reality | **Resolved** — services now present |
| Workspace AGENTS map | **Resolved** — BG row present |

### 3.6 Plan footer vs authorization

Plan still ends with *“Implementation is not authorized by this document.”* Epic + tickets authorize L1 by Grill locks. Implement sessions should cite **tickets**, not the plan alone. Work graph agrees.

---

## 4. Contract freeze readiness (MG0–MG2)

| Gate | Ready? | Blocker |
|------|--------|---------|
| **MG0 — Paper policy** | **No** | Operator confirm Option A / B / hybrid matrix |
| **MG1 — Evidence contract** | **Almost** | Freeze API paths + cursor names + path layout + dummy key; mark interface frozen or 0.1.x note |
| **MG2 — Dummy profile** | **No** | Key name + emit synthetic events (implement) |
| **MG3 — Vertical slice** | **No** | JSONL writer + Wv2 client + match/prefill + integration green |
| **MG4 — Live read** | **No** | Schwab sandbox spike |

**Recommended order:** MG0 (operator, minutes) → MG1 freeze pass (GC/short session) → implement store + dummy + Wv2 client in contractor mode (or ultrawork **after** MG1).

---

## 5. Light reconciliation performed by GC

| Action | Result |
|--------|--------|
| INDEX.md rows for all existing 2026-08-09 L1 tickets | **Added** |
| Plan §15 one-line progress + link to this status | **Added** |
| Discovery re-scope | Already done by ticket agent |
| Compose / large rewrites | **Not done** by GC (scaffold agent completed compose) |
| Commit / push | **Not done** (per charter) |

---

## 6. Recommended operator next actions

1. **Lock MG0 paper policy** — Confirm hybrid matrix (recommended) or pure Manual paper. Speak the choice; CONTEXT update only after lock.
2. **Smoke compose BG** — `bin/compose build broker_gateway` → `up -d bg_postgres broker_gateway broker_gateway_sidekiq` → `db:create db:migrate` → `curl localhost:3003/health`.
3. **Authorize MG1 freeze** — Align interface paths with implement direction (prefer per-binding); freeze `dummy_sim` key; mark interface Frozen 0.1.
4. **Start critical path implement** (contractor): evidence store writer → internal API → dummy emits fixtures → Wv2 client (after freeze).
5. **Defer Schwab live** until dummy E2E + sandbox spike.
6. **Do not start** place_order / ADR-010 / shared PG / email SoT.

---

## 7. Follow-up checklist (next session assignments)

### P0 — freeze + smoke

- [ ] Operator: MG0 paper → dummy vs Manual lock  
- [ ] GC: MG1 freeze note (API prefix, per-binding routes, cursor names, dummy key, evidence path)  
- [ ] Ops: compose build/migrate/health smoke on :3003  
- [ ] Scaffold polish: rename dummy key to frozen name; product README (optional)

### P1 — vertical slice (after MG1)

- [ ] BG: JSONL append writer + idempotency (evidence store ticket)  
- [ ] BG: refresh/events per frozen routes (internal API ticket)  
- [ ] BG: dummy emits golden `trade.executed` / `order.upserted`  
- [ ] Ecosystem: shared fixtures (fixtures harness ticket)  
- [ ] Wv2: BG client + durable cursor  
- [ ] Wv2: TradeNotification store  
- [ ] Wv2: match + prefill; **no** auto-book  
- [ ] Wv2: desk workflow evidence UI + request specs via `JournalConfirmationService`  
- [ ] Integration: compose dummy → pull → match → prefill → human confirm  

### P2 — later

- [ ] Schwab read fixtures/VCR  
- [ ] Operator: Schwab sandbox spike  
- [ ] Grill B Q8/Q9 after build learning  
- [ ] Optional thin BG charter ADR  
- [ ] Optional DAR orphan/auth-fail polish  

---

## 8. Readiness scorecard

| Question | Answer |
|----------|--------|
| Tickets filed end-to-end? | **Yes** |
| Interface draft landed? | **Yes** |
| Work graph landed? | **Yes** |
| Compose BG wired? | **Yes** (smoke pending) |
| MG0 paper policy locked? | **No** — pending operator |
| MG1 API/schema frozen? | **No** — draft + path thrash |
| Can ultrawork dual implement start? | **Not yet** — freeze MG1 first |
| Domain law consistent (HITL, no L3)? | **Yes** |
| Biggest open decision | Paper → dummy-BG vs Manual zero-IO only |
| Biggest technical thrash risk | API path shape if Wv2 client codes against flat stubs |

---

## 9. Artifact index (absolute paths)

| Artifact | Absolute path | Status |
|----------|---------------|--------|
| Epic | `/home/johnkoisch/Documents/com/sawtooth/ecosystem/docs/tickets/2026-08-09-l1-confirmation-intake-bg-build.md` | Done (children complete) |
| All L1 child tickets | `/home/johnkoisch/Documents/com/sawtooth/ecosystem/docs/tickets/2026-08-09-*.md` | Done |
| Discovery (superseded) | `/home/johnkoisch/Documents/com/sawtooth/ecosystem/docs/tickets/2026-07-21-broker-confirmation-email-api-intake.md` | Re-scoped |
| Interface | `/home/johnkoisch/Documents/com/sawtooth/ecosystem/interfaces/winston-broker-evidence-standard.md` | Draft done |
| Work graph | `/home/johnkoisch/Documents/com/sawtooth/ecosystem/docs/analysis/2026-08-09-l1-confirmation-intake-work-graph.md` | Done |
| This GC status | `/home/johnkoisch/Documents/com/sawtooth/ecosystem/docs/analysis/2026-08-09-l1-bg-build-gc-status.md` | Done |
| Scaffold | `/home/johnkoisch/Documents/com/sawtooth/broker_gateway/` | Mostly done |
| Root compose | `/home/johnkoisch/Documents/com/sawtooth/compose.yml` | BG services present |
| Plan | `/home/johnkoisch/Documents/com/sawtooth/ecosystem/plans/trade-fulfillment-engine.md` | §15 annotated |
| INDEX | `/home/johnkoisch/Documents/com/sawtooth/ecosystem/docs/tickets/INDEX.md` | L1 rows present |

---

*GC monitor complete. No commit/push. Implementation proceeds from tickets after MG0/MG1; no L3 from this package.*
