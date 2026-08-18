# Ticket: Commit leftover Wv2 signal-inspect legend sheet

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-08-18  
**Related:** `winston_v2/docs/session-reports/2026-08-18-0932-signal-inspect-legend-sheet.md`

## Problem

A separate session delivered the Signal inspect external legend sheet (hide in-chart Plotly legend; **Legend · N** slide-up / drawer). Those files were still dirty on `winston_v2` `main` when the after-close EOD wrap ran and were **intentionally not committed** there.

Unstaged at wrap time:

- `app/views/operations/signal_inspect/show.html.erb`
- `spec/requests/operations_signal_inspect_spec.rb`
- `docs/session-reports/2026-08-18-0932-signal-inspect-legend-sheet.md`

## Acceptance

- [ ] Review the leftover diff against the 09:32 session report
- [ ] Commit/push on `winston_v2` `main` as its own commit (not mixed with EOD session-contract)
- [ ] Request spec still asserts sheet mount, open button, `showlegend: false`
