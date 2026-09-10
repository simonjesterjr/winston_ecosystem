# Ticket: WEV work catalog — index archive tickets not listed in INDEX

**Status:** Proposed
**Priority:** P3
**Mode:** normal
**Program:** Winston Ecosystem View
**Parent:** [`2026-09-07-winston-ecosystem-view.md`](2026-09-07-winston-ecosystem-view.md)
**Graph nodes:** ecosystem, winston_v2
**Edges:** `ecosystem/ecosystem_view/bin/index_work`, `docs/tickets/INDEX.md`, `docs/tickets/archive/`
**Depends on:** [`2026-09-09-wev-work-json-split-bodies.md`](2026-09-09-wev-work-json-split-bodies.md) if the extra bodies make Tailscale first-open slow
**DoD:** Code **Completed** tab for a cuboid can open a ticket that lives only under `docs/tickets/archive/` and is not a row in INDEX; `work.json` size impact is measured and accepted (or bodies are split first)

## Why

`index_work` collects tickets from `docs/tickets/INDEX.md` only. Archive is a fallback when the INDEX path is missing on disk. ~84 files in `docs/tickets/archive/` are **not** INDEX rows, so the Code **Completed** tab (2026-09-09) cannot show them. INDEX hygiene (move Done rows to archive and drop them from the table) would make this worse unless the indexer walks `archive/`.

Walking archive with 16 KB clipped bodies could add ~1 MB to the already ~1.1 MB `work.json`. Do not do this blindly on Tailscale `/wv2`.

## Work

1. Count archive files not already in the catalog; estimate byte delta.
2. If delta is large, split index vs bodies first (depends-on ticket) or index archive as metadata-only (`body` empty until row open).
3. Deduplicate by stem against INDEX rows (some INDEX lines already point at `archive/…`).
4. Re-run indexer; Completed tab on `ecosystem` cuboid lists archive-only Done tickets.

## Not this ticket

- YAML / Status-banner into catalog `status` — [`2026-09-09-wev-index-work-yaml-status.md`](2026-09-09-wev-index-work-yaml-status.md)
- INDEX hygiene (move remaining Done rows out of the active table)
- Split `work.json` itself — [`2026-09-09-wev-work-json-split-bodies.md`](2026-09-09-wev-work-json-split-bodies.md)
