# Ticket: Wv2 journals browse UI or remove dead route

**Status:** Proposed  
**Priority:** P2
**Date:** 2026-07-15  
**Series:** `journal-to-ledger` **#5**  
**Analysis:** [`docs/analysis/2026-07-15-winston-journal-vs-trading-ledger.md`](../analysis/2026-07-15-winston-journal-vs-trading-ledger.md)

## Problem

`winston_v2/config/routes.rb` declares:

```ruby
resources :journals, only: [:index, :show]
```

There is **no** `JournalsController` and no journal views. Desk operators hit a dead end if they try browser journal browse. Ops shell + MCP already cover inquiry; either wire a thin HTML surface or delete the route to avoid false accessibility claims.

## Scope (pick one path — recommend A if series #1–4 are in flight)

### Path A — Thin browse (preferred if ledger work continues)

1. `JournalsController#index` / `#show` (HTML, ops styling if possible).  
2. Index: filter by portfolio, status, date range; columns match ledger export subset.  
3. Show: single journal + linked position + task if any.  
4. Link from ops shell home panels when useful.  
5. Optional: “Export CSV” button calling series #4 exporter.

### Path B — Delete dead route

1. Remove `resources :journals` from routes.  
2. Document that journal inquiry is MCP / ops shell / internal only until a future UI ticket.  
3. Keep internal `GET /internal/journals/:id`.

## Non-goals

- Full Tradervue-style journal app  
- Editing executed journals in UI  
- Replacing ops shell confirm flow  

## Acceptance

- [ ] Either index/show return 200 with real data **or** route removed and analysis accessibility table updated  
- [ ] No silent 500 / missing constant for `/journals`  
- [ ] Internal/MCP paths unchanged  

## Depends on / unblocks

| Relation | Ticket |
|----------|--------|
| Optional after | #1 (richer columns on show) |
| Nice with | #4 export button |

## Related code

- `winston_v2/config/routes.rb`  
- `winston_v2/app/controllers/` (missing journals controller)  
- Ops shell panels  

## Discovery

Search: `journal-to-ledger`, analysis § Accessibility “dead route”, series ticket #5.  
