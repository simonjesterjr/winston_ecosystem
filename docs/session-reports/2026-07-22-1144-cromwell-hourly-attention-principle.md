# Session Report — Cromwell Hourly Attention Principle + Seed/Observe

**Date:** 2026-07-21 → 2026-07-22  
**Time:** ~session open 2026-07-21 afternoon – 11:44 MDT 2026-07-22  
**Duration:** multi-block (principle/tickets + overnight watch)  
**Project:** Winston ecosystem (Cromwell / Telegram ops quality)  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `ecosystem` `main` (`5818496`)  
**Model:** Grok 4.5  
**Operator:** John  

---

## 1. Goal & Outcome

**Stated goal:** Inventory open issues/tickets; then capture four related Cromwell hourly-Telegram concerns and record *human attention is the most valuable commodity* as an architectural principle; seed Cromwell and watch the next natural market-snapshot.

**Outcome:** Partially delivered  

**One-line summary:** Principle §12 and a four-ticket Cromwell hourly cluster are filed; skills/cron seeded and bot restarted; Jul 21 cadence is reliable but attention-fail; post-seed Jul 22 hourlies still verbose — soft prompt is not enough.

---

## 2. Work Completed

- Answered open backlog question from `ecosystem/docs/tickets/INDEX.md` + issues dirs.
- Added **principle §12** (*Human Attention Is the Most Valuable Commodity*) to `principles/01_core_principles.md`.
- Clustered four P1 Cromwell hourly items; filed **4th** as issue + ticket (verbose quiet dumps waste attention).
- Tightened `winston-market-snapshot`, `winston-heartbeat`, open/hourly cron messages, `cromwell-tools.md`.
- Cross-linked confirm / scrub / observe tickets + placeholder-path issue; updated INDEX.
- Seeded workspace (`bin/seed-cromwell-workspace --force-cron`) and restarted `nanobot_cromwell`.
- Catalogued full **2026-07-21** open+hourlies: cadence green, content attention-fail.
- Armed durable overnight watcher; captured that open/hourly **fired** 2026-07-22 (watcher raced `queued` before response filled).
- Post-seed **2026-07-22** natural hourlies still long dumps/menus despite new prompts → runtime rewrite next.

---

## 3. Code Delivered

### Files changed (this session only)

| File | Change | Notes |
|------|--------|-------|
| `ecosystem/principles/01_core_principles.md` | modified | §12 attention principle; Evolving → §13 |
| `ecosystem/docs/issues/2026-07-21-cromwell-hourly-verbose-quiet-attention-waste.md` | added | Ready defect |
| `ecosystem/docs/tickets/2026-07-21-cromwell-hourly-telegram-attention-discipline.md` | added | P1 implementation |
| `ecosystem/docs/tickets/2026-07-09-confirm-cromwell-hourly-telegram.md` | modified | Cluster + Jul 21 cadence |
| `ecosystem/docs/tickets/2026-07-13-cromwell-scrub-placeholder-path-memory.md` | modified | Cluster link |
| `ecosystem/docs/tickets/2026-07-13-observe-cromwell-market-snapshot-hourlies.md` | modified | Jul 21 table + seed note |
| `ecosystem/docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md` | modified | Cluster items 6–7 |
| `ecosystem/docs/tickets/INDEX.md` | modified | New P1 row |
| `ecosystem/ai/skills/winston-market-snapshot/SKILL.md` | modified | Quiet one-liner, bans |
| `ecosystem/ai/skills/winston-heartbeat/SKILL.md` | modified | Attention rule |
| `ecosystem/ai/schedule/cromwell-cron.json` | modified | Hard quiet path in job text |
| `ecosystem/ai/personas/cromwell-tools.md` | modified | Attention note |
| `ecosystem/docs/session-reports/2026-07-22-1144-cromwell-hourly-attention-principle.md` | added | This report |
| `ecosystem/logs/watch-market-snapshot-next.py` | added (gitignored under `logs/`) | Overnight observer |

