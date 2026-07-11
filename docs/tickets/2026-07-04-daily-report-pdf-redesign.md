# Ticket: Redesign Wv2 daily activity report PDF layout

**Status:** In progress → largely delivered (2026-07-10 multi-page expert package)

**Context:** Task 7 delivered basic PDF. 2026-07-10 plan expands to multi-page expert reports with equity graphs, markdown archive, and Telegram Sawtooth Main delivery.

## Problem

The original one-page PDF was dense lists only — no per-portfolio pages, no equity graphs, no markdown archive, weak phone usability.

## Goal

Expert, phone-openable **report package**:

- Markdown + multi-page PDF (1 summary + 1 page per Active portfolio)
- Equity curves from initial capital; exposure charts
- Next steps global + per portfolio
- Final PDF sent to **Sawtooth Main** Telegram channel

## Acceptance criteria

- [x] Multi-page PDF: summary + one page per portfolio
- [x] Equity series + Prawn charts
- [x] Markdown archive under `storage/reports/wv2_YYYYMMDD.md`
- [x] Manifest includes md/pdf/json + telegram_channel
- [x] `TelegramReportDelivery` → Sawtooth Main (`-1003884714483`)
- [x] Additive payload `portfolio_chapters` / `next_steps` (schema v1.2)
- [ ] Compose smoke: 2021-03-17 Red/Orange/Blue package + Telegram confirm
- [x] Backup plan inventories report paths as P2

## Related

- `winston_v2/app/services/daily_activity_report_pdf_renderer.rb`
- `winston_v2/app/services/daily_activity_report_markdown_renderer.rb`
- `winston_v2/app/services/telegram_report_delivery.rb`
- `ecosystem/interfaces/cromwell-notification-v1.md` v1.2
- `ecosystem/plans/operational-data-backup-dr.md`