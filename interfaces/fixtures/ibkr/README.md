# Interactive Brokers Web API — L1 vendor-shaped fixtures

**Status:** canned JSON for Broker Gateway `interactive_broker_trader_api` fixture mode  
**Not a live IBKR session.** Field names follow Client Portal Web API / IBKR Web API (`/iserver/account/orders`, `/iserver/account/trades`).  
**Normalize to:** Winston Broker Evidence Standard v0.1.

| File | Vendor shape | Evidence |
|------|----------------|----------|
| `trades.json` | `GET /iserver/account/trades` | `trade.executed` |
| `orders.json` | `GET /iserver/account/orders` | filled + canceled orders |

Live HTTP is **off** unless `BG_IBKR_LIVE_READ=true`. Individuals typically authenticate via the **Client Portal Gateway** (browser SSO to a local Java proxy), not a long-lived bearer token in git. Paper uses a **paper username**, not a slider.
