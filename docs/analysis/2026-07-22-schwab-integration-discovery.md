# Schwab Integration Discovery — Confirmation Intake → Full Automation Ladder

**Date:** 2026-07-22  
**Status:** Discovery / grill input (not domain law; **not** an implementation plan)  
**Monoliths:** primarily **Wv2**; optional host-side broker adapter; Cromwell/MCP later  
**Series:** `adr-009-desk-fulfillment`  
**Do not implement yet** — examine architecture, product boundary, and channel choice.

### Parent artifacts

| Artifact | Role |
|----------|------|
| [`docs/tickets/2026-07-21-broker-confirmation-email-api-intake.md`](../tickets/2026-07-21-broker-confirmation-email-api-intake.md) | **Parent discovery ticket** — confirmation intake (email/API) |
| [`docs/analysis/2026-07-22-winston-fulfillment-ownership-and-broker-intake.md`](./2026-07-22-winston-fulfillment-ownership-and-broker-intake.md) | **Grill tee** — fulfillment ownership + broker intake design |
| [`docs/analysis/2026-07-22-schwab-thinkorswim-access-landscape.md`](./2026-07-22-schwab-thinkorswim-access-landscape.md) | **Pre-design landscape** — full Schwab/ToS access map, issues register, capabilities |
| ADR-009 + `docs/business-context/human-gated-desk-and-fulfillment.md` | Product law: Winston is signal + desk prioritization, **not** OMS |
| This doc | Winston-scoped channel recommendation + **full automation ladder** for grill |

**Grill command:** `/grill-with-docs` against the fulfillment ownership analysis **and** this Schwab discovery (channel + automation ladder sections).

---

## Purpose

1. Answer the parent ticket’s discovery questions for **Charles Schwab as first exemplar**: email vs API vs both.  
2. Expand discovery beyond “read confirmations” to a **full automation ladder** (place orders, stops, reconcile positions, eventual autotrader component) — still **examine only**.  
3. Keep every option stress-tested against ADR-009: **Daily Analysis never opens lots**; **real** stays **Human-Gated** until a **separate explicit ADR**; broker truth feeds **Booked Capital Spine / Fulfillment evidence**, never **Signal Spine**.  
4. Honor **Extra-Modal Fulfillment**: signal Market stays on the Book for DA/risk methodology; cash/returns/broker fills track packaging (LEAP, options, futures, CLETF, …) asynchronously and linked.

---

## Executive recommendation (v1 discovery)

| Decision | Recommendation | Why |
|----------|----------------|-----|
| **v1 intake channel** | **Schwab Trader API (read path)** as primary; email as optional secondary / fallback | Structured fills, order IDs, partial fills, positions; same OAuth already required for any later automation |
| **Email** | Keep as **backup / human-forward** path, not primary SoT | Brittle HTML; no stable public schema; delay; PII mailbox ops; still useful if API tokens lapse |
| **Normalized event** | One **BrokerFillEvent** (name TBD in grill) from any channel | Dual-path design already in parent ticket |
| **Human-Gated** | **v1 always human confirms** (prefill / mismatch attention) | ADR-009; WMT double-book frailty is desk UX + amend, not silent book-from-broker |
| **Write / place orders** | **Out of v1**; design as **L3** on the ladder below | Separate component + ADR; not inside DA |
| **Full autotrader** | **L4** — future product; separate majestic component, not Wv2 DA | ADR-009 decision C already named this |

**Bottom line:** Prefer **API poll of orders + transactions** for Winston fulfillment evidence. Treat email as degraded mode. Design the normalized event and matcher so a later **order-placement adapter** reuses the same spine without turning DA into an OMS.

---

## What Schwab actually offers (research snapshot, 2026-07)

Sources: Schwab Developer Portal product positioning; community reverse-engineering and `schwab-py` client surface (unofficial wrapper around Trader API — Individual). Official portal pages are auth-walled; treat field-level schemas as **verify-on-spike**, not gospel.

### Product surface

Schwab’s retail **Trader API — Individual** is the relevant product for a self-directed brokerage account:

| API product group | Capability class |
|-------------------|------------------|
| **Accounts and Trading Production** | Account hashes, balances, positions, orders (place/replace/cancel/get), transactions |
| **Market Data Production** | Quotes, price history, option chains, movers, hours |

