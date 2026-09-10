# Ticket: Browser-verify Signal Inspect Focus chart

**Status:** Proposed
**Priority:** P3
**Date:** 2026-09-10
**Mode:** contractor
**Graph nodes:** winston_v2
**Edges:** `winston_v2/app/views/operations/signal_inspect/show.html.erb` (`bindChartFocus`)
**Human gates:** none (read-only inspect)
**DoD:** Operator (or agent with a browser) has clicked Focus chart end-to-end on a live inspect page
**Origin:** session `docs/session-reports/2026-09-10-1355-signal-inspect-market-insights.md`

## Problem

Signal Inspect gained **Focus chart**: hide surrounding cards, keep candles + Average True Range (ATR) + Moving Average Convergence Divergence (MACD), Escape to leave. The 2026-09-10 inspect session verified the page over HTTP (button present, `keepInFocus` on traces, CSS `.is-focus`). It did **not** click the control in a browser, so Plotly restyle, resize, Escape vs legend sheet, and mobile layout are unverified.

## Work

1. Open a live inspect with MACD pane, e.g. GOOGL portfolio 11 as_of 2026-09-09.
2. Click **Focus chart**. Confirm eval / market / holdings / bars / insights hide; chart grows; only OHLC + ATR + MACD remain (entry/stop/breakout lines off).
3. Escape exits focus (legend sheet open first should close legend, not focus).
4. Exit via the button as well. Confirm traces/shapes return.
5. Repeat at a narrow viewport if convenient.
6. Note any restyle bugs on the ticket; fix if small, else spawn an issue.

## Acceptance

- [ ] Focus on: surrounding cards gone; candles + ATR + MACD visible.
- [ ] Focus off (button and Escape): layout and overlays restored.
- [ ] Legend Escape does not steal focus-exit when the sheet is closed.
- [ ] Result noted here or in a short session-report line.

## Out of scope

- Redesigning the inspect chrome
- Playwright CI (manual / one browser pass is enough)

## Related

- `winston_v2/app/views/operations/signal_inspect/show.html.erb` (`bindChartFocus`, `.ops-inspect.is-focus`)
- URL: `https://sawtooth-ai.tail944ffb.ts.net/wv2/operations/signal_inspect?as_of=2026-09-09&portfolio_id=11&symbol=GOOGL&window=90`
