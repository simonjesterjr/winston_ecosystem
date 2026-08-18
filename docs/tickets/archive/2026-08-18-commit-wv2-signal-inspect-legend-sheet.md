# Ticket: Commit leftover Wv2 signal-inspect legend sheet

**Status:** Done  
**Priority:** P3  
**Date:** 2026-08-18  
**Related:** `winston_v2/docs/session-reports/2026-08-18-0932-signal-inspect-legend-sheet.md`; Wv2 `2d86e7a`

## Problem

A separate session delivered the Signal inspect external legend sheet (hide in-chart Plotly legend; **Legend · N** slide-up / drawer). Those files were still dirty on `winston_v2` `main` when the after-close EOD wrap ran and were **intentionally not committed** there.

Unstaged at wrap time:

- `app/views/operations/signal_inspect/show.html.erb`
- `spec/requests/operations_signal_inspect_spec.rb`
- `docs/session-reports/2026-08-18-0932-signal-inspect-legend-sheet.md`

## Acceptance

- [x] Review the leftover diff against the 09:32 session report
- [x] Commit/push on `winston_v2` `main` as its own commit (not mixed with EOD session-contract)
- [x] Request spec still asserts sheet mount, open button, `showlegend: false`

Closed by Winston v2 (Wv2) wrap: `2d86e7a` feat(ops): move Signal inspect legend into a slide sheet. Follow-ups filed on Wv2:

- `winston_v2/docs/tickets/2026-08-18-signal-inspect-legend-chip-strip.md`
- `winston_v2/docs/tickets/2026-08-18-signal-inspect-legend-phone-smoke.md`