Individual developers: typically **one app**; brokerage account required; app approval (“Ready for Use”) before production. OAuth 2.0; apps authorize access to selected linked accounts.

### Auth reality (ops cost)

| Token | Lifetime (community-reported) | Implication for Winston |
|-------|------------------------------|-------------------------|
| Access token | ~30 minutes | Sidekiq/host must refresh on schedule |
| Refresh token | ~7 days | **Human re-auth weekly** (or on failure) — not “set and forget” |
| Initial OAuth | Browser consent + callback (often `https://127.0.0.1`) | Host-side secret store; never git |

This alone argues against treating broker integration as a casual Rails gem with env vars only: **token lifecycle is an ops product**.

### Read endpoints useful for intake (L1–L2)

Mapped to Winston needs via community client surface (`schwab-py` and equivalents):

| Need | Schwab-ish capability | Winston use |
|------|----------------------|-------------|
| Account id mapping | `GET …/accounts/accountNumbers` → `accountNumber` + **hashValue** | Map OP / desk “broker account ref” to hash; never store raw account as only key in logs |
| Positions | `GET account` with positions fields | Reconcile open lots vs Booked Capital Spine; orphan detection |
| Order history | `GET …/orders` (status filter includes **FILLED**; window often **~60 days**) | Primary fill discovery when Winston (or human) placed order and has order id |
| Single order | `GET order by id` | Poll after place (L3) or after human trade if order id known |
| Transactions | `GET …/transactions` type **TRADE** (and kin); **~60 day** window typical | Best **post-fill economic truth** (qty, price, fees, symbol) for matching |
| Balances | Account balances | Cash sanity vs CashEvents (secondary) |

**No official webhook / push fill stream** is a first-class documented retail product in public guides reviewed here. Streaming exists more for **market data** (WebSocket) than “fill arrived” push into your app. **Async poll (Sidekiq)** is the realistic ops model for L2.

### Write endpoints (L3+ — examine only)

| Capability | Notes for Winston |
|------------|-------------------|
| `place_order` | Equity + option asset types commonly available; complex multi-leg option strategies supported in schema |
| `replace_order` / `cancel_order` | Needed for resting stops / amend |
| Order types | Market, limit, stop, stop-limit, trailing, conditional; community docs emphasize reverse-engineered order specs |
| Rate limits | Order of magnitude: ~60–120 req/min class for trading/account; order POST/PUT/DELETE often capped (~120/min configurable on app). EOD desk volume is not the bottleneck — **correctness and dual-spine honesty are** |
| Futures via API | Often **not** available for order entry even if platform supports futures |

### What the API does *not* solve by itself

- Mapping a Schwab fill to a **Winston Journal / Desk Handoff / fingerprint** — that is **our matcher**.  
- **Signaled Entry Rule** — broker will happily accept a naked equity buy; Winston policy must still require signal provenance before booking on OP.  
- **Fulfillment Packaging** (stock signal → LEAP booked) — API returns the instrument traded; Signal Spine must remain separate.  
- **7-day refresh** — operational gate for unattended automation.

---

## Channel comparison (email vs API vs hybrid)

| Dimension | Email confirmation | Schwab Trader API (read) | Hybrid |
|-----------|--------------------|--------------------------|--------|
| Structure | HTML/text; format churn | JSON schemas (evolve but typed) | Prefer API; email fallback |
| Latency | Minutes–hours after fill | Seconds–minutes (poll interval) | API for desk hours; email catch-up |
| Partial fills | Often one “final” notice | Order status + legs more honest | API |
| Order / confirmation id | Sometimes present | Strong | API |
| Stop-outs / unsignaled | May arrive as trade email | Transactions + position delta | API + Unsignaled Exit path |
| Auth | Mailbox password / OAuth (Gmail) | Schwab OAuth + weekly re-auth | Two secret systems |
| Setup time | Faster if mailbox already exists | App approval + OAuth plumbing | Phase API first if approval in flight |
| Parser maintenance | High (HTML drift) | Medium (schema + matcher) | Email only as degraded |
| Fits ADR-009 evidence path | Yes | Yes (better) | Yes |
| Unblocks L3 place-order later | Weak (no order lifecycle) | Strong (same credentials) | API path |

### Email path (if pursued)

Sketch only (not build):

