---
name: session-report
description: >
  Generate a thorough, audit-grade Grok session report before ending a session.
  Use when the user says "wrap up", "end session", "session report", "/wrap",
  "save this session", "close out", or asks for a handoff doc or recap.
  Every session that produced code or decisions gets a report saved to
  docs/session-reports/.
metadata:
  short-description: "Audit-grade end-of-session report"
---

# Grok Session Report

Produce a high-signal, audit-grade report of the work performed in this session. The report is for three audiences: future-you resuming the work, another human or agent inheriting it, and stakeholders auditing what changed.

## When to invoke

- Explicit: "wrap up", "end session", "session report", "/wrap", "save the session", "close this out".
- Implicit: the user shifts context, says "thanks, that's all", or signals they're done.
- Defensive: if a session produced code, decisions, or insights and the user is leaving, offer to generate the report.

If unsure, ask once: "Full session report saved to `docs/session-reports/`, or just a quick recap inline?"

## File location and naming

Save to: `docs/session-reports/YYYY-MM-DD-HHMM-<slug>.md`

- `YYYY-MM-DD-HHMM` — local date and time the session ended (24-hour, no colon in time, e.g. `2026-06-30-1430`).
- `<slug>` — short kebab-case description, 2–5 words.

Create `docs/session-reports/` if missing. On name collision, append `-v2`, `-v3`, etc.

**Cross-monolith sessions:** if work spanned multiple repos, save the report in `ecosystem/docs/session-reports/` and note which monoliths were touched.

## How to gather content

1. Re-read the conversation from session start.
2. Run `git status` and `git log --oneline` if in a git repo.
3. List files touched from tool-call history.
4. Check unfinished TODOs and deferred items.
5. Note environment changes (packages, migrations, compose services).

Don't fabricate. Mark uncertain claims as such.

## Report template

Fill every section. Empty sections get `_None._` — do not delete them.

```markdown
# Session Report — <Short Title>

**Date:** YYYY-MM-DD
**Time:** HH:MM–HH:MM <TZ>
**Duration:** ~Xh Ym
**Project:** <repo or project name>
**Working directory:** <absolute path>
**Branch:** <branch name> (started from `<base>`)
**Model:** <model name>
**Operator:** <name, optional>

---

## 1. Goal & Outcome

**Stated goal:** <what the session was for>

**Outcome:** <Delivered / Partially delivered / Blocked / Pivoted>

**One-line summary:** <stakeholder-readable summary>

---

## 2. Work Completed

- <concrete deliverable 1>
- <concrete deliverable 2>

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `path/to/file` | added/modified/deleted | <note> |

### Commits

- `<sha>` — <message>

### Branch / PR state at sign-off

- Branch: `<name>` — <clean / dirty>
- Pushed: <yes/no>
- PR: <#number or "not opened">

---

## 4. Decisions Made

### Decision 1: <name>
- **Choice:** <what>
- **Why:** <rationale>
- **Alternatives considered:** <brief>
- **Reversibility:** <easy / costly / one-way>
- **Promote to ADR?** <yes/no — Wave 2 will add ecosystem/docs/adr/>

---

## 5. Insights Surfaced

- <new observation about codebase, domain, or system>

---

## 6. Issues & Tickets

### Resolved this session
- <issue — fix, reference>

### Deferred
- <issue — why deferred, ticket to create>

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| <feature> | <test/smoke/manual> | ✅ / ⚠️ / ❌ |

**Test command(s):** `<exact command>`

---

## 8. Environment, Dependencies, Data

- **Dependencies:** <or None>
- **Services:** <compose services started, or None>
- **Migrations:** <or None>

---

## 9. Risks & Technical Debt

- <risk or debt item>

---

## 10. Open Questions

- **<Question>** — needs answer from: <source>; blocks: <what>

---

## 11. Handoff & Resume Notes

- **Where I left off:** <last action>
- **Next concrete step:** <first action when resuming>
- **Files to read first:** <ranked list>

---

## 12. Stakeholder Communications

- <who needs to know what — or _None._>

---

## 13. Tools & Workflow Notes

Lessons learned for future sessions (this is the primary "lessons learned" capture).

- **Skills used:** <list>
- **What worked well:**
- **Friction points:**
- **Subagent usage:**

---

## 14. Follow-up Actions

- [ ] <Action> — owner: <name> — due: <when>

---

## 15. Appendix (optional)

<error messages, URLs, investigation snippets>
```

## Quality bar

- Honest about verification gaps.
- Specific file paths and line references, not vague summaries.
- Sections 1, 2, and 11 must be skimmable in 30 seconds.
- Size the report to the session — short sessions get short reports.

## Non-negotiable sections

For any session that produced code or decisions: §1 Goal, §2 Work, §3 Code, §7 Verification, §11 Handoff.

## After saving

Tell the user the report path.

- If invoked as part of **`/wrap`**, defer follow-up filing to wrap **Step 2 — Follow-up promotion** (interactive ticket/task capture).
- If invoked standalone, offer:
  1. Walk §6 / §14 follow-ups one at a time (same prompts as wrap Step 2), or shortcuts `create all tickets` / `create all tasks` / `skip all`.
  2. Draft stakeholder messages from §12 (use `/stakeholder` skill).