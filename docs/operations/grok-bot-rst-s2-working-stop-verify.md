# Grok Bot — verify WUT S2 Working Stop B1/B4 (RST)

Paste this into Grok Bot. Host is **Grok Bot / Grok CLI on sawtooth** (Builder). **Not** Cromwell Telegram. **Not** Lab Scout execute.

**Job:** User-acceptance-test (UAT) the Winston Unit Test (WUT) runner work Grok CLI shipped (A0–A4 overnight arm list + B1–B4 Working Stop phases). **Report only.** Do **not** run the 32-cell matrix. Do **not** execute smoke Portfolio Backtest Run (PBR) **#596**.

| What | Path |
|------|------|
| Plan | [`winston-rst-slate-exit-parity-grok-cli.md`](../../plans/winston-rst-slate-exit-parity-grok-cli.md) |
| Lab law | [`wut-s2-working-stop-lab.md`](../business-context/wut-s2-working-stop-lab.md) |
| Domain law | [`turtle-s2-pyramid-and-working-stop.md`](../business-context/turtle-s2-pyramid-and-working-stop.md) |
| Fixtures (B) | `winston_unit_test/spec/services/portfolio_backtest_s2_working_stop_spec.rb` |
| Fixtures (A) | `winston_unit_test/spec/services/portfolio_backtest_rst_overnight_arm_spec.rb` |
| A spec | [`wut-rst-session-slate.md`](../business-context/wut-rst-session-slate.md) |
| Fill regression | `winston_unit_test/spec/services/portfolio_backtest_resting_stop_touch_spec.rb` |
| Shell hop | [`grok-bot-shell-lab-eval.md`](grok-bot-shell-lab-eval.md) |

**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`

---

## What shipped (do not re-derive)

Under Resting Stop Touch (RST) + Turtle System 2 (S2: 55-day entry, 20-day exit, `move_to_last_entry`):

1. **B1** — while lots &lt; max, 20-day is **not** evaluated. No channel exit. Only 2N + next pyramid.
2. **B2** — on the max-fill bar, Working Stop stays last ± 2N. 20-day watch starts the **next** session.
3. **B3** — when 20-day has **passed** 2N, Working Stop **becomes** the 20-day and replaces nightly. No revert to 2N. No second stop.
4. **B4** — pierce of the then-current Working Stop flattens **all** lots (touch / gap-open). No parallel Donchian close.

System 1 (S1) 20/10 is unchanged. Hybrid / next-open is unchanged. Trading Strategy (TS) fingerprint / Winston v2 (Wv2) Daily Analysis (DA) are unchanged.

Also shipped: overnight **arm list** (A) — one ranked park list of entries **and** pyramids; heat/cash refuse before park; overflow not armed; unarmed names do not fill even if they print.

**Not shipped:** Edge (R) re-score (A5/B5). Fingerprint unchanged.

---

## Fences

- Report only — no pack promotion.
- No Broker Gateway `order_write`.
- No Cromwell cron. No `wut_execute_portfolio_backtest_run` on #596.
- No `FULL=1` 32-cell UAT.
- Do **not** treat completed `strategy77_rst_heat_risk_v1` journals as proof of B1/B4 — those PBRs ran **before** this gate. Old 20-day-under-max rows are pre-fix evidence, not a fail of this pass.
- Do **not** implement further runner code in this UAT. File findings.

---

## Step 1 — confirm the diff is in the tree

```bash
cd /home/johnkoisch/Documents/com/sawtooth
test -f winston_unit_test/spec/services/portfolio_backtest_s2_working_stop_spec.rb && echo SPEC_OK
rg -n "skip_s2_channel_exit|apply_s2_20d_working_stop" winston_unit_test/app/services/portfolio_backtest_runner.rb
```

Expect: spec exists; both methods exist on the runner.

## Step 2 — run the golden tapes (this is the UAT)

```bash
./bin/compose exec -T winston_unit_test bundle exec rspec \
  spec/services/portfolio_backtest_rst_overnight_arm_spec.rb \
  spec/services/portfolio_backtest_s2_working_stop_spec.rb \
  spec/services/portfolio_backtest_resting_stop_touch_spec.rb \
  --format documentation
```

**Pass:** A arm-list examples green **and** S2 B1–B4 green **and** RST fill tapes green.

Ignore a leading `db:test:load` / `ConnectionNotEstablished` to `::1:5432` **if** the documentation block still prints examples and `0 failures`. That noise is a test-DB purge against localhost inside the container; these specs allocate the runner and do not need the test schema.

**Fail:** any A or S2 example red, or RST fill tapes red. Quote the example name and the error. Stop. Do not “fix Edge” by changing fill cadence.

A names that must hold:

| Example | Must show |
|---------|-----------|
| `A4: 8 entry candidates, heat cap 3` | parks markets 1–3 (highest ATR); rest `heat_direction` |
| `ranks entries and pyramids on one list` | parks entry then two pyramids |
| `does not fill an unarmed name that prints a breakout` | `execute_entry` only for the three parks |
| `expires an armed park that does not touch` | `no_price_level_touch` |
| `does not use the overnight arm list on hybrid/next-open` | `process_entries`, not arm |

S2 names that must hold:

| Example | Must show |
|---------|-----------|
| `B1: 3/4 long, 20-day prints, 2N not hit → no channel exit` | no `execute_exit` |
| `B1+B4` / `B4` flatten-all | all lots, reasons match `/stop/i` |
| `B2: 4/4, 20-day still below 2N` | still at 2N, no channel exit |
| `B2: max-fill bar keeps last±2N` | no 20-day replace same session as max fill |
| `B3: 20-day has passed 2N` | `updated_stop` = 20-day level |
| `B3: pierce of the 20-day Working Stop` | flatten-all at the 20-day, not a Donchian close |
| `B3: nightly replace` | follows 20-day; does not revert to 2N |
| `does not suppress 20-day under max on a non-S2 recipe` | one 20-Day Breakout channel exit (lot 1) |

## Step 3 — report (required shape)

Write to the operator (and optionally `ecosystem/docs/analysis/YYYY-MM-DD-wut-s2-b1-b4-verify.md` if they ask to file):

1. Spec command + counts (A + S2 + RST fill, failures).
2. Whether A and B1–B4 fixtures match the tables above.
3. Remaining holes (do not bury these):
   - **Edge (R) on the 32-cell matrix is still the old chassis** (ran before A+B). Do not promote. Do not call TS **#77** dead off that panel.
4. Recommendation: next is a **narrow** Yellow + Blue × turtle heat × 1% × RST Edge panel on **new** PBRs (A5/B5). No `FULL=1` 32. Operator lock before execute.

## Out of scope this UAT

- Implementing more runner code.
- Re-executing Mint smoke #596 or any full-window PBR (hours of CPU).
- 32-cell `FULL=1`.
- `/edge-scorecard` on old cells as if B1/B4 changed them.
- Wv2 DA / Walnut Session Order Slate / fingerprint payload.
