---
name: wrap
description: >
  End-of-session wrap-up — session report, then commit and push. Use when the
  user says "/wrap", "wrap up the session", or wants a clean handoff before
  starting fresh. Optionally skip merge with "no-merge".
metadata:
  short-description: "Session report + commit + push"
---

# /wrap — End-of-Session Wrap-Up

Wrap up this session for a clean restart. Do these in order; stop and ask if any step is ambiguous.

## Steps

1. **Session report** — Run the `session-report` skill. Save to `docs/session-reports/`.
2. **Follow-up promotion** — Interactive backlog capture from the report (see below). Do not skip silently; always offer this step before commit.
3. **Commit** — Stage only files this session actually touched (never `git add .` — avoids secrets and build artefacts). Commit with a clear message.
4. **Push** — Push the branch. If a PR is open, push to it; otherwise ask before opening a new one.
5. **Merge (unless `no-merge`)** — If the user passed `no-merge`, stop after push. Otherwise follow the repo's branching conventions in `CONTRIBUTING.md` or `AGENTS.md`.
6. **Cleanup** — If using a worktree, remove it and delete the local branch after merge. Confirm `git worktree list` and `git branch` are clean.
7. **Final state** — Report in three lines: branch status, worktree status, what is on the target branch.

## Step 2 — Follow-up promotion (interactive)

After the session report is saved, collect every actionable deferral from **§6 Deferred** and **§14 Follow-up Actions**. Present them as a numbered list (one line each).

**Open with shortcuts** — ask once before walking items:

> I found N follow-up items in the session report. Reply with a shortcut, or I'll ask one at a time:
> - **`create all tickets`** — file each item as `docs/tickets/YYYY-MM-DD-<slug>.md` (confirm bucket with user if ambiguous)
> - **`create all tasks`** — append each item to the relevant `*.tasks.json` (default: infer plan from session context; ask if unclear)
> - **`skip all`** — leave items in the session report only; proceed to commit
> - **`ask`** (default) — walk items one at a time

**Per item** (when not using a bulk shortcut), ask exactly:

> **Item k/N:** \<one-line summary\>
> Do you want to create a **ticket**, add a **task** (plan `.tasks.json`), **link** an existing artifact, or **skip**?

Interpret replies flexibly: "yes" → ticket; "task" / "plan" → `.tasks.json`; "link #foo" → cross-link in report §6/§14 and ticket; "no" / "skip" → leave in report only.

**When creating artifacts:**

- **Ticket** — run the `record` skill (`docs/tickets/`, `Status: Proposed`). Cross-link from the session report §6 or §14.
- **Task** — append to `{plan}.md.tasks.json` with next sequential `id`, `status: "pending"`, and a `note` citing the session report path. Cross-link from the report.
- **Link** — add `See: docs/tickets/...` or `plans/...tasks.json#id` to the report item; do not duplicate content.

**Already tracked?** If an item is clearly done or already filed (e.g. cron repurpose completed, task marked completed in `.tasks.json`), say so and offer: skip, update existing ticket/task status, or file anyway for redesign scope.

**After promotion** — summarize: created tickets, updated tasks, skipped items. Then continue to commit unless the user says `no-merge` or wants to stop.

## Guardrails

- If there is uncommitted or unpushed work you cannot account for, STOP and show `git status` before deleting branches or worktrees.
- Never delete the branch you are currently on without switching first.
- Cross-monolith work: commit in each repo that was touched; session report goes in `ecosystem/docs/session-reports/`.

## Usage

```
/wrap
/wrap no-merge
```