# Session Report — Signal Inspect market card, DM eval, holdings, insights

**Date:** 2026-09-10
**Time:** ~13:00–13:55 MDT
**Duration:** ~55m
**Project:** sawtooth Winston ecosystem — `winston_v2`, `data_manager`, `ecosystem/`
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on each touched repo (from `origin/main`)
**Model:** Grok 4.6
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** On Winston v2 (Wv2) Signal Inspect (GOOGL, portfolio 11, as_of 2026-09-09), add a market metadata card, a data_manager (DM) eval/coverage report, chart focus (candles + Average True Range (ATR) + Moving Average Convergence Divergence (MACD)), a bars-card button to blow away/rebuild parquet so MACD is baked, insight tabs for indicators vs Trend Following (TF) / Trading Strategy (TS), cross-portfolio holdings (including Winston Quiver (WQ)), and a header portfolio control that shows `#id name` as a link, listing every OP that books the market.

**Outcome:** Delivered on the inspect page. Rebuild is in-place restandardize (no EODHD re-download). Issuer name/exchange is whatever DM registry has (GOOGL has no Alphabet/Nasdaq string).

**One-line summary:** Signal Inspect now shows what is booked, where the parquet stands (including MACD), who holds the name across OPs, and what ATR/MACD/levels mean for this TS — plus a per-symbol parquet rebuild button.

---

## 2. Work Completed

- Market metadata card (symbol, venue, EODHD symbol, period, DM screener, registry source).
- DM eval card: latest/earliest, bar count, file mtime, coverage ingest, reconciled-at, indicator tags, Winston EOD Standard v0.2 missing-column warning.
- Holdings card: open lots across all OPs that hold the symbol (direction, units, lot count, pyramid/scale label, link to inspect in that OP). Live GOOGL: #11 Rust short 9u, #381 Blue long 2u, #1372 WQ short 0.111u.
- Header portfolio select is `#id name`; current OP links to `/operations/portfolios/:id`. “Also booked in” lists every Book on the symbol (including WQ).
- Focus chart: hides surrounding cards, keeps OHLC + ATR + MACD; Escape exits.
- Insight tabs for whatever is on the chart (price levels, ATR 17, MACD 12/26/9, RSI 14 if present, MA series if painted). Live reading + Winston/TF/this-TS copy.
- Bars card: **Blow away parquet & rebuild** → DM `POST /api/v1/triggers/restandardize` → `ParquetRestandardizeService` + `notify_consumers` → Wv2 ingest. Confirm dialog. Does not re-fetch from EODHD.
- DM markets API now returns `eodhd_symbol`, `period`, ticks, `last_reconciled_at`, `source`.

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `data_manager/app/controllers/api/v1/triggers_controller.rb` | modified | `restandardize` action |
| `data_manager/app/controllers/api/v1/markets_controller.rb` | modified | richer serialize |
| `data_manager/config/routes.rb` | modified | `POST /api/v1/triggers/restandardize` |
| `data_manager/spec/requests/api_v1_triggers_restandardize_spec.rb` | added | 3 examples |
| `winston_v2/app/controllers/operations/signal_inspect_controller.rb` | modified | rebuild action, booked portfolios |
| `winston_v2/app/services/operations/signal_inspect_payload.rb` | modified | market/dm_eval/holdings/insights |
| `winston_v2/app/services/operations/signal_inspect_insights.rb` | added | insight catalog + live reading |
| `winston_v2/app/services/dm_parquet_rebuild.rb` | added | HTTP client to DM |
| `winston_v2/app/views/operations/signal_inspect/show.html.erb` | modified | header, focus, bars rebuild, JS/CSS |
| `winston_v2/app/views/operations/signal_inspect/_market_card.html.erb` | added | |
| `winston_v2/app/views/operations/signal_inspect/_dm_eval.html.erb` | added | |
| `winston_v2/app/views/operations/signal_inspect/_holdings.html.erb` | added | |
| `winston_v2/app/views/operations/signal_inspect/_insights.html.erb` | added | |
| `winston_v2/config/routes.rb` | modified | `rebuild_parquet` |
| `winston_v2/spec/requests/operations_signal_inspect_spec.rb` | modified | UI + rebuild POST |
| `winston_v2/spec/services/operations/signal_inspect_payload_spec.rb` | modified | holdings/booked/insights |
| `winston_v2/spec/services/operations/signal_inspect_insights_spec.rb` | added | |
| `winston_v2/spec/services/dm_parquet_rebuild_spec.rb` | added | |
| `ecosystem/docs/session-reports/2026-09-10-1355-signal-inspect-market-insights.md` | added | this report |

