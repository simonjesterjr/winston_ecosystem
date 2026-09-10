# Ticket: Record issuer name and exchange on DM Market / registry

**Status:** Proposed
**Priority:** P2
**Date:** 2026-09-10
**Mode:** contractor
**Graph nodes:** data_manager, winston_v2
**Edges:** `data_manager/app/services/market_metadata_recorder.rb`, `GET /api/v1/markets`, Signal Inspect market card
**Human gates:** none (EODHD read; no capital action)
**DoD:** Signal Inspect Market card for GOOGL shows issuer name and listing venue, not only the ticker
**Origin:** session `docs/session-reports/2026-09-10-1355-signal-inspect-market-insights.md`

## Problem

Winston v2 (Wv2) Signal Inspect now has a Market card (what is traded, where). For **GOOGL** the data_manager (DM) `SymbolRegistryEntry` has `name` / `trading_market` / `asset_class` all nil (`list_source: manual`). Wv2 `Market` stores `name: "GOOGL"`, `trading_market: "US"`. The card therefore says “GOOGL · US cash session · daily Winston EOD bars via EODHD” instead of Alphabet Class A / Nasdaq.

`MarketMetadataRecorder.record_success!` only writes `name` / `trading_market` when the acquire path already has them. Manual / demand-driven acquire does not call EODHD search or fundamentals.

## Work

1. On successful EODHD acquire (or a cheap one-shot backfill), persist issuer `name`, listing venue / `trading_market`, and `asset_class` on `Market` + `SymbolRegistryEntry`.
2. Prefer one EODHD lookup per symbol (search or exchange-symbol-list), not a fundamentals hit on every inspect page load.
3. Keep inspect fail-open: missing name still shows the ticker.
4. Spot-check GOOGL on Signal Inspect after backfill.

## Acceptance

- [ ] GOOGL registry row has a human issuer name and a venue richer than blank/`US` alone.
- [ ] New acquires populate name/venue without a separate rake.
- [ ] Inspect Market card shows the issuer line when `name != symbol`.
- [ ] No EODHD call on every inspect GET.

## Out of scope

- Changing Winston Market Suitability floors
- Per-page live EODHD search from Wv2

## Related

- `data_manager/app/controllers/api/v1/markets_controller.rb` (`serialize_entry`)
- `winston_v2/app/views/operations/signal_inspect/_market_card.html.erb`
- Live inspect: `/wv2/operations/signal_inspect?as_of=2026-09-09&portfolio_id=11&symbol=GOOGL&window=90`
