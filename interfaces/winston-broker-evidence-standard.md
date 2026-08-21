# Winston Broker Evidence Standard (v0.1)

**Version:** 0.1  
**Status:** **Accepted** for L1 Confirmation Intake (2026-08-09) — Grill B Q4 locked; implementers code against this file  
**Owner (writer):** **Broker Gateway** (`broker_gateway`)  
**Primary consumers (readers):** **Winston v2** Confirmation Intake (match / prefill / attention); ops tooling; optional mount-side readers  
**Orthogonal to:** **Winston EOD Standard** (market bars / parquet — DM)  

This is the durable **file + pull API** contract for broker order/fill/lifecycle **evidence**. It is not capital source of truth, not Signal Spine, and not a desk/OMS product surface.

Glossary: `CONTEXT.md` — Broker Gateway, Winston Broker Evidence Standard, Trade Notification, Confirmation Intake, CapabilityProfile (via plan), Extra-Modal Fulfillment.  
Plan locks: `plans/trade-fulfillment-engine.md` Grill B Q2–Q4.  
Fill-field provenance (vendor-shaped notes): `docs/analysis/2026-07-22-schwab-integration-discovery.md`.

---

## 1. Purpose and ownership

| Role | Owns | Does not own |
|------|------|----------------|
| **Broker Gateway** | OAuth/session, adapter registry + **CapabilityProfile**, poll/refresh jobs, **append-only evidence events**, optional rebuildable snapshots, raw payload refs, bindings registry, ingest cursors/status, minimal ops UI | Journals, stack-rank, `capital_base`, Desk Confirm / Desk Send policy, match→book |
| **Wv2 Confirmation Intake** | Pull events (API and/or mount), normalize into in-process **Trade Notification** faces, match to **Single Fulfillment Identity**, prefill / mismatch / orphan attention, Human-Gated **Desk Confirm** / **Corrective Amend** | Writing the BG evidence store; placing broker orders (L1) |
| **Manual fulfillment** | Zero-IO path **inside Wv2** (human types fills) | Does not require BG for L0 |

**Composition pattern (DM-shaped):** API commands to *do work*; **files as evidence truth**; PG as registry / bindings / cursors / status — **not** the event log as sole truth.

| This standard is | This standard is not |
|------------------|----------------------|
| Durable broker lifecycle evidence (orders, trades/txns, auth health) | Capital SoT (`CashEvent` + booked journals remain SoT) |
| Input to Confirmation Intake | Signal Spine / DA methodology truth |
| Orthogonal to Winston EOD parquet | A substitute for Market bars or risk sizing |
| Append-only, idempotent events | Mutable status-only files with no event log |
| Allowed to store **orphans** (no Winston intent) | Allowed to require a Winston journal id before store |

Consumers **read**; they **do not write** the evidence store.

---

## 2. Primary store shape

### 2.1 Event log (source of truth for evidence history)

- **Format:** append-only **JSONL** (one JSON object per line, UTF-8).
- **Semantics:** each line is one **logical evidence event** after normalize + idempotency gate.
- **Idempotency:** same vendor event → **one** logical event (see §7). Re-polls and retries must not double-append logical duplicates.
- **Ordering:** append order is ingest order; consumers should sort/filter by `occurred_at` / `event_id` as needed. Do not assume vendor chronological perfection across channels.

### 2.2 Optional snapshots (rebuildable)

- Per-entity **snapshots** (e.g. latest order state, last auth status) may exist under a `snapshots/` tree.
- Snapshots are **derived** from the event log and may be rebuilt/repaired from JSONL.
- Snapshots **never** replace the log as audit history; if log and snapshot disagree, **log wins** after rebuild.

### 2.3 Postgres (registry / ops, not sole event truth)

PG (BG-owned DB) holds:

- Adapter registry keys and **CapabilityProfile**
- **Bindings** (account/session pointers — secrets by reference only)
- Poll / pull **cursors** (vendor window + consumer cursor positions)
- Auth health, last refresh outcome, job status
- Optional indexes of event_id / idempotency_key for ops (may mirror file; file remains portable truth)

**No shared PG with Wv2.** No balances-as-capital_base.

### 2.4 Raw payloads

Vendor JSON (or later MIME) is stored as **raw payload objects** referenced by `raw_payload_ref` — not inlined into every JSONL line when large. Retention of raw vs normalized: **TBD** (ops policy); contract requires a stable ref string at write time.

