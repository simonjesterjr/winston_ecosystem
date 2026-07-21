# Ticket: Portfolio `id_or_name` — fingerprint / short-fp resolution + multi-match error

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-21  
**Domain:** Wv2 internal API, MCP  
**Glossary:** fingerprint, Operational Portfolio, seed_name

## Problem

`InternalController#find_portfolio_by_id_or_name` today:

- digit string → `Portfolio.find_by(id:)`  
- else → exact `name` then `name ILIKE %s%` **`.first`**

Short fingerprint `9cf64e64` can match multiple OPs that embed the suffix in `name`. `.first` is silent and may activate the wrong twin. Full fingerprint on `portfolios.fingerprint` is not consulted.

## Scope (Wv2)

1. Resolution order proposal:
   - numeric id  
   - exact name  
   - exact full fingerprint (64 hex)  
   - unique short fingerprint prefix (8+ hex) when exactly one match  
   - unique case-insensitive name substring only when exactly one match  
2. On multi-match: **422** with `code: ambiguous_portfolio` and candidate `{id, name, fingerprint_short, active}[]`.  
3. Mirror behavior for MCP tools that map `id_or_name` / `portfolio_id_or_name`.  
4. Specs for twin Blue #240/#241 style fixtures.

## Non-goals

- Changing Active mutex rules  
- Auto-mergeing duplicate OPs  

## Acceptance

- [ ] `id_or_name=9cf64e64` with two name matches returns ambiguous error, not silent first  
- [ ] Full fingerprint uniquely resolves when stored on OP  
- [ ] Numeric id still preferred and documented  
- [ ] MCP activate/deactivate/close surfaces the same ambiguity payload  

## Related

- Session: `docs/session-reports/2026-07-21-0927-wut80-transfer-activate-recovery.md`  
- Code: `winston_v2/app/controllers/internal_controller.rb` (`find_portfolio_by_id_or_name`)  
- MCP: `ecosystem/ai/mcp/mcp_winston/server.py` (`_portfolio_id_payload`)  
- Sibling ops: `2026-07-21-blue-241-successor-cleanup.md`  
