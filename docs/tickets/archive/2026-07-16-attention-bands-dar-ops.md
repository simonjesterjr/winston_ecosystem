# Ticket: Attention bands in DAR + Wv2 (multi-Active is intentional)

**Status:** Done  
**Date:** 2026-07-16  
**Source:** Operator requirement clarification (session after `2026-07-16-1529`)  
**Domain:** ADR-006, `wv2-operational-portfolio-lifecycle`, CONTEXT **Active** / **DAR**  
**Supersedes:** `2026-07-16-dual-active-hygiene-ops.md` (wrong sole-focus framing)  
**Implemented:** 2026-07-16 — `Operations::AttentionBands` + DAR builders/renderers + ops shell/panels

## Requirement (canonical)

Wv2 may — and should — run **multiple Active Operational Portfolios** at once, paper and real.

| Band | Meaning | Soft capacity (operator norm) | Human attention |
|------|---------|-------------------------------|-----------------|
| **Inactive** | Archive / noise | many | Cleanup, remove, or later activate — not daily capital work |
| **Active + paper** | Strategies/markets too risky or under-researched; still execution hygiene | ~1–7 concurrent | Watch signals, paper fills, regime evidence |
| **Active + real** | Capital at risk; TS + non-correlated books + way forward | ~1–3 concurrent | Highest priority — fills, risk, stops, capital path |

**Not a defect:** having several Active paper OPs and a few Active real OPs.

**Still a defect:** two Active OPs with the same **seed_name** or identical **Books** without force (existing mutex).

**Product goal:** DAR and Wv2 make it **super clear** where the human’s attention needs to go — by band, not by “first Active id” focus hacks.

## Problem today

1. Ticket/session language treated multi-Active as smoke residue to collapse.  
2. DAR payload/PDF largely flattens **all Active** (and hard-codes “paper” in places).  
3. Ops shell “focus” defaults to lowest Active id when multiple Active exist — wrong model for multi-book attention.  
4. Inactive portfolio queue is not a first-class “hygiene appendix” surface.

## Scope (implementation)

### A. Docs (done with this ticket filing)

- [x] CONTEXT: **Active**, **DAR**, relationships (multi-Active + attention priority)  
- [x] Business-context lifecycle Active section  
- [x] ADR-006 attention hygiene  
- [x] Supersede sole-focus dual-Active ticket  

### B. DAR structure

1. [x] Summary page: counts by band — Active real / Active paper / inactive (optional count).  
2. [x] Chapter order: **Active real → Active paper**; never interleave without labels.  
3. [x] Section headers must show **execution_mode** (and Active) on every portfolio block.  
4. [x] Next steps / desk handoffs: group by band; real actions visually first.  
5. [x] Optional short **Inactive hygiene** appendix (names + ids only) — not full chapters unless operator expands later.  
6. [x] Soft capacity note when over norm (e.g. “8 Active paper — over ~7 norm”) — **warn only**; never block Daily Analysis or activate.  
7. [x] Remove misleading global “paper” footer/label when any Active real exists.

### C. Wv2 ops surfaces

1. [x] Ops home / shell: list Active split by paper vs real; no single “focus = min(id)”.  
2. [x] Status/list commands: band tags (`paper` / `real` + Active).  
3. [x] Positions view: section by band.  
4. [x] Desk handoffs: preserve band in phrases (e.g. real vs paper portfolio label).

### D. Out of scope (unless follow-on)

- Hard-blocking activate above 7 paper / 3 real — **explicitly rejected** for now (soft norms only).  
- Auto-deactivating “extras” after smokes.  
- Capital Activation feature work.  
- Closing inactive archive rows.

## Acceptance

- [x] Operator can keep multiple Active paper + Active real without any “hygiene” ticket telling them to deactivate  
- [x] DAR PDF/MD: real band before paper band; each chapter labeled paper|real  
- [x] DAR summary shows band counts  
- [x] Ops shell does not pretend there is a sole focus OP when many Active exist  
- [x] Soft over-capacity is advisory only (never blocks activate or Daily Analysis)  
- [x] Mutex tests still pass (same seed / same Books without force) — activation service unchanged; band module is advisory only

## Related code (starting points)

| Area | Path |
|------|------|
| DAR chapters | `winston_v2/app/services/daily_report_payload_builder.rb` |
| PDF | `winston_v2/app/services/daily_activity_report_pdf_renderer.rb` |
| MD | `winston_v2/app/services/daily_activity_report_markdown_renderer.rb` |
| Shell focus | `winston_v2/app/services/operations/ops_shell_chat.rb` (`sole_or_nil_active`) |
| Activate mutex | `winston_v2/app/services/operations/portfolio_activation_service.rb` |

## Decision (locked 2026-07-16)

**Soft norms only.** ~1–7 Active paper and ~1–3 Active real are the operator’s sense of how the book will evolve over the next ~2 months — planning/attention guidance, not product caps. DAR/ops may *note* over-norm counts; activate and Daily Analysis must **not** reject solely for count.

If hard caps are ever wanted, that is a **new** ticket with an explicit force-override story — not implied by these numbers.