**Not this session (do not commit under this wrap):** dirty `winston_v2/` desk/DAR work; other ecosystem dirt (ADR-009, CONTEXT, unrelated tickets, other session reports).

### Commits

- _Pending wrap commit on `ecosystem` `main`._

### Branch / PR state at sign-off

- Branch: `ecosystem` `main` — dirty with this session + unrelated WIP
- Pushed: pending selective commit
- PR: not opened (direct main workflow historically)

---

## 4. Decisions Made

### Decision 1: Human attention as core principle
- **Choice:** Principle §12 in `01_core_principles.md` — attention is scarcest commodity; scheduled Telegram must earn interrupt rights.
- **Why:** Principal feedback on verbose all-quiet hourlies; product failure even when delivery works.
- **Alternatives considered:** Ticket-only guidance without principle elevation.
- **Reversibility:** easy (edit principles)
- **Promote to ADR?** no — principle list is the right home; ADR only if conflicting designs appear

### Decision 2: Soft skill/cron first, runtime second
- **Choice:** Ship skill + cron message harden first; optional runtime rewrite if soft fails.
- **Why:** Cheaper; skill already said the right thing and was ignored.
- **Alternatives considered:** Immediate post-process rewrite in nanobot patch.
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 3: Four-item hourly quality epic
- **Choice:** Confirm delivery, memory scrub, observe MCP+clean Telegram, attention discipline as one cluster.
- **Why:** Same surface (Sawtooth Main hourlies); partial greens mislead if treated separately.
- **Reversibility:** easy (docs)
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- **Jul 21 cadence was green** end-to-end (07:38 open through 14:08 hourly); principal “last at 10:21” was the worst *content* sample, not the last post.
- Skill already forbade menus and quiet tables; **compliance** is the defect class, not missing product intent.
- **Soft prompt seed failed** on 2026-07-22: hourlies use new prompt text (`All markets quiet` in job message) but still emit multi-symbol dumps and “Would you like me to” menus.
- Open job 07:30 MT completed with **empty `response`** in run artifact (status later `ok`) — delivery reliability still uneven.
- Watcher bug: captured runs while `status=queued` / empty response → false “attention_ok”.
- Cron turns remain slow (~4–12+ minutes); truncation/empty-response retries still occur.

---

## 6. Issues & Tickets

### Resolved this session
- _None fully closed._ Principle + filing + seed only.

### Deferred
- **Runtime attention enforcement** for snapshot cron (length/menu rewrite or structured format) — soft text failed post-seed. See `docs/tickets/2026-07-21-cromwell-hourly-telegram-attention-discipline.md`.
- **Memory scrub** `path/to/file.txt` — still open.
- **Empty open response** 2026-07-22 07:42 run artifact — investigate separately if Telegram also blank.
- **Watcher tooling** — wait for `status=ok` + non-empty response before scoring.
- Unrelated dirty trees (`winston_v2` desk polish, other ecosystem docs) — **not** this session.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Principle §12 | File review | ✅ |
| Skill/cron text post-seed | Workspace `jobs.json` + skill read | ✅ messages include quiet one-liner |
| Seed + nanobot restart | Compose restart, MCP connect | ✅ 2026-07-21 ~16:20 MT |
| Jul 21 cadence | `cron/runs` + podman logs | ✅ all slots MCP + completed |
| Jul 21 attention quality | Telegram/run text | ❌ verbose quiet + menus |
| Jul 22 post-seed natural hourlies | `cron/runs` 08–11 MT | ⚠️ fire OK; content still verbose/menus |
| Overnight watcher scoring | log | ⚠️ raced queued/empty (false heuristic) |

**Test command(s):**  
`bin/seed-cromwell-workspace --force-cron`  
`./bin/compose --profile ai restart nanobot_cromwell`  
`ls -lt ai/data/cromwell-bot/workspace/cron/runs/market-snapshot-*`

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new  
- **Services:** `nanobot_cromwell` restarted; stack already up  
- **Migrations:** None  
- **Runtime seed:** `ai/data/cromwell-bot/workspace` (skills, cron merge); not git  

