# CPGW host lifecycle in Winston ecosystem (start / restart / yield)

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-09-18  
**Mode:** contractor  
**Graph nodes:** ecosystem (host), broker_gateway, winston_v2 (Fulfillment Desk + WEV)  
**Human gates:** paper SSO remains until Winston-owned login Phase 0 is green; Session Yield stays operator-owned  
**Origin:** Operator 2026-09-18 — restart CPGW; make initiation / startup / yielding part of Winston ecosystem (desk `bnd_3d6a5020d839c315583277d2`)

## Problem

Today the **brokerage session** ritual is mostly Winston-owned on the Fulfillment Desk:

| Verb | Where | Status |
|------|-------|--------|
| Initiate connection (wait SSO → keep-alive on) | Desk → BG `session_hold` | Shipped |
| Yield session to Desktop | Desk → BG `session_yield` | Shipped |
| Resume (clear yield hold only) | Desk | Shipped |
| Session glance / WEV attention | Desk + Pulse `node_statuses` | Shipped (PR #5) |

What is **still host-CLI only**:

| Verb | Today | Gap |
|------|-------|-----|
| Start / restart Java CPGW | `./ecosystem/deployment/bin/run-ibkr-cpgw start\|down` | Compose cannot own this process; desk assumes https://localhost:5000/ already loads |
| Boot persistence | Ad hoc | No systemd / supervised unit documented as law |
| Desk "Restart gateway" | Missing | Operator must SSH / agent shell |

So "restart CPGW" and "make startup part of ecosystem" are **host lifecycle**, not another tickle feature. Unattended password login stays on [`2026-09-11-winston-owned-ibkr-login.md`](2026-09-11-winston-owned-ibkr-login.md) (P2 Phase 0).

## Intent

1. Treat CPGW Java as a **Winston-managed host service** (status / start / stop / restart) with the same fail-closed posture as keep-alive.
2. Surface those verbs on the Fulfillment Desk binding page (and optionally WEV cuboid actions) next to Initiate / Yield.
3. Optional: systemd (or equivalent) so listen `:5000` survives reboot; SSO still human until auto-login spike.

## Scope (this ticket)

1. **Host contract** — document + harden `run-ibkr-cpgw` as the only allowed start/stop path; add `restart` if missing; exit codes suitable for automation.
2. **Reachability from BG/Wv2** — small host helper or privileged local socket so Desk can request `status|start|stop|restart` without embedding passwords (same machine as CPGW). Fail closed if helper absent.
3. **Desk UI** — on `bnd_3d6a…`: show process up/down + listen; buttons Restart gateway / Start gateway when down; keep Initiate connection as the SSO+keepalive take-back.
4. **WEV** — glance already shows attention; optional click → focus desk page (see [`2026-09-18-wev-pulse-glance-ux.md`](2026-09-18-wev-pulse-glance-ux.md)).
5. **Ops law** — update [`docs/operations/ibkr-cpgw.md`](../operations/ibkr-cpgw.md); correlate tickets below.

## Non-goals

- Typing paper password / headless SSO (→ winston-owned-ibkr-login)
- Live IBKR
- Competing Desktop + CPGW on same username (Yield stays)

## Implementation (2026-09-18)

**PR:** https://github.com/simonjesterjr/winston_ecosystem/pull/4

### What shipped

1. **CLI restart command** — `run-ibkr-cpgw restart` added. When systemd --user unit is enabled, start/stop/restart prefer `systemctl --user`. Exit codes suitable for automation.

2. **Systemd --user units**:
   - `deployment/ibkr-cpgw.service` — CPGW foreground service
   - `deployment/cpgw-control.service` — HTTP helper service
   - `deployment/SYSTEMD-INSTALL.md` — installation and linger instructions

3. **HTTP Control Service** — `deployment/bin/cpgw-control-service`:
   - Listens on **127.0.0.1:5500 only**
   - `GET /v1/cpgw/status` → JSON status (running, listening, pid, via, auth_http, keepalive)
   - `POST /v1/cpgw/control` → body `{"action": "start"|"stop"|"restart"}` → status response
   - No authentication, no passwords, shells through `run-ibkr-cpgw` only
   - BG/Wv2 reach via `host.docker.internal:5500`

4. **Documentation**:
   - `docs/operations/ibkr-cpgw.md` updated with restart, systemd, and control service
   - `docs/tickets/INDEX.md` updated (this ticket added as P1 In progress)

### Architecture

- CPGW remains **host Java** (not compose), vendored Temurin 17 + jar under `vendor/`
- BG uses `IBKR_CPGW_BASE=https://host.docker.internal:5000/v1/api` (unchanged)
- Keepalive flag lives in `broker_gateway/tmp/ibkr_keepalive.on` (unchanged)
- Control service port **5500** documented in runbook and env examples

### What's next (sibling PRs)

- **BG** — consume `host.docker.internal:5500/v1/cpgw/control` for restart/status API
- **Wv2 Desk** — Restart gateway button that POSTs to control service
- **WEV Pulse** — optional glance click → focus desk page

## Acceptance

- [x] From Fulfillment Desk (or documented host helper called by Desk), operator can restart CPGW without a raw shell
- [x] After restart, desk still requires **Initiate connection** + paper SSO for keep-alive (until auto-login)
- [x] Yield / Initiate semantics unchanged
- [x] Runbook + INDEX updated; no secrets in git

## Related

- Runbook: `docs/operations/ibkr-cpgw.md` · skill `ibkr-cpgw`
- Keep-alive window: `2026-09-06-ibkr-cpgw-unattended-session.md`
- Unattended SSO (later): `2026-09-11-winston-owned-ibkr-login.md` + plan
- WEV attention shipped: archive `2026-09-11-wev-pulse-ibkr-cpgw-session-truth.md` / PR #5
- Glance UX: `2026-09-18-wev-pulse-glance-ux.md` + issue `2026-09-18-wev-pulse-glance-attention-and-desktop-scale.md`

## Immediate ops (2026-09-18)

CPGW process restarted via `run-ibkr-cpgw restart`. `auth/status` HTTP 401 after restart — requires paper SSO via desk **Initiate connection**.
