# Ticket: Add a single market to a single Operational Portfolio (Wv2)

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-07-23  
**Domain:** Operational Portfolio, Books, Daily Analysis, DM Symbol Demand, ADR-006  
**Monoliths:** winston_v2, data_manager, winston_mcp, Cromwell  
**See:** ADR-006 engagement lock / successor rebalance;  
[`wv2-operational-portfolio-lifecycle.md`](../business-context/wv2-operational-portfolio-lifecycle.md);  
MCP `wv2_add_market` / `wv2_successor_portfolio` in [`winston-mcp-tools.md`](../../interfaces/winston-mcp-tools.md);  
Yellow transfer: [`2026-07-23-yellow-elephant-pbr-and-wv2-transfer.md`](2026-07-23-yellow-elephant-pbr-and-wv2-transfer.md);  
Telegram desk fastpath: [`2026-07-23-cromwell-telegram-ops-fastpath-empty-response.md`](2026-07-23-cromwell-telegram-ops-fastpath-empty-response.md)

## Operator use case

A **new market comes online** (example: **SPCX**) and is showing **active volatility**. Operator wants that symbol evaluated **on an existing OP recipe** (example: **Portfolio Yellow** / same TradingStrategy) without rebuilding membership in WUT first.

Speech examples:

- “Add SPCX to Yellow”  
- “Add SPCX to portfolio 312”  
- “Put SPCX on Mint and make sure data is there”

Outcome: symbol is on **Books**, **DM parquet** exists (or is requested and readiness is visible), and next **Daily Analysis** can emit signals / desk tasks for that market under the OP’s strategy.

## Problem (today)

| Layer | Reality | Gap |
|-------|---------|-----|
| MCP / internal | `POST /internal/portfolios/add_market` + `wv2_add_market` exist | Thin: `Book.find_or_create` + fire-and-forget DM request; weak errors; no `reply_text` contract |
| ADR-006 | Engaged OPs: **Books immutable** until close/successor | `add_market` does **not** refuse engaged reshape — can silently violate lifecycle |
| Engaged path | `wv2_successor_portfolio` requires full **symbols[]** list | No first-class “append one symbol” API/speech; operator must restate entire book |
| New symbols | DM must know symbol + produce Winston EOD Standard | No operator-visible “requested → covered → ready for DA” loop on add |
| Product | Yellow may not yet be an OP in Wv2 (lab-only until transfer) | Feature must work once Yellow OP exists; not blocked on WUT re-vet for a one-off book add |
| Caps | `max_markets_per_portfolio` / paper caps | Add may need explicit refuse or successor with raised cap + warn |
| Telegram | Skill lists add market | Same empty-LLM / tool-selection hang risk as activate; phrase should be on desk fastpath later |

**Net:** operator cannot reliably run the “new name showing vol → park it on Yellow and watch DA” loop from desk speech or a single honest tool chain.

## Desired outcome

### A. Policy (keep ADR-006)

| OP state | Add-one-market behavior |
|----------|-------------------------|
| **Not engaged** (no journals), not closed | **In-place** Book create OK (same series, same TS) |
| **Engaged** | **Refuse** in-place; require **successor** A′ with books = old ∪ {symbol} (journals stay on A) |
| **Closed** | Refuse; open new series or pick open OP |

Document speech: *“add market on engaged series → opens successor with expanded books”* (not silent mutation).

Optional convenience flag on successor MCP: `add_symbols: ["SPCX"]` (merge with current books) so humans don’t paste 17 tickers.

### B. Service-level API (Wv2)

Replace/extend controller one-liner with something like `Operations::PortfolioAddMarketService`:

1. Resolve OP by `id_or_name` / seed / short fp (same resolver as activate).  
2. Normalize symbol (upcase; optional alias table later).  
3. Branch engaged vs not (above).  
4. Ensure `Market` row; create `Book` (or successor books).  
5. Request DM acquisition for the symbol (`DmParquetIngester.request_dm_data` or consumer demand path).  
6. Return structured JSON always:

```json
{
  "status": "ok",
  "action": "book_added | successor_opened | already_on_books",
  "symbol": "SPCX",
  "portfolio": { "id": 312, "name": "...", "active": true, "engaged": false },
  "markets": ["..."],
  "data": { "requested": true, "coverage": null },
  "summary": "...",
  "reply_text": "Added SPCX to #312 Yellow · … (17→18 markets). DM sync requested."
}
```

Errors (JSON, never HTML): `not_found`, `closed_refuse`, `engaged_require_successor`, `active_mutex` (if successor+activate), `max_markets`, `invalid_symbol`, `dm_request_failed` (warn vs hard-fail — prefer soft warn if Book landed).

### C. DM / data readiness for brand-new names

For symbols not yet in consumer demand or EODHD history:

1. Add path must **surface** whether parquet exists (`DataCoverage` / DM health).  
2. If missing: request sync and return `data.status=pending` + how to poll (`wv2_sync_data` / DM).  
3. DA should skip or `missing_data` cleanly until coverage exists — no silent empty signal.  
4. Out of scope for v1: full EODHD catalog UX; operator may need DM registry steps for exotic tickers — document when add alone is insufficient.

### D. MCP + Telegram + ops shell

- Harden `wv2_add_market` to the service above.  
- Skill `winston-portfolio-lifecycle`: engaged → call successor (or service that does) with clear reply.  
- Ops shell phrase: `add_market Yellow SPCX` (or equivalent).  
- Prefer listing on desk **fastpath** grammar when numeric id + symbol present (sibling ticket).

### E. Attention / mutex hygiene

- Adding a market **changes** the Books set → Active **identical_books** mutex key changes (good).  
- Same `seed_name` still one Active unless force.  
- Successor default: keep `execution_mode` + capital policy consistent with existing successor service; activate only if asked.

## Acceptance

- [ ] **Pre-engaged** OP: `wv2_add_market` adds one symbol; markets list includes it; `reply_text` has `#id` + symbol  
- [ ] **Engaged** OP: in-place add returns structured refuse **or** auto-successor with expanded books (product choice documented); journals remain on A  
- [ ] Idempotent: second add of same symbol → `already_on_books`, not error spam  
- [ ] New symbol triggers DM request; response indicates requested vs already covered  
- [ ] `max_markets` exceeded → clear 422 (not silent create)  
- [ ] Specs: pre-engaged add, engaged refuse/successor, closed refuse, DM request stub  
- [ ] Smoke: “add SPCX to \<Yellow OP id\>” via MCP or curl; list markets; optional one evaluate after data ready  
- [ ] Docs: lifecycle business-context one paragraph + MCP tools interface update  

## Non-goals

- WUT lab membership redesign / re-vet required for every desk add (lab can lag; ops observation is intentional)  
- Changing TradingStrategy / fingerprint in the same call (that remains successor with new TS)  
- Auto-activate successor  
- Broker listing / options chain for SPCX  
- Correlation re-gate hard block (optional warn later)  
- Removing markets (separate if needed)

## Suggested implementation slices

1. **P0 hygiene:** engaged lock on current `add_market` (refuse or successor-only) — stops ADR-006 violation.  
2. **Service + MCP reply_text** for pre-engaged path.  
3. **`add_symbols` convenience** on successor / unified service.  
4. **DM readiness** fields + skill text.  
5. Telegram fastpath phrase + smoke with real Yellow OP once transferred.

## Evidence / context

- Controller today: `winston_v2` `InternalController#add_market` (~L373) — no engaged check.  
- ADR-006: Engaged Books immutable; shape → successor.  
- Yellow OP not present in Wv2 as of 2026-07-23 afternoon (Mint #311 is); Yellow transfer ticket still open — this feature is for any OP seed once Yellow lands.  
- Operator intent captured in session 2026-07-23: volatility name (SPCX) on Yellow-class recipe without full WUT rebuild.
