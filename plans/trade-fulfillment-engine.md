# Plan: Configurable Trade Fulfillment Engine (Wv2)

**Status:** Draft — **Phase 1 + Grill A (Phase 2) complete (2026-08-06)**; Grill B next — **do not implement L1/L3 yet**  
**Date:** 2026-08-05 (Phase 1–2 decisions through 2026-08-06)  
**Monoliths:** primarily **Wv2**; optional host-side broker worker; Cromwell/MCP surfaces  
**Builds on:** ADR-009, ADR-006, Schwab discovery (2026-07-22), fulfillment ownership analysis  
**Series:** `trade-fulfillment-engine` (successor/expansion of `adr-009-desk-fulfillment` L3+)  
**Review:** Incorporates operator comments 2026-08-05 (atomic ops + orchestrators, HITL stack-rank, adapter abstraction, capital APIs, sandbox/contract tests)

---

## 1. Why this plan exists

We are ready to **plan or validate** automated trading components for real Operational Portfolios (OPs). Target brokers include **Charles Schwab / thinkorswim** and **Interactive Brokers (IBKR)**, but the product requirement is stronger than “build Schwab then IB”:

> **Per real OP, Fulfillment Engine is configurable.**  
> Engine selection is a **policy + adapter binding**, not a hard-coded “basic Schwab” module.

Behind that config sits a **Trade Fulfillment abstraction**: Winston desk, journals, capital, and attention call **atomic operations** and **orchestrators** without knowing which broker transport is wired.

**This plan is not authorization to implement.** It sequences discovery lock-in, grill sessions, ADR work, and phased build.

---

## 2. What already exists (do not re-discover)

### Domain law (accepted)

| Artifact | Settled |
|----------|---------|
| [ADR-009](../docs/adr/ADR-009-human-gated-desk-and-fulfillment.md) | DA never opens lots; real is Human-Gated; future automation is a **separate component**, not DA |
| [human-gated-desk-and-fulfillment.md](../docs/business-context/human-gated-desk-and-fulfillment.md) | Dual spines; Signaled Entry / Unsignaled Exit; Desk Handoff; Working Stop ≠ broker stop SoT; capacity packages |
| ADR-006 | `execution_mode` paper\|real; Capital Activation; CashEvents; engagement; Active mutex |
| CONTEXT.md | Fulfillment, Extra-Modal Fulfillment, Fulfillment Packaging, Booked Capital Spine, Signal Spine |

### Shipped product (prerequisites)

| Capability | Status |
|------------|--------|
| Single-fulfillment invariant + refuse double book | **Done** (`SingleFulfillmentGuard`) |
| Post-confirm amend same lot (price/qty/stop) | **Done** (`JournalExecutedAmendService`) |
| Desk Workflow / correct_fill | **Done** |
| Stop-Out Reconciliation | **Done** |
| Signaled Entry Rule (force+notes escape) | **Done** |
| EOD Signal Date / Fill Date next-open | **Done** |
| CashEvent top-up / adjustment (real Active only) | **Done** (`wv2_add_cash_event`, `CashEventService`) |
| Related-instrument packaging (LEAP/option/proxy) on book/confirm | **Partial** (MCP/desk fields exist; not full engine path) |

### Discovery written but not domain-locked

| Artifact | Role |
|----------|------|
| [fulfillment ownership + broker intake](../docs/analysis/2026-07-22-winston-fulfillment-ownership-and-broker-intake.md) | Grill tee |
| [Schwab integration discovery](../docs/analysis/2026-07-22-schwab-integration-discovery.md) | API primary, email fallback, L0–L4 ladder |
| [Schwab/ToS landscape](../docs/analysis/2026-07-22-schwab-thinkorswim-access-landscape.md) | Streamer vs webhook, paperMoney gap, extra-modal, issue register |
| Ticket [broker confirmation intake](../docs/tickets/2026-07-21-broker-confirmation-email-api-intake.md) | Discovery open |
| Ticket [grill fulfillment/Schwab](../docs/tickets/2026-07-22-grill-fulfillment-schwab-extra-modal.md) | **Still Proposed** |
| Deferred [order vs fill](../docs/tickets/2026-07-15-journal-ledger-order-vs-fill-deferred.md) | Resting-order model for `place_stop` |
| Gap: capacity swap packages in Wv2 DA | Ticket `2026-07-20-wv2-capacity-swap-desk-packages` |

### Gaps this plan closes

1. **Multi-engine configurability** with a real **adapter / capability** architecture (not Schwab-shaped core).  
2. **Atomic operations + explicit orchestrators** (composable, testable).  
3. **HITL stack-rank** coupling: fulfillment consumes Desk Handoff priority; human may re-rank / pass.  
4. **Richer capital update surface** for operator inflows **and** fill/packaging divergence from signal story.  
5. **Loose coupling** of Signal Spine (EODHD/risk/methodology) vs Booked Capital (actual fills/P&L).  
6. **IBKR** as first-class target (discovery still missing).  
7. **Sandbox / contract-test** strategy at every boundary.  
8. Scheduled **Q&A + grill-with-docs** sessions before code.

---

## 3. Product boundary (non-negotiable)

```
Daily Analysis  →  ranked Desk Handoffs + draft Journals + tasks only
       │
       ▼
HITL desk  →  accept / pass / re-rank / package  (human or policy)
       │
       ▼
Fulfillment Orchestrators  →  compose atomic ops + adapters
       │
       ▼
Booked Capital Spine  →  Journal / Position / CashEvent / evidence
```

