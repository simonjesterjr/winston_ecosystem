# Schwab / thinkorswim Access Landscape — Capabilities, Automation Paths, and Issues

**Date:** 2026-07-22  
**Status:** Pre-design technical landscape (not domain law; not an implementation plan)  
**Audience:** Operators / architects who want issues and options clear **before** a design or `/grill-with-docs` session  
**Scope:** How a system (including Winston) can systematically talk to Charles Schwab and thinkorswim — API, streaming, email, platform features, automation ceiling  

### Related Winston artifacts

| Artifact | Role |
|----------|------|
| [`2026-07-22-schwab-integration-discovery.md`](./2026-07-22-schwab-integration-discovery.md) | Winston-scoped recommendation (intake channel, L0–L4 ladder, ADR-009 fit) |
| [`2026-07-22-winston-fulfillment-ownership-and-broker-intake.md`](./2026-07-22-winston-fulfillment-ownership-and-broker-intake.md) | Grill tee: fulfillment ownership + broker evidence |
| [`docs/tickets/2026-07-21-broker-confirmation-email-api-intake.md`](../tickets/2026-07-21-broker-confirmation-email-api-intake.md) | Discovery ticket for confirmation intake |
| ADR-009 / human-gated desk BC | Product law: Winston ≠ OMS; real is Human-Gated |

**This document** is the broader **“what does Schwab actually give you?”** map. The sibling discovery doc is **“what should Winston do first?”**

---

## 1. Executive picture

There is **no single “thinkorswim API”** that automates the desktop platform end-to-end. After the TD Ameritrade → Schwab migration, the practical stack is:

| Layer | What it is | Can place live orders? | Good for systematic Winston-style work? |
|-------|------------|------------------------|----------------------------------------|
| **Schwab Trader API (Individual)** | Official REST + OAuth for **your** brokerage account(s) | **Yes** (equity/option class) | **Yes — primary path** |
| **Schwab Streamer (WebSocket)** | Market data + **account activity** stream | N/A (events only) | **Yes for near-real-time fills / order state** |
| **thinkorswim desktop / mobile** | Human trading UI; charts; paperMoney | Manual + conditional orders | Human desk; not a clean external API |
| **thinkScript** | Chart studies, strategies, alerts, **conditional order** conditions | **Not** full algo loop; limited auto-trigger | Weak for Winston; useful only for human stop/condition aids |
| **Email / statements** | Trade confirmations, alerts | No | Fragile evidence path |
| **HTTP webhooks into your app** | Schwab does **not** publish a retail “POST fill to your URL” product | No | Not available as first-class retail feature |

**Bottom line for systematic access:** use the **Schwab Developer Trader API** (read + optional write) and optionally the **account-activity streamer**. Treat thinkorswim as the **human** execution surface. Treat email as degraded evidence. Do not plan on thinkScript as your OMS.

**Critical Winston product constraint (extra-modal fulfillment):** broker fills will often **not** be the same instrument as the Winston signal **Market**. A stock signal may be filled with LEAPs or option-chain structure; a commodity / futures-theme signal may be filled with futures, options, or commodity/levered ETFs (CLETF-class). Any Schwab integration must **link signal ↔ fulfillment**, keep DA on the signal Market, and put cash/returns on the booked instruments — never collapse the two spines by equating broker symbol with methodology Market. See §2a.

---

## 2a. Extra-modal fulfillment (first-class design constraint)

Glossary: **Extra-Modal Fulfillment**, **Fulfillment Packaging**, **Signal Spine**, **Booked Capital Spine** (`CONTEXT.md`).

### What “extra-modal” means

Winston’s methodology evaluates **Markets on Books** (signal instruments — e.g. equity ABC, or a commodity theme the OP is built around). **Fulfillment** is how capital is actually deployed. Those need not share modality:

| Signal modality (methodology / Book) | Example fulfillments (booked capital) |
|--------------------------------------|----------------------------------------|
| Equity / ETF stock | Shares; LEAPs; shorter-dated options; verticals / structures on the chain |
| Commodity / futures theme | Futures contracts; options on futures; commodity or levered ETFs (CLETF-class); option overlays |
| Index / broad theme | Futures, ETF proxy, options on index or ETF |