1. Dedicated mailbox or label (e.g. `schwab-confirms@…`) — not personal inbox.  
2. IMAP or Gmail API poll (Sidekiq).  
3. Allowlist From/subject patterns (Schwab trade confirmation subjects vary; treat as unstable).  
4. Extract: symbol, side, qty, price, time, account tail, confirmation/order refs when present.  
5. Store **raw MIME** + normalized **BrokerFillEvent**.  
6. Same matcher as API path.

**When email wins:** API app stuck in approval; temporary token failure; human forwards a single confirm into desk.  
**When email loses:** LEAP multi-leg packaging, partials, systematic stop-out reconciliation, any path toward L3.

### API path (recommended primary)

Sketch only (not build):

```
Sidekiq: Broker::Schwab::PollFillsJob (e.g. every 1–5 min market hours + EOD)
  → refresh access token if needed
  → get_transactions(TRADE, since cursor) and/or get_orders(status=FILLED, window)
  → normalize → BrokerFillEvent (idempotent on broker+order_id/transaction_id)
  → Matcher → draft Journal / open Position / orphan queue
  → Desk attention: prefill | mismatch | orphan
  → Human still confirms / amends (v1)
```

**Cursor discipline:** 60-day lookback means durable cursor + raw payload store; do not rely on infinite history.

---

## Normalized confirmation / fill event (draft for ticket acceptance)

Name in product language may stay **BrokerFillEvent** until grill locks glossary.

**Extra-modal is the default expectation**, not an exception: broker `symbol` is the **fill instrument** (equity, OCC option, future root, CLETF, …). Winston **signal Market** may differ. Matching and schema must not assume equality.

```
broker:              "schwab"
account_ref:         "hash:…" | last-4 mapping key (not full account in Telegram)
source_channel:      "api_orders" | "api_transactions" | "email" | "manual_attach"
external_order_id:   string?
external_txn_id:     string?

# Booked / broker side (Booked Capital Spine evidence)
fill_symbol:         "WMT" | OCC option root | future | ETF …
instrument_type:     equity | option | future | etf | …
packaging_kind:      stock | leap | option_structure | future | cletf | proxy | …
underlying_hint:     string?        # if broker/OCC encodes underlying
side:                buy | sell | buy_to_cover | sell_short | …
quantity:            decimal        # shares or contracts as broker reports
price:               decimal        # avg fill if partials aggregated
multiplier:          decimal?       # e.g. 100 for equity options
filled_at:           iso8601
fees:                decimal?

# Signal side (when known — often only after human/desk link)
signal_market:       string?        # Winston Book Market, e.g. WMT — may ≠ fill_symbol
signal_journal_id:   int?
signal_task_id:      int?

raw_ref:             storage key for raw JSON/MIME
received_at:         iso8601
parse_version:       "schwab-txn-v1"
```

**Matching keys (sketch) — order of preference:**

1. **Explicit link:** human/desk already set `signal_journal_id` / task, or `external_order_id` on Journal (L3 place).  
2. **Underlying-aware soft match:** map fill → candidate underlyings (OCC parse, future root map, CLETF→theme table) then open drafts on those **signal Markets** in window — **not** `fill_symbol == Book.symbol` alone.  
3. **Weak soft match:** `(account_ref, side, time window, OP Active real)` when only one open draft exists.  
4. Ambiguous → human pick (especially multi-OP same underlying or multi-packaging).  
5. No match → orphan queue (possible **Unsignaled Exit**, non-Winston trade, or extra-modal fill waiting for packaging link).  
6. Match + price/qty/packaging diverge from human entry → **mismatch attention** (post-confirm amend).

**Never** create Signal Spine rows from this event. **Never** retarget OP Books to `fill_symbol` because a LEAP/future/CLETF filled.

**Examples (extra-modal):**

| Signal Market (Book / DA) | Booked fill | Link |
|---------------------------|-------------|------|
| WMT equity | 2× WMT Jan 2028 150 C LEAPs | Same signal; packaging=leap; cash = premium path |
| Commodity theme / proxy Book | GC future or CLETF shares | Same signal identity; DA stays on Book Market |
| ABC equity | ABC short-dated put vertical | Structure packaging; multi-leg may be N BrokerFillEvents → one fulfillment lineage |

---

## Full automation ladder (examine; do not climb yet)