| Rule | Meaning |
|------|---------|
| DA never places orders or opens Positions | ADR-009 |
| DA **ranks work**; it does not fulfill | WMS analogy |
| Automation is not DA silently filling | Separate orchestrator + adapter |
| Broker truth → Booked Capital / evidence only | Never rewrites Signal Spine |
| Extra-modal is normal | LEAP/proxy/structure ≠ signal share count |
| Paper stays Winston-paper by default | No live broker place for paper OPs |
| Kill switch + audit on any write path | Capital-adjacent |

### Human-Gated evolution (to lock in grill)

| Mode | v1 (near term) | Later (explicit ADR) |
|------|----------------|----------------------|
| Manual adapter | Human trades; types/confirm in Winston | + L1 evidence prefill |
| Broker adapter **read** (L1–L2) | Poll/notify; **human still confirms** book/amend | Optional autofill policy |
| Broker adapter **write** (L3) | Human (or policy) approves **send**; fill → accept/amend | L4 autotrader (new product ADR) |

---

## 4. Atomic operations vs orchestrators

The original five verbs (validate / create / market / stop / notify) are a **product shorthand**. Implementation and tests need a **finer atomic surface**, plus **orchestrators** that own multi-step workflows and HITL gates.

### 4.1 Atomic operations (smallest units; no multi-step policy)

Each is idempotent where possible, returns a typed result, and is independently mockable.

#### A. Policy / Winston-side (no broker IO)

| Atomic op | Input (sketch) | Output | Notes |
|-----------|----------------|--------|-------|
| `validate_signal_link` | journal/task/position | ok \| refuse | Signaled Entry Rule |
| `validate_capacity` | OP, proposed leg, open lots | ok \| refuse + reason | Max markets / pyramid / heat |
| `validate_kill_switch` | OP or global | ok \| refuse | Fail closed |
| `validate_packaging` | signal market + packaging draft | ok \| warn \| refuse | Extra-modal shape |
| `resolve_stack_rank` | OP, as-of | ordered handoff list | Read-only view of desk work |
| `mark_passed` | journal/task, reason | PassedSignal | Algorithmic vs process vs **human pass** |
| `attach_evidence` | journal, TradeNotification id | link | No capital change |
| `compute_signal_size_story` | OP, market, risk ladder | units @ risk | EODHD/ATR methodology — Signal Spine |

#### B. Booked Capital Spine (Winston DB; no broker IO)

| Atomic op | Input | Output | Notes |
|-----------|-------|--------|-------|
| `book_fill` | draft journal + fill fields + packaging | executed journal + position | Existing confirm path |
| `amend_fill` | executed journal + deltas | same lot, audit trail | Existing amend path |
| `book_exit` | position + fill + reason | closed lot | Incl. unsignaled / stop-out |
| `update_working_stop` | position + stop | position | Desk SoT; not broker |
| `record_cash_event` | OP, type, amount, notes | CashEvent + new capital_base | inflow / adjustment |
| `apply_fill_cash_impact` | journal fill economics | flow / capital_base | Premium×mult, fees, avg price |
| `snapshot_capital_base` | OP | number | Derived from CashEvents + executed journals |

#### C. Transport / broker adapter (external IO; capability-gated)

| Atomic op | Meaning | Capability flag |
|-----------|---------|-----------------|
| `adapter.authenticate` | Token/session ready | `auth` |
| `adapter.place_order` | Submit one order | `order_write` |
| `adapter.replace_order` | Amend working order | `order_write` |
| `adapter.cancel_order` | Cancel working order | `order_write` |
| `adapter.get_order` | Fetch order state | `order_read` |
| `adapter.list_orders` | Windowed order history | `order_read` |
| `adapter.list_transactions` | TRADE (and kin) window | `txn_read` |
| `adapter.list_positions` | Broker lots | `position_read` |
| `adapter.get_balances` | Cash / BP hints | `balance_read` |
| `adapter.subscribe_activity` | Optional stream | `activity_stream` (optional) |

**Manual adapter:** implements validate-facing ops as no-op success for transport; `place_*` returns `requires_human`; notifications come only from human entry / optional email attach.

#### D. Notification / match (read path)

| Atomic op | Input | Output |
|-----------|-------|--------|
| `normalize_notification` | raw payload + channel | TradeNotification |
| `store_notification` | TradeNotification | durable id (idempotent on external ids) |
| `match_notification` | notification → candidates | exact \| soft \| ambiguous \| orphan \| mismatch |
| `prefill_from_match` | match → draft journal fields | draft deltas (not auto-execute v1) |

### 4.2 Gaps in the original five-verb list (explicit)

| Gap | Why it matters | Atomic / orchestrator owner |
|-----|----------------|----------------------------|
| **cancel / replace** | Stops and working orders need lifecycle | `adapter.cancel_order` / `replace_order` |
| **partial fill / multi-leg** | Avg price, N legs → one signal identity | `normalize` + match lineage + amend |
| **human pass / re-rank** | Pyramid A skipped for entry D | HITL orchestrator + `mark_passed` |
| **stack-rank resolve** | Engine must not invent priority | `resolve_stack_rank` + Desk Handoff SoT |
| **capital top-up** | Operator “add $5k” | `record_cash_event` (exists; surface in plan) |
| **fill economics ≠ signal size** | 210 IBM @ signal vs 2 LEAPs booked | packaging + `apply_fill_cash_impact` |
| **fill price ≠ prefill open** | 288.44 story vs 287.33 fill | `amend_fill` / book at actual |
| **auth / token hygiene** | Weekly re-auth etc. | `adapter.authenticate` + ops job |
| **reconcile positions** | Broker lot vs Winston Position | L2 orchestrator |
| **idempotency keys** | Double-send protection | `client_order_key` on place |

### 4.3 Alternatives considered (capability grouping)

| Alternative | Description | Verdict |
|-------------|-------------|---------|
| **A. Fat “create_order” only** | One mega method per engine | Reject — untestable, hides cancel/partial |
| **B. Atomic ops + thin adapters + orchestrators** | This plan | **Prefer** |
| **C. Full OMS order book in Winston day one** | Resting orders as first-class SoT | Defer — see order-vs-fill ticket; Working Stop remains SoT until insufficient |
| **D. Broker portfolio as Winston capital** | Mirror Schwab/IB balances as capital_base | Reject — CashEvents + booked journals remain capital SoT; broker balances are **reconciliation hints** |

### 4.4 Explicit orchestrators (compose atomics; own HITL gates)

Orchestrators **never** talk to a vendor SDK directly — only to atomic ops + adapter interface.

| Orchestrator | Steps (atomic) | HITL gate | Level |
|--------------|----------------|-----------|-------|
| **DeskStackOrchestrator** | `resolve_stack_rank` → present ordered actions → accept human pass/re-rank → `mark_passed` / open workflow | Human chooses which ranked item to act on; may pass pyramid A for entry D | L0+ (today partial) |
| **ValidateIntentOrchestrator** | signal link + capacity + kill switch + packaging (+ optional adapter BP hint) | Failures surface as desk attention | L0–L3 |
| **BookFromHumanOrchestrator** | validate → `book_fill` / `book_exit` / `amend_fill` → capital snapshot | Confirm / correct_fill | L0 (today) |
| **IngestNotificationOrchestrator** | auth → list/poll or stream chunk → normalize → store → match → prefill or attention | Human confirms book/amend on match (v1) | L1 |
| **SendOrderOrchestrator** | ValidateIntent → `adapter.place_order` → store external id on intent → poll `get_order` | Explicit **Send** action (not silent DA) | L3 |
| **PyramidMarketOrchestrator** | requires open entry lot + pyramid signal leg in stack → ValidateIntent → place market → ingest fill → book/amend | Same Send gate unless policy later | L3 |
| **StopSyncOrchestrator** | `update_working_stop` (always) → optional `place/replace/cancel` stop at adapter | Policy: dual-write optional; Working Stop SoT | L3 optional |
| **StopOutIngestOrchestrator** | match position-gone / fill without Winston exit → prefill unsignaled exit | Human books exit (Unsignaled Exit Allowance) | L1–L2 |
| **CapitalUpdateOrchestrator** | routes operator inflow vs fill-driven economics vs adjustment | Real Active for operator top-up (existing policy) | L0+ |
| **ReconcileBrokerStateOrchestrator** | list_positions + balances vs Winston lots/cash | Mismatch queue; no silent overwrite | L2 |
| **FailureAttentionOrchestrator** | rejected order, auth fail, orphan, mismatch → DAR/Telegram short alert | Operator triage | All levels |

```
┌──────────────────────────────────────────────────────────────┐
│  DeskStackOrchestrator  (HITL stack-rank SoT)                 │
│  DA packages → ordered handoffs → human accept/pass/re-rank   │
└────────────────────────────┬─────────────────────────────────┘
                             │ chosen leg / intent
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  ValidateIntentOrchestrator                                   │
└────────────────────────────┬─────────────────────────────────┘
           ┌─────────────────┼──────────────────┐
           ▼                 ▼                  ▼
  BookFromHuman      SendOrder (+ Pyramid)   IngestNotification
  Orchestrator       Orchestrator            Orchestrator
           │                 │                  │
           └─────────────────┼──────────────────┘
                             ▼
              Booked Capital + CapitalUpdate + FailureAttention
```

---

## 5. HITL stack-rank (critical product tie)

Fulfillment **must not** invent which trade to do next. That is Winston’s **desk prioritization** job (WMS), refined by **human-in-the-loop (HITL)**.

### 5.1 Stack-rank source of truth

| Layer | Role |
|-------|------|
| **Daily Analysis** | Emits deterministic **Desk Handoffs** / draft Journals / algorithmic passes (capacity, no valid swap) |
| **Desk stack (per OP)** | Ordered list of actionable items for the operator: exits first in multi-leg packages, then enters/pyramids per algorithm rank |
| **HITL** | Human may **accept**, **pass**, **defer**, or **re-prioritize** within policy |
| **Fulfillment orchestrators** | Execute **only** the chosen (or policy-approved) intent via manual or broker adapter |

### 5.2 Example: pass pyramid A, take entry D

1. DA ranks: (1) pyramid add Market A, (2) initial entry Market D (or capacity contest: algorithm may already pass one).  
2. Human decides: skip pyramid A (human pass reason), take entry D instead.  
3. System: `mark_passed` on A’s draft (reason `human_pass` / `desk_reprioritize` — grill names), free capacity if needed, open Desk Workflow for D.  
4. Fulfillment (manual or L3 send) runs **only** for D’s intent.  
5. Signal Spine retains: A was recommended and passed; D was recommended and booked (or also passed). Methodology evaluation stays honest.

**Product tension (grill):** ADR-009 currently says casual skip is **not** a normal strategy lever, and capacity contests should be **algorithm packages** not multi-choice ER menus. Operator reality: humans will re-rank. Plan stance:

- **Default:** algorithm stack-rank + package order.  
- **HITL override:** allowed with **explicit reason** + audit; never silent.  
- **Capacity never waived:** cannot take 13th seat on a 12 cap without freeing a seat (exit/pass package).  
- **Do not** re-rank expected returns as a free menu; re-rank is “act on / pass this handoff,” not “pick any market you like.”

### 5.3 Implementation implications