Fulfillment may also be **asynchronous**: signal on date T, fill T+1 (or later), roll later into a different packaging, partial size, multi-leg over time. The **signal identity** stays; the **booked packages** accumulate or replace under desk rules.

### Dual tracking (non-negotiable)

```
┌─────────────────────────────────────────────────────────────┐
│  SIGNAL SPINE (methodology continuity)                        │
│  • OP Book Market (e.g. ABC, or commodity theme symbol)     │
│  • DA continues: entries, exits, pyramids, capacity, stops    │
│    story in signal units / underlying                        │
│  • Risk *methodology* narrative (ATR, % risk ladder story)    │
│  • Process: Passed Signal vs filled vs process miss           │
└────────────────────────────┬────────────────────────────────┘
                             │  mandatory link
                             │  (signal_journal_id / task / fulfillment id)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  BOOKED CAPITAL SPINE (economic / cash truth)                 │
│  • Actual instrument(s): OCC option, future root, CLETF, …   │
│  • Cash, fees, premium × multiplier, P&L, equity curve        │
│  • Live capital risk base for DAR / sizing of *new* capital   │
│  • Broker evidence (Schwab order/txn) attaches here           │
└─────────────────────────────────────────────────────────────┘
```

| Concern | Tracks on | Does **not** |
|---------|-----------|--------------|
| Continued signal generation | Signal Market on Book | Switch DA to the LEAP/future/ETF symbol as if it were a new Book |
| Capacity / max markets / pyramid | Signal-side lot / Book occupancy | Count every option leg as a new methodology market unless product says so |
| Cash, returns, fees | Booked packaging | Fake stock-share P&L when LEAPs were used |
| Broker API match | Fulfillment / evidence | Assume `broker.symbol == market.symbol` |
| Working stop (methodology) | Signal / Position working stop story | Assume broker stop instrument equals signal units |

### Implications for Schwab (and any broker) integration

1. **Matcher cannot key only on symbol equality.**  
   - Signal: `GLD` or a commodity Book → fill: `/GC` future, `GC` option, or `UGL`/`GLD` option.  
   - Signal: `WMT` stock → fill: `WMT  … C` LEAP OCC symbol.  
   Soft-match must use **explicit signal/journal link**, human desk choice, or a curated **underlying → candidate instrument** map — not `symbol == Book.symbol` alone.

2. **Normalized BrokerFillEvent must carry instrument modality**, not a single stock-shaped field:

   ```
   signal_market:     "WMT" | "…"     # Winston Book / signal underlying (when known)
   fill_instrument:   OCC | future root | ETF | equity
   instrument_type:   equity | option | future | etf | …
   packaging_kind:    stock | leap | option_structure | future | cletf | proxy | …
   ```

3. **Position reconciliation is many-to-one.** One Winston signal lot may map to:
   - one equity lot, or  
   - N option contracts, or  
   - a futures position + hedge, or  
   - sequential rolls (close LEAP, open later expiry) still linked to the same engagement story.

4. **L3 place_order** must place the **packaging instrument**, not blindly the signal share count of the Book symbol.

5. **API asset-class gaps bite extra-modal hard:** if commodity signals are fulfilled with **futures** but retail API cannot place futures, L3 automation is blocked for that path even when L1 read of transactions might still see fills from ToS UI.

6. **Email parsers** that only extract equity tickers will systematically fail LEAP/future/CLETF packaging — another reason API + human packaging fields win.

### What stays linked

```
Desk Handoff / draft Journal (signal: long ABC, size story 206 @ next open)
        │
        ├─ human (or L3) fulfills: 2× Jan 2028 150 LEAP calls @ 12.50
        │
        ▼
executed Journal + Position (booked)
   signal_ref → draft/task/ABC
   packaging  → leap, strike, expiry, contracts, premium
   broker_ref → Schwab order/txn ids (optional evidence)
        │
        ▼
DA next day: still evaluates ABC on the Book for exit/pyramid/risk story
Equity/DAR: uses LEAP MTM / premium path on Booked Capital Spine
```

### Issue register addenda (extra-modal)

