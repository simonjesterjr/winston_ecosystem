# Ticket: Track host compose.yml + portfolio_configs outside monolith gits

**Status:** Proposed  
**Date:** 2026-07-14  
**Source:** session `2026-07-14-1112-paper-telegram-phase0-1.md`

## Problem

Phase 1 changed root `compose.yml` (Telegram `env_file`) and added `portfolio_configs/portfolio-blue-pbr62.json`. Neither lives in a monolith git repo (`ecosystem/`, `winston_v2/`, etc.). Easy to lose on another host or forget in wrap.

## Scope

1. Decide ownership: workspace meta-repo, ecosystem submodule note, or documented “host-local only” list.  
2. Document in `ecosystem/deployment/README.md` and/or `portfolio_configs/README.md`.  
3. Optional: commit compose under a thin workspace git if operator wants.

## Acceptance

- [ ] Written policy for what is git vs host-local  
- [ ] Phase 1 compose + blue-pbr62 config covered by that policy  

## Related

- `ecosystem/deployment/README.md`  
- Paper Phase 1 wrap  
