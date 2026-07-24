# Session Report — DAR Telegram MT Production Clock

**Date:** 2026-07-24
**Time:** ~16:35–16:48 MDT
**Duration:** ~15m
**Project:** sawtooth Winston ecosystem (Wv2 + ecosystem interfaces)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `winston_v2` main; `ecosystem` main
**Model:** Grok 4.5
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Investigate ops UI `Last DAR` showing Telegram `skipped non_production_date` for the 2026-07-24 EOD report; align Telegram decision clock with report-generation clock (US MT production day).

**Outcome:** Delivered

**One-line summary:** EOD DAR at 16:30 MT had already posted to Telegram; the skip was a morning smoke using `Date.current` (UTC app TZ) while production was still yesterday — generate defaults now use `DailyReportSchedule.default_report_date` (America/Denver).

---

## 2. Work Completed

- Traced ops UI → `storage/cromwell_notifications/wv2_*.json` → `CromwellNotifier.deliver_telegram!` → `DailyReportSchedule.telegram_delivery_allowed?`
- Confirmed production cron (`30 16 * * * America/Denver`) delivered PDF to Sawtooth Main (msg **493**) at `2026-07-24T22:30:18Z`
- Found morning job (~15:50 UTC / 09:50 MT) that wrote `non_production_date` for report `2026-07-24` while production was `2026-07-23` (smoke / `wv2:portfolios:evaluate` via `Date.current`)
- Fixed default report date on rake evaluate paths, CromwellNotifier, and DAR PDF/MD renderers
- Added regression specs for morning pre-cutoff, post-cutoff deliver, and UTC-midnight-vs-MT edge
- Updated `ecosystem/interfaces/cromwell-notification-v1.md` clock note

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `winston_v2/lib/tasks/wv2.rake` | modified | `daily_analysis` + `portfolios:evaluate` → `default_report_date` |
| `winston_v2/app/services/cromwell_notifier.rb` | modified | default `date:` → production EOD |
| `winston_v2/app/services/daily_activity_report_pdf_renderer.rb` | modified | same default |
| `winston_v2/app/services/daily_activity_report_markdown_renderer.rb` | modified | same default |
| `winston_v2/app/services/daily_report_schedule.rb` | modified | shared-clock policy comment |
| `winston_v2/spec/services/daily_report_schedule_spec.rb` | modified | MT/UTC regression cases |
| `winston_v2/spec/services/cromwell_notifier_telegram_guard_spec.rb` | modified | post-cutoff allow + pre-cutoff skip |
| `ecosystem/interfaces/cromwell-notification-v1.md` | modified | document shared MT clock |
| `ecosystem/docs/session-reports/2026-07-24-1648-dar-telegram-mt-clock.md` | added | this report |

### Commits

- `d6c47f6` — winston_v2: fix(dar): align generate defaults with MT production clock
- `ac317f1` — ecosystem: docs: DAR Telegram MT clock session report + interface note

### Branch / PR state at sign-off

- Branch: `main` (both repos) — session commits clean; unrelated dirty files left unstaged
- Pushed: yes (wrap)
- PR: n/a (direct main)

**Not this session (do not stage):**

- `winston_v2`: `daily_report_payload_builder.rb`, `portfolio_equity_series.rb` (+ spec)
- `ecosystem`: other ticket/INDEX/business_analysis dirt
- `winston_unit_test`: extensive close-trigger work (unrelated)

---

## 4. Decisions Made

### Decision 1: Default generate date = production EOD, not Date.current
- **Choice:** Rake, notifier, and report renderers default to `DailyReportSchedule.default_report_date`
- **Why:** App `config.time_zone` is UTC; `Date.current` diverges from MT production day (morning of trading day and UTC midnight edge)
- **Alternatives considered:** Only set `config.time_zone = America/Denver` (broader blast radius); force Telegram for any date past its cutoff (weaker historical guard)
- **Reversibility:** easy
- **Promote to ADR?** no — interface note + schedule comment sufficient

### Decision 2: Leave Telegram production-date guard unchanged
- **Choice:** Keep `production_date?` / `non_production_date` skip for historical dates
- **Why:** Guard worked as designed; bug was generate path choosing the wrong date
- **Alternatives considered:** “Allow telegram if report_date has passed its MT cutoff” (would post historical smokes to Sawtooth Main)
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 3: Defer app-wide Rails time_zone change
- **Choice:** Do not set `config.time_zone = "America/Denver"` this session
- **Why:** Affects ops `as_of`, market bars, journals, etc. — separate review
- **Alternatives considered:** Do it now
- **Reversibility:** easy later
- **Promote to ADR?** maybe if ecosystem standardizes on MT wall-clock everywhere