ADR-009 already says future automation is a **separate component**, not DA silently filling. The ladder makes that operational.

```
L0  Human-only desk (today)
      DA → draft Journal + task → human trades at Schwab → human types fill in Desk Workflow

L1  Evidence ingest (parent ticket target)
      + email and/or API read → BrokerFillEvent → prefill / verify / orphan
      Human still confirms. No place_order.

L2  Rich reconciliation (same credentials, more jobs)
      + position poll vs open Positions
      + cash vs CashEvents
      + stop-out detection heuristics (position gone, no Winston exit) → Unsignaled Exit queue
      Still no auto place. Still Human-Gated book.

L3  Assisted execution (new ADR; separate adapter)
      Human (or policy) approves Desk Action “send to broker”
      Adapter place_order from confirmed intent / packaging
      Poll fill → book Booked Capital Spine (human confirm may collapse to “accept fill”)
      Resting Working Stop as broker stop order (optional; dual-write risk)

L4  Autotrader component (new product ADR)
      Policy engine consumes Desk Handoffs / Active real OPs
      Places / cancels / replaces without per-trade human click
      Hard risk limits, kill switch, audit, capital bands
      MUST remain outside Daily Analysis process boundary
```

### Ladder vs Winston domain objects

| Ladder | Touches Signal Spine? | Touches Booked Capital? | DA mutates Positions? | New ADR? |
|--------|----------------------|-------------------------|----------------------|----------|
| L0 | via DA drafts only | human confirm | No | No |
| L1–L2 | No (evidence only) | prefill / amend assist | No | No (policy already allows evidence) |
| L3 | No | Yes after fill | No (adapter + desk policy) | **Yes** — write path + kill switch |
| L4 | Consumes handoffs; does not invent methodology | Yes | No (component does; DA still must not) | **Yes** — product identity of autotrader |

### L3 design notes (examine)

**Recommended shape if we ever build it:**

1. **Separate process / gem / host worker** — e.g. `broker_adapter` or host Sidekiq under strict allowlist — not `DailyAnalysisService`.  
2. **Explicit intent record:** `BrokerOrderIntent` linked to Journal/task (signal provenance required for enters).  
3. **Idempotency:** client order id / Winston journal id in order annotation if Schwab supports; else durable mapping table.  
4. **Failure modes:** rejected, partial, canceled, replaced — all first-class; never assume FILLED.  
5. **Packaging / extra-modal:** place the **fulfillment instrument** (LEAP legs, future, CLETF, …), not the Signal Spine share count of the Book symbol. Signal link required on enter.  
6. **Stops:** Working Stop → broker stop is **optional sync**, not SoT (CONTEXT already: broker stop ≠ Working Stop SoT).  
7. **Kill switch:** global + per-OP; default off for real.  
8. **Paper:** L3 against Schwab paper/simulate if available, or keep paper Winston-only (prefer: paper never hits broker).

### L4 design notes (examine)

- Cromwell is **coordinator**, not the risk-bearing order router.  
- Autotrader should read **Desk Handoffs / Active real** the way a human reads DAR — not re-run methodology inside the broker worker.  
- Capacity packages (exit then enter) become **ordered order batches** with dependency; out-of-order is a system bug, not a warn-only UX.  
- Regulatory / ToS: individual Trader API is for **your** account automation; commercial multi-user is a different portal role.  
- Weekly OAuth re-auth is hostile to true unattended L4 — plan human “token hygiene” or accept automation windows.

### Explicit non-goals (restate for automation expansion)

- Building L3/L4 in this discovery session.  
- Putting `place_order` inside **Daily Analysis**.  
- Silent Position open from email or transaction poll without policy.  
- Multi-broker abstraction completeness on day one (Schwab exemplar; interface should stay broker-shaped-neutral).  
- Replacing dual spines with “whatever Schwab says the portfolio is.”

---

## Fit to current Winston frailty (why L1 matters before L3)

From fulfillment ownership analysis (WMT double short):

- Product bug is **second book instead of amend**.  
- Broker truth at 109.53 would **not** fix double-book by itself if desk still has two enter paths.  
- **Sequence:** (1) single-fulfillment invariant + post-confirm amend, (2) L1 BrokerFillEvent match → prefill/mismatch, (3) only then L3 send-to-broker.

Automation without amend/match multiplies bad lots faster than humans do.

