# Session Report — TF six principles + CAGR/Calmar

**Date:** 2026-09-04
**Time:** ~12:00–14:29 MDT
**Duration:** ~2h 30m
**Project:** sawtooth Winston ecosystem + winston_v2
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `ecosystem/main`, `winston_v2/main` (started from `origin/main`)
**Model:** Grok 4.6
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** (1) Analyze Winston Trend Following (TF) against the six Bell Labs / Kelly trading principles and file an ecosystem tracker. (2) Implement Compound Annual Growth Rate (CAGR) and Calmar on Active Operational Portfolio live pages, then on the Daily Activity Report (DAR) and Mid-month Scoreboard (MMS) as bar graphs next to equity curves.

**Outcome:** Delivered

**One-line summary:** Competency audit of Winston TF against Shannon→Lo is filed; CAGR and Calmar now show on live ops pages and will appear beside equity curves on the next DAR and MMS.

---

## 2. Work Completed

- Read the six-principles essay; mapped each layer to Winston ADRs, lab, and live ops (four explore subagents + primary evidence).
- Wrote a one-page-per-principle analysis deck in the librarian foundations folder.
- Filed an ecosystem competency tracker: analysis pointer, program INDEX, epic, six principle tickets; linked existing P0/P1 tickets instead of cloning them.
- Implemented `Operations::CagrCalmar` (same formula as Winston Unit Test bake-off scorecards: calendar days / 365.25; Calmar = CAGR% / max DD%).
- Wired metrics through `PortfolioEquitySeries`; first-class meters on the portfolio live page (paper and real).
- DAR and MMS PDFs: equity curve left, signed CAGR% and Calmar bar panels right; markdown/tables updated.
- Verified live HTML on portfolio #384 (Mint) and specs in the `winston_v2` compose container.

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `typewriter/.../winston_foundations/20260904/*.md` | added | Librarian deck (outside sawtooth git) |
| `ecosystem/docs/analysis/2026-09-04-tf-six-principles-competency.md` | added | Pointer agents will find |
| `ecosystem/docs/tickets/2026-09-04-tf-foundations-*.md` | added | Epic + INDEX + P1–P6 |
| `ecosystem/docs/tickets/INDEX.md` | modified | Program rows (also mixed with concurrent lab-archive edits) |
| `winston_v2/app/services/operations/cagr_calmar.rb` | added | Calculator |
| `winston_v2/app/services/operations/portfolio_equity_series.rb` | modified | Merges compounding into metrics |
| `winston_v2/app/views/operations/desk_workflows/_portfolio_live.html.erb` | modified | Score meters |
| `winston_v2/app/assets/stylesheets/ops_shell.css` | modified | Window label + live meters |
| `winston_v2/app/services/report_pdf_chart_drawer.rb` | modified | `equity_with_compounding`, `signed_bar_chart` |
| `winston_v2/app/services/daily_activity_report_{pdf,markdown}_renderer.rb` | modified | Bars + table columns |
| `winston_v2/app/services/mid_month_scoreboard_{pdf,markdown}_renderer.rb` | modified | Bars + table |
| `winston_v2/app/services/operations/mid_month_scoreboard_builder.rb` | modified | Period + lifetime CAGR/Calmar |
| `winston_v2/spec/services/operations/cagr_calmar_spec.rb` | added | Formula tests |
| related Wv2 specs | modified | Live snapshot, equity series, DAR/MMS renderers, request |

### Commits

- _Pending wrap commit._

### Branch / PR state at sign-off

- Branch: `main` on both `ecosystem` and `winston_v2` — dirty at report write
- Pushed: no (wrap will push)
- PR: not opened (direct `main`)

---

## 4. Decisions Made

### Decision 1: Calmar = CAGR% / max drawdown%
- **Choice:** Industry Calmar, not total-return / DD.
- **Why:** Bake-off scripts already used this; matches the compounding question.
- **Alternatives considered:** total_return_pct / DD (ticket 2026-07-26 left it open).
- **Reversibility:** easy (one formula).
- **Promote to ADR?** no