| ID | Issue | Why it matters |
|----|-------|----------------|
| A6 | **Extra-modal symbol mismatch** | Naive fill↔journal match on ticker is wrong by design |
| A7 | **DA continuity vs booked instrument** | Must not re-point Books to fill symbols or DA “follows the LEAP” |
| A8 | **Risk double-count** | Methodology risk % story vs option notional/Greek risk — product must say which drives capital_base sizing |
| A9 | **Multi-fill one signal** | Rolls, adds, partial packages need lineage under one signal identity |
| B11 | **Futures API gap vs commodity packaging** | ToS UI futures fulfill possible; API place may not |
| D4 | **Email equity-only parsers** | Silent miss on OCC / future symbols |

---

## 2. Product map (names that get confused)

```
┌─────────────────────────────────────────────────────────────┐
│  Charles Schwab brokerage account(s)                        │
│    ├── thinkorswim (UI / paperMoney / conditional orders)   │
│    └── Schwab.com web trading                               │
└───────────────────────────┬─────────────────────────────────┘
                            │ OAuth 2.0 (your app authorized)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  developer.schwab.com  — Trader API (Individual)            │
│    ├── Accounts & Trading Production  (balances, positions, │
│    │     orders place/replace/cancel, transactions)         │
│    ├── Market Data Production         (quotes, history,     │
│    │     option chains, movers, hours)                      │
│    └── Streamer (WebSocket)           (L1 quotes, books,    │
│          charts, ACCT_ACTIVITY)                             │
└─────────────────────────────────────────────────────────────┘
```

### Individual developer constraints (typical)

- Schwab brokerage account required for Trader APIs.  
- Individual role: often **one registered app**.  
- App must be approved (“Ready for Use”) for production.  
- You authorize which **linked accounts** the app may access.  
- Account identifiers in API calls are **hashed** (`hashValue`), not raw account numbers — privacy design, not optional.

Commercial / multi-client products are a different portal path; this landscape assumes **self-directed / own capital** automation.

---

## 3. REST API capabilities (what you can actually do)

Capabilities below are synthesized from Schwab product positioning, community client libraries (e.g. `schwab-py`), and public guides. **Field-level schemas should be verified on a live spike** — Schwab’s official docs are portal-gated and change.

### 3.1 Accounts and portfolio state

| Capability | Typical use | Notes / issues |
|------------|-------------|----------------|
| List account numbers + hashes | Map human account → API key | Multi-account households need explicit mapping |
| Get account (balances) | Cash available, buying power | Not a substitute for Winston CashEvents |
| Get positions | Open lots / qty / average | Lot identity ≠ Winston Journal identity |
| User preferences | Linked accounts metadata | Secondary |

**Issue — position vs Winston lot:** Broker positions are **clearing truth**. Winston **Positions** are **Booked Capital Spine** lots tied to methodology journals. They will diverge (packaging LEAPs, partials, process miss, external stop). Reconciliation is a product problem, not a free API feature.

### 3.2 Orders (read + write)

| Capability | Direction | Notes / issues |
|------------|-----------|----------------|
| Place order | Write | Equity + option common; complex multi-leg option strategies in schema |
| Replace order | Write | Amend working order |
| Cancel order | Write | |
| Get order by id | Read | After place, extract id from response headers/helpers (JSON body often empty on place success) |
| List orders (account or all linked) | Read | Filter by status (e.g. FILLED), time window |
| Order statuses | Read | Rich state machine: QUEUED, WORKING, FILLED, CANCELED, REJECTED, partial lifecycle, etc. |

**Asset class issues:**

- **Equities / ETFs:** well supported for automation.  
- **Options / multi-leg:** supported in order schema; complexity and partial leg fills are real.  
- **Futures:** often tradable on thinkorswim UI but **order entry via retail Trader API is commonly limited or unavailable** — verify for your account entitlements; do not assume futures automation.  
- **Mutual funds / bonds / specialty:** not the happy path for algo order APIs.

**Order type coverage (community-observed):** market, limit, stop, stop-limit, trailing, duration/session variants, conditional / complex strategy types. Exact support is entitlement- and schema-dependent.

**Issue — no durable client order id contract assumed:** You must store Schwab `orderId` ↔ Winston journal/task yourself. Place-order responses are easy to mishandle (no JSON body).

