# Ticket: DAR Next Steps table truncates portfolio names to “Portfolio”

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-08-12  
**Monolith:** winston_v2  
**Domain:** Daily Activity Report (DAR), PDF / markdown summary  
**Related:** risk-equity DAR workstream; multi-Active real/paper bands  

---

## Problem

On the DAR **Next Steps** summary table (PDF column **Portfolio**, and any consumer that reuses the same clip), every row shows a truncated label that collapses to **`Portfolio`** (or `Portfolio…`) so the operator cannot tell which OP owns the task.

**Root cause (verified):** `DailyActivityReportPdfRenderer#draw_summary_actions` builds the Portfolio column with:

```ruby
clip(st[:portfolio], 10)
```

Chapter names are typically `Portfolio Blue`, `Portfolio Yellow · a1b2c3d4`, etc. **10 characters** cuts after `Portfolio` / `Portfolio ` and drops the color and fingerprint.

Markdown uses the unclipped `st[:portfolio]` string, so PDF is the main offender; still fix both for a single display helper.

---

## Desired outcome

Next Steps (and Desk Handoffs if they clip the same way) show a **disambiguating portfolio label**, e.g.:

- `#385 Yellow · a1b2c3d4` preferred when id is available  
- or `Yellow · a1b2c3d4` / `Blue` without the redundant “Portfolio ” prefix  
- Clip length ≥ 22–28 if a short form is required for table width

Use `portfolio_id` already on step rows (`handoff_step_row` sets `portfolio_id`) when present.

---

## Acceptance

- [ ] PDF Next Steps Portfolio column distinguishes ≥2 Active OPs that share the “Portfolio …” name prefix  
- [ ] Markdown Next Steps still readable; optional short-form helper shared with PDF  
- [ ] Spec covering clip/label helper with multi-OP fixtures  
- [ ] No change to task ordering (real then paper)

## Non-goals

- Redesign of full DAR layout  
- Telegram copy rewrite (can reuse helper later)

## Implementation hint

- `winston_v2/app/services/daily_activity_report_pdf_renderer.rb` (~line 189 `clip(st[:portfolio], 10)`)  
- `daily_report_payload_builder.rb` `next_steps` / `handoff_step_row` (add `portfolio_label` or seed+fp)  
- Reuse / extend `portfolio_title` pattern from markdown renderer
