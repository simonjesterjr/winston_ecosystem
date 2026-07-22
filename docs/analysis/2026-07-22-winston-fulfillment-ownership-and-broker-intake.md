# Winston Fulfillment Ownership + Broker Confirmation Intake

**Date:** 2026-07-22  
**Status:** Draft for `/grill-with-docs` (not yet domain law)  
**Monoliths:** primarily **Wv2**; Cromwell/MCP surfaces; optional host ingest  
**Glossary:** `CONTEXT.md` — Journal, Fulfillment, Desk Action, Desk Handoff, Desk Workflow, Signal Spine, Booked Capital Spine, Passed Signal, Human-Gated, Signaled Entry Rule, Unsignaled Exit Allowance, Signal Date, Fill Date  

### Parent ticket (broker intake — last night)

**This analysis is the design / grill vehicle for:**

[`docs/tickets/2026-07-21-broker-confirmation-email-api-intake.md`](../tickets/2026-07-21-broker-confirmation-email-api-intake.md)

That ticket (2026-07-21, series `adr-009-desk-fulfillment`) owns **discovery** of how Winston reads broker trade confirmations (email first; API second) so fills can be prefilled, matched, or verified — without becoming an OMS. The § Broker confirmation intake section below expands that ticket’s problem, desired flow, discovery scope, and acceptance checklist into grill-ready design. Grill outcomes should close or re-scope **that** ticket’s acceptance boxes, then spawn implementation tickets if needed.

**Sibling (process frailty, not a substitute for the parent):**  
[`docs/tickets/2026-07-22-single-fulfillment-invariant-and-post-confirm-amend.md`](../tickets/2026-07-22-single-fulfillment-invariant-and-post-confirm-amend.md) — one-fulfillment-per-signal + post-confirm amend (motivated by WMT double book). Complements broker intake: amend path is how “asked 253.66 / got 255.02” lands once broker truth arrives.

**Also related:**  
- `docs/business-context/human-gated-desk-and-fulfillment.md` (ADR-009 accepted)  
- `docs/analysis/2026-07-15-winston-journal-vs-trading-ledger.md`  
- **Schwab channels + automation ladder (companion discovery):** [`docs/analysis/2026-07-22-schwab-integration-discovery.md`](./2026-07-22-schwab-integration-discovery.md) — API vs email recommendation; L0–L4 full automation examine-only  
- Session evidence: Orange WMT double short (journals 105 + 119, 2026-07-22)

---

## Purpose

1. **Agree or refine** the operator’s process model: Winston owns the fulfillment list; humans validate/edit; re-booking is the exception.  
2. Capture **process frailty** exposed by a real desk session (double WMT short).  
3. **Design depth for the parent ticket** [`2026-07-21-broker-confirmation-email-api-intake`](../tickets/2026-07-21-broker-confirmation-email-api-intake.md): tee broker-notified fulfillment (API / email / push / async poll) for `/grill-with-docs` — without jumping to OMS scope.

This analysis is **engineering + product reference**. Domain rules crystallize only after grill (then `CONTEXT.md` / business-context / ADR as needed). Broker-channel decisions land back on the **parent ticket** acceptance list.

---

## Motivating incident (evidence)

DAR **2026-07-21** created **one** draft enter for Orange **WMT** short:

| Artifact | Id | Role |
|----------|----|------|
| Task | 84 | `enter`, pending → completed |
| Journal | 105 | draft → **executed** via `desk_workflow` @ 109.89 (36 units) |
| Position | 48 | OPEN short 36 WMT @ 109.89 |

~29 minutes later, a second human desk action:

| Artifact | Id | Role |
|----------|----|------|
| Journal | 119 | **new** ad-hoc book (`source=ad_hoc`), linked `signal_task_id=84` @ 109.53 (36 units) |
| Position | 50 | **second** OPEN short 36 WMT @ 109.53 |

**Likely operator intent:** amend the fill (price 109.53 vs 109.89), not open a second lot.  
**What the product did:** treat “enter/book” as a **new fulfillment** against an already-completed signal task.

That is the frailty: **no single owned fulfillment row that stays open for edit after first confirm** — only “book again.”

---

## Operator process model (proposed)

Paraphrased and mapped to Winston terms:

| Operator statement | Domain mapping | Agree? |
|--------------------|----------------|--------|
| Each signal creates a **single draft fulfillment** | DA → one **draft Journal** + one **OperationsTask** (or one ordered package of N legs, each one draft) | **Yes** — already ADR-009 / DA intent |
| Draft can be validated, edited, then becomes non-draft | Desk Workflow: amend draft → **confirm** → `executed` Journal + Position | **Yes** |
| Non-draft fulfillments may still be **edited multiple times** (asked 253.66, got 255.02) | **Post-confirm amendment** of Booked Capital Spine (price/units/fees/time) without inventing a second signal or second lot | **Agree as product goal** — **not built** today (`confirmable?` is draft-only; executed is effectively immutable except ad-hoc side paths) |
| Broker eventual truth arrives via API/email/push/poll | Inbound **Fulfillment evidence** → match → prefill or verify; still Human-Gated unless separate ADR | **Agree** — discovery ticket exists; grill needed |
| Draft or non-draft may mark **Passed Signals**; humans verify pass vs force-take within **TS rules** | Algorithmic pass + process miss; force only inside capacity/pyramid/max markets | **Yes** — capacity never waived silently |
| Human *can* create a new draft, but **should never have to** for a normal signal | Ad-hoc enter is escape hatch (`force` + notes), not the happy path | **Yes** — Signaled Entry Rule |
| Winston owns the fulfillment list: status, attention, ledger, DAR, carry-forward jobs | Winston = WMS of desk work + dual spines; not broker OMS completeness | **Yes as product ownership** |

### Recommended lifecycle (target)

```
Signal (DA / package leg)
  → Fulfillment row (Journal + Task) status=draft
       │
       ├─ amend (units, price prefill, stop, packaging, notes)  [still draft]
       ├─ pass / algorithmic pass / process-miss pass
       └─ confirm → status=executed  [Position open/close]
              │
              ├─ amend fill (price/qty/fees/time)  [same Journal/lot; audit trail]
              ├─ attach broker confirmation evidence
              └─ (exit path separate: signalled exit or unsignaled exit allowance)
```

**Invariant (proposed product law):**

> For a given signal identity `(portfolio_id, market_id, signal_date, signal_type/direction, task_id)` there is **exactly one** fulfillment Journal that humans open for that work item. Confirm does not end the *identity* of the row — it ends the *draft* phase. Later corrections edit that row (or a deliberate superseding amendment with lineage), never a silent second open.

Packages (exit ABC then enter XYZ) are **N fulfillments under one Desk Handoff**, still one row per leg.

---

## Where we agree tightly

1. **Winston owns the work queue.** DAR, pending tasks, Sunday “still open for Monday fill,” process-miss attention on Active real — all Winston. Broker owns market truth; Winston owns prioritization + dual-spine honesty.  
2. **One signal → one draft.** DA already aims here; desk UX must not fork a second enter when the first is executed.  
3. **Passed Signals are first-class work.** Algorithmic pass ≠ process miss ≠ “I skipped casually.” Human may overturn a process miss only within TS capacity (never 13th seat on a 12 cap).  
4. **Ad-hoc create is rare.** Force + audit for true exceptions (unsignaled exit is the intentional asymmetry for closes).  
5. **Post-confirm edit is normal life.** Broker fill ≠ prefill open. That must not mean “book a second short.”

---

## Where to refine (grill targets)

### R1 — “Fulfillment” vs Journal vs Task

Today three objects blur:

| Object | Owns today |
|--------|------------|
| `OperationsTask` | Attention queue (`pending` / `completed` / `expired`) |
| `Journal` | Draft → executed cash spine |
| `Position` | Live lots |

Operator language says **fulfillment**. Options for grill:

- **A.** Keep Journal as the fulfillment record; Task is the attention pointer.  
- **B.** Introduce an explicit `Fulfillment` aggregate (task + journal + evidence attachments).  
- **C.** Rename/UX-only (“fulfillment list” = pending tasks joined to journals).

**Recommendation:** **A** for v1 (least schema churn); harden invariants on Journal+Task. Promote B only if evidence attachments and multi-amend history need first-class identity.

### R2 — Post-confirm “edit” semantics

Editing an executed fill can mean:

| Mode | Effect | Risk |
|------|--------|------|
| **Corrective amend** | Same Position lot; rewrite price/units/flow; audit note | Equity path must recompute |
| **Cancel + rebook** | Close wrong lot, open right one | Heavy; clear for double-book cleanup |
| **Superseding amendment journal** | Append-only correction linked to original | Best audit; more complex equity |

**Recommendation for grill:** prefer **corrective amend** for simple price/qty mistakes within same lot; **cancel+rebook** (or explicit reverse) for accidental second lots like WMT #50.

### R3 — Executed immutability vs ledger honesty

`Journal#confirmable?` is draft-only — good against double-confirm of the same draft, **bad** against “I need to fix 255.02 → 253.66.”  
Human-Gated must still apply to amendments (who, when, why).

### R4 — Desk UX: edit vs enter

Root cause of WMT double: **desk form “enter” path does not detect “signal already fulfilled”** and offer **amend** instead of ad-hoc book.  
Product rule: opening a handoff for a completed task defaults to **view/amend**, not **new book**.

### R5 — Capacity override language

Agree: never outside TS rules. Grill should nail the verb:

- **Force take** of a process-miss signal only if capacity frees (exit another lot first via package) or algorithm swap package already permits.  
- No free-form “take 13th seat.”

### R6 — Broker intake boundary (parenthetical → first-class grill topic)

See § Broker confirmation intake below. Default stay: **evidence + prefill + mismatch attention; human still confirms or amends** — not silent Position open from email.

---

## Gaps vs current code (non-normative)

| Capability | Today | Target |
|------------|-------|--------|
| One draft per DA signal | Yes (TaskGenerator) | Keep + enforce uniqueness |
| Amend draft pre-confirm | Partial (`JournalDraftEditService`, desk edit intent) | Default desk path |
| Confirm draft → executed | Yes | Keep |
| Amend executed fill same journal/lot | **No** first-class path | **Need** |
| Block second book on same signal_task | **No** (ad-hoc allowed with signal_task_id) | **Need** warn/refuse default |
| Desk opens completed task → amend | **No** (can re-enter) | **Need** |
| Broker confirmation ingest | **No** (ticket only) | Discovery → design → build |
| Carry-forward undone tasks (e.g. Sunday job) | Expire/pass paths exist; **no** “Monday fill queue” product | Job + DAR section |
| Fulfillment list SoT UI | Ops shell panels / pending actions partial | Explicit list by status |

---

## Broker confirmation intake (for grill)

**Already filed:** `docs/tickets/2026-07-21-broker-confirmation-email-api-intake.md` (P2 discovery).  
This section expands the **analysis** the grill should walk.

### Why

Booked Capital Spine is currently **whatever the human typed**. For paper that is fine for regime tracking. For **real** (and for honest paper hygiene):

- Asked open 253.66, broker filled 255.02 → amendment, not second lot.  
- Stop-out at broker may never become a Winston exit signal → Unsignaled Exit + evidence.  
- Process miss vs “actually filled but Winston not updated” needs external truth.

### Channels (compare in grill)

| Channel | Pros | Cons | v1 candidate? |
|---------|------|------|----------------|
| **Email** (Schwab etc. confirmations) | Already arrives; no broker API approval | Brittle parsers; delay; PII in mailbox | **Fallback / degraded** (see Schwab discovery) |
| **Broker API** (orders/fills poll or webhook) | Structured; partial fills; order ids | Auth/ToS/app approval; weekly OAuth re-auth; scope creep to OMS | **Recommended primary** (Schwab Trader API read path) |
| **Push** (webhook into Wv2/Cromwell) | Low latency | Retail Schwab: no first-class fill webhook in public guides | Later / unlikely v1 |
| **Async poll** (Sidekiq “pull fills since T”) | Simple ops model; matches Schwab reality | Rate limits; not real-time; ~60d history windows | **Default transport with API** |

**Research deep-dive (2026-07-22):** [`2026-07-22-schwab-integration-discovery.md`](./2026-07-22-schwab-integration-discovery.md) — API vs email, OAuth lifetimes, endpoint map, and **L0–L4 automation ladder** (place orders / autotrader as examine-only).

**Design invariant:** all channels normalize to one **BrokerFillEvent** (name TBD in grill):

```
broker, account_ref, symbol, side, qty, price, filled_at,
order_id / confirmation_id, raw_ref, source_channel
```

### Match → Winston

```
BrokerFillEvent
  → match open draft Journal / pending task / open Position
  → outcomes:
       exact match → prefill Desk Workflow / offer one-click confirm or amend
       soft match  → human pick from candidates
       no match    → orphan queue (unsignaled exit? wrong account? external trade)
       mismatch    → attention: human-entered 109.89 vs broker 109.53
```

**Never** write Signal Spine from a broker event. Broker only feeds **Fulfillment / Booked Capital** evidence.

**Extra-modal (product law, not edge case):** a signal on a stock **Market** may be fulfilled with LEAPs / option-chain structure; a commodity theme may be fulfilled with futures, options, or CLETFs. DA and capacity stay on the **signal Market**; cash, returns, and broker evidence stay on **packaging**. Matcher must not require `broker.symbol == Book.symbol`. See landscape §2a and glossary **Extra-Modal Fulfillment**.

### Human-Gated default (proposed)

| Policy | Meaning |
|--------|---------|
| **v1** | Ingest + match + prefill; **human** confirms or amends |
| **v2 optional** | Paper autofill when Active+paper + exact match (separate decision) |
| **Never implied** | DA or email alone opens lots without policy |

### Security / ops

- Dedicated confirmation mailbox or broker API credentials on host, not in git.  
- Retain raw payload with retention policy.  
- No Telegram dump of full account numbers.

### Non-goals (restate)

- Full OMS / resting multi-leg option engine  
- Multi-broker day one (Schwab exemplar OK)  
- Replacing Human-Gated real without ADR  
- Collapsing LEAP packaging into stock share counts

---

## Carry-forward / attention jobs (example of ownership)

