# Ticket: WUT operations journal schema alignment

**Status:** Proposed  
**Priority:** P2
**Date:** 2026-07-15  
**Series:** `journal-to-ledger` **#6** (parallel hygiene)  
**Analysis:** [`docs/analysis/2026-07-15-winston-journal-vs-trading-ledger.md`](../analysis/2026-07-15-winston-journal-vs-trading-ledger.md)

## Problem

WUT **lab** journals (`run_id`, flow, MTM, expected_return) match `schema.rb`.  
WUT **Operations** path (`Operations::TaskGenerator`, `Operations::TasksController#accept_journal`) writes fields that are **not** on `journals` in schema:

- `status` (`draft` / `executed`)  
- `execution_price`, `execution_volume`, `executed_at`  
- `active_account_id`, `bar_date` (used at create)

Model also `belongs_to :active_account, optional: true` without a matching column in schema. Live ops SoT is **Wv2**; this drift confuses anyone who treats WUT Operations as a parallel ledger and can cause silent failures if ops is run against a strict DB.

## Scope (WUT)

**Choose explicitly and document in ticket closeout:**

### Option A — Align schema to ops (if WUT Operations remains supported)

1. Migration(s) adding missing columns with safe defaults.  
2. Specs for draft create + accept_journal.  
3. Note in WUT AGENTS/docs: ops is lab/paper parallel; Wv2 is operational.

### Option B — Retire ops write path (if abandoned)

1. Mark Operations daily/task journal writes as deprecated or guard behind flag.  
2. Remove or no-op fields that don’t exist.  
3. Keep backtest journals + `export_journal` as primary WUT journal surface.  
4. Point operators to Wv2 for live/paper engagement journals.

**Recommendation from analysis:** prefer **B** if no one runs WUT Operations daily; prefer **A** only if paper ops in WUT is still intentional. Do not re-home the live ledger in WUT.

## Non-goals

- Implementing full journal→ledger series in WUT  
- Changing backtest PositionManager journal semantics  
- Porting MCP confirm tools to WUT  

## Acceptance

- [ ] Documented decision A or B  
- [ ] No ops code path that assumes non-existent columns without migration **or** code removed  
- [ ] `db:schema:load` + relevant specs green  
- [ ] Analysis WUT section updated one line when done  

## Depends on / unblocks

| Relation | Ticket |
|----------|--------|
| Parallel | Entire series; does not block #1–#5 |
| Clarity | Prevents wrong monolith for ledger work |

## Related code

- `winston_unit_test/db/schema.rb` `journals`  
- `winston_unit_test/app/services/operations/task_generator.rb`  
- `winston_unit_test/app/controllers/operations/tasks_controller.rb`  
- `winston_unit_test/app/models/journal.rb`  
- `winston_unit_test/docs/operations_flow.md`  

## Discovery

Search: `journal-to-ledger`, analysis § WUT schema drift, series ticket #6.  
