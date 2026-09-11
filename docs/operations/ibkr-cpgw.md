# Interactive Brokers Client Portal Gateway (CPGW)

Host process (not compose). Paper Single Sign-On (SSO) is a browser step. Broker Gateway never stores the username or password.

**Commands:** `./ecosystem/deployment/bin/run-ibkr-cpgw`  
**Skill:** `ibkr-cpgw`  
**Ticket:** `docs/tickets/2026-09-06-ibkr-cpgw-unattended-session.md`

## Java (Eclipse Temurin 17)

CPGW is a Java app. Sawtooth vendors **Eclipse Temurin 17** — the Adoptium OpenJDK 17 Java Runtime Environment — at `ecosystem/vendor/jdk-17-jre`. It is not a second product and not Interactive Brokers software. Using the vendored runtime avoids depending on whatever `java` is on PATH.

## Timeouts (measured)

| What | Duration |
|------|----------|
| Idle without any tickle | ~6 minutes (Interactive Brokers documented) |
| Logged-in CPGW self-tickle | ~30 seconds (gateway timer) |
| Broker Gateway `TickleJob` | every minute, **only while keep-alive is on** and `BG_IBKR_LIVE_READ=true` |
| One paper SSO + tickle, 2026-09-09 08:26 → 2026-09-11 04:56 | **~44.5 hours** until DNS `api.ibkr.com` killed the session |

The 6-minute figure is **idle**, not a max session length. 10 Sep had **zero** browser logins; DAY-order polls were the leftover 9 Sep 08:26 paper SSO held by keep-alive.

Leaving CPGW logged in **is** a multi-hour keep-alive (the Java process tickles itself). `down` is the real off switch. `keepalive off` only stops Broker Gateway’s minute job.

## Non-programmatic (operator)

1. Do not leave Interactive Brokers Desktop / Trader Workstation logged in as the **paper** username.
2. Fulfillment Desk (IBKR binding) → **Initiate connection**.
3. Browser: https://localhost:5000/ — accept the self-signed cert — **paper** username. The desk waits (reload) until `auth/status` is HTTP 200, then turns keep-alive on.
4. Bound Operational Portfolios may use Broker Gateway (polls, Desk Send, 15-minute DAY-order eval).
5. **Yield session to Desktop** when you need the same paper username in Desktop. **Initiate connection** to take it back.
6. Host process down (page does not load): `./ecosystem/deployment/bin/run-ibkr-cpgw start` once, then Initiate connection again. End of window: `down` (stops Java) or leave CPGW running.

Foreground alternative: `start --fg` in a terminal (Ctrl+C stops). From another terminal after SSO: `keepalive on`.

## Programmatic (agent / script)

```bash
./ecosystem/deployment/bin/run-ibkr-cpgw status
./ecosystem/deployment/bin/run-ibkr-cpgw start          # process only
./ecosystem/deployment/bin/run-ibkr-cpgw up             # start + wait SSO + keepalive on
./ecosystem/deployment/bin/run-ibkr-cpgw up --timeout 0 # start, do not wait
./ecosystem/deployment/bin/run-ibkr-cpgw keepalive on   # requires HTTP 200 unless FORCE=1
./ecosystem/deployment/bin/run-ibkr-cpgw keepalive off
./ecosystem/deployment/bin/run-ibkr-cpgw down           # keepalive off + stop Java
```

Keep-alive flag (bind-mounted into Broker Gateway): `broker_gateway/tmp/ibkr_keepalive.on`.  
`TickleJob` no-ops without it and **deletes it** on 401/error so a dead session is not hammered 24×7.

## Session Yield (Desktop / Trader Workstation)

Same paper username cannot sit in CPGW and Interactive Brokers Desktop at once. CPGW tickle / `compete=true` disconnects Desktop.

On the Fulfillment Desk binding page (`/operations/fulfillment/:id`): **Yield session to Desktop**. That:

- sets `operator_holds_session` on the Adapter Binding
- turns keep-alive off
- best-effort CPGW logout so Desktop can take the session
- makes TickleJob, live polls, and Desk Send fail closed on that bind

**Resume Client Portal Gateway** clears the hold only. **Initiate connection** is the take-back: clears yield, waits for paper SSO, keep-alive on. Browser login without Initiate connection is **keep-alive off**.

Fulfillment Desk session (not Adapter Binding `status`):

| Session | Tag | Yield |
|---|---|---|
| Keep-alive on and authenticated | `active` (Winston holds) | offered |
| Operator using Desktop | `Desktop holds session` | Resume |
| Gateway logged in, keep-alive off | `keep-alive off` | disabled — **Initiate connection** turns tickle on |
| Waiting for paper SSO | `waiting for login` | disabled — desk polling |
| Brokerage session dead | `needs login` | disabled — **Initiate connection** then login |

Glance tag: `Desktop holds session` (not `needs login`). Do not print Adapter Binding lifecycle `active` as if Winston holds.

## Winston cannot yet

- Type the paper password / complete SSO without a human.
- Treat Pulse `ibkr_cpgw` as session truth (cron can look fresh while HTTP is 401).

Next slice (same ticket): after `up`, Winston owns keep-alive + Broker Gateway for bound clients, then `down` or leave the window open for 15-minute DAY-order eval. Unattended SSO stays a human gate until that ticket decides otherwise.
