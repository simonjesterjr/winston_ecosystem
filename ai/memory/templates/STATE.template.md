# Daily loop STATE — {{DATE}}

loop_status: complete | skip | partial
skip_reason: none | not_trading_day | dar_missing | mcp_error | coverage_stale
as_of: {{DATE}}
written_at_mt:

## Active Operational Portfolios
- #id name · mode · attention

## DAR
status: ok | missing | error
date:
notes:

## Signals (from payload only)
taken:
passed:

## Pending
count: 0
- journal_id · OP · symbol · type · fill_date

## Verifier (advisory — human still confirms)
- journal_id · TAKE|SIZE_DOWN|SKIP|HOLD · one-line reason

## Errors / open questions
- none