| Need | Status | Plan action |
|------|--------|-------------|
| Ordered handoffs / multi-leg packages | Gap (WUT has swap evaluators) | Capacity-swap ticket remains P2; **blocker for smart L3 batches** |
| Per-OP “next actions” list API | Partial (pending tasks, DAR) | Explicit **stack-rank API** for desk + Cromwell |
| Human pass reason codes | Thin | Extend Passed Signal taxonomy |
| Fulfillment only on selected intent | N/A until L3 | SendOrderOrchestrator requires journal/task id from stack |

### 5.4 HITL surfaces

| Surface | Stack-rank | Fulfillment |
|---------|------------|-------------|
| Desk Workflow page | Shows rank + package links | Confirm / correct / send |
| DAR / Telegram | Attention-ordered bands | Phrases for pass / confirm / send |
| MCP | `list_pending_actions` evolve → stack-rank | confirm, amend, future send_order |
| Manual merge | Human always may set adapter=`manual` and book by hand | Override in-flight L3: cancel + amend policy |

---

## 6. Architectural abstraction (not “basic Schwab”)

Vendor names appear only at **config and adapter edges**. Core Winston types stay broker-neutral.

### 6.1 Layered model

```
┌─────────────────────────────────────────────────────────────┐
│  Orchestrators (HITL + Winston policy)                       │
│  DeskStack · ValidateIntent · SendOrder · Ingest · Capital … │
└────────────────────────────┬────────────────────────────────┘
                             │ uses
┌────────────────────────────▼────────────────────────────────┐
│  TradeFulfillmentPort (interface)                            │
│  place/replace/cancel/get/list_orders · list_txns ·          │
│  list_positions · balances · optional activity stream          │
└────────────────────────────┬────────────────────────────────┘
                             │ implemented by
┌────────────────────────────▼────────────────────────────────┐
│  Adapters (transport)                                        │
│  ManualAdapter · SchwabTraderApiAdapter · IbkrAdapter · …    │
└────────────────────────────┬────────────────────────────────┘
                             │ described by
┌────────────────────────────▼────────────────────────────────┐
│  CapabilityProfile + BrokerAccountBinding                    │
│  what this binding can do (equity write, options, futures,   │
│  stream, sandbox) + account_ref + secrets pointer              │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Per-OP configuration (draft)

```
portfolio.execution_mode              # paper | real  (exists)
portfolio.fulfillment_adapter_key     # manual | schwab_trader_api | ibkr_…  (registry key)
portfolio.broker_account_binding_id   # FK to credentials/account map (opaque)
# optional:
portfolio.fulfillment_policy_json     # e.g. auto_send_pyramids: false, dual_write_stops: false
```

**Prefer registry keys over enum forever:** new adapters register without schema migration for every vendor. UX may still show friendly labels: “Manual”, “Schwab”, “Interactive Brokers”.

**CapabilityProfile (example fields):**

| Capability | Manual | Schwab retail (typical) | IBKR (TBD discovery) |
|------------|--------|-------------------------|----------------------|
| `order_write` equity | no | yes | yes |
| `order_write` options | no | yes | yes |
| `order_write` futures | no | often **no** | often yes |
| `order_read` / `txn_read` | no | yes | yes |
| `activity_stream` | no | optional streamer | TBD |
| `sandbox` | n/a (Winston paper) | limited / often live-only | paper accounts common |
| `oauth_refresh_days` | n/a | ~7 | TBD |

Orchestrators **query capabilities** before calling write ops. Pyramid LEAP send on a futures-only binding → refuse with clear error, not a cryptic API 400.

### 6.3 Normalized domain types (broker-neutral)

| Type | Role |
|------|------|
| `OrderIntent` | Winston-side request: signal link, packaging, side, qty, order_kind, prices, client_order_key |
| `OrderAck` | external_order_id, status, raw_ref |
| `TradeNotification` | normalized fill/status event (née BrokerFillEvent) |
| `MatchResult` | exact / soft / ambiguous / orphan / mismatch |
| `CapitalDelta` | cash impact on Booked spine (fees, premium, flow) |
| `StackItem` | one ranked desk action (journal/task/package leg + reason) |

### 6.4 Extra-modal loose coupling (signal vs fulfillment economics)

**Tracked Winston position / risk story** (Signal Spine):

- Methodology sizes risk using EODHD parquet (e.g. ATR-17), fingerprint rules, One-Way Dynamic Risk ladder.  
- Example: “long **210** IBM @ next open, stop @ …, risk % = …”  
- DA continues evaluating **IBM** on the Book for exit/pyramid/capacity.

**Booked fulfillment** (Booked Capital Spine) may diverge:

| Signal story | Example fulfillment |
|--------------|---------------------|
| 210 shares IBM | 210 shares IBM @ **287.33** (signal prefill was 288.44) |
| 210 shares IBM | **2× Jan 2029 LEAPs** (1 ITM + 1 OTM); trade options on underlying signals |
| Commodity theme | Future / CLETF / options on future |

**What does not change Winston DA behavior:**

- Books and signal generation stay on **signal Market**.  
- Capacity / pyramid / max markets count **signal-side** occupancy (product law).  
- Methodology risk narrative remains comparable across OPs.

**What does change (Phase 1 D10 lock — supersedes “book LEAP cash immediately” for mid-life):**

- Mid-life: Wv2 **signal path** stays operational truth for sizing / stops / pyramids / exits (e.g. 210-share story).  
- Fulfillments **link** to signal with **indicated capital ±$D** (speech: “fulfillment A is for signal S…”).  
- **On exit (or explicit reconcile):** CashEvent adjustment applies actual vs signal-path honesty.  
- Same-instrument confirm price may be intentional (stop-aligned), not only broker print (D11).  
- Broker evidence matches **fill instrument**, not necessarily Book.symbol.  
- Ticket: `docs/tickets/2026-08-05-signal-path-truth-fulfillment-link-exit-reconcile.md`. Grill must update CONTEXT if law hardens.

Extra-Modal Fulfillment / Fulfillment Packaging in CONTEXT remain the names; **when capital adjusts** is the Phase 1 refinement.

---

## 7. Capital update APIs (richer surface)

Operator and system capital changes are **not** only “broker filled.” Need a clear family of APIs (internal + MCP) that orchestrators and humans share.

### 7.1 Existing (keep; document as family members)

| API | Use |
|-----|-----|
| Capital Activation | New **real** OP series + initial CashEvent `$X` |
| `wv2_add_cash_event` / `CashEventService` | Top-up **inflow** or **adjustment** on Active real only |
| Confirm / book journal | Opens lot; applies flow to capital path |
| Amend executed journal | Price/qty/stop correction; recomputes flow |
| Exit / stop-out | Closes lot; cash impact |

### 7.2 Gaps to design (grill + tickets)

| Need | Example | Proposed surface |
|------|---------|------------------|
| **Fill price divergence** | Signal 288.44 → fill 287.33 long | Book at actual on confirm; or amend after; `CapitalDelta` from fill |
| **Packaging economics** | 210 shares story → 2 LEAPs @ premium | `book_fill` with packaging; cash = premium×mult×contracts + fees — **not** 210×share |
| **Fees / commissions** | Broker charges $X | Field on fill / amend; include in flow |
| **Partial fill cascade** | 100 then 110 | Amend or multi-notification lineage under one signal identity |
| **Operator top-up** | “Add $5000 to fingerprint” | Exists — keep; show in capital family docs |
| **Operator adjustment** | Correct capital_base without trade | `adjustment` CashEvent (exists; tighten reasons) |
| **Do not** | Rewrite capital from Schwab balance dump | Reconciliation **hint** only (L2) |
| **Signal spine size** | Remains 210 risk story for audit | Never overwrite from LEAP contract count |

### 7.3 CapitalUpdateOrchestrator responsibilities

1. Classify mutation: `operator_inflow` | `operator_adjustment` | `fill_economics` | `amend_economics` | `exit_economics`.  
2. Call atomic `record_cash_event` and/or journal flow paths.  
3. Emit new `capital_base` for DAR / risk sizing of **subsequent** signals.  
4. Never invent Signal Spine share counts from booked packaging.  
5. Audit who/what (human MCP, desk, ingest match, L3 accept).

### 7.4 Loose coupling summary

```
Signal Spine (EODHD + methodology)     Booked Capital Spine (fills + cash)
─────────────────────────────────     ──────────────────────────────────
210 IBM risk story                    2 LEAPs, premiums, fees
next-open 288.44 narrative            actual 287.33 share fill (if stock)
pyramid ladder in signal units        packaging may scale differently
DA continues on IBM Book              equity curve follows booked P&L
```

Link = `signal_journal_id` / task / fulfillment lineage. **Gains/losses and capital are loosely coupled from signals by design.**

---

## 8. Adapter registry, ladder, and engines

### 8.1 Automation ladder (engine-agnostic)

| Level | Name | Orchestrators | Human |
|-------|------|---------------|-------|
| **L0** | Manual desk | DeskStack, BookFromHuman, CapitalUpdate | Always |
| **L1** | Evidence ingest | IngestNotification, FailureAttention | Confirm still |
| **L2** | Reconcile | ReconcileBrokerState, StopOutIngest | Exception review |
| **L3** | Assisted execution | SendOrder, PyramidMarket, optional StopSync | Explicit Send / accept fill |
| **L4** | Autotrader component | Policy consumes stack-rank without per-trade click | Kill switch only |

Climb: L0 → L1 → L2 → L3 (one adapter) → second adapter → L4 only with separate product ADR.

### 8.2 Where adapters live — **Phase 1 H22 locked**

| Option | Pros | Cons | Phase 1 |
|--------|------|------|---------|
| **A. Wv2 services** | Local journals; simple deploy | Secrets in Rails blast radius | Not primary |
| **B. Host worker** | Token isolation; kill process | Two deployables | Possible worker inside new monolith |
| **C. New majestic monolith** | Clean boundary; OAuth/poll isolated | Extra deployable; API contracts | **Locked day one** |

**Phase 1 lock:** **C**. Grill B charters name, internal API to Wv2, secrets, compose service, Manual placement (Wv2 vs monolith).

---

## 9. Sandbox and integration testing (mandatory)

### 9.1 Reality check (Schwab)

Prior landscape research: retail Trader API is often **live-account oriented**; thinkorswim **paperMoney ≠ API sandbox**. Official sandbox, if present, is limited and must be **re-verified in a spike** — do not assume paper order placement via API.

IBKR often has **paper trading accounts** via Gateway/TWS — promising for L3 dry-run if we choose IB first for write tests.

### 9.2 Strategy (in priority order)

1. **Prefer real vendor sandbox / paper account** when the adapter supports it (`CapabilityProfile.sandbox = true`).  
   - Spike: document Schwab app environments; IBKR paper Gateway.  
   - Config: separate binding `env: sandbox|live`; never point paper Winston OP at live write credentials.

2. **If no usable vendor sandbox:**  
   - **Contract tests** at every connection point (see matrix).  
   - **Recorded fixtures** (redacted) for normalize/match.  
   - **Adapter fakes** implementing `TradeFulfillmentPort` for orchestrator specs.  
   - **Manual + Winston paper** remains the safe methodology path (already exists).

3. **Live tiny-size** only after L3 ADR, kill switch, and contract suite green — never as the first test.

### 9.3 Connection-point contract matrix

Every row must have an automated test (unit/contract/integration) before that path is “done.”

| Boundary | Producer → consumer | Test type |
|----------|---------------------|-----------|
| DA → Desk stack | handoffs / drafts / passes | service specs + fixture DAR |
| Desk stack → ValidateIntent | StackItem → ValidationResult | unit |
| ValidateIntent → BookFromHuman | intent → journal/position | request/service specs (exist; extend) |
| ValidateIntent → SendOrder | intent → OrderAck | port mock + adapter contract |
| Adapter ↔ vendor HTTP | place/list/get | VCR/fixture or sandbox |
| Vendor/raw → normalize | payload → TradeNotification | pure unit + real fixtures |
| Notification store → match | event → MatchResult | unit + multi-OP cases |
| Match → prefill / amend | MatchResult → journal deltas | service |
| Book/amend → capital_base | fill economics → capital | service (packaging cases) |
| CashEvent API → capital_base | inflow/adjustment | existing + extend |
| Orchestrator → FailureAttention | errors → DAR/Telegram payload | unit + payload schema |
| MCP → internal API | tool → controller | MCP/contract specs |
| Wv2 ↔ host worker (if B) | job payload ↔ result | integration |
| Extra-modal match | LEAP fill ↔ equity signal | unit (no symbol equality) |
| HITL pass pyramid / take entry | mark_passed + other leg book | integration |

**Rule:** No orchestrator merges vendor JSON directly into Journal columns — always Intent / Notification types.

---

## 10. Phased plan

### Phase 0 — Land this plan (now)

1. This file at `ecosystem/plans/trade-fulfillment-engine.md`.  
2. Cross-link broker intake + grill tickets.  
3. **No** OAuth / place_order / schema until Phase 1–3.

### Phase 1 — Key questions session (operator + agent) — **DONE 2026-08-06**

Operator-prose Q&A complete. Full answers in **§13 Phase 1 decision log**. Question bank §11 retained for reference.

### Phase 2 — Grill A (`/grill-with-docs`) — desk ownership + L1 + HITL — **DONE 2026-08-06**

**Inputs:** ownership analysis, Schwab discovery, landscape §2a, ADR-009, this plan §§3–5.

**Grill A log (all locked):**
- **Q1:** Corrective amend same lot. CONTEXT: **Single Fulfillment Identity**, **Corrective Amend**.
- **Q2:** L1 match → human still confirms/amends (no silent book). CONTEXT: **Human-Gated**.
- **Q3:** API poll primary; streamer L2+; **no email SoT**; missing conf → DAR/Telegram warn + human link workflow.
- **Q4:** Extra-modal: never symbol-equality alone.
- **Q5:** **Desk Pass** third Passed Signal kind; required reason.
- **Q6:** Signal-path mid-life; **Fulfillment Link** ±$D; **Exit Capital Reconcile**.
- **Q7:** Intent-first enters; trade-first unsignaled exits.
- **Q8:** Near-term ceiling **L1 only** (L3 needs ADR / Grill B).
- **Q9:** Journal + Task as fulfillment object (v1); no new aggregate yet.

### Phase 3 — Grill B (`/grill-with-docs`) — port abstraction + capital + L3 boundary

**Inputs:** this plan §§4–9; order-vs-fill deferred; Phase 1 answers.

**Lock:** TradeFulfillmentPort shape; adapter registry; capital API family; Send vs Confirm UX; ADR-010 draft; sandbox approach; first write adapter (Schwab vs IB).

### Phase 4 — Optional Grill C — IBKR discovery

After `docs/analysis/…-ibkr-integration-discovery.md`.

### Phase 5 — Prerequisites (build when authorized)

| Item | Why |
|------|-----|
| Stack-rank API / next-actions clarity | HITL + L3 input |
| Human pass reason codes | Pyramid A vs entry D |
| DAR real process-miss attention | Open ticket |
| Durable TradeNotification store | L1 |
| Matcher + prefill | L1 |
| Capital family docs + packaging cash specs | Loose coupling |
| Contract test harness + fixtures | §9 |
| Sandbox/paper spike notes per adapter | §9 |

### Phase 6 — Port + Manual adapter + capital tests

- **Phase 1 H22:** new **majestic monolith** for broker adapters day one (not only in-Wv2). Grill B must name the monolith, APIs to Wv2, and deploy shape.  
- Interface + registry + ManualAdapter (Manual may still live in Wv2 as zero-IO path).  
- CapitalUpdateOrchestrator / signal-path + exit-reconcile tests (see D10 ticket).  
- Schema: adapter key + binding on real OPs.  
- Paper never selects live write binding.

### Phase 7 — L1 ingest (first read-capable adapter)

- Prefer adapter with sandbox or rich fixtures (likely Schwab **read**).  
- IngestNotificationOrchestrator + desk prefill / fulfillment link.  
- Human still confirms.  
- Minutes poll primary; same-day email fallback.

### Phase 8 — L2 reconcile + stop-out ingest

### Phase 9 — L3 write (one adapter; sandbox/paper first if possible)

Requires **ADR-010**. SendOrder + PyramidMarket; kill switch; contract suite green.

### Phase 10 — Second adapter + hybrid manual merge

### Non-goals

- L4 unattended autotrader without separate product ADR.  
- `place_order` inside Daily Analysis.  
- Silent Position open from notifications.  
- Full multi-leg option OMS as first-class Position.  
- Broker balances as capital_base SoT.  
- Coupling Winston paper OPs to vendor paperMoney for methodology.

---

## 11. Key questions session — question bank

### A. HITL & stack-rank

1. Confirm: humans may **pass** a ranked pyramid to free attention/capacity for another handoff, with explicit reason?  
2. Should re-rank be “pass this / do that” only, or allow free-form “enter any market”? (Draft: former only.)  
3. Who owns stack-rank display SoT — DAR only, `/operations` stack page, or both?

### B. Config & adapters

4. Registry keys (`schwab_trader_api`) vs friendly enum only?  
5. Default Capital Activation: always Manual adapter?  
6. One brokerage account → many real OPs — expected?

### C. Ladder ceiling

7. Next quarter success = L1 evidence or L3 send?  
8. Dual-write broker stops required for v1 real hygiene?  
9. Auto-send pyramids without click after entry lot open?

### D. Capital & packaging

10. When 210 IBM signal fills as 2 LEAPs, should subsequent risk % use **booked premium equity** or still **signal share risk story**? (Draft: capital_base from booked; methodology narrative retains signal.)  
11. Fill 287.33 vs story 288.44 — always book actual; amend only when already booked wrong?  
12. Operator adjustment vs amend-fill — when is each correct?

### E. Notifications

13. Acceptable notify latency: seconds / minutes / same-day?  
14. Intent-first default for enters; trade-first for stop-outs — confirm?

### F. Broker & sandbox

15. First **write** adapter: Schwab or IBKR?  
16. Futures/extra-modal near-term? (Affects capability matrix.)  
17. Accept weekly OAuth re-auth as ops ritual if Schwab?  
18. Is IBKR paper Gateway acceptable as primary L3 test bed?

### G. Failure & merge

19. Auth fail / API down → fail closed + page operator?  
20. Human books while order working → cancel adapter order + keep human book?  
21. Rejected place → high-priority Telegram/DAR always?

### H. Component boundary

22. Adapters inside Wv2 first vs host worker day one?  
23. L4 multi-year / maybe-never under current product identity?

---

## 12. Grill sessions (scheduled)

| Session | Skill | Primary docs | Outcome |
|---------|-------|--------------|---------|
| **Q&A Phase 1** | operator-prose | This plan §11 | **Done 2026-08-06** — §13 filled |
| **Grill A** | `/grill-with-docs` | Ownership + Schwab discovery + landscape §2a + ADR-009 + §5 HITL | L1 + amend law + human pass taxonomy |
| **Grill B** | `/grill-with-docs` | This plan §§4–9 + capital + port | ADR-010 outline; adapter registry; capital APIs; sandbox |
| **Grill C (opt)** | `/grill-with-docs` | IBKR discovery + ADR-010 | Second adapter matrix |

**Grill A opener:** Ratify corrective amend (shipped) as domain law; then human pass vs algorithm package.

**Grill B opener:** On `fulfillment_adapter=schwab_trader_api`, is Desk **Confirm** = book only, **Send** = place then book on fill, or operator chooses per action?  
**Draft:** Confirm ≠ Send; keep verbs distinct.

---

## 13. Decision log

### Prior / plan architecture (pre–Phase 1)

| # | Decision | Status | Source |
|---|----------|--------|--------|
| D1 | Automation never inside DA | **Accepted** | ADR-009 |
| D2 | Single fulfillment + corrective amend | **Shipped** | 2026-07-22 archive |
| D3 | Atomic ops + orchestrators (not fat verbs only) | **Accepted (plan)** | Review 2026-08-05 |
| D4 | HITL stack-rank is fulfillment input | **Phase 1 locked** | A1–A3 |
| D5 | Port + CapabilityProfile + adapters (not Schwab-core) | **Phase 1 locked** | B4 registry keys |
| D8 | Sandbox preferred; else contracts at every boundary | **Accepted (plan)** | Review 2026-08-05 |
| D13 | L3 requires new ADR-010 | **Accepted (plan)** | This plan |
| D14 | Paper OP never live place_order | **Accepted (plan)** | Landscape |

### Phase 1 Q&A — locked 2026-08-05 / 2026-08-06

| # | Decision | Status |
|---|----------|--------|
| **A1** | Humans may **pass** a ranked handoff with **reason + audit** (e.g. pass pyramid A, take entry D). Capacity never waived. **Work item:** `reason` field on Passed workflow. | **Locked** |
| **A2** | Re-rank = pass this / do that **among current handoffs only** — not free-form enter any market. | **Locked** |
| **A3** | Stack-rank display SoT: **DAR + dedicated ops stack page** (same ordered data). | **Locked** |
| **B4** | Adapter identity: **registry keys + friendly labels**. | **Locked** |
| **B5** | Capital Activation default adapter: **always Manual**. | **Locked** |
| **B6** | One brokerage account → **many real OPs** expected. | **Locked** |
| **C7** | First success = **L1 read trade confirmations** (not L3 place). | **Locked** |
| **C8** | **No dual-write** Working Stop → broker in v1; L1 may **detect** stop-out fills. | **Locked** |
| **C9** | Pyramids: **always explicit** Send or confirm — no auto-send. | **Locked** |
| **D10** | Mid-life Wv2 tracks **signal path as operational truth** (e.g. 210 shares forever for sizing/path). Fulfillments **link** to signal with **indicated capital ±$D**. **Reconcile on exit** (CashEvent). Ticket: `2026-08-05-signal-path-truth-fulfillment-link-exit-reconcile`. Grill must ratify vs current CONTEXT LEAP cash-immediate language. | **Locked** |
| **D11** | Same-instrument: confirm books **fulfillment/confirm price** (may be intentional for stop, not only broker print). Extra-modal: **link + indicated delta**. L1 may prefill actual; human confirms. | **Locked** |
| **D12** | **Amend-fill** = trade path; **CashEvent adjustment** = capital-only (incl. D10 exit ±$D); never adjustment as silent second book. | **Locked** |
| **E13** | Notify: **API poll primary** (minutes); streamer L2+; **no email SoT fallback**. Missing conf after day → DAR/Telegram warn + human link workflow. (Grill A Q3 revised Phase 1.) | **Locked (revised Grill A)** |
| **E14** | **Intent-first** for signaled enters; **trade-first** for stop-outs / unsignaled exits. | **Locked** |
| **F15** | First **write** adapter: **defer** — L1 only this phase. | **Locked** |
| **F16** | **LEAPs/options** extra-modal near-term; **futures later**. | **Locked** |
| **F17** | Schwab ~weekly OAuth re-auth: **yes**, treat as product/ops (runbook + fail closed). | **Locked** |
| **F18** | IBKR paper Gateway as L3 test bed: **N/A until write path**. | **Locked** |
| **G19** | Auth fail / API down: **fail closed + page operator**. | **Locked** |
| **G20** | Human book while order working (L3): **cancel working order + keep human book**; hard flag if cancel fails. | **Locked** |
| **G21** | Rejected place / needs-eyes L1 failures: **always high-priority DAR/Telegram**. | **Locked** |
| **H22** | Adapter home: **new majestic monolith day one** (not in-Wv2-only, not host-worker-only). Grill B names repo/service, contracts with Wv2, secrets, compose. | **Locked** |
| **H23** | L4 full autotrader: **multi-year / maybe-never**. | **Locked** |

### Implications for Grill B / architecture (from H22)

Phase 1 overrode the plan’s earlier “start inside Wv2” draft. Target shape to grill:

```
Wv2 (signal path, journals, stack-rank, capital, desk)
        │  narrow APIs / jobs
        ▼
