# Ticket: Capital Activation (MCP / Telegram)

**Status:** Proposed (Phase 3 follow-on — after ADR-006 minimum)  
**Priority:** P1  

**Date:** 2026-07-09 (grill refresh 2026-07-20)  

**Context:** ADR-006 + Capital Activation grill 2026-07-20. Session [`2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill`](../session-reports/2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill.md).  
**Unblocked by:** Phase 3 PR 1–3 (schema, import lineage, Active mutex) — done.

## Problem

Paper→real must open a **new** OP series with stated capital — not rewrite paper equity. Telegram “Activate” is overloaded with the Active attention flag.

## Speech (grill 2026-07-20)

Prefer: **“Make Portfolio Red + Ts10 real with initial capital $X”** or **“make \<fingerprint\> real with initial capital $X”**.  
Do not use “Activate … with capital” in skills.

## Scope

### A. Capital Activation (new real series)

1. Domain service from existing Wv2 unit (OP id / seed+TS / fingerprint short or full) + initial capital $X.  
2. Prerequisites: source OP (Books) and TS in Wv2; else hard error “import from WUT first” (no transfer wizard).  
3. Defaults: new OP `execution_mode=real`, Active true, **same methodology fingerprint**, CashEvent = $X only.  
4. Paper A: not auto-**Closed**; journals unchanged; **default auto-deactivate** paper A (same seed/Books).  
5. Dual Active same seed/Books → `force` / `keep_paper_active`.  
6. Non-trade_ready / observation: **warn** in `reply_text` / warnings[] — **do not hard-block**.  
7. MCP tool + Cromwell skill; rake smoke.  
8. Clear errors distinguishing set-**Active** vs **Capital Activation**.  
9. Never invent `$X` or fingerprint; ask once if capital missing.

### B. CashEvent top-up (same ticket — no separate ticket)

Telegram: “**Add $5000 to [fingerprint]**” / “We are adding $5000 to …”  
→ **Not** Capital Activation — existing `wv2_add_cash_event` / `CashEventService`.

10. Enforce top-up **only** on **Active + real** OPs; refuse paper / inactive / closed with clear error.  
11. Resolve fingerprint among Active real only; ask if multiple.  
12. Skills distinguish **make real** vs **add to** (never route add → CA).  
13. Specs: paper top-up refused; Active real inflow ok.

## Acceptance

**Capital Activation**

- [ ] New OP capital_base starts at $X independent of paper terminal equity  
- [ ] Same fingerprint on real OP as source unit  
- [ ] Paper series journals unchanged; paper not Closed; paper deactivated by default  
- [ ] Force only for dual Active (keep paper Active), not for observation provenance  
- [ ] Observation/trade_ready gap → warning still **status ok**  
- [ ] Missing Red/TS → import error, not multi-step workflow  

**CashEvent top-up (folded in)**

- [ ] `CashEventService` / MCP refuse paper and inactive  
- [ ] Active real inflow succeeds; capital_base updates  
- [ ] Fingerprint resolution Active-real-only; ambiguous → ask/error  
- [ ] Skills/docs: make real vs add to  

**Shared**

- [ ] Lifecycle / MCP interface / Cromwell skills updated  

## Grill notes

- Fingerprint = methodology, not paper-vs-real (option A).  
- Dual-Active hygiene default deactivate paper (option A).  
- Trade-ready: soft warn only (option C) — capital hygiene is human.  
- Add $X to fingerprint = CashEvent top-up, not CA; **Active real only** (folded into this ticket).

## Related

- `wv2-operational-portfolio-lifecycle.md`
- Active mutex: `2026-07-09-wv2-active-mutex-seed-books.md`
- export_kind: `2026-07-08-wv2-importer-honor-export-kind.md`
- MCP: `wv2_add_cash_event` in `interfaces/winston-mcp-tools.md`
- Still open after ops demo epic 0–7: `docs/session-reports/2026-07-18-1024-ops-demo-5-7-related-draft-equity.md`
