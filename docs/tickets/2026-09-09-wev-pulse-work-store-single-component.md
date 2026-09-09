# Ticket: PulseWork::Store as one component (import or single deploy)

**Status:** Proposed
**Priority:** P2
**Mode:** contractor
**Program:** Winston Ecosystem View
**Parent:** [`2026-09-07-winston-ecosystem-view.md`](2026-09-07-winston-ecosystem-view.md)
**Graph nodes:** ecosystem, winston_v2, winston_unit_test, data_manager, broker_gateway
**Depends on:** named emit shipped 2026-09-09 (four copies live)
**Human gates:** Do not invent a fifth majestic monolith. WEV plan still forbids a new compose service unless a grill overturns that. Schema stays `wev:pulse:work` on the **owner’s** Redis DB (`/0..3`) — not a shared Pulse database.
**DoD:** One source of `PulseWork::Store` (and the opt-in `PulseWork` emit API) that DM / WUT / Wv2 / BG consume. Four in-tree copies deleted. Interface `winston-ecosystem-view-v1.md` Pulse Work Record unchanged.

## Why

Named Pulse Work (session `2026-09-09-1445-wev-pulse-named-work`) copied an identical ~60-line `PulseWork::Store` into four Rails apps. That will drift the first time someone “improves” one copy (TTL, key names, forbidden PnL keys, memory-mode for specs).

The Pulse Work **record** is the contract. The Ruby that writes HASH / LIST / `PUBLISH wev:pulse` should live once.

## Shape (grill if needed; default is the smallest that keeps one copy)

Prefer in this order unless a session says otherwise:

1. **Shared Ruby component imported by each monolith** (path gem, `lib/` vendored from `ecosystem/`, or a tiny private gem). Each process still writes to **its** `REDIS_URL` DB. No new container.
2. **Single deployable helper** only if import is genuinely worse (version skew you cannot live with). Still not a fifth majestic monolith: no UI, no PG, no PnL. Must not become the Pulse projector (that stays Wv2).

Not: Redis `/4` “for WEV.” Not: copying Store into a fifth app that also reimplements `EcosystemPulse`.

## Work

- Pick 1 vs 2 (import first). If 2, grill against ADR-001 + WEV “no new compose service.”
- One tree for `PulseWork` + `PulseWork::Store` + specs.
- Each monolith `require`s / gems it; job `include PulseWork` stays local (titles are owner-specific).
- Delete the four copies. Spec that forbidden keys and key names still match the interface.

## See

- Interface: `ecosystem/interfaces/winston-ecosystem-view-v1.md` (Pulse Work Record)
- Copies today: `{winston_v2,winston_unit_test,data_manager,broker_gateway}/app/services/pulse_work/`
- Session: [`docs/session-reports/2026-09-09-1445-wev-pulse-named-work.md`](../session-reports/2026-09-09-1445-wev-pulse-named-work.md) §4 Decision 4, §9
- Sibling grill (cuboid identity, not this Store): [`2026-09-09-wev-pulse-container-catalog-sot.md`](2026-09-09-wev-pulse-container-catalog-sot.md)