---

## 3. Location convention (**locked for L1**)

Under Broker Gateway data root (compose volume), not Wv2 storage:

```
data/evidence/{binding_id}/events.jsonl
data/evidence/{binding_id}/snapshots/          # optional; rebuildable
data/evidence/{binding_id}/raw/{yyyy}/{mm}/…   # optional raw payload objects
```

| Path element | Meaning |
|--------------|---------|
| `binding_id` | Opaque BG binding identifier (stable string/UUID, e.g. `bnd_…`). **Not** a Winston OP id by itself — OP↔binding is Grill B **Q8** (deferred). |
| `events.jsonl` | Append-only log for that binding |
| `snapshots/` | Optional derived latest-state files (schema free to evolve if rebuildable) |
| `raw/` | Optional opaque vendor payloads; referenced from events |

**Rotation (L1):** single `events.jsonl` per binding. Later partition (`events_YYYYMMDD.jsonl` or size segments) may land **without** changing the event envelope — document in a version-note if/when added.

**Mount read:** Wv2 (or agents) may mount BG evidence volume **read-only** for offline/debug; product path is **pull API** (§9).

Analog: DM `data/markets/{SYMBOL}/bars.parquet` — different domain, same “files + API commands + PG metadata” spirit. See `interfaces/winston-eod-parquet-standard.md`.

---

## 4. Event envelope

Every JSONL line is an object with this **envelope** (v0.1 minimum). Unknown fields: consumers **ignore**; producers may add vendor diagnostics under `payload.extensions` or envelope extensions only with a schema_version bump when semantic.

| Field | Type | Required | Notes |
|-------|------|----------|--------|
| `schema_version` | string | yes | This document: `"0.1"` |
| `event_id` | string | yes | Globally unique within BG (UUID recommended). Assigned at store time. |
| `idempotency_key` | string | yes | Stable key for vendor event identity (see §7). |
| `occurred_at` | string (ISO-8601) | yes | When the broker-side fact happened (fill time, order update time, auth change). Prefer vendor timestamps; if missing, use best available and set `payload.time_quality`. |
| `ingested_at` | string (ISO-8601) | yes | When BG accepted/stored the event (UTC recommended). |
| `binding_id` | string | yes | BG binding that sourced the event. |
| `adapter_key` | string | yes | Registry key, e.g. `schwab_trader_api`, `ibkr_…`, `dummy_sim`. |
| `event_type` | string | yes | See §5. |
| `vendor_account_ref` | string | yes | **Redacted / hashed** account handle (e.g. `hash:…` or last-4 mapping key). Never full account number in JSONL or logs. |
| `raw_payload_ref` | string \| null | yes (nullable) | Storage key for raw vendor payload; null only when synthetic and no raw exists. |
| `payload` | object | yes | Normalized body for `event_type` (see §6). |

### 4.1 Example (illustrative)

```json
{
  "schema_version": "0.1",
  "event_id": "0192f0a1-b2c3-7def-8901-23456789abcd",
  "idempotency_key": "schwab_trader_api:txn:hash:9f3a:T-123456789",
  "occurred_at": "2026-08-08T15:42:11Z",
  "ingested_at": "2026-08-08T15:43:02Z",
  "binding_id": "bnd_01HZX…",
  "adapter_key": "schwab_trader_api",
  "event_type": "trade.executed",
  "vendor_account_ref": "hash:9f3a…",
  "raw_payload_ref": "raw/2026/08/txn-T-123456789.json",
  "payload": {
    "source_channel": "api_transactions",
    "external_order_id": "…",
    "external_txn_id": "T-123456789",
    "symbol": "WMT",
    "instrument_type": "option",
    "underlying_hint": "WMT",
    "side": "buy",
    "quantity": "2",
    "fill_price": "27.00",
    "multiplier": "100",
    "filled_at": "2026-08-08T15:42:11Z",
    "fees": "1.30",
    "partial": false,
    "legs": null,
    "extra_modal_note": "broker symbol may differ from Winston signal Market"
  }
}
```

---

## 5. Event types (L1 minimum + extensible)

Use dotted nouns. **L1 first-ship** adapters must produce enough of these to support Confirmation Intake (`auth` + `order_read` + `txn_read`). Types are **extensible**; unknown types are stored and passed through — consumers may ignore until supported.