### 3.3 Transactions (economic truth after the fact)

| Capability | Use | Issues |
|------------|-----|--------|
| List transactions by type/date/symbol | Best **post-trade** economic record (TRADE, dividends, wires, etc.) | **Lookback windows often ~60 days** — need durable local store |
| Get transaction by id | Audit detail | Schema richness varies |

**Issue — orders vs transactions:**  
- **Orders** = intent + lifecycle (including unfilled).  
- **Transactions** = settled/cleared economic events.  
For “what fill price do I book?”, transactions (or fill legs on filled orders) matter. Partial fills can appear as multiple execution messages before a final average.

### 3.4 Market data (optional for Winston)

Winston’s **EOD SoT is DM / EODHD parquet**, not Schwab. Schwab market data is relevant only if you want:

- Intraday quotes for desk UX  
- Option chains for LEAP packaging helpers  
- Streaming L1 for monitors  

**Do not** replace Winston EOD Standard with Schwab daily bars without a deliberate data ADR.

Community-reported rate-limit ballpark (varies by app config / source):

| Class | Order of magnitude |
|-------|--------------------|
| Market data | ~120 requests / minute |
| Account / trading GETs | ~60 / minute class |
| Order mutating (POST/PUT/DELETE) | Often capped (e.g. up to ~120/min configurable on app) |

For **EOD desk volume** (handful of fills/day), limits are not the bottleneck. For **HFT-style polling**, they are.

---

## 4. Streaming / “webhook-like” paths

### 4.1 What people mean by webhook

| Pattern | Available for retail Schwab? | Notes |
|---------|------------------------------|-------|
| **Schwab POSTs to your HTTPS URL** when a fill happens | **No** (not a documented first-class retail product) | Do not design v1 around inbound webhooks from Schwab |
| **You open a WebSocket to Schwab** and receive pushes | **Yes** (Streamer) | This is **pull-subscribe**, not “webhook into Wv2” |
| **You poll REST** on a timer | **Yes** | Simplest ops model |
| **Email arrives → your IMAP poll** | **Yes** (DIY) | Pseudo-push with high latency |

### 4.2 Streamer services (high level)

Documented in unofficial streamer guides and client libs:

| Service class | Content |
|---------------|---------|
| Level-one equities/options/futures/forex | Quotes |
| Books / charts / screeners | Market microstructure / visuals data |
| **`ACCT_ACTIVITY`** | **Account activity including order lifecycle / fills** |

**Account activity is the important one for automation evidence.** Community demos filter messages for order accepted / fill completed, etc.

**Issues with streaming:**

1. **Connection ops:** reconnect, heartbeat, token refresh mid-stream.  
2. **Payload opacity:** message formats are less friendly than REST; need fixtures and versioning.  
3. **Not a substitute for durable store:** if your process is down, you miss events → must **reconcile via REST transactions/orders** on catch-up.  
4. **Security:** long-lived process with trading-capable tokens is a high-value target.  
5. **Still not a webhook into Rails:** you need a host worker that translates stream events into your app’s queue.

**Practical pattern:**

```
Streamer (optional, low latency) ──┐
                                   ├──► normalize → durable BrokerFillEvent store
REST poll (required safety net)  ──┘         │
                                             ▼
                                    matcher / desk attention
```

Design for **poll as source of truth recovery**; stream as acceleration.

---

## 5. Authentication and token lifecycle (major issue)

| Token | Typical lifetime (community) | Consequence |
|-------|------------------------------|-------------|
| Access token | ~**30 minutes** | Every worker must refresh or fail closed |
| Refresh token | ~**7 days** | **Human re-login weekly** (or on failure) — not set-and-forget unattended |
| Initial OAuth | Browser consent + redirect (often `https://127.0.0.1`) | Awkward on headless servers; often bootstrap on a laptop then copy tokens |

**Issues this creates:**

1. **Unattended L4 autotrader** fights a weekly human OAuth wall.  
2. **Container restarts** need careful token file / secret manager ownership (single writer).  
3. **Multiple clients on one token file** corrupt sessions (community libs warn: one client per token).  
4. **Approval delay:** new apps can sit “pending” days before Ready for Use.  
5. **Secrets:** app key, secret, refresh token are capital-adjacent credentials — host secret store, rotation runbook, never git.

