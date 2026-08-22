# ADR-012: Scored-Session DAR Publication Gate

**Status:** Accepted
**Date:** 2026-08-22
**Deciders:** Operator (session 2026-08-22) + Architecture
**Builds on:** ADR-003, ADR-009
**Domain context:** `docs/business-context/eod-scored-session-and-dar-publication.md`
**Glossary:** `CONTEXT.md` — Scored Session, Not Scored, Daily Analysis, Daily Activity Report, Hold

## Context

Preferred End of Day (EOD) times are data_manager (DM) at 15:30 America/Denver and Winston v2 (Wv2) Daily Analysis + Daily Activity Report (DAR) at 16:30 America/Denver. Those times are **preferences**, not a license to publish an empty desk.

On Friday 2026-08-21 the 16:30 Daily Analysis ran while parquet still lacked Friday session bars. Every Active Trend Following Operational Portfolio skipped `missing_data`. The DAR said **hold / 0 next actions** and Telegram posted it. Saturday 08:00 DM weekend sync then wrote Friday bars. No second analysis ran. A read-only re-scan found 15 recipe fires that never became desk tasks.

A DAR that says “no next actions” when the session was **never scored** is worse than a report that is up to ~30 minutes late. Monday–Thursday the 15:30 pull usually has the print; Friday End of Day Historical Data (EODHD) lag is the demonstrated miss.

Alternatives considered:

- **A. Keep clock-fire DAR; skip is honest enough** — operator still reads skip-as-hold; Telegram teaches “quiet day”
- **B. Always wait overnight / weekend job** — punts Friday desk to Saturday; M–Th already works at EOD
- **C. Gate DAR on a Scored Session; wait on DM; catch-up mints tasks without rewriting a false hold** — punctuality yields to desk truth

## Decision

We choose **C**.

1. **Honesty over punctuality.** Prefer DM 15:30 MT and Daily Analysis / DAR 16:30 MT. Waiting up to ~30 minutes past 16:30 (deadline **17:00 America/Denver**) is acceptable. Publishing **hold** for an unscored session is not.
2. **Chain:** completed New York session bars on every Active Trend Following book → Daily Analysis evaluates → DAR is written. DAR is the document of a **Scored Session**, not a clock tick.
3. **Friday is a trading day.** Same contract as Monday–Thursday. Weekend sync is a backstop, not the Friday EOD path.
4. **Hold means scored-and-empty.** `_No actionable items — hold._` is allowed only after Active Trend Following books were evaluated against that session’s exact bars. `missing_data` skips are **Not Scored**.
5. **Force majeure:** if bars are still missing at 17:00 MT, do **not** emit a hold DAR. Record **Not Scored**. When bars later arrive, **catch-up Daily Analysis** mints tasks onto the **current desk**. Do not silently replace a published DAR; do not require a new DAR for the missed date.
6. **Quiver Tracking / copy-book recipes** do not participate in this gate (they are not Daily Analysis). Inactive Operational Portfolios do not block.
7. **Report date is a New York session date**, never Saturday/Sunday.

## Rationale

- The operator acts on next steps. A false hold is a missed Monday fill window.
- M–Th already shows the contract is achievable most days; the gap is “publish anyway when EODHD is late,” especially Friday.
- Catch-up onto the live desk preserves Signal Date T / Fill Date T+1 without a second Telegram DAR that looks like a new day.

## Consequences

### Positive

- Desk next steps exist if the recipes fired, even when EODHD lagged
- Telegram / PDF cannot teach a quiet day that was never scored
- Weekend backstop still heals Friday prints and can enqueue catch-up

### Negative

- DAR may land as late as ~17:00 MT
- A Not Scored evening has no hold PDF; operator must read the not-scored record or wait for catch-up tasks
- Catch-up does not rewrite the original DAR (tasks appear on the current as_of desk)

### Risks mitigated

- False hold → publication gate
- Friday-only miss → same trading-day contract + DM retry until deadline
- Late parquet after DAR already posted → mint-only catch-up, no second DAR