### 5.1 Auth / binding health

| `event_type` | Meaning |
|--------------|---------|
| `auth.status` | Auth/session state change or periodic health sample (ok, needs_reauth, failed, refreshed). |

### 5.2 Order lifecycle

| `event_type` | Meaning |
|--------------|---------|
| `order.upserted` | Order observed or updated (working, partial, filled, canceled, rejected, expired, …). Prefer upsert semantics over separate create/update types at L1. |
| `order.filled` | Terminal or cumulative filled state for an order (may accompany or follow `order.upserted`). |
| `order.canceled` | Optional explicit cancel (may be folded into `order.upserted` status). |
| `order.rejected` | Optional explicit reject. |

### 5.3 Trade / transaction

| `event_type` | Meaning |
|--------------|---------|
| `trade.executed` | Economic trade/transaction print (qty, price, fees, instrument) — often best match fuel for fills. |

### 5.4 Later (not required for L1 store; reserved)

| `event_type` | Level |
|--------------|--------|
| `position.snapshot` | L2 hint (not capital SoT) |
| `balance.snapshot` | L2 hint (never `capital_base`) |
| `activity.stream` | Optional stream-sourced activity |

**Do not invent L3 place-order request/response types here** — Order Intent / write ack lives under ADR-010 when authorized. Evidence of *fills that resulted from* human or future send still uses order/trade events above.

---

## 6. Normalized trade / order payload (minimum fields)

`payload` shape depends on `event_type`. Decimal quantities and prices are **strings** in JSON (avoid float drift) unless an implement ticket locks numeric with fixed scale.

### 6.1 Common payload fields (orders + trades)

| Field | Required for trade/order events | Notes |
|-------|----------------------------------|--------|
| `source_channel` | recommended | e.g. `api_orders`, `api_transactions`, `sim`, `manual_attach` (attach still normalizes into this store only if BG is told to; Manual path usually stays in Wv2) |
| `external_order_id` | when known | Vendor order id |
| `external_txn_id` / `external_confirmation_id` | when known | Vendor transaction / confirmation id |
| `symbol` | yes for trade; yes when order has instrument | **Broker / fill instrument** (equity ticker, OCC option, future root, ETF, …) |
| `instrument_type` | recommended | `equity` \| `option` \| `future` \| `etf` \| `other` |
| `underlying_hint` | when available | Parsed/underlying for extra-modal soft match **in Wv2** — BG stores; does not match to journals |
| `side` | yes when applicable | `buy` \| `sell` \| `buy_to_cover` \| `sell_short` \| vendor-normalized equivalent |
| `quantity` | yes when applicable | Shares or contracts as broker reports |
| `fill_price` / `avg_fill_price` | when filled | Avg if partials aggregated |
| `limit_price` / `stop_price` | optional | Order working prices |
| `filled_at` / `order_updated_at` | when known | Prefer vendor |
| `order_status` | for order.* | Vendor-normalized: `working`, `partial`, `filled`, `canceled`, `rejected`, `expired`, `unknown` |
| `fees` | optional | Commission/fees if provided |
| `multiplier` | optional | e.g. `100` equity options |
| `currency` | optional | Default assume account currency |
| `partial` | recommended for fills | `true` if partial fill slice |
| `legs` | optional | Array of leg objects for multi-leg; each leg has symbol/side/qty/price as available |
| `time_quality` | optional | e.g. `vendor`, `inferred_ingest` |

### 6.2 Extra-modal awareness (required product note)

- **Broker `symbol` may ≠ Winston signal Market** (LEAP/OCC, proxy ETF, structure, etc.).
- Evidence store **must not** require equality with any Winston Book.
- Matching and packaging link are **Wv2** concerns (Grill B **Q9** deferred for match detail); this standard only requires honest fill-instrument fields + optional `underlying_hint`.
- Never rewrite Signal Spine from these events.

### 6.3 Multi-leg / partial notes

- **Partials:** either one `trade.executed` per partial with `partial: true`, or aggregated avg with explicit note in `payload.extensions` — adapter must document which; idempotency keys must not collapse distinct partials incorrectly.
- **Multi-leg:** prefer one event with `legs[]` when vendor returns a structure; otherwise N leg events sharing a common external order/strategy id in payload.

### 6.4 `auth.status` payload (minimum)