---

## 5. Insights Surfaced

- **Two runs, one filename:** Morning smoke overwrites `wv2_YYYYMMDD.json` with `telegram skipped`; real EOD later overwrites with `delivered`. Ops “Last DAR” reflects last write only — easy to misread if you glance between runs.
- **EOD at 16:30 MT is still UTC same calendar day** (22:30Z). Pure “UTC is already tomorrow at EOD” does not explain a 16:30 failure; UTC day roll is **18:00 MT** in summer (MDT).
- `DailyReportSchedule` was already MT-correct; cron was already MT-correct. Divergence lived in rake/`Date.current` defaults.
- Rails `config.time_zone` remains commented → UTC; many controllers still use `Date.current` for `as_of` (out of scope).

---

## 6. Issues & Tickets

### Resolved this session
- Generate vs Telegram clock split on default date selection (operational confusion + morning smoke false “failure”)

### Deferred
- App-wide `config.time_zone = "America/Denver"` (or equivalent) so residual `Date.current` call sites align with production day
- Optional: ops UI show `production_date` + `generated_at` next to telegram skip reason (UX clarity)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Schedule + telegram shared clock | `rspec spec/services/daily_report_schedule_spec.rb spec/services/cromwell_notifier_telegram_guard_spec.rb` | ✅ 21 examples, 0 failures |
| Live EOD 2026-07-24 | notification JSON + sidekiq log msg 493 | ✅ delivered (pre-fix; no re-run needed) |
| Morning smoke path | log + session smoke notes | ⚠️ intentional skip before fix; post-fix morning evaluate defaults to prior day |

**Test command(s):**

```bash
bin/compose exec -T winston_v2 bundle exec rspec \
  spec/services/daily_report_schedule_spec.rb \
  spec/services/cromwell_notifier_telegram_guard_spec.rb \
  --format documentation
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None
- **Services:** compose already up (winston_v2, winston_v2_sidekiq, etc.)
- **Migrations:** None
- **Operational data:** `wv2_20260724.json` telegram delivered true; `generated_at` 2026-07-24T22:30:18Z

---

## 9. Risks & Technical Debt

- Other `Date.current` call sites (ops panels `as_of`, market bars, expire service defaults) still use app UTC calendar day
- Rake historical evaluates with explicit date still skip Telegram without force — correct, but UI may still confuse operators

---

## 10. Open Questions

- **Should Wv2 set `config.time_zone` to America/Denver?** — needs answer from: operator / ecosystem standards; blocks: residual Date.current drift
- **Should ops Last DAR show production_date when telegram skipped?** — UX polish only

---

## 11. Handoff & Resume Notes

- **Where I left off:** Code + specs + interface note ready; wrap commit/push pending; follow-up promotion pending
- **Next concrete step:** Commit only session files in `winston_v2` + `ecosystem`; decide ticket for Rails time_zone
- **Files to read first:**
  1. `winston_v2/app/services/daily_report_schedule.rb`
  2. `winston_v2/lib/tasks/wv2.rake` (evaluate default date)
  3. `winston_v2/app/services/cromwell_notifier.rb` (telegram guard)
  4. This session report

---

## 12. Stakeholder Communications

- _None required._ Ops: Friday 7/24 EOD DAR **did** post to Sawtooth Main (msg 493). Morning multi-cohort smoke skip was intentional historical guard.

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report (this)
- **What worked well:** Sidekiq log job IDs + notification JSON + `production=` log line disambiguated two-run story quickly
- **Friction points:** Host `bin/compose` cwd; docker sock permission for raw docker; `rg` missing in container — used grep
- **Subagent usage:** none

---

## 14. Follow-up Actions

- [ ] Consider `config.time_zone = "America/Denver"` for Wv2 (blast-radius review) — owner: operator — due: when convenient
- [ ] Optional ops UI: show `production_date` / `generated_at` beside telegram skip — owner: operator — due: backlog

---

## 15. Appendix (optional)

**Log excerpts**

```
# Morning smoke (~15:50 UTC)
Telegram skipped for non-production date 2026-07-24 (production=2026-07-23)

# EOD cron
[TelegramReportDelivery] PDF sent to Sawtooth Main (-1003884714483) msg=493
telegram=sawtooth_main:ok
DailyAnalysisJob (Wv2): Completed for 2026-07-24
```

**Policy recap**

- Production date = today MT after 16:30, else prior calendar day MT
- Telegram only if `report_date == production_date` (unless force / ENV)