---

## Security, privacy, ops

| Concern | Guidance |
|---------|----------|
| Secrets | Host secret store / env outside git; rotate app secret + tokens |
| Account numbers | Prefer hashValue; redact in Telegram/DAR |
| Raw payloads | Retain with retention policy (audit); encrypt at rest if mailbox/API dumps full statements |
| Telegram | Never dump full confirms; short “matched WMT fill — review desk” |
| Blast radius L3+ | Separate credentials optional; hard max notional; dry-run mode |
| Compliance | Individual developer ToS; no sharing tokens; logging of who authorized OAuth |

---

## Parent ticket acceptance — proposed answers

| Acceptance item | Proposed answer |
|-----------------|-----------------|
| Email vs API vs both for v1 | **API primary (poll orders + transactions)**; email optional fallback |
| Normalized event shape | Draft above (`BrokerFillEvent`) |
| Matching algorithm sketch | Explicit order id → soft window match → ambiguous queue → orphan; never silent wrong book |
| Human confirm still required? | **Yes for v1 real** (and paper unless separate decision). Auto-book only via later ADR |
| Security note | OAuth + weekly refresh; dedicated secrets; raw retention; no full account in chat |
| Follow-on tickets | (1) implement L1 matcher after grill; (2) post-confirm amend / single-fulfillment; (3) L3 adapter spike only after ADR |

---

## Grill-with-docs — questions this doc tees

Use with the fulfillment ownership analysis. Suggested order:

1. **Fulfillment identity / post-confirm amend** (already in ownership analysis — open there).  
2. **v1 channel lock:** API-primary vs email-first if API approval lag.  
3. **Trade-then-book vs book-then-trade default** for real desk (both modes may exist; product default?).  
4. **Where does the Schwab adapter live?** Host worker vs Wv2 monolith vs future `broker_adapter` majestic monolith.  
5. **When (if ever) may BrokerFillEvent auto-confirm paper? Real?**  
6. **L3 boundary:** is “Send to Schwab” a Desk Action on an already-draft Journal, or a new entity?  
7. **L4 appetite:** multi-year horizon vs “never for real capital under this product identity.”

**Recommended defaults to challenge in grill:**

| # | Recommendation |
|---|----------------|
| Channel | API primary |
| Confirm | Human always v1 |
| Adapter home | Host-side worker owned by ops, called from Wv2 — not DA, not Cromwell “just place it” |
| Trade order | Prefer **intent in Winston first** (draft exists) then fulfill at broker — reduces orphans; support reverse for stop-outs |
| L3/L4 | Explicit future; require ADR; kill switch; outside DA |

---

## Spike checklist (when discovery → build is authorized)

Not authorized now; list for completeness:

- [ ] Register Schwab developer app (Accounts and Trading + optional Market Data)  
- [ ] Complete OAuth; store tokens; prove refresh + 7-day re-auth runbook  
- [ ] Capture one real filled order JSON + one TRADE transaction JSON (redacted) as fixtures  
- [ ] Capture one Schwab confirmation email MIME as fixture (if email path kept)  
- [ ] Prototype normalize + match against a single OP journal in staging  
- [ ] Document rate limits observed and poll interval  

---

## Decision log (pre-grill)

| # | Statement | Status |
|---|-----------|--------|
| S1 | API preferred over email for v1 intake | **Recommended** (this research) |
| S2 | Email remains optional degraded path | **Recommended** |
| S3 | Human-Gated confirm remains for v1 | **Aligned ADR-009** |
| S4 | Full automation examined as L3/L4 ladder, not in DA | **Recommended architecture** |
| S5 | Implement nothing until grill + ticket acceptance | **Explicit** |

---

## Related

- Parent ticket: `docs/tickets/2026-07-21-broker-confirmation-email-api-intake.md`  
- Grill tee: `docs/analysis/2026-07-22-winston-fulfillment-ownership-and-broker-intake.md`  
- ADR-009, `human-gated-desk-and-fulfillment.md`, ADR-006  
- Sibling: `docs/tickets/2026-07-22-single-fulfillment-invariant-and-post-confirm-amend.md`  
- Community refs (non-normative): `schwab-py` client docs; Schwab developer portal Trader API — Individual; unofficial Medium/API guides for OAuth lifetimes and order payload shape  
