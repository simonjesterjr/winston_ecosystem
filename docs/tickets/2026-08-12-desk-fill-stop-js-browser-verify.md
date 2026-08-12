# Ticket: Browser-verify desk fill-stop JavaScript

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-08-12  
**Monolith:** winston_v2  
**Domain:** Desk Workflow, desk confirm, ATR stop  
**See:** [`2026-08-12-1541-dar-risk-equity-desk-stop.md`](../session-reports/2026-08-12-1541-dar-risk-equity-desk-stop.md)

## Problem

Desk confirm now re-anchors the Winston ATR stop onto the actual fill (same stop distance, new entry) and shows **“adjusted using ATR to new stop level.”** Server-side confirm is spec-locked. The live form JavaScript (type fill → stop field + note) was only curl-checked for markup, not clicked in a browser.

## Scope

1. Open Desk Workflow (or classic desk) on a paper enter draft.
2. Leave the suggested stop; change fill away from expected entry.
3. Confirm: stop field updates live; note appears; booked `original_stop` / `updated_stop` match fill ± distance.
4. Second pass: type a custom stop after changing fill — JS must not overwrite (dirty flag).
5. Option-like fulfillment still skips ATR default.

## Suggested fixture

Draft journal **#523** MSFT, portfolio **#385**, task **#335** (as of wrap): expected 504.33, distance 30.5882, suggested stop 473.7418. Fill 510 → stop 479.4118 if suggestion left in place.

## Acceptance

- [ ] Operator (or agent with browser tools) exercises type-to-adjust on enter
- [ ] Human override kept
- [ ] Booked stop matches the adjusted (or overridden) field
- [ ] Any JS bug filed as an issue, not silently patched without a spec

## Related

- `winston_v2/app/views/operations/shared/_fill_stop_adjust_script.html.erb`
- `Operations::DeskContext.apply_fill_adjusted_stop`
- `Operations::StopSuggestion.stop_from_fill`
