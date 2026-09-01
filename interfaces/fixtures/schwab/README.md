# Schwab Trader API — L1 vendor-shaped fixtures

**Status:** canned JSON for Broker Gateway `schwab_trader_api` fixture mode  
**Not live Schwab.** Field names follow Trader API — Individual (`activityId`, `transferItems`, `orderLegCollection`).  
**Normalize to:** Winston Broker Evidence Standard v0.1 (`trade.executed`, `order.upserted` / `order.canceled`).

| File | Vendor shape | Evidence |
|------|----------------|----------|
| `transactions.json` | `GET …/transactions?types=TRADE` | `trade.executed` (equity + option extra-modal) |
| `orders.json` | `GET …/orders` | filled upsert + canceled |

Live HTTP is **off** unless `BG_SCHWAB_LIVE_READ=true` **and** tokens are present. Portal sandbox verdict is still an operator spike (`docs/tickets/2026-08-07-schwab-trader-api-sandbox-spike.md`).
