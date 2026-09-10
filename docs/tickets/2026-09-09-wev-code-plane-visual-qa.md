# Ticket: WEV Code plane — operator visual QA

**Status:** Proposed
**Priority:** P2
**Mode:** normal
**Program:** Winston Ecosystem View
**Parent:** [`2026-09-07-winston-ecosystem-view.md`](2026-09-07-winston-ecosystem-view.md)
**Graph nodes:** winston_v2, ecosystem
**Edges:** `interfaces/winston-ecosystem-view-v1.md`, `public/ecosystem/wev-live.js`
**Human gates:** none (read-only clickthrough)
**DoD:** Operator has clicked Code cuboids + all four work sub-tabs + opened one ADR under the diagram on both local `:3002` and Tailscale `/wv2/operations/ecosystem`

## Why

Winston Ecosystem View (WEV) Code plane v2 (Architecture Decision Record / tickets·issues / plans sub-tabs, cuboid metadata, document reader) shipped in the 2026-09-08 session. Request specs and `curl` 200s passed; **no browser MCP** exercised clicks. The wrap must not claim the reader works until a human opens it.

## Work

1. Open Code on `http://127.0.0.1:3002/operations/ecosystem` (hard refresh; assets are `?v=20260909r`).
2. Click `dm`: metadata answers what / for / helps Winston / externals (End of Day Historical Data, Quiver Quantitative).
3. Switch **ADRs**, **open tickets / issues**, **Completed**, **plans**. Open one ADR — markdown appears **under** the cuboids, not in a new tab.
4. Repeat on Tailscale `/wv2/operations/ecosystem` (`work.json` is ~1.1 MB; note if the first Code-tab open is slow).
5. File a one-line note on this ticket (pass / fail + URL). Failures spawn a defect issue, not a silent re-theme.

## Not this ticket

- git/CI “code health” — still a parent follow-on
- Split `work.json` — [`2026-09-09-wev-work-json-split-bodies.md`](2026-09-09-wev-work-json-split-bodies.md)
