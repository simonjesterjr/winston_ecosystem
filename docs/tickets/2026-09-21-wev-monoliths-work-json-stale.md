# Ticket: WEV Monoliths backlog serving stale work.json

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-09-21  
**Lane:** B (hotfix / ops hygiene)  
**Program:** Winston Ecosystem View  
**Parent:** [`2026-09-07-winston-ecosystem-view.md`](2026-09-07-winston-ecosystem-view.md)  
**Implements via:** [`2026-09-09-wev-index-work-refresh-hook.md`](2026-09-09-wev-index-work-refresh-hook.md)  
**Graph nodes:** winston_v2, ecosystem  
**Implementer:** Chief of Staff (regen now) → Grok CLI for wrap hook (shared session)  
**DoD:** Operator hard-refresh sees current INDEX tickets; regen documented; refresh-hook ticket advanced  

## Symptom

https://sawtooth-ai.tail944ffb.ts.net/wv2/operations/ecosystem — Monoliths → open tickets / issues (and likely ADR/plan tabs) looked frozen: old Proposed rows, Done tickets still open-looking, no 2026-09-21 tickets.

## Root cause

Code/Monoliths plane fetches static `GET …/ecosystem/work.json` (copied into Wv2 public). `ecosystem/docs` is **not** mounted in the container, so Rails cannot scan markdown live. Catalog is produced by:

```bash
python3 ecosystem/ecosystem_view/bin/index_work
```

Last successful regen before this ticket: **2026-09-08**. Tickets are INDEX-driven; archived Done rows drop out of open once INDEX no longer lists them **and** `work.json` is regenerated.

## Immediate mitigation (done 2026-09-22)

Regenerated both:
- `ecosystem/ecosystem_view/catalog/work.json`
- `winston_v2/public/ecosystem/work.json`

## System One checkpoints

1. `generated_at` on `work.json` ≥ 2026-09-22  
2. Open backlog includes probe-before-promote + packaging M-band  
3. Open backlog does **not** include archived stale-parquet as Proposed  
4. Hard refresh Tailscale `/wv2/operations/ecosystem` Monoliths tab confirms (1)–(3)

## Remaining (Lane B → CLI)

Finish [`2026-09-09-wev-index-work-refresh-hook.md`](2026-09-09-wev-index-work-refresh-hook.md): README + wrap note; optional `/wrap` hook when docs change. Do **not** mount all of `ecosystem/docs` into Wv2.

## CLI seed

```
cwd: /home/johnkoisch/Documents/com/sawtooth
Lane B. Finish WEV work.json refresh hygiene per
ecosystem/docs/tickets/2026-09-09-wev-index-work-refresh-hook.md
and 2026-09-21-wev-monoliths-work-json-stale.md.
Add README + wrap/ship one-liner for: python3 ecosystem/ecosystem_view/bin/index_work
Optional: call indexer from /wrap when docs/adr|tickets|issues or plans changed.
Do not mount ecosystem/docs into Wv2. Push main. In-band wrap.
System One: regen; confirm generated_at fresh; Monoliths shows INDEX-current open set.
```