fulfillment / broker majestic monolith  (adapters, poll, OAuth, normalize)
        │
        ▼
Schwab / IBKR / Manual transports
```

Manual may remain a null adapter inside Wv2 or a no-op in the new monolith — grill chooses.

---

## 14. Related artifacts

### Domain / ADR

- `docs/adr/ADR-009-human-gated-desk-and-fulfillment.md`  
- `docs/business-context/human-gated-desk-and-fulfillment.md`  
- `docs/adr/ADR-006-operational-portfolio-lineage-and-lifecycle.md`  
- `CONTEXT.md`

### Analysis

- `docs/analysis/2026-07-22-winston-fulfillment-ownership-and-broker-intake.md`  
- `docs/analysis/2026-07-22-schwab-integration-discovery.md`  
- `docs/analysis/2026-07-22-schwab-thinkorswim-access-landscape.md`  
- `docs/analysis/2026-07-15-winston-journal-vs-trading-ledger.md`

### Tickets

- `docs/tickets/2026-07-21-broker-confirmation-email-api-intake.md`  
- `docs/tickets/2026-07-22-grill-fulfillment-schwab-extra-modal.md`  
- `docs/tickets/archive/2026-07-22-single-fulfillment-invariant-and-post-confirm-amend.md`  
- `docs/tickets/2026-07-15-journal-ledger-order-vs-fill-deferred.md`  
- `docs/tickets/2026-07-20-dar-real-process-miss-attention.md`  
- `docs/tickets/2026-07-20-wv2-capacity-swap-desk-packages.md`  
- `docs/tickets/2026-08-05-signal-path-truth-fulfillment-link-exit-reconcile.md` (Phase 1 D10)  
- After grills: L1 implement, ADR-010, broker monolith charter, IBKR discovery, port/registry schema, Passed `reason` field, contract harness

### Interfaces

- `interfaces/winston-mcp-tools.md` — confirm, amend, cash_event, packaging

---

## 15. Immediate next steps

1. ~~Write plan~~  
2. ~~Cross-links~~  
3. ~~**Phase 1 key questions**~~ — complete 2026-08-06  
4. ~~**Grill A (Phase 2)**~~ — complete 2026-08-06; CONTEXT/BC updated  
5. **Next: Grill B (Phase 3)** — TradeFulfillmentPort, **broker majestic monolith** charter (H22), Exit Capital Reconcile APIs, Confirm vs Send, ADR-010 outline  
6. Optional IBKR discovery (not blocking L1)  
7. Then L1 tickets + monolith scaffold — **no place_order** until ADR-010

---

## 16. Author notes

**Why atomic + orchestrators:** Vendor APIs and desk policy change at different rates. Partials, cancels, and human re-rank are not special cases of `create_order` — they are first-class atomics and HITL orchestrations.

**Why not “basic Schwab”:** Schwab is a **transport adapter** with a capability profile. Core types (OrderIntent, TradeNotification, CapitalDelta, StackItem) must work for IBKR and Manual without rename.

**Why capital APIs sit next to fulfillment (updated Phase 1 D10):** Mid-life Wv2 keeps **signal-path** economics for sizing; fulfillments attach **indicated ±$D**; **exit reconcile** applies CashEvent honesty. Do not continuously rewrite capital from LEAP premiums mid-trade unless grill revises D10.

**Why stack-rank is on the critical path:** An automated send path that ignores desk priority will fight the operator (pyramid A auto-sent while human wanted entry D). HITL re-rank with audit preserves WMS integrity.

**Why sandbox/contracts are non-optional:** Capital-adjacent code without boundary tests will learn production the hard way. Prefer vendor paper; always contract-test the port.

---

*End of plan. Implementation is not authorized by this document.*
