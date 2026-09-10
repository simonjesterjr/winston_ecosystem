# Ticket: WEV work catalog — parse YAML / Status-banner into `status`

**Status:** Proposed
**Priority:** P3
**Mode:** normal
**Program:** Winston Ecosystem View
**Parent:** [`2026-09-07-winston-ecosystem-view.md`](2026-09-07-winston-ecosystem-view.md)
**Graph nodes:** ecosystem, winston_v2
**Edges:** `ecosystem/ecosystem_view/bin/index_work`, `winston_v2/public/ecosystem/work.json`
**DoD:** Catalog `status` on issues (and tickets without INDEX override) matches YAML `status:` or `**Status banner:**` when `**Status:**` is absent; Code **Completed** tab still classifies correctly if the JS body fallback is removed

## Why

Winston Ecosystem View (WEV) Code **Completed** tab (2026-09-09) classifies tickets/issues from catalog `status`, then falls back to the document body. `index_work.meta_status()` only reads `**Status:**` (and a table form). Nine ecosystem issues therefore ship with empty `status` even though they have YAML `status: resolved|done|ready` and a human **Status banner**. The JS fallback works; the catalog field still lies.

## Work

1. In `ecosystem/ecosystem_view/bin/index_work` `meta_status()`, also read:
   - `**Status banner:**` / `**Status banner (human-readable):**`
   - YAML frontmatter `status:`
2. Prefer `**Status:**`, then banner, then YAML.
3. Re-run `python3 ecosystem/ecosystem_view/bin/index_work` and spot-check issues that previously had empty `status`.
4. Optional: drop the JS body fallback once catalog `status` is filled (keep `/archive/` path rule).

## Not this ticket

- Refresh hook when docs change — [`2026-09-09-wev-index-work-refresh-hook.md`](2026-09-09-wev-index-work-refresh-hook.md)
- Index archive files missing from INDEX — [`2026-09-09-wev-index-work-archive-tickets.md`](2026-09-09-wev-index-work-archive-tickets.md)
- Owner heuristic — [`2026-09-09-wev-index-work-owner-heuristic.md`](2026-09-09-wev-index-work-owner-heuristic.md)