---

## 6. Email as an integration channel

### 6.1 What email can do

Schwab (and most brokers) send **trade confirmations**, order alerts, and statements by email. In principle you can:

1. Dedicated mailbox / Gmail label  
2. IMAP or Gmail API poll  
3. Parse MIME/HTML → structured fields  
4. Attach as evidence to a desk journal  

### 6.2 Why email is a weak primary path

| Problem | Detail |
|---------|--------|
| **Format churn** | HTML templates change without notice; parsers break silently |
| **Incomplete structure** | Partial fills, multi-leg options, average price vs print — inconsistent |
| **Latency** | Minutes to hours; not useful for same-session amend |
| **PII / security** | Full account numbers, tax IDs in some notices; mailbox is a second high-value secret |
| **No order lifecycle** | Hard to see REJECTED / CANCELED / WORKING |
| **Ambiguous matching** | Weak IDs vs API order/transaction ids |

### 6.3 When email still helps

- API app not approved yet  
- Refresh token expired and human hasn’t re-authed  
- Human forwards one confirm into desk (“attach this”)  
- Offline audit “what did the broker say on paper”  

**Recommendation for systematic design:** email = **degraded / secondary** channel feeding the **same** normalized event as API. Never email-only if you care about LEAPs, partials, or future order placement.

---

## 7. thinkorswim platform (not an external automation bus)

### 7.1 What ToS is good for

- Human charting and order entry  
- **paperMoney** simulated account (UI)  
- Conditional orders (including thinkScript **conditions**)  
- Alerts  
- Strategy studies / chart backtests (thinkScript `AddOrder` is **chart simulation**, not live auto-execution)

### 7.2 What ToS is **not**

| Myth | Reality |
|------|---------|
| “thinkorswim API automates ToS” | Retail automation goes through **Schwab Trader API**, which hits the **brokerage account**, not a scriptable ToS process API |
| “thinkScript places live orders in a loop” | **No** full strategy autotrader. Studies/strategies do not continuously fire live tickets |
| “Conditional orders = algo platform” | Semi-auto: condition → order; limited; often one-shot; platform running constraints; not Winston methodology engine |
| “API paperMoney” | **Widely reported: developer API is live-account only**; paperMoney is a ToS UI mode, not a clean API sandbox for place_order |

### 7.3 paperMoney / sandbox issues (critical for design)

| Environment | Can Winston/your bot place orders? | Notes |
|-------------|-------------------------------------|-------|
| **thinkorswim paperMoney** | Via UI (and limited platform features) | **Not** the same as API paper endpoint in community reports / Schwab support answers |
| **Schwab API “sandbox”** | Limited; many report Production-only apps; sandbox not a full paper brokerage twin | Component testing ≠ realistic fills |
| **Winston paper OPs** | Yes (already) | **Best paper path for methodology** — keep paper in Winston; do not require Schwab paper for regime tracking |
| **Live API** | Yes | Real capital risk immediately |

**Design implication:** Do **not** couple “Winston paper trading” to “Schwab paperMoney.” They solve different jobs. Live API testing needs tiny size, hard kill switches, and preferably a dedicated sub-account if available.

### 7.4 Conditional orders vs Winston Working Stop

ToS/Schwab can hold resting stops and conditionals. Winston already treats **Working Stop** as desk SoT and **broker stop as outside**. Dual-writing stops via API is optional L3 complexity (sync drift, cancel races). Unsignaled stop-outs remain an **intake + book exit** problem either way.

---

## 8. Automation spectrum (platform-agnostic ladder)

| Level | Name | Mechanism | Human in loop? | Capital risk | Fits current Winston product? |
|-------|------|-----------|----------------|--------------|-------------------------------|
| **L0** | Manual desk | Human trades in ToS/Schwab.com; types fill in Winston | Always | Human | **Today** |
| **L1** | Evidence ingest | API poll and/or stream and/or email → normalized fill event → prefill desk | Confirm still | Low (read-only) | **Near-term discovery target** |
| **L2** | Reconcile | Positions/cash/order state vs Winston books; orphan/mismatch queues | Review exceptions | Low–med | Natural extension of L1 |
| **L3** | Assisted execution | “Send to broker” places order from Winston intent; poll/stream fill; book | Approve send / accept fill | **High** | Requires **new ADR**; separate component |
| **L4** | Autotrader | Policy places/cancels without per-trade click | Kill switch / oversight only | **Highest** | Explicit product; **outside Daily Analysis** |

