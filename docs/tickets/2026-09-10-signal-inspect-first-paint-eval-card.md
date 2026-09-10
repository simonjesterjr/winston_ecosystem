# Ticket: Browser-verify Signal Inspect first-paint Evaluation card

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-09-10  
**Monolith:** winston_v2  
**Mode:** contractor  
**Graph nodes:** winston_v2  
**Human gates:** none (read-only inspect)  
**DoD:** Hard-refresh of a live inspect page shows Evaluation in the right column on **first paint**, not only after a window resize  
**See:** session [`winston_v2/docs/session-reports/2026-09-10-1532-walnut-unit-risk-inspect-layout.md`](../../../winston_v2/docs/session-reports/2026-09-10-1532-walnut-unit-risk-inspect-layout.md); sibling [`2026-09-10-signal-inspect-focus-chart-browser-verify.md`](2026-09-10-signal-inspect-focus-chart-browser-verify.md)

---

## Problem

Signal Inspect Price · overlays used to paint at full width on first load and overlap the Evaluation card. A window resize called `Plotly.Plots.resize` and the grid looked correct.

Fix landed 2026-09-10: plot on `DOMContentLoaded` (page-local grid CSS sits below the script), `Plots.resize` after `newPlot`, chart cell `min-width: 0` + `overflow: hidden`. Verified in HTML/curl. **Not** visually verified as a cold first paint in a browser (no browser tools in that session).

## Work

1. Hard-refresh (bypass cache)  
   `https://sawtooth-ai.tail944ffb.ts.net/wv2/operations/signal_inspect?portfolio_id=1428&symbol=DBC`
2. **Do not** resize the window. Confirm Evaluation is a right-hand column, not under the candles.
3. Then resize once — layout must stay the two-column grid (no jump).
4. Repeat at a typical laptop width (~1400px) and after a full reload from Ops shell → inspect link.
5. If still overlapping: note screenshot + whether `DOMContentLoaded` ran before the inline `<style>` (move CSS above the Plotly script).

## Acceptance

- [ ] First paint: chart in left grid cell; Evaluation fully readable on the right
- [ ] Resize does not change column membership
- [ ] Focus chart still works (or defer remaining Focus checks to the sibling ticket)

## Out of scope

- Playwright CI
- Redesigning inspect chrome
- Focus-chart restyle matrix (sibling ticket)

## Origin

Wrap follow-up item 2 from session `2026-09-10-1532-walnut-unit-risk-inspect-layout.md`.