### Decision 2: Always show CAGR with window label, no 90-day hide
- **Choice:** Show the number; put `6.7y` / `54d` on the meter.
- **Why:** Short-window annualization is the point of CAGR (Rust +14.6% in 54d → 152% CAGR).
- **Alternatives considered:** hide under 30/90 days.
- **Reversibility:** easy.
- **Promote to ADR?** no

### Decision 3: MMS bars use the MMS window, not lifetime
- **Choice:** Period CAGR/Calmar next to the window equity overlay; lifetime fields stay on JSON (`lifetime_cagr_pct`).
- **Why:** Same idea as the live page: bars match the curve’s window.
- **Alternatives considered:** lifetime bars beside a one-month curve (would mismatch).
- **Reversibility:** easy.
- **Promote to ADR?** no

### Decision 4: TF competency program is tickets, not Evolution Mode
- **Choice:** Six architecture tickets in competency order; do not start Evolution Mode or global Kelly.
- **Why:** Essay failure mode is arguing layer one while 2–6 are unfinished. Discipline (layer 5) is already load-bearing.
- **Alternatives considered:** another bake-off cell; Evolution Mode.
- **Reversibility:** easy (tickets are Proposed).
- **Promote to ADR?** no — tracker first; plans later if operator accepts grades.

---

## 5. Insights Surfaced

- Winston is a competent TF **operations factory** with a missing **measurement layer**. Layer 5 (Human-Gated desk) is the one principle already managed well.
- Repo “capacity” means heat slots, not Shannon channel capacity.
- Practical Sharpe ranks on the same path used to pick the winner; two-phase vet is not out-of-sample.
- Live sizing is Turtle 1% of notional equity; Capital Authority / Leverage Guardrail are glossary, not Ruby.
- Mint #384 live: −4.66% return over 6.7y → −0.71% CAGR, Calmar −0.07. Quiver Tracking #1372: −16.85% in 14d → −99% CAGR (window on the label).
- All Active Operational Portfolios were paper at check time; no Active real book to hit.
- Concurrent session (14:28) archived lab-dead-end tickets and wrote a separate report; do not mix those files into this wrap except where `INDEX.md` already points at archives.

---

## 6. Issues & Tickets

### Resolved this session
- Live-page CAGR/Calmar (operator request; P4 compounding slice).
- DAR/MMS CAGR/Calmar bar graphs beside equity.