| Field | Notes |
|-------|--------|
| `status` | `ok` \| `needs_reauth` \| `failed` \| `refreshed` \| `unknown` |
| `detail` | Non-secret human/ops message |
| `expires_at` | Optional token/session expiry if known |

### 6.5 Relation to Trade Notification

**Trade Notification** (CONTEXT) is the **in-process / product face** Wv2 uses after pull. A stored evidence event of type `trade.executed` / `order.filled` / `order.upserted` is the durable BG form; Wv2 maps envelope + payload → Trade Notification for match. Do not require two divergent schemas long-term — evolve together under version bumps.

---

## 7. Idempotency rules

**Rule:** Same vendor fact → **one** logical event in the log (one `event_id` / one append for that `idempotency_key`).

### 7.1 Key construction (normative sketch)

```
idempotency_key = "{adapter_key}:{kind}:{vendor_account_ref}:{vendor_stable_id}"
```

| Prefer vendor_stable_id | Kind example |
|-------------------------|--------------|
| Transaction / activity id | `txn` |
| Order id + status version or filled cumulative hash | `order` |
| Auth transition id or `(status, occurred_at bucket)` | `auth` |

If vendor lacks stable ids: hash of canonical normalized fields (symbol, side, qty, price, occurred_at truncated, channel) — document risk of collision; prefer upgrading when vendor id appears.

### 7.2 Behavior on duplicate

1. Compute `idempotency_key` before append.  
2. If key already stored for this `binding_id` → **do not append** a second logical event; may update PG cursor only; optional ops metric `duplicate_suppressed`.  
3. **Material change** with same vendor id (rare correction): either new event with new key suffix (`:rev2`) **or** explicit `event_type` correction later — **do not silently mutate** prior JSONL lines. Append-only.

### 7.3 Atomic ops (plan alignment)

Normalize + store are atomic ops on the transport side (`normalize_notification` / `store_notification` in plan language). Store is idempotent on external ids / `idempotency_key`.

---

## 8. Orphans (first-class)

An **orphan** is an evidence event with **no** known Winston intent (no journal / task / Order Intent link) at store time.

| Rule | Detail |
|------|--------|
| Store always | BG **must** store orphans; do not drop because no OP matched |
| No journal required | Requiring `signal_journal_id` before store is **out of contract** |
| Match later | Wv2 may link later (human attach, soft match, unsignaled exit path) |
| Same envelope | Orphans use the same JSONL shape; optional `payload.winston_link` only if BG is ever told a link (usually Wv2-side) |

Spirit: same as DM holding market data before a Book cares.

---

## 9. Consumer pull API (**normative for L1**)

Internal HTTP **owned by Broker Gateway**.

Base: `/api/v1` (compose DNS `http://broker_gateway:3000`; host **:3003**).  
**Auth:** optional shared secret header `X-BG-Token` (or `Authorization: Bearer …`) when `BG_INTERNAL_TOKEN` is set on BG; when unset (local dev), open on the private network.  
**Freeze (MG1 2026-08-09):** per-binding routes under `/api/v1/bindings/{binding_id}/…`. Flat `/api/v1/refresh` and `/api/v1/events` are **not** the product contract.

### 9.1 Refresh / poll command

```
POST /api/v1/bindings/{binding_id}/refresh
```

| | |
|--|--|
| **Purpose** | Ask BG to authenticate if needed and poll vendor (orders/txns per CapabilityProfile); normalize + store new events |
| **Body (optional)** | `{ "since": "ISO-8601", "force": false }` — hints; BG owns actual vendor cursors |
| **Response** | `{ "binding_id", "status": "accepted"\|"ok"\|"auth_failed"\|"error"\|"not_found", "events_appended": N, "head_cursor": "…", "auth_status": "…", "error": "…" }` |
| **Semantics** | Retries are safe (store idempotent). L1 may run **sync** (`status: "ok"`) or async (`accepted` + `job_id`) — if async, include `job_id`. |

**Fail closed** on auth failure: surface `auth_failed`; page operator per plan (G19). Do not invent fills.

### 9.2 Pull events

```
GET /api/v1/bindings/{binding_id}/events?since_cursor={cursor}&limit={n}
```

