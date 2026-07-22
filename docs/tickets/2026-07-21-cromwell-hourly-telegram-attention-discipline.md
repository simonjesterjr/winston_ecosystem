# Ticket: Cromwell hourly Telegram — attention discipline (quiet = one line)

**Status:** Proposed  
**Priority:** P1  
**Context:** Issue `docs/issues/2026-07-21-cromwell-hourly-verbose-quiet-attention-waste.md`. Principle `principles/01_core_principles.md` §12 (*Human attention is the most valuable commodity*). Skill already states the rule; agent still dumps quiet tables + menus.

## Cluster (Cromwell hourly Telegram)

Treat these four as one ops quality epic — do not close “hourlies work” until all are green:

| # | Artifact | Intent |
|---|----------|--------|
| 1 | [`2026-07-09-confirm-cromwell-hourly-telegram.md`](2026-07-09-confirm-cromwell-hourly-telegram.md) | Hourlies actually post non-error content after CPU tuning |
| 2 | [`2026-07-13-cromwell-scrub-placeholder-path-memory.md`](2026-07-13-cromwell-scrub-placeholder-path-memory.md) | Scrub `path/to/file.txt` poison from permanent memory |
| 3 | [`2026-07-13-observe-cromwell-market-snapshot-hourlies.md`](2026-07-13-observe-cromwell-market-snapshot-hourlies.md) | Live proof: real MCP call + clean Telegram |
| 4 | **This ticket** + [issue](../issues/2026-07-21-cromwell-hourly-verbose-quiet-attention-waste.md) | Quiet → one line; movers only when volatile; no menus |

## Problem

Point of hourly updates: engage the user with markets **displaying volatility**. Uninteresting all-quiet detail is a product failure even if delivery succeeds. Evidence 2026-07-21 ~10:21: multi-symbol Quiet table, placeholders, “Would you like me to…” menu.

## Work

1. **Skill / persona** — Make quiet path non-negotiable: default copy `All markets quiet.` (or short rotation); explicit ban on per-quiet-symbol tables and offer menus on cron. (**Done 2026-07-21** seed.)
2. **Cron job message** — Shorten open/hourly strings with hard quiet one-liner. (**Done 2026-07-21** seed; verified in `prompt_vars` on 2026-07-22 runs.)
3. **Runtime (NOW required)** — Soft text **failed** natural posts 2026-07-22 08–11 MT (quiet symbols listed, menus, long dumps). Implement post-process or structured format for scheduled snapshot replies:
   - If payload movers empty → force `All markets quiet.`
   - If movers present → allow only short radar lines; strip menus / “Would you like”
   - Cap length; never post quiet symbols as “notable”
4. **Observe** — Jul 22 samples on observe ticket; re-verify after runtime.

## Acceptance criteria

- [ ] All-quiet natural hourly → single all-clear line (no symbol table, no menu)
- [ ] Movers hourly → short radar list only
- [ ] Principle §12 cited from skill or persona so future agents do not re-expand quiet posts
- [ ] Cross-linked observe ticket notes the quiet-path sample

## Related

- Issue: [`docs/issues/2026-07-21-cromwell-hourly-verbose-quiet-attention-waste.md`](../issues/2026-07-21-cromwell-hourly-verbose-quiet-attention-waste.md)
- Principle: `ecosystem/principles/01_core_principles.md` §12
- Skill: `ecosystem/ai/skills/winston-market-snapshot/SKILL.md`
- Heartbeat: `ecosystem/ai/skills/winston-heartbeat/SKILL.md`
- Parent quality issue: [`docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md`](../issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md)
