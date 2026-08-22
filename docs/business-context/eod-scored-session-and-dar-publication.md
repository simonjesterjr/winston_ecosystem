# EOD Scored Session and DAR Publication

**Type:** Domain rule (authoritative for ecosystem)
**Related ADR:** ADR-012
**Related:** ADR-003, ADR-009; `data-invariant-and-derivatives.md`; `daily-analysis-phase1-design.md`

## What a trading day owes the desk

On every New York equity **session** (Monday–Friday, including Friday):

1. **data_manager (DM)** pulls End of Day (EOD) bars through that completed session for Active Trend Following (TF) books.
2. **Winston v2 (Wv2) Daily Analysis** evaluates those books against the **exact session bar**.
3. Only then is a **Daily Activity Report (DAR)** a document of the day.

Preferred clocks (America/Denver): DM **15:30**, Daily Analysis / DAR **16:30**. Those are preferences. The operator will wait up to **~30 minutes** (hard wait budget **17:00 MT**) for prints or evaluation. A DAR that says there are no next actions when recipes would have produced next actions is worse than lateness.

## Scored Session vs Not Scored vs Hold

| Label | Meaning | Desk reading |
|-------|---------|--------------|
| **Scored Session** | Active TF Operational Portfolios (OPs) were evaluated on that session’s exact bars | Next steps or a true **hold** |
| **Hold** | Scored, and the recipes + heat/capacity produced no actionable items | Quiet day — believe it |
| **Not Scored** | Evaluation did not run (typical: `missing_data` — no exact session bar) | **Not** a quiet day. Do not confirm, do not skip Monday |

Skip reasons that are methodology (`no_strategy`, `quiver_tracking_book`, `closed`) are not this rule. This rule is about **session bars that should have been there**.

## Chain

```
NY session complete
  → DM acquire through CompletedNySession
  → exact session bar on every Active TF Book
  → Daily Analysis (signals → draft journals → tasks)
  → DAR (human document) + Telegram of a scored day
```

If the 15:30 pull does not yet have the End of Day Historical Data (EODHD) print, DM retries until the session is on parquet or **17:00 MT**. Wv2 Daily Analysis at 16:30 **waits** on that readiness rather than skipping every OP and writing hold.

Quiver Tracking and other non-TF recipes are excluded from the gate. Inactive OPs do not block.

## Force majeure

Vendor outage, holiday-with-no-print, or bars still missing at 17:00 MT:

- Do **not** publish hold.
- Record **Not Scored** (missing symbols).
- When bars later arrive (including Saturday 08:00 weekend sync), run **catch-up Daily Analysis** for that session date.
- Catch-up **mints tasks onto the current desk**. Fill Date remains next session after Signal Date (Friday signal → Monday fill).
- Catch-up does **not** require a new DAR for the missed date. Do not auto-replace a false hold PDF.

## Report date

The production report date is a **New York session date**, never Saturday or Sunday. Saturday morning still “owes” Friday until Monday’s session is the live production date after Monday 16:30 MT.

## Edge cases (locked)

| Case | Rule |
|------|------|
| One thin symbol missing in one Active TF OP | Wait for **all** Active TF books; do not publish a mixed scored/skipped day as success |
| True 0-signal day after scoring | Hold is valid |
| Early NY close | Same chain; 15:30 MT is after close |
| Weekday holiday, no print | Not Scored (no holiday calendar in v1); catch-up if a bar later appears |
| Weekend | No Saturday/Sunday report date; Friday remains the session until Monday EOD |
| Catch-up Telegram | Do not send a second full DAR PDF for the missed date. Tasks on the current desk are the operator surface |
| M–Th 15:30 already has the print | No retry; 16:30 scores immediately (today’s usual path) |

## What this is not

- Not permission to auto-fill Positions (ADR-009 Human-Gated).
- Not a change to exact-bar readiness (a prior close is not “today”).
- Not a requirement that Quiver Tracking wait on Daily Analysis.