| | |
|--|--|
| **Purpose** | Consumer (Wv2) reads events after its last processed cursor |
| **Response** | `{ "binding_id", "events": [ /* envelope objects */ ], "next_cursor": "…", "has_more": bool, "limit": n }` |
| **Empty** | `events: []`; `next_cursor` equals request cursor (or `"0"` at epoch) |

Default `limit` **100**, max **1000**. Optional later: “events available” notify — **not** required for L1; pull remains primary.

### 9.3 Cursor semantics (**locked**)

| Rule | Detail |
|------|--------|
| Opaque | `cursor` / `next_cursor` / `head_cursor` are opaque strings issued by BG (L1: monotonic per-binding sequence as decimal string). Consumers **must not** parse structure for business logic. |
| Monotonic pull | `since_cursor` means “events **after** this cursor” in BG’s total order for that binding. |
| **Consumer owns durable cursor** | **Wv2 stores** its own last committed `next_cursor` per binding (Wv2 DB). BG does **not** require consumer ack to advance the stream; pull is stateless w.r.t. consumer progress. |
| BG ops metadata | BG **may** track last-served / head seq for ops dashboards; that is not the consumer SoT. |
| Restart | Re-pull from last committed cursor; consumer dedupes on `event_id` / `idempotency_key`. |
| Bootstrap | Omit `since_cursor` or pass empty / `"0"` → from binding epoch. Vendor lookback windows (e.g. ~60 days) apply at **poll** time, not at pull. |
| No shared event PG | Cursor is not a join key into Wv2 journals. |

### 9.4 Related read endpoints (L1)

| Path | Purpose |
|------|---------|
| `GET /api/v1/bindings` | List bindings (registry) |
| `GET /api/v1/bindings/{binding_id}` | Binding status, CapabilityProfile, auth / last refresh health |

---

## 10. CapabilityProfile (L1)

First-ship profile for Confirmation Intake (Grill B Q2):

| Capability | L1 | Notes |
|------------|----|--------|
| `auth` | **required** | OAuth/session ready; `auth.status` events |
| `order_read` | **required** | list/get orders → `order.*` events |
| `txn_read` | **required** | transactions/trades → `trade.executed` |
| `position_read` | L2 | hints only |
| `balance_read` | L2 | **never** capital_base SoT |
| `order_write` | L3 | **out of scope** until ADR-010 — not this standard’s write API |
| `activity_stream` | optional later | |

**Confirmation Intake** is the product workflow name — **not** a capability flag named `order_confirm` (collides with Desk Confirm).

Bindings without `order_write` support **Desk Confirm** + evidence only (no Desk Send).

---

## 11. Dummy / sim adapter

**Product law (locked 2026-08-09):** paper OPs default to **`dummy_sim`** in BG; synthetic evidence events **must still conform** to this standard (same envelope, idempotency, event types, pull API). **`manual`** remains a zero-IO escape hatch **inside Wv2 only** (does not write this store).

| Rule | Detail |
|------|--------|
| Conformance | Synthetic events use `adapter_key` **`dummy_sim`**; `source_channel: "sim"` |
| No special consumer branch for shape | Wv2 Confirmation Intake should not need a second schema |
| Paper OPs | Winston paper stays Winston-paper by default (plan); sim is for **rehearsing intake**, not live write |
| No live credentials | Paper/`dummy_sim` never holds live OAuth or `order_write` |

---

## 12. Security and retention

| Rule | Detail |
|------|--------|
| **Secrets** | Never in JSONL, snapshots, or API event bodies. Tokens live in secret store; PG holds pointers only. |
| **Account numbers** | Redact in `vendor_account_ref`, logs, Telegram, DAR excerpts. Prefer hash / last-4 mapping. |
| **Raw payloads** | May contain sensitive fields — access-controlled; do not copy full raw into Telegram. |
| **Wv2 process** | Must not hold primary OAuth material when BG is live (secrets isolated). |
| **Retention** | **TBD** — legal/ops policy for JSONL + raw. Contract requires append-only while retained; deletion policy is a later ops note, not silent rewrite. |

---

## 13. Versioning

| Version | Date | Notes |
|---------|------|--------|
| **0.1** | 2026-08-09 | Initial from Grill B Q4; L1 envelope + pull API |
| **0.1 Accepted** | 2026-08-09 | Location layout locked; consumer-owned cursor locked; MG1 routes normative; paper→`dummy_sim` locked |