### Commits

- `data_manager` `58ed28b` — feat(api): restandardize trigger and richer market metadata
- `winston_v2` `4086379` — feat(ops): Signal Inspect market card, holdings, insights, parquet rebuild
- `ecosystem` — this report (SHA at push)

### Branch / PR state at sign-off

- Branch: `main` on `winston_v2`, `data_manager`, `ecosystem`
- Pushed: yes (wrap)
- PR: not opened (direct `main`, matching recent wraps)

**Not this session (left dirty on purpose):** Wv2 quiver-tracking / slate / broker_gateway / `db/schema.rb`; ecosystem ADR-013, other tickets, `vendor/`.

---

## 4. Decisions Made

### Decision 1: Rebuild = restandardize, not EODHD re-fetch
- **Choice:** Bars-card button calls `ParquetRestandardizeService` (rewrite parquet from existing OHLCV; bake ATR/MACD/MAs). Confirm copy says no EODHD re-download.
- **Why:** Operator parenthetical was “so the MACD data would be generated.” Restandardize is seconds; full acquire is minutes + quota. Same service as `rake data:restandardize[SYMBOL]`.
- **Alternatives considered:** Delete file + `DataAcquisitionService.acquire`; two buttons.
- **Reversibility:** easy — add a force-reacquire endpoint later.
- **Promote to ADR?** no

### Decision 2: Inspect eval still requires one OP; holdings/books are cross-OP
- **Choice:** Strategy overlays still come from the selected portfolio’s TS. Header lists every Book on the symbol; holdings lists open lots everywhere.
- **Why:** Eval path is per-TS. WQ + Blue + Rust can all hold GOOGL.
- **Alternatives considered:** Inspect without a portfolio (no TS overlays).
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 3: Focus hides non-price/ATR/MACD paint
- **Choice:** Focus mode hides cards/eval/bars and restyles Plotly to OHLC + ATR + MACD only (entry/stop/breakout shapes off).
- **Why:** Operator asked to “just look at the chart and ATR + MACD.”
- **Reversibility:** easy
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- DM `SymbolRegistryEntry` for GOOGL has `name`/`trading_market`/`asset_class` nil (`list_source: manual`). Card cannot show Alphabet / Nasdaq until acquire records it.
- Wv2 `DmCoverage.indicators_present` for GOOGL was stale (ingest 2026-09-09, parquet rewritten 2026-09-10). Inspect unions parquet DESCRIBE + DM `/api/v1/markets` so MACD still shows. Rake restandardize does not notify consumers; the new HTTP path does.
- Live GOOGL 2026-09-09: MACD line below signal (bearish); Rust TS is 5-day breakout, so the MACD pane is context, not a confirm.
- `serialize_lots` used `@portfolio.id` for GTC lookup; switched to `pos.portfolio_id` so cross-OP holdings do not steal the current OP’s protective orders.
- Units serialized as `to_f` (WQ fractional lots).

---

## 6. Issues & Tickets

### Resolved this session
- Operator had no UI to re-bake MACD on a symbol (only `rake data:restandardize[SYMBOL]`). Button on inspect Bars card.

### Deferred
- Remaining corpus restandardize — already ticketed: `ecosystem/docs/tickets/2026-09-10-dm-restandardize-macd-corpus.md`.
- Issuer/exchange metadata empty on many registry rows (GOOGL).
- True “delete parquet + EODHD re-fetch” not built.
- Browser click-through of Focus chart (HTTP dump only).

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| DM restandardize API | compose rspec | ✅ 3 examples |
| Wv2 payload / insights / rebuild client | compose rspec `RAILS_ENV=test TEST_DB_HOST=wv2_postgres` | ✅ 13 examples |
| Live inspect GOOGL p11 2026-09-09 | curl localhost:3002 (HTTP 200; cards, tabs, rebuild form `/wv2/operations/signal_inspect/rebuild_parquet`, portfolio link `/wv2/operations/portfolios/11`) | ✅ |
| Focus chart click / Plotly restyle | not exercised in a browser | ⚠️ |
| Rebuild button against live DM | not clicked (would rewrite GOOGL parquet again) | ⚠️ |