Operator example: **Sunday job** — “tasks still open from last week that need fulfillment Monday.”

Fits Winston ownership:

| Job idea | Behavior |
|----------|----------|
| Action-window expiry | Already: stale → Passed Signal / expired task |
| **Pre-open carry-forward** | Before Monday session: list pending drafts with fill_date ≤ next session; DAR / Cromwell attention band |
| Process-miss triage | Active **real** unconfirmed after window → high priority (ticket already: DAR real process-miss attention) |
| Orphan broker fills | Unmatched BrokerFillEvents → desk queue |

These are **queue hygiene**, not new strategy signals.

---

## Immediate product fixes (not blocked on full grill)

Small, high-leverage, motivated by WMT:

1. **Guard:** if `signal_task_id` / journal already `executed` or task `completed`, ad-hoc enter and desk enter **refuse** default (force + notes only).  
2. **Desk Workflow:** completed task deep link opens **amend/view**, not confirm-as-new.  
3. **UX copy:** distinguish “Confirm draft” vs “Correct fill” vs “Book unsignaled exit.”  
4. **Ops cleanup:** Orange WMT double short (pos 48 + 50) — human choose keep one lot; reverse the other with reason `desk_duplicate_correct`.

Post-confirm amend service + broker intake remain **grill → ticket → build**.

---

## Grill-with-docs session brief

**Command:** `/grill-with-docs` against this analysis **and** [`2026-07-22-schwab-integration-discovery.md`](./2026-07-22-schwab-integration-discovery.md)  
**Outcomes wanted:**

1. Confirm **one fulfillment identity per signal leg** as domain law (CONTEXT / business-context update).  
2. Choose post-confirm edit mode (corrective vs superseding).  
3. Choose fulfillment object model (Journal-centric vs new aggregate).  
4. Lock broker intake v1 channel + human-still-confirms (**draft: Schwab API primary, email fallback**).  
5. Decide whether paper autofill ever attaches to matched broker/paper path (likely still separate).  
6. Lock automation **ceiling for near term** (L1–L2 only vs appetite for L3 “send to broker” ADR later).  
7. File/refresh tickets:  
   - single-fulfillment invariant + amend-executed  
   - desk UX completed-task → amend  
   - broker intake implementation (after discovery acceptance)  
   - carry-forward attention job  
   - (later) L3 broker adapter ADR/spike — only if grill wants a horizon  

**Suggested first grill question:**

> When you said you wanted 109.53 instead of 109.89 on WMT, should Winston have **rewritten journal 105 / position 48**, or **appended a correction journal** linked to 105, or **closed 48 and opened a new lot**?

**Recommendation to open with:** rewrite same lot (corrective amend) for simple price fix; reserve close+reopen for true cancel/re-trade.

**Second grill block (Schwab / automation):** after amend semantics, lock channel (API vs email) and “trade-then-book vs intent-first” default — see discovery analysis recommended defaults.

---

## Ticket / doc cross-links

| Artifact | Role |
|----------|------|
| `docs/tickets/2026-07-21-broker-confirmation-email-api-intake.md` | Discovery for broker channels |
| `docs/analysis/2026-07-22-schwab-integration-discovery.md` | Schwab API vs email + L0–L4 automation ladder |
| `docs/tickets/2026-07-20-dar-real-process-miss-attention.md` | Process-miss attention |
| `docs/tickets/2026-07-15-journal-ledger-*` | Ledger evolution series |
| `docs/business-context/human-gated-desk-and-fulfillment.md` | Accepted boundary — extend after grill |
| This analysis | Process model + frailty + grill tee |

**Follow-on tickets to file after grill (stubs, not filed here):**

- `single-fulfillment-invariant-and-post-confirm-amend`  
- `desk-completed-task-opens-amend-not-rebook`  
- `fulfillment-carry-forward-attention-job`  

---

## Decision log (pre-grill)

| # | Statement | Status |
|---|-----------|--------|
| D1 | Agree with operator model: Winston owns fulfillment list; one draft per signal; post-confirm edit; pass as work; ad-hoc rare | **Agreed** (this session) |
| D2 | Paper autofill still **not** current behavior; optional later | Unchanged |
| D3 | Broker intake is evidence path, not DA | Proposed |
| D4 | WMT double book is product frailty + ops cleanup | **Fact** |

---

## Appendix — status vocabulary (today)

`Journal::STATUSES` = `draft | executed | cancelled | passed`  
`OperationsTask::STATUSES` = `pending | expired | completed | in_progress`

Proposed operator-facing labels (UX only until grill):

| Operator | Journal | Task |
|----------|---------|------|
| Needs attention | draft | pending |
| Filled / booked | executed | completed |
| Passed (algo or process) | passed | expired/completed + PassedSignal |
| Corrected after book | executed (+ amendment audit) | completed |
