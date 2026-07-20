# Ticket: Rotate / truncate WUT development.log

**Status:** Proposed
**Priority:** unset

**Date:** 2026-07-09

**Context:** Session [`2026-07-09-1308-orange-white-vet-trend`](../session-reports/2026-07-09-1308-orange-white-vet-trend.md). Observed `winston_unit_test` `log/development.log` at **~40GB** / ~220M lines during Orange/White vets.

## Problem

- Disk pressure and slow I/O during long backtests (ActiveRecord SQL logging)
- Log greps time out; containers harder to inspect
- May amplify validation-run wall-clock when runners write heavily

## Scope

1. Truncate or rotate current `development.log` on compose WUT (operator-safe procedure).
- Prefer logrotate / Rails config over one-off delete without documenting recovery.
2. Ensure development/test logging level or tagged loggers don't grow unboundedly under Sidekiq + long rakes.
3. Document in WUT AGENTS or ops notes: where logs live, how to rotate.

## Acceptance

- Log size back to operational baseline after procedure
- Documented rotation path (compose exec steps)
- No silent loss of needed audit trail for integration (ecosystem audit log remains separate)

## Related

- Session: `docs/session-reports/2026-07-09-1308-orange-white-vet-trend.md`
- Related operational: ecosystem log hygiene tickets if any
