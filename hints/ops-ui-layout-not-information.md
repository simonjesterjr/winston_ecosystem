# Ops UI: layout vs information

When an operator says a Winston v2 (Wv2) ops-shell page (Desk Workflow, classic desk, Pending **desk form**, live book) is bad on a phone, that is a **layout** problem until they say the **information** is wrong or too much.

**Do:** reflow. Form first, sticky submit, 44px / 16px inputs, tables as stacked cards, two columns on desktop. Keep proposed units, Average True Range (ATR), lots, ledger, packaging, broker evidence **visible**.

**Do not:** hide that book behind closed `<details>` / “mobile-first” folds. CSS cannot force a closed `<details>` open on desktop (`display: block` on the body does not win). The 2026-09-11 phone-first Desk Workflow pass did that; the operator had to ask to put the fields back.

Closed disclosures are only for true progressive disclosure the operator asked for, or for empty optional chrome — not for the live book they confirm against.

See: `winston_v2/docs/session-reports/2026-09-11-1358-desk-workflow-mobile.md`, `winston_v2/docs/session-reports/2026-09-11-2054-desk-form-information.md`.
