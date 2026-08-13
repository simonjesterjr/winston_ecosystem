# Ticket: Ops shell — Next steps / pending grouped by portfolio

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-08-12  
**Monolith:** winston_v2  
**Domain:** Ops shell (`/operations`), multi-Active desk  
**Related:** ADR-006 multi-Active bands; DAR Next Steps by portfolio; positions panel already groups by OP  

---

## Problem

Ops shell **Pending (human confirm)** is a **flat list** of tasks (band tag, task#, journal#, market, type) **without portfolio grouping**. With multiple Active OPs (paper + real bands), the operator cannot scan “what does Yellow need vs Mint?” the way **Positions (by band)** already groups lots under each OP.

Operator request: **Next steps should be by portfolio.**

---

## Desired outcome

1. Pending / next-step panel grouped **by attention band (REAL then PAPER)** then **by Operational Portfolio** (`#id` + display name), matching positions panel hierarchy.  
2. Within each OP: task rows as today (market, type, date, desk form, inspect, telegram phrase).  
3. Empty OPs with no pending items omitted (or single “none” under band).  
4. Panel refresh (`operations/panels` JSON + JS rebuild in `home/index.html.erb`) stays consistent with server partial `_panels.html.erb`.

---

## Acceptance

- [ ] With ≥2 Active OPs and pending tasks on more than one, pending panel shows distinct portfolio headers  
- [ ] Real band tasks appear above paper  
- [ ] First-paint ERB and JS `refreshPanels` both group (no flash of flat list only)  
- [ ] Request or service spec for `OpsShellPanels` pending payload shape if grouping is computed server-side (preferred)

## Non-goals

- Full desk workflow redesign  
- Telegram message layout  
- Auto-sorting tasks by ATR (stack-rank) beyond existing order

## Implementation hint

- `app/services/operations/ops_shell_panels.rb` — group `pending` like `positions` (`by_portfolio` real/paper)  
- `app/views/operations/home/_panels.html.erb` `#panel-pending`  
- `app/views/operations/home/index.html.erb` JS pending renderer  
