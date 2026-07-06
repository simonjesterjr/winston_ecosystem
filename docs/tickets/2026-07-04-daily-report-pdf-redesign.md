# Ticket: Redesign Wv2 daily activity report PDF layout

**Status:** Proposed
**Context:** Task 7 in `winston-mcp-next-steps.md.tasks.json` delivered basic PDF generation (`DailyActivityReportPdfRenderer`) and stable report links. Layout polish and stakeholder-ready design were discussed in session only (2026-07 Cromwell/Telegram work).

## Problem

The current one-page PDF (`storage/reports/wv2_YYYYMMDD.pdf`) is functional but not presentation-quality. Telegram inline summary (Cromwell LLM) and the PDF should tell the same story; the PDF is the durable artifact principals may forward or archive.

## Goal

Redesign `winston_v2/app/services/daily_activity_report_pdf_renderer.rb` for clarity, scanability, and brand-consistent tables — without changing the underlying report JSON schema.

## Acceptance criteria

- [ ] Design brief captured (section outline, typography, table columns) — reference `wv2_20260617.pdf` or mock
- [ ] PDF renders from existing `storage/cromwell_notifications/wv2_YYYYMMDD.json` payload
- [ ] MT display boundaries use `TimeZoneConverter` (UTC in DB; MT at display only)
- [ ] Graceful fallback unchanged: JSON report still works if Prawn fails
- [ ] Cromwell `telegram_media_path` / MCP `wv2_get_daily_activity_report_pdf` unchanged contract
- [ ] Smoke: generate PDF for a known date in compose and attach via Cromwell delivery path

## Out of scope

- Changing daily analysis logic or notification payload shape
- HTML report variant (unless explicitly added as follow-on ticket)

## Related

- `winston_v2/app/services/daily_activity_report_pdf_renderer.rb`
- `winston_v2/app/services/daily_report_schedule.rb` — 4:30 PM MT analysis gate
- `ecosystem/plans/winston-mcp-next-steps.md.tasks.json` — task 7 (basic PDF, completed)
- Session context: Cromwell auto-delivery in `openclawd-stack/nanobot/nanobot/agent/loop.py`