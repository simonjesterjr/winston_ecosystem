---
name: ibkr-cpgw
description: >
  Interactive Brokers Client Portal Gateway lifecycle: status, start/stop,
  paper browser SSO, explicit keep-alive window, TickleJob. Triggers:
  /ibkr-cpgw, CPGW up/down, IBKR login, tickle, keep-alive, localhost:5000.
metadata:
  short-description: "CPGW up / keep-alive / down"
---

# Interactive Brokers Client Portal Gateway

Runbook (source of truth): `ecosystem/docs/operations/ibkr-cpgw.md`

```bash
./ecosystem/deployment/bin/run-ibkr-cpgw status
./ecosystem/deployment/bin/run-ibkr-cpgw up      # start + wait paper SSO + keep-alive on
./ecosystem/deployment/bin/run-ibkr-cpgw down    # keep-alive off + stop Java
```

- Host process on https://localhost:5000 — **not** compose.
- Operator path: Fulfillment Desk **Initiate connection**, then paper SSO in a browser. Do not store or type the password. Same paper username: **Yield session to Desktop** on that page before using Interactive Brokers Desktop / Trader Workstation.
- `TickleJob` (every minute) runs **only** while `broker_gateway/tmp/ibkr_keepalive.on` exists and `BG_IBKR_LIVE_READ=true`. A 401 closes the window.
- Idle without tickle ~6 minutes. A logged-in gateway self-tickles; measured hold ~44 hours until DNS/IBKR drop. **`down` ends the window.**
- Vendored Java is Eclipse Temurin 17 (`ecosystem/vendor/jdk-17-jre`), not a second product.
