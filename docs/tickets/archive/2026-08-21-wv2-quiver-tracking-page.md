# Ticket: Wv2 Quiver Tracking desk page + empty paper OP

**Status:** Done  
**Priority:** P1  
**Date:** 2026-08-21  
**Monoliths:** winston_v2 (Wv2), ecosystem compose / Tailscale Serve  
**See:** [`plans/quiver-tracking-desk.md`](../../../plans/quiver-tracking-desk.md); analysis [`2026-08-21-quiver-quant-vs-api-vs-dm.md`](../../analysis/2026-08-21-quiver-quant-vs-api-vs-dm.md)

## Problem

Congress Long-Short tracking needs its own desk, not the TF ops shell and not the WUT Quiver Skim tab. Public URL: `https://sawtooth-ai.tail944ffb.ts.net/wv2/quiver_tracking`.

## Scope

1. Route `GET /quiver_tracking` (Tailscale already prefixes `/wv2`).
2. Reuse `ops_shell.css` / ops-shell chrome; copy is “Quiver Tracking”, not “Ops Shell.”
3. Bootstrap (idempotent rake) one **paper** Tracking Operational Portfolio (OP), **empty Books**, execution_mode paper, Daily Analysis skip (`quiver_tracking_book`). Default capital **$2,000**. Fingerprint **must not** be `qcls13030-l30-filedate-v1` (old 15/10 copy-book).
4. Isolation: tracking pending/journals/positions **not** in TF `/operations` 25-row pending. Optional one-line link from ops shell.
5. Panels: last PDF (empty state), target vs current (empty), pending, positions, journals, equity placeholder.
6. Disable / do not run `QuiverCongressLongShortRebalanceJob` against this OP.

## Acceptance

- [x] `/wv2/quiver_tracking` HTTP 200, ops-shell styled
- [x] Empty paper tracking OP listed only on this page
- [x] TF Active OPs and `/operations` pending unchanged
- [x] Request spec: isolation + skip Daily Analysis
- [x] No Quiver API key on Wv2

## Non-goals

- PDF parse (next ticket)
- Telegram
- Broker Gateway
- WUT Skim UI
