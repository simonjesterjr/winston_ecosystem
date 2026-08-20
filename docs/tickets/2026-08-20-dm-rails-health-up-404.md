# Ticket: Diagnose data_manager GET /up 404

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-08-20  
**Monoliths:** data_manager (DM)  
**See:** [`docs/session-reports/2026-08-19-1505-dm-pending-migration-telegram.md`](../session-reports/2026-08-19-1505-dm-pending-migration-telegram.md); sibling [`2026-08-20-compose-starting-healthcheck-inventory.md`](2026-08-20-compose-starting-healthcheck-inventory.md)

## Problem

`data_manager/config/routes.rb` registers:

```ruby
get "up" => "rails/health#show", as: :rails_health_check
```

After the 2026-08-19 Quiver migrate, host `GET http://127.0.0.1:3001/` returned **200**. `GET http://127.0.0.1:3001/up` returned **404**.

The ecosystem watchdog probes `/` (accepted 200/302), so this did not page Telegram. It does mean Rails’ advertised health path is dead.

**Hypothesis (not confirmed):** DM is Rails `~> 7.0.6`. `Rails::HealthController` shipped in Rails 7.1. The route would 404 if the controller is missing.

## Scope

1. Confirm whether `Rails::HealthController` exists in the running image (`bundle show rails`, `rails routes | grep up`).
2. Either implement a 7.0-compatible `/up` (or `/health`) that returns 200 when the process can serve, or drop the dead route.
3. Do **not** make `/up` run pending-migration checks if the intent is liveness. Pending migrations already 500 the whole app in development.

## Acceptance

- [ ] `curl -sS -o /dev/null -w '%{http_code}' http://127.0.0.1:3001/up` is **200** when DM is serving, **or** the route is removed and docs/compose do not mention `/up`
- [ ] Watchdog still uses `/` (or is explicitly switched with a spec)
- [ ] Existing `EcosystemHealthCheckService` specs still pass

## Non-goals

- Upgrading Rails to 7.1
- Changing Telegram watchdog schedule