**Test command(s):**

```bash
./bin/compose exec -T data_manager bundle exec rspec \
  spec/requests/api_v1_triggers_restandardize_spec.rb

./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 \
  bundle exec rspec \
  spec/services/operations/signal_inspect_payload_spec.rb \
  spec/services/operations/signal_inspect_insights_spec.rb \
  spec/services/dm_parquet_rebuild_spec.rb \
  spec/requests/operations_signal_inspect_spec.rb
```

**Live URL:** `https://sawtooth-ai.tail944ffb.ts.net/wv2/operations/signal_inspect?as_of=2026-09-09&portfolio_id=11&symbol=GOOGL&window=90`

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None added
- **Services:** existing compose (Wv2 bind-mount, DM bind-mount); no rebuild
- **Migrations:** None
- **Data:** GOOGL `bars.parquet` already had MACD from earlier `data:restandardize[GOOGL]` (1801 bars). This session did not rewrite it.

---

## 9. Risks & Technical Debt

- Rebuild is a destructive overwrite of shared DM parquet (WUT + Wv2). Confirm dialog only; no auth beyond ops UI CSRF.
- Inspect page load does a 3s DM HTTP GET for registry metadata; fails open to local Market + DmCoverage.
- Header “Also booked in” can be long (Rust + several Blue series + WQ).
- Unrelated dirty files remain on `winston_v2` and `ecosystem` — do not `git add .`.

---

## 10. Open Questions

- **Should DM pull issuer/exchange from EODHD search/fundamentals on acquire?** — needs answer from: operator; blocks: useful Market card names.
- **Should rebuild also offer a slow EODHD re-fetch?** — needs answer from: operator; blocks: nothing (restandardize covers MACD bake).

---

## 11. Handoff & Resume Notes

- **Where I left off:** Live inspect page serving new cards; specs green; wrap.
- **Next concrete step:** Operator reloads the GOOGL inspect URL, tries Focus chart, optionally rebuilds a non-GOOGL Book symbol that still lacks `macd_*`.
- **Files to read first:**
  1. `winston_v2/app/views/operations/signal_inspect/show.html.erb`
  2. `winston_v2/app/services/operations/signal_inspect_payload.rb`
  3. `winston_v2/app/services/operations/signal_inspect_insights.rb`
  4. `data_manager/app/controllers/api/v1/triggers_controller.rb` (`restandardize`)
  5. `ecosystem/docs/tickets/2026-09-10-dm-restandardize-macd-corpus.md`

---

## 12. Stakeholder Communications

- Operator-facing inspect page is live on Tailscale Serve; no Telegram / DAR copy change.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, session-report, wrap
- **What worked well:** curl of bind-mounted Wv2 caught the payload `p` loop-variable shadow immediately in principle (fixed in view); live holdings matched the desk (Rust #565 short 9u).
- **Friction points:** Wv2 request specs 422 without `protect_against_forgery?` stub when not forcing `RAILS_ENV=test`; default compose exec is development DB.
- **Subagent usage:** none

---

## 14. Follow-up Actions

- [ ] Enrich DM `Market`/`SymbolRegistryEntry` name + exchange (GOOGL → Alphabet / Nasdaq) — owner: next session — due: when Market card feels thin
- [ ] Restandardize remaining Active OP Book symbols — owner: operator or next session — due: see ticket `2026-09-10-dm-restandardize-macd-corpus.md` (per-symbol button now exists)
- [ ] Optional: force-reacquire (delete + EODHD fetch) — owner: only if operator wants true blow-away — due: unscheduled
- [ ] Browser-verify Focus chart — owner: operator on reload — due: now

---

## 15. Appendix (optional)

Live GOOGL DM eval (curl 2026-09-10 ~13:50 MDT): latest 2026-09-09, earliest 2019-07-11, 1801 bars, file written 2026-09-10 14:34 UTC, MACD columns present.

MACD insight reading: line −3.6228 vs signal −2.8645 (bearish); histogram expanding; TS does not use MACD 12/26/9 as entry/confirm.
