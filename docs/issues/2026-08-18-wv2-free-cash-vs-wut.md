---
id: ISSUE-20260818-wv2-free-cash-vs-wut
title: Wv2 free cash vs WUT — executed ledger matches; drafts still unsigned
status: ready
type: investigation
priority: medium
created: 2026-08-18
updated: 2026-08-18
labels: [winston_v2, winston_unit_test, free-cash, journal-flow]
related:
  - docs/issues/2026-08-17-wv2-short-flow-breaks-wut-equity.md
  - docs/tickets/2026-08-17-wv2-equity-wut-parity-flow-dar-shell.md
  - winston_v2/docs/tickets/2026-08-18-dar-draft-journal-unsigned-flow.md
---

# Wv2 free cash vs WUT — executed ledger matches; drafts still unsigned

**Status banner (human-readable):** Under investigation complete — executed cash is WUT-aligned; remaining defect is Daily Analysis draft `flow` / `debit_credit`

Map YAML `status` ↔ banner: `ready`.

## Summary

Operator asked whether Winston v2 (Wv2) free cash matches Winston Unit Test (WUT). Live sawtooth Active Operational Portfolios (OPs), as of 2026-08-18, reconstruct **exactly** from CashEvents + executed journal flows using WUT stock/proxy signs. `cash_vs_pnl_delta` is $0 on all seven Active books. Daily Analysis **drafts** still store unsigned `|units × price|` with `debit_credit` by signal type (enter → debit), which is not the WUT journal contract and can mislead the Flow column; confirm enter/pyramid recomputes `signed_flow`, so those drafts do **not** currently move executed free cash.

Primary classification: **executed path — not a candidate defect** (matches WUT after 2026-08-17 backfill). **Draft producer — candidate defect** (presentation / pre-confirm).

## Comparison contract

- **Governing requirement:** WUT Portfolio Backtest Run (PBR) cash ledger — `CASH_EQUITY_VERIFICATION.md`; `PortfolioPositionManager#update_cash_on_entry/exit`; `PositionManager` journal signs.
- **Shared input / time:** sawtooth paper Active OPs; as_of 2026-08-18; no real-capital mutation.
- **Baseline:** WUT identity `free_cash = initial + signed notionals` (long enter −, short enter +, option enter −premium).
- **Candidate:** Wv2 `Portfolio#capital_base` = `Σ CashEvents(event_date ≤ as_of) + Σ executed Journal.flow(trade_date ≤ as_of)`.

| Field | Baseline (WUT) | Candidate (Wv2 executed) | Contract |
|---|---|---|---|
| Long enter | −units×price, debit | −units×price, debit | same |
| Short enter | +units×price, credit | +units×price, credit (live samples) | same after `cd37a1f` |
| Long/short exit | opposite of enter | confirm `signed_flow` side:exit | same |
| Option/LEAP enter | −premium×mult | `signed_flow` option-like always purchase | same (no live option lots in this capture) |
| Equity | cash + long MV − short MV | `RiskEquity` same identity | same |
| Draft enter flow | signed | unsigned positive + type-based debit | **differs** |

Do not compare Wv2 free cash to WUT **sizing** `capital_base` (initial + realized PnL, single-market profit-only). Those are different numbers.

## Target comparison (live sawtooth 2026-08-18)

| OP | A UI / `capital_base` | C reconstruct `initial + Σ executed flow` | A−C | `cash_vs_pnl_delta` | Risk equity |
|---|---:|---:|---:|---:|---:|
| Rust #11 | −1,913.27 | 10,050 + (−11,963.27) = −1,913.27 | 0 | 0 | 10,119.59 |
| Orange #308 | 18,094.98 | 10,000 + 8,094.98 = 18,094.98 | 0 | 0 | 9,412.23 |
| Blue #381 | 10,936.76 | (status path; delta 0) | 0* | 0 | 9,105.84 |
| Mint #384 | 25,851.06 | 10,000 + 15,851.06 = 25,851.06 | 0 | 0 | 9,598.53 |
| Mango #385 | −3,383.05 | (status path; delta 0) | 0* | 0 | 10,066.75 |
| Mint Turtle #797 | 6,392.10 | 10,000 + (−3,607.90) = 6,392.10 | 0 | 0 | 10,034.14 |
| Yellow Turtle #798 | 5,420.80 | (status path; delta 0) | 0* | 0 | 9,912.68 |

