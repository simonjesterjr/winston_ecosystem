# Ticket: WEV work catalog — tighten owner heuristic

**Status:** Proposed
**Priority:** P3
**Mode:** normal
**Program:** Winston Ecosystem View
**Parent:** [`2026-09-07-winston-ecosystem-view.md`](2026-09-07-winston-ecosystem-view.md)
**Graph nodes:** ecosystem, winston_v2
**Edges:** `ecosystem/ecosystem_view/bin/index_work`
**DoD:** Clicking `dm` on the Code plane no longer lists cross-cutting plans that only mention data_manager in passing; owner tags match the ticket/ADR’s real graph nodes

## Why

Winston Ecosystem View (WEV) Code plane filters ADRs / tickets / plans by cuboid using `owner_for()` in `ecosystem/ecosystem_view/bin/index_work`. It is a first-keyword scan (`data_manager`, `eodhd`, `parquet`, …). Plans such as `winston-v2-initial` can land on `dm` because the body mentions parquet. That makes the `dm` tablet lie about “work that touches this node.”

## Work

1. Prefer YAML / ticket **Graph nodes** / ADR title over full-body keyword order.
2. Allow multiple owners (show on each cuboid) **or** a primary + `also:` list — pick one; do not invent a fifth monolith.
3. Re-run `python3 ecosystem/ecosystem_view/bin/index_work` and spot-check `dm` vs `wv2` vs `ecosystem` tabs.
4. Keep UNKNOWN when nothing matches — do not default every leftover to `ecosystem` if the file is clearly a WUT lab plan.

## Not this ticket

- Live scan from inside the Wv2 container (docs are not mounted)
- Refresh hook — [`2026-09-09-wev-index-work-refresh-hook.md`](2026-09-09-wev-index-work-refresh-hook.md)