**Hard rule for Winston (already ADR-009):** Daily Analysis never places orders and never opens Positions. Automation is a **separate fulfillment component**, if ever.

---

## 9. Issue register (read this before design)

### A. Product / domain issues

| ID | Issue | Why it matters |
|----|-------|----------------|
| A1 | **Broker truth ≠ Winston truth** | Dual spines (signal vs booked); **Extra-Modal Fulfillment**; process miss |
| A2 | **One signal → one fulfillment identity** | Without this, API autofill can double-book (see WMT frailty); rolls/packages are amendments/lineage, not silent second signals |
| A3 | **Signaled entry vs unsignaled exit** | API will accept naked buys; policy must refuse book without signal for enters |
| A4 | **Order vs fill vs journal** | Order lifecycle is not a Journal; need mapping table |
| A5 | **Multi-account / multi-OP** | One Schwab account may fund many Winston OPs — matching needs OP context, not only symbol |
| A6 | **Extra-modal symbol mismatch** | Fill ticker (OCC, future, CLETF) ≠ signal Market — matcher must use signal link |
| A7 | **DA stays on signal Market** | Do not retarget Books/DA to booked packaging symbols |
| A8 | **Risk story vs capital risk** | ATR/share risk narrative vs option/future notional — sizing base must be explicit |
| A9 | **Multi-fill / roll under one signal** | Asynchronous packaging changes need lineage, not new methodology signals |

### B. Platform / API issues

| ID | Issue | Why it matters |
|----|-------|----------------|
| B1 | **7-day refresh token** | Breaks naive unattended bots weekly |
| B2 | **30-minute access token** | Every job path needs refresh |
| B3 | **No retail fill webhook URL** | Must poll and/or maintain streamer |
| B4 | **~60-day history windows** | Local durable store mandatory |
| B5 | **API ≈ live only** | No clean Schwab paperMoney via API |
| B6 | **Futures / some assets** | May not be orderable via API |
| B7 | **Partial fills & multi-leg** | Matcher and avg price logic required |
| B8 | **Streamer downtime** | Must catch up via REST |
| B9 | **App approval / one app limit** | Lead time; env separation hard |
| B10 | **Unofficial docs drift** | Community libs reverse-engineer; pin fixtures |

### C. Security / ops issues

| ID | Issue | Why it matters |
|----|-------|----------------|
| C1 | Trading-capable tokens on host | Compromise = capital loss |
| C2 | Telegram / DAR leakage of account numbers | Redact |
| C3 | Email mailbox as second secret | Prefer dedicated label/account |
| C4 | Audit retention of raw fills | Compliance + debug vs PII |
| C5 | Kill switch for L3+ | Non-negotiable if write path exists |

### D. Email-specific issues

| ID | Issue | Why it matters |
|----|-------|----------------|
| D1 | HTML churn | Silent parse failures |
| D2 | Latency | Late amend after human already booked wrong price |
| D3 | Weak identifiers | Higher orphan/ambiguous rate |

---

## 10. Comparison matrix (choose with eyes open)

| Criterion | REST API read | Streamer ACCT_ACTIVITY | Email | ToS conditional / thinkScript | REST place_order |
|-----------|---------------|------------------------|-------|-------------------------------|------------------|
| Structured data | Excellent | Good (opaque) | Poor | N/A | Excellent |
| Latency | Poll interval | Near real-time | Slow | Event-driven in platform | Immediate submit |
| Setup cost | Medium (OAuth app) | Higher (long-lived process) | Low–medium | Low (human) | Medium + risk |
| Reliability if process down | Catch-up poll | **Misses without reconcile** | Eventually | Platform must run | N/A |
| Partials / options | Good | Good if parsed | Weak | Limited | Full complexity |
| Unattended ops | Weekly re-auth | Weekly re-auth + reconnect | Mailbox auth | ToS must be up | Weekly re-auth |
| Winston L1 fit | **Best primary** | Best accelerator | Fallback | Not for Winston SoT | L3 only |
| Winston paper | Not needed | Not needed | Not needed | Different paperMoney | Avoid for paper OPs |