\*Blue / Mango / Yellow: full journal HTML not summed this session; `RiskEquity` reports `cash_vs_pnl_delta = 0` and `capital_base` equals listed free cash.

Mint #384 SHY 2026-08-05 flow **+$6,793.55** (was the August 16 debit that collapsed equity). Live sign is now WUT short-enter credit.

## Dependency or contention scope

| Peer | Order | Baseline | Candidate | Classification |
|---|---|---|---|---|
| CashEvent initial | first | initial capital | same | same |
| Rust +$50 inflow 2026-07-17 | after initial | n/a lab | included | candidate-only event; reconstruct used 10,050 |
| Executed stock lots | fill order | signed notionals | stored `flow` matches units×price and direction | same |
| Draft DA journals | not in WUT cash | n/a | unsigned; excluded from `capital_base` | candidate-only / presentation |
| Passed journals | not cash | n/a | unsigned or 0; excluded | same exclusion |
| Open MV / marks | after cash | equity identity | `cash_vs_pnl_delta=0` | same |
| Fees / borrow | none | none | none | same (absent) |

## Invariant and conservation checks

- **Strict (per OP):** `|UI free cash − (CashEvents + executed flows)| = 0` on the four fully summed books.
- **Aggregate:** seven Active `cash_vs_pnl_delta` all $0 → cash-identity equity equals position-PnL equity.
- **Exclusions:** drafts, passed, expired — `capital_base` uses `status: executed` only (`portfolio.rb` 172–181).
- **Units:** stock notional = units × execution_price; no option lots in the summed set.

Algebra (certain): short enter as **debit** would make equity `C0 − 2·P·Q`. That is not what live books show (risk equity ~$9.1k–$10.1k on $10k seeds).

## Executable trace

### Baseline (WUT)

- Cash: `winston_unit_test/app/services/portfolio_position_manager.rb` 215–248 (`update_cash_on_entry/exit`).
- Journals: `winston_unit_test/app/services/position_manager.rb` 233–246 enter; 359–370 exit (signed `flow` + matching `debit_credit`).
- Reconstruct: `portfolio_backtest_runner.rb` ~2436 `initial + sum(flow)` where `debit_credit` present.
- Worked examples: `winston_unit_test/CASH_EQUITY_VERIFICATION.md`.

WUT lab Daily Analysis `operations/task_generator.rb` 59–79 also writes **unsigned** draft flow. That is not the PBR cash SoT.

### Candidate (Wv2)

- Free cash SoT: `winston_v2/app/models/portfolio.rb` 172–181.
- Executed writer: `RelatedInstrumentFulfillment.signed_flow` (`related_instrument_fulfillment.rb` 74–88); confirm enter/pyramid/exit (`journal_confirmation_service.rb` 82–156).
- Draft writer: `TaskGenerator#journal_flow` (`task_generator.rb` 207–216) unsigned; `debit_credit` 157–167 by signal type only.
- Confirm `else` (task_type not enter/pyramid/exit) reuses stored draft flow (157–160). Not hit for DA enter/pyramid/exit.
- Surfaces: `RiskEquity`, ops shell, DAR, MCP `capital_base` all read `capital_base` / snapshot cash.

## Classification

**Executed free cash: not a candidate defect** — matches WUT reconstruct; August 17 issue remains the historical root and is resolved on this database.

