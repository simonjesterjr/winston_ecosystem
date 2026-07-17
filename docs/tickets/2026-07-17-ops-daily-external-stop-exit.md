# Ticket: External stop / discretionary exit packaging

**Status:** Done (2026-07-17)  
**Date:** 2026-07-17  
**Epic:** `2026-07-17-ops-daily-demo-epic.md`  

## Problem

Stops can hit outside Winston without a Winston exit signal. Ad-hoc `exit` covers fill, but lacks first-class reason packaging so DAR/journal hygiene doesn’t look like a miss.

## Scope

1. Ad-hoc exit accepts `reason=external_stop|discretionary|…` (notes + fulfillment_details).  
2. Optional ops shell / desk field.  
3. Document speech: “AMZN stopped out — book exit, no Winston signal.”  
4. Non-goal: broker stop sync.

## Acceptance

- [x] Exit journals carry machine-readable external-stop reason  
- [x] Operator path documented for Ops UI + Telegram  

## Delivered

| Surface | Detail |
|---------|--------|
| Service | `AdHocExitService` — `reason` / `exit_reason`; `fulfillment_details.exit_reason` + `winston_signal=false`; speech notes |
| Ops shell | `exit Blue AMZN price=252 reason=external_stop` |
| Desk form | Exit reason select |
| Internal API | `POST /internal/journals/exit` body `reason` |
| MCP | `wv2_exit_trade.reason` + external-stop `reply_text` |
| Docs | MCP interface §6b, `winston-ad-hoc-fill` skill |
| Specs | external_stop packaging, aliases, default ad_hoc, shell parse |

### Codes

`external_stop` · `discretionary` · `ad_hoc` (default) · `other`  
Aliases: `stopped_out`, `broker_stop`, `stop_hit`, `disc`, `desk`

## Related

- Ad-hoc exit Done: `2026-07-16-mcp-exit-trade-and-skill.md`  
- Epic: `2026-07-17-ops-daily-demo-epic.md`  