---

## 9. Risks & Technical Debt

- Operators learn to ignore Sawtooth Main while quiet dumps continue.
- Soft-only controls create false “fixed after seed” confidence.
- Empty open response risks silent duty fail with `status: ok`.
- Unrelated uncommitted ecosystem/Wv2 work can be accidentally mixed into wrap commits — **must use path-scoped add**.

---

## 10. Open Questions

- **Does Telegram show empty when open run `response` is empty?** — check Sawtooth Main; blocks confirm-ticket close.
- **Runtime rewrite vs model upgrade** for snapshot-only cron — needs product call if rewrite still insufficient.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Principle + cluster filed; seed live; Jul 22 hourlies prove soft path insufficient; wrap selective commit next.
- **Next concrete step:** Implement **runtime** quiet/mover formatting (or hard post-filter) on attention-discipline ticket; re-observe one natural hourly.
- **Files to read first:**
  1. `ecosystem/principles/01_core_principles.md` §12  
  2. `ecosystem/docs/tickets/2026-07-21-cromwell-hourly-telegram-attention-discipline.md`  
  3. `ecosystem/docs/issues/2026-07-21-cromwell-hourly-verbose-quiet-attention-waste.md`  
  4. `ecosystem/ai/skills/winston-market-snapshot/SKILL.md`  
  5. This report §5 / §7 Jul 22 results  

---

## 12. Stakeholder Communications

- Principal: Hourlies *are* firing; problem is **attention quality**, not silence. Soft fix deployed; still dumping. Runtime next.

---

## 13. Tools & Workflow Notes

- **Skills used:** record (implicit), session-report, wrap  
- **What worked well:** Full-day `cron/runs` table beat memory of “last post 10:21”; path-scoped wrap critical with multi-session dirt.  
- **Friction points:** Session background task 10h max vs overnight watch; watcher scored too early; `git add .` would be dangerous.  
- **Subagent usage:** none  

---

## 14. Follow-up Actions

- [ ] Runtime enforcement for quiet one-liner / no-menu snapshot posts — owner: eng — due: next session — See: `docs/tickets/2026-07-21-cromwell-hourly-telegram-attention-discipline.md`  
- [x] Update observe ticket with Jul 22 post-seed fail evidence — done in wrap  
- [ ] Scrub Cromwell `path/to/file.txt` permanent memory — See: `docs/tickets/2026-07-13-cromwell-scrub-placeholder-path-memory.md`  
- [ ] Empty open `response` vs `message` tool — ticket: `docs/tickets/2026-07-22-cromwell-snapshot-open-empty-response-artifact.md`  
- [ ] Fix overnight watcher false-positive — ticket: `docs/tickets/2026-07-22-cromwell-snapshot-watcher-queued-false-positive.md`  
- [ ] Do **not** commit unrelated `winston_v2` / other ecosystem WIP in this wrap  

---

## 15. Appendix

### Cluster map

| # | Artifact | Role |
|---|----------|------|
| 1 | `docs/tickets/2026-07-09-confirm-cromwell-hourly-telegram.md` | Delivery |
| 2 | `docs/tickets/2026-07-13-cromwell-scrub-placeholder-path-memory.md` | Memory |
| 3 | `docs/tickets/2026-07-13-observe-cromwell-market-snapshot-hourlies.md` | Live MCP + quality |
| 4 | `docs/tickets/2026-07-21-cromwell-hourly-telegram-attention-discipline.md` + issue | Attention |

### Jul 22 post-seed sample (hourly 08:07)

- Prompt includes hard `All markets quiet.` language.  
- Response: multi-paragraph intraday dump + menu (attention fail).  
- Later slots 09–11 MT same class; 11:07 still has menu.  

### Watcher

- Log: `ecosystem/logs/watch-market-snapshot-next.log` (gitignored).  
- Captured open/hourly at fire time while still `queued` / empty.  
