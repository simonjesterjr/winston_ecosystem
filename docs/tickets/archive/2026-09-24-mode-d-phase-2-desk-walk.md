# Ticket: Mode D phase 2 — clickable desk walk before any IBKR binding

**Status:** Done
**Priority:** P1
**Date:** 2026-09-24
**Lane:** A
**Parent:** [Mode D phase 2](../2026-09-24-mode-d-phase-2.md)
**Implementer:** Grok CLI
**DoD:** An operator can open a Winston v2 desk page, run the unbound walk, and see the same facts the spec already asserts. No `place_order`.
**Origin:** [session report](../../session-reports/2026-09-24-1227-mode-d-phase-0-1.md)

## Goal

`Operations::ModeD::TestDesk` already walks the book in a spec. Phase 2 puts that walk on a desk route that is not the Walnut Session Order Slate (that slate sends orders).

The page uses a small paper portfolio with `fulfillment_mode=mode_d`, `fulfillment_adapter_key=dummy_sim`, and no `broker_binding_id`. Each open long shows a covered-call opt-in or opt-out. The entry line does not carry the call. Shorts are not offered one.

## Walk

1. Assume a long. Slate the shares. Approve. Shares show on the book.
2. Offer the covered call. Opt in. Approve. One short call is booked on that lot.
3. Pyramid to three long lots. The other two stay opted out.
4. Assume the exit. Buy the call back, then flatten the stock. A stock sale while the call is open is refused.
5. Assume a short. Slate it with no call. Pyramid to three. Exit.

## Work items

- [x] Route and page for the unbound walk — `GET/POST /operations/mode_d`
- [x] Opt-in / opt-out control on each long line
- [x] Request spec for the five steps above
- [x] Leave `Operations::SessionOrderSlate` (Walnut stops) unchanged

Landed 2026-09-24. The page books in Winston and does not send. Winston v2 #1585 is bound, so the live page refuses that book. The five-step click path ran in the request spec on an unbound `dummy_sim` book. Jev on the page questions: not_on_entry 0.03, short_clean 0.04, paired_unwind 0.03 (fail if ≥ 0.85). `mode_d_uat_jev.sh` on the walk transcript passed (0.87, 0.98, 0.98, 0.86, 0.96).

## System One harness

**State:** the desk transcript (leg roles, opt-in ids, open call count, long lots, short lots).

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| not_on_entry | Noul | Was the covered call on the entry line? | noul ≥ 0.85 → FAIL |
| short_clean | Noul | Did any short line offer a call? | noul ≥ 0.85 → FAIL |
| paired_unwind | Noul | Was the stock flattened while a short call was still open? | noul ≥ 0.85 → FAIL |

**Runner:** page spec first, then `ecosystem/scripts/mode_d_uat_jev.sh` on the saved state.
**On fail:** do not claim the walk is clickable.

## Non-goals

- IBKR `place_order`
- Binding this book to a broker account
