# Ticket: WEV work catalog — refresh when docs change

**Status:** Proposed
**Priority:** P3
**Mode:** normal
**Program:** Winston Ecosystem View
**Parent:** [`2026-09-07-winston-ecosystem-view.md`](2026-09-07-winston-ecosystem-view.md)
**Graph nodes:** ecosystem, winston_v2
**Edges:** `ecosystem/ecosystem_view/bin/index_work`, `winston_v2/public/ecosystem/work.json`
**DoD:** A documented (or hooked) step regenerates both catalog copies after ADR / ticket / plan edits; Code plane does not silently serve a stale 2026-09-08 snapshot

## Why

Winston Ecosystem View (WEV) Code plane reads `winston_v2/public/ecosystem/work.json`. `ecosystem/docs` is **not** mounted in the Wv2 container, so Rails cannot scan markdown live. The indexer writes:

- `ecosystem/ecosystem_view/catalog/work.json`
- `winston_v2/public/ecosystem/work.json`

If nobody re-runs it, new ADRs never appear under the cuboids.

## Work

1. Add a one-liner to `ecosystem/ecosystem_view/README.md` and the wrap/`ship-to-test` notes: `python3 ecosystem/ecosystem_view/bin/index_work`.
2. Optional hook: call the indexer from `/wrap` when `ecosystem/docs/{adr,tickets,issues}` or `ecosystem/plans/` changed this session — do not add a cron that rewrites git on the host unattended.
3. Do not mount the whole `ecosystem/docs` tree into Wv2 just to avoid this (blast radius / secrets).

## Not this ticket

- Owner heuristic quality — [`2026-09-09-wev-index-work-owner-heuristic.md`](2026-09-09-wev-index-work-owner-heuristic.md)
- Splitting the 1.1 MB JSON — [`2026-09-09-wev-work-json-split-bodies.md`](2026-09-09-wev-work-json-split-bodies.md)