**Draft / passed Flow column: candidate defect** — `TaskGenerator#journal_flow` violates the WUT journal sign contract. Does not change desk free cash until a non-enter/pyramid/exit confirm path persists the draft number.

Competing labels rejected:

- *Baseline defect* — operator designated WUT PBR cash as truth; executed Wv2 matches it.
- *Intentional contract change* — no ADR says drafts should be unsigned.
- *Capture artifact* — four books reconstructed from the same HTML the operator can open.

## Recommendation

1. Do **not** backfill executed journals. Live executed `flow` already matches WUT signs on sampled shorts/longs.
2. Teach the desk: large or negative **free cash** with ~$10k **risk equity** is the WUT balance sheet (shorts credit cash; longs debit). Wealth is risk equity.
3. Fix DA drafts to call `signed_flow` and set `debit_credit` from the signed amount (ticket `winston_v2/docs/tickets/2026-08-18-dar-draft-journal-unsigned-flow.md`).
4. Fix the stale `capital_base` comment that still says “profitable exits / losses.”
5. Optional: WUT lab `operations/task_generator.rb` has the same unsigned draft pattern — out of scope unless lab drafts are used as cash.

## Adversarial verification

- Mode: independent hostile subagent 2026-08-18 (`/tmp/adversarial-free-cash.md`)
- Verdict: **holds-with-caveats**
- Corrections applied to this issue:
  - Executed stock/proxy flows use the WUT PBR **free-cash sign identity**. This was **not** a WUT PBR replay (no lab DB).
  - WUT has three numbers: free cash; single-market sizing `capital_base` (profits only); PBR sizing `portfolio_capital_base` (all closed PnL). Wv2 desk free cash is the first. Wv2 `PositionSizer` uses **risk equity**, not PBR sizing capital.
  - `cash_vs_pnl_delta = 0` proves signs vs price/direction PnL, not “same lots as a WUT run.”
  - HTML reconstruct of four books is consistent with `capital_base` but is not an independent third ledger.
  - Confirm **else** (no task / unknown `task_type`) can persist unsigned draft `flow` into executed cash. Not observed in today’s executed set (`delta = 0`). Latent hole — spec / refuse.
  - Option/LEAP not live-proven; series MV/recon does not ×100, so first LEAP would flag a fake disagree.
  - Narrow “desk numbers”: executed free cash + risk equity. Draft Flow and proposed units were out of alignment.
- Claims that survived: `capital_base` is WUT free cash; `signed_flow` matches WUT stock/proxy; drafts unsigned; SHY now +$6,793.55.

## Problem statement

Operators can read Wv2 free cash as “wrong vs WUT” because (1) free cash is not account value on two-way books, and (2) draft Flow cells are unsigned.

## Current behavior

- Executed `capital_base` = CashEvents + signed executed flows (WUT).
- Drafts: `flow = |units×price|`, `debit_credit = debit` unless signal type is exit/stop_out.
- Example: Rust #11 RXT draft pyramid `j#938` flow +628.29 debit on a **short** book (executed RXT `j#845` was credit). Flow magnitude/sign of notional is short-enter-like; debit_credit is long-enter-like.

## Expected behavior

- Executed: keep current WUT identity.
- Drafts: same signs as WUT / `signed_flow` so Flow/debit_credit preview the cash move confirm will apply.

## Reproduction

### Preconditions

Tailscale to sawtooth-ai; paper Active OPs.

### Steps

1. Open `https://sawtooth-ai.tail944ffb.ts.net/wv2/internal/portfolio_status?portfolio_id_or_name=308`.
2. Sum executed journal Flow on `/wv2/operations/portfolios/308/journals?status=executed`.
3. Compare to `capital_base` / `free_cash`.
4. Open status=draft on Rust #11 or Mango #385.

### Observed result

Step 3 matches to the cent. Step 4 shows unsigned positive flows and enter→debit.

### Reproducibility

Always on this compose database as of 2026-08-18.

## Environment