- Bump `schema_version` when envelope semantics change or required fields are added/removed.  
- Additive optional fields may land under 0.1.x notes without forcing consumer breaks if ignore-unknown holds.  
- Old events remain readable; consumers tolerate unknown `event_type` and extra fields.

---

## 14. Non-goals

| Non-goal | Why |
|----------|-----|
| **`order_write` / place_order contract** | ADR-010 / L3; not this file |
| **Balances as `capital_base`** | CashEvents + booked journals remain capital SoT |
| **Email as SoT** | Grill A: API poll primary; no email SoT fallback |
| **Shared PG with Wv2** | Monolith boundary |
| **Silent book from evidence** | Human-Gated Desk Confirm (or later explicit policy) |
| **Requiring Winston journal id to store** | Orphans first-class |
| **Mutating JSONL in place** | Append-only |
| **Signal Spine rewrite** | Extra-modal fills stay evidence only |
| **Full OMS order book in Winston** | Deferred; Working Stop remains desk SoT until insufficient |
| **Scaffolding `broker_gateway` app** | Separate build (landed); this file is the event contract only |

---

## 15. Consumer expectations (Wv2)

1. Call `POST …/refresh` on a schedule or desk-triggered poll (minutes during market hours + EOD hygiene — implement ticket).  
2. `GET …/events?since_cursor=` and advance cursor only after durable local handling.  
3. Map events → **Trade Notification**; run match (exact / soft / ambiguous / orphan / mismatch).  
4. Prefill or attention only; **Desk Confirm** / **Corrective Amend** books capital.  
5. Never treat missing events as permission to invent fills; missing expected confirm → DAR/Telegram attention + human link workflow.

---

## 16. BG producer expectations

1. Authenticate per binding; emit `auth.status` on material changes.  
2. Poll orders + transactions within CapabilityProfile; respect vendor windows (e.g. ~60 days).  
3. Normalize → idempotent store → append JSONL; optional snapshot rebuild.  
4. Keep raw payload refs when vendor body exists.  
5. Serve pull API; maintain opaque cursors.  
6. Minimal ops UI: bindings, registry, auth health, ingest logs (product charter — not this schema’s detail).

---

## 17. Open questions (esp. Grill B Q8)

Deferred by design until after build phases; listed so implementers do not invent locks:

| ID | Topic | Impact on this standard |
|----|--------|-------------------------|
| **Q8** | OP ↔ broker account **binding model** (account-level BG binding vs per-OP isolation; multi-OP same account) | `binding_id` granularity; whether path layout is 1:1 with brokerage account; how Wv2 maps OP → binding for refresh/pull; match ambiguity across OPs |
| **Q9** | Match ownership detail | Mostly Wv2; may add optional `payload` correlation fields later — not required for store |
| Retention | How long raw + JSONL kept | Ops note; not envelope |
| Partition / rotation | Daily segments after L1 | Location note only; single file locked for L1 |
| Async refresh | Sync vs job_id on POST refresh | Both allowed; L1 may ship sync |

---

## 18. Related artifacts

- `CONTEXT.md` — Broker Gateway, Winston Broker Evidence Standard, Trade Notification, Confirmation Intake  
- `plans/trade-fulfillment-engine.md` — Grill B Q2–Q4; atomic normalize/store; connection matrix  
- `interfaces/winston-eod-parquet-standard.md` — peer style (market data; orthogonal domain)  
- `docs/analysis/2026-07-22-schwab-integration-discovery.md` — vendor read fields, normalized fill sketch  
- `docs/analysis/2026-07-22-winston-fulfillment-ownership-and-broker-intake.md` — ownership tee  
- `docs/session-reports/2026-08-09-1408-trade-fulfillment-grill-b.md` — Q4 lock  
- `docs/business-context/human-gated-desk-and-fulfillment.md` — desk law  
- `docs/tickets/2026-08-09-winston-broker-evidence-standard-interface.md` — acceptance ticket  
- `docs/tickets/2026-08-09-bg-evidence-store-jsonl-and-cursors.md` — BG store implement  
- `docs/tickets/2026-08-09-bg-internal-api-refresh-events.md` — pull/refresh API implement  
- `interfaces/fixtures/broker-evidence/` — L1 contract fixtures (v0.1)

---

*End of Winston Broker Evidence Standard v0.1 (Accepted for L1). Schema bumps require a version note in §13; domain locks still require Grill/ADR process.*