### Deferred
- Re-render 2026-09-03 DAR PDF in place (would overwrite the stored artifact; no Telegram).
- WUT bake-off scorecard CAGR (`docs/tickets/2026-07-26-bakeoff-scorecard-cagr-calmar.md`) — still Proposed, lab scripts only.
- TF P1–P6 architecture work — filed, not built.
- First-pass doctrine / gate retune — other session closed as operator dead end; P1 must not reopen it.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| `Operations::CagrCalmar` | rspec in compose | ✅ |
| Portfolio equity series metrics | rspec | ✅ |
| Live page HTML (Mint #384, Rust #11, Quiver #1372) | curl localhost:3002 and Tailscale 200 | ✅ |
| Live page CSS window class | served application.css contains rule | ✅ |
| DAR/MMS PDF + markdown renderers | rspec (9 examples) | ✅ |
| Next live DAR/MMS PDF | not generated this session (did not overwrite 2026-09-03) | ⚠️ |
| Browser click-through | no browser tool; HTTP only | ⚠️ |
| Active real OP | none Active | ⚠️ |

**Test command(s):**

```
bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 \
  bundle exec rspec spec/services/operations/cagr_calmar_spec.rb \
  spec/services/portfolio_equity_series_spec.rb \
  spec/services/operations/portfolio_live_snapshot_spec.rb \
  spec/requests/operations_portfolios_spec.rb \
  spec/services/report_pdf_chart_drawer_spec.rb \
  spec/services/daily_activity_report_pdf_renderer_spec.rb \
  spec/services/daily_activity_report_markdown_renderer_spec.rb \
  spec/services/mid_month_scoreboard_pdf_renderer_spec.rb \
  spec/services/operations/mid_month_scoreboard_builder_spec.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new (Prawn already in DAR/MMS).
- **Services:** existing compose (`winston_v2` restarted twice for CSS cache).
- **Migrations:** None.

---

## 9. Risks & Technical Debt

- CAGR on 14-day Quiver Tracking annualizes to ruin-looking numbers; window label is the mitigation.
- Simple return vs initial CashEvent is not time-weighted for later top-ups (same as existing `return_pct`).
- MMS period CAGR on ~one month will look large vs lifetime live-page CAGR — labels must stay “window.”
- `INDEX.md` also contains concurrent lab-archive row edits; wrap must keep archive files in sync if that INDEX is committed.
- Uncommitted prior work on portfolio live eval (controller/route/ops-shell links) was on the bind-mount; this session’s CAGR meters depend on that surface.

---

## 10. Open Questions

- **Accept the six competency grades?** — needs answer from: operator; blocks: promoting P1–P6 to plans.
- **Rebuild 2026-09-03 DAR PDF now?** — needs answer from: operator; blocks: seeing bars before tonight’s DAR.
- **WUT scorecard CAGR still wanted?** — already a P3 ticket; not this session.

---

## 11. Handoff & Resume Notes

- **Where I left off:** CAGR/Calmar on live pages + DAR/MMS renderers; specs green; next scheduled DAR will pick up charts.
- **Next concrete step:** Observe tonight’s DAR PDF (equity + CAGR/Calmar bars). Optionally accept TF grades and schedule P1 walk-forward.
- **Files to read first:**
  1. `ecosystem/docs/tickets/2026-09-04-tf-foundations-INDEX.md`
  2. `typewriter/.../winston_foundations/20260904/00-the-stack.md`
  3. `winston_v2/app/services/operations/cagr_calmar.rb`
  4. `winston_v2/app/services/report_pdf_chart_drawer.rb` (`equity_with_compounding`)

---

## 12. Stakeholder Communications

- _None._ Operator-facing; no outward email.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, record (taxonomy), session-report, wrap; explore subagents for evidence.
- **What worked well:** four parallel explore agents produced citeable evidence; live curl on #384 matched the formula.
- **Friction points:** sprockets digest looked stale until CSS was grepped in the served file; host `bundle exec rspec` cannot reach `wv2_postgres` (must compose exec).
- **Subagent usage:** explore ×4 (signal, tails, sizing, compounding/discipline/reality).

---

## 14. Follow-up Actions

- [ ] Observe next DAR PDF for CAGR/Calmar bars beside equity — owner: operator — due: next scored session ~16:30 MT
- [ ] Observe next MMS (third Wednesday 06:00 MT) for the same panel — owner: operator
- [ ] Optional: re-render 2026-09-03 DAR PDF without Telegram — owner: operator
- [ ] Accept or amend TF competency grades, then schedule P1 — owner: operator — already filed `2026-09-04-tf-p1-residual-signal-and-oos.md`

---

## 15. Appendix

Librarian deck: `/home/johnkoisch/Documents/com/typewriter/librarian/koisch-jr/winston_foundations/20260904/`

Live check (2026-09-04):

| OP | Return | Max DD | CAGR | Calmar | Window |
|----|--------|--------|------|--------|--------|
| Mint #384 | −4.66% | 9.78% | −0.71% | −0.07 | 6.7y |
| Rust #11 | +14.63% | 3.65% | 151.85% | 41.58 | 54d |
| Quiver #1372 | −16.85% | 86.42% | −99.19% | −1.15 | 14d |

Formula: `wealth = 1 + return_pct/100`; `CAGR% = (wealth**(1/years) − 1)×100`; `years = days/365.25`; `Calmar = CAGR% / max_dd%`.