---

## 11. Recommended mental model for Winston (pre-decision)

Not a locked ADR — a **default stance** to stress-test in design/grill:

1. **Systematic access = Schwab Trader API**, not thinkorswim scripting.  
2. **v1 job = read path** (transactions + orders ± streamer) → durable events → match desk work.  
3. **Email optional.**  
4. **Human confirm stays** until a deliberate L3 ADR.  
5. **Winston paper stays Winston paper** — do not wait on Schwab paperMoney API (it likely does not exist for place_order).  
6. **Write path later** as a separate adapter with kill switch; never inside Daily Analysis.  
7. **Fix fulfillment identity / post-confirm amend before** trusting automation to book capital.  
8. **Extra-modal is normal, not an edge case:** always design signal↔fulfillment links; DA on signal Market; cash/returns on packaging; never require broker symbol == Book symbol.

---

## 12. Spike list (when you want ground truth)

Run these before writing production code; capture redacted fixtures in a private ops store (not git if PII):

1. Register Individual app; wait for Ready for Use.  
2. OAuth once; document refresh failure mode on day 8.  
3. Dump: one filled equity order JSON, one option order JSON, one TRADE transaction JSON.  
4. Subscribe `ACCT_ACTIVITY` for one manual ToS fill; save raw messages.  
5. Confirm futures place_order accept/reject on your account.  
6. Confirm whether any paper/sandbox place_order is real for your app.  
7. Time email arrival vs API visibility for the same fill.  
8. Measure rate-limit headers / 429 behavior under aggressive poll (optional).

---

## 13. Glossary (Schwab-side terms)

| Term | Meaning here |
|------|----------------|
| **Trader API — Individual** | Retail developer APIs for own account trading + market data |
| **Account hash** | Opaque account id required by API calls |
| **Streamer** | Schwab WebSocket market + account activity feed |
| **ACCT_ACTIVITY** | Streamer service for order/fill/account messages |
| **paperMoney** | thinkorswim UI simulated account — not equivalent to API paper |
| **thinkScript** | ToS scripting language for studies/conditions — not full autotrader |
| **Conditional order** | Platform order that fires when a condition/study hits |
| **OCC / option symbol** | Broker option root — often the fill symbol when packaging is LEAP/options |
| **CLETF-class** | Commodity / levered ETF-style products used as proxies for commodity themes |

Winston domain terms (**Extra-Modal Fulfillment**, **Fulfillment Packaging**, Journal, dual spines, Human-Gated) stay in `ecosystem/CONTEXT.md`.

---

## 14. Sources and confidence

| Area | Confidence | Basis |
|------|------------|-------|
| REST capability map | Medium–high | Community clients + widespread production use |
| Token lifetimes | Medium | Consistent community reports; verify in spike |
| No retail fill webhook | High | Absence in public product docs + architecture of streamer |
| API ≠ paperMoney | High | Schwab support answers reported by traders; repeated community claims |
| thinkScript ≠ live algo loop | High | Platform docs + long-standing ToS community consensus |
| Exact rate limits / schemas | Low–medium until spike | Portal-gated; app-configurable |

Official portal: [https://developer.schwab.com/](https://developer.schwab.com/) (auth-walled). Unofficial but useful client docs: `schwab-py` (HTTP + streaming). Treat unofficial material as **hypothesis generators**, not contracts.

---

## 15. What to do next (process)

1. Read this landscape for **issues**.  
2. Read sibling [`2026-07-22-schwab-integration-discovery.md`](./2026-07-22-schwab-integration-discovery.md) for **Winston-shaped recommendations**.  
3. Run `/grill-with-docs` on fulfillment ownership + Schwab discovery when ready to lock decisions.  
4. Only then: spike fixtures → implementation tickets (L1), separate ADR for any L3 write path.

**No implementation is authorized by this document.**