- Host: sawtooth-ai (`https://sawtooth-ai.tail944ffb.ts.net/wv2`)
- Paper Active OPs listed above
- Local clone for code: `~/Winston/winston_v2` `main` @ `eee19f7` (this Mac). Live image commit not printed this session; behavior matches post-`cd37a1f` signs.

## Evidence

| Evidence | Source | What it establishes |
|---|---|---|
| WUT cash table | `portfolio_position_manager.rb` 215–248; `CASH_EQUITY_VERIFICATION.md` | Gold-standard signs |
| Wv2 `capital_base` | `portfolio.rb` 172–181 | Executed-only sum |
| Live OP table | `GET /wv2/internal/portfolios` + `portfolio_status` 2026-08-18 | A, risk equity, delta=0 |
| Journal reconstruct | `/operations/portfolios/{11,308,384,797}/journals?status=executed` | A=C to the cent |
| Draft unsigned | same pages `status=draft`; `task_generator.rb` 157–216 | Producer defect |
| Prior fix | ISSUE-20260817, commit `cd37a1f` | Historical short-debit collapse |

## Impact and priority

- Desk free cash / risk equity **numbers used for sizing and DAR** are WUT-aligned. Priority of a cash-identity emergency: **none**.
- Draft Flow column can teach the wrong sign. Priority **medium** for producer hygiene.
- Workaround: ignore draft `flow`; trust executed ledger and risk equity.

## Scope and preservation requirements

### In scope

- Draft `signed_flow` + comment fix
- Operator explanation of free cash vs risk equity

### Must preserve

- Executed WUT signs (do not flip shorts back)
- Option/LEAP purchase-signed (ignore signal direction)
- `equity = free_cash + long MV − short MV`
- No Telegram / no real-capital journal rewrite

### Out of scope

- Changing WUT PBR sizing `capital_base`
- Copying sawtooth Postgres to this Mac
- Fee/borrow model
- Executed backfill

## Acceptance criteria

- [x] Given each fully summed Active OP, when reconstruct = CashEvents + executed flows, then it equals UI free cash within $1
- [x] Given Active snapshots, when `RiskEquity` runs, then `cash_vs_pnl_delta` is $0
- [ ] Given a DA draft long enter, when created, then `flow` is negative and `debit_credit` is debit
- [ ] Given a DA draft short enter/pyramid, when created, then `flow` is positive and `debit_credit` is credit
- [ ] Given existing executed shorts, when left untouched, then `capital_base` does not change

## Investigation notes

Hypothesis that “Wv2 executed free cash is wrong right now” is **falsified** on the four summed OPs and inconsistent with delta=0 on the other three.

Hypothesis that drafts are unsigned is **confirmed**.

WUT single-market `PositionManager#capital_base` only **adds profits**. That is sizing, not free cash. Wv2 `PositionSizer` uses risk equity. Separate axis.

## Unknowns and clarifying questions

- [ ] Live container git SHA vs local `eee19f7`
- [ ] Line-item reconstruct for Blue #381, Mango #385, Yellow #798
- [ ] Any option/LEAP executed lots on Active OPs
- [x] Draft-only writer fixed in local clone `~/Winston/winston_v2` (`TaskGenerator` + `capital_base` comment). Not deployed to sawtooth. Specs written; compose test DB / bind-mount on this Mac is stale (container still sees 2026-08-06 tree).

## Dependencies and risks

Related: August 17 short-flow issue (resolved). Draft fix must not rewrite executed rows.

## Verification plan

- Repeat reconstruct after any journal writer change.
- Specs: DA `TaskGenerator` long/short/option draft signs from `CASH_EQUITY_VERIFICATION.md`.
- Live: one paper draft create on compose test — do not mint on sawtooth to “get a sample.”

## History

- 2026-08-18 — Investigation from operator request; live Tailscale read of sawtooth Wv2; WUT code + verification doc as baseline.
