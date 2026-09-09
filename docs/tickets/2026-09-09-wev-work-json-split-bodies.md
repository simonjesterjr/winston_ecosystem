# Ticket: WEV work catalog — split index vs bodies (if Tailscale hurts)

**Status:** Proposed
**Priority:** P3
**Mode:** normal
**Program:** Winston Ecosystem View
**Parent:** [`2026-09-07-winston-ecosystem-view.md`](2026-09-07-winston-ecosystem-view.md)
**Graph nodes:** winston_v2, ecosystem
**Edges:** `public/ecosystem/work.json`, `wev-live.js`
**Depends on:** [`2026-09-09-wev-code-plane-visual-qa.md`](2026-09-09-wev-code-plane-visual-qa.md) (measure first)
**DoD:** Code tab first paint fetches a small index; opening a row fetches that document only — **only if** visual QA shows the 1.1 MB `work.json` fetch is slow on Tailscale `/wv2`

## Why

Winston Ecosystem View (WEV) Code plane fetches `GET /ecosystem/work.json` (~1.1 MB, 285 items with bodies clipped at 16 KB) when the Code tab opens. That avoided stuffing bodies into the HTML `data-work` attribute. On a LAN `:3002` it is fine; under Tailscale Serve `/wv2` it may not be.

## Work (only after QA notes slowness)

1. Keep `work.json` as `{ generated_at, nodes, items[] }` **without** `body`.
2. Per-item files or `GET /ecosystem/work/:kind/:id` for the markdown (static files under `public/ecosystem/work/` are enough — no new Rails action required).
3. Metadata pane still uses `nodes` from the index (no extra round-trip).

## Not this ticket

- Rebuild as a CMS
- Action Cable for docs
