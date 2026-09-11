---
name: wrap
description: >
  End-of-session wrap-up — session report, Graphify Graph refresh (ADR-014),
  then commit and push. Use when the user says "/wrap", "wrap up the session",
  or wants a clean handoff before starting fresh. Optionally skip merge with
  "no-merge".
metadata:
  short-description: "Session report + graph refresh + commit + push"
---

# /wrap — End-of-Session Wrap-Up

Wrap up this session for a clean restart. Do these in order; stop and ask if any step is ambiguous.

## Steps

1. **Session report** — Run the `session-report` skill. Save to `docs/session-reports/`. Fill **Graphify Graph** / **Ponytail flags** after step 2 if they were still pending.
2. **Graphify Graph (ADR-014)** — Keep the map current. See below. Do this before commit.
3. **Follow-up promotion** — Interactive backlog capture from the report (see below). Do not skip silently; always offer this step before commit.
4. **Commit** — Stage only files this session actually touched (never `git add .` — avoids secrets and build artefacts). Commit with a clear message. Do **not** stage `graphify-out/` unless the user asked to pin the map.

   In this multi-monolith workspace, traverse by monolith (see "Multi-monolith / independent git repos" section below). Use precise relative paths under each monolith's git root.
5. **Push** — Push the branch. If a PR is open, push to it; otherwise ask before opening a new one.
6. **Merge (unless `no-merge`)** — If the user passed `no-merge`, stop after push. Otherwise follow the repo's branching conventions in `CONTRIBUTING.md` or `AGENTS.md`.
7. **Cleanup** — If using a worktree, remove it and delete the local branch after merge. Confirm `git worktree list` and `git branch` are clean.
8. **Final state** — Report in three lines: branch status, worktree status, what is on the target branch. Include one line: Graphify Graph updated / skipped / missing.

## Step 2 — Graphify Graph (ADR-014)

Skill `graphify-ponytail`. The graph is the map for the *next* session; wrap is when it must not go stale.

Skip only if this session changed **neither** code **nor** contractor docs (`ecosystem/` markdown, plans, ADRs, skills). If skipped, write `skipped: no code-doc changes` in the session report.

Otherwise:

1. For each touched top-level repo that has `graphify-out/graph.json` (`ecosystem`, `data_manager`, `winston_unit_test`, `winston_v2`, `broker_gateway`, `ai`): run `graphify update ./<repo>` (AST, no LLM). If the graph is **missing** and this session added substantial code, say so in the report — do **not** silently `/graphify` a full 12k-node rebuild.
2. If workspace `graphify-out/graph.json` exists and any per-repo graph was updated, re-merge the graphs that exist:

```bash
graphify merge-graphs \
  ./ecosystem/graphify-out/graph.json \
  ./data_manager/graphify-out/graph.json \
  ./winston_unit_test/graphify-out/graph.json \
  ./winston_v2/graphify-out/graph.json \
  ./broker_gateway/graphify-out/graph.json \
  ./ai/graphify-out/graph.json \
  --out graphify-out/graph.json
```

   Omit paths that do not exist. If the shrink-guard refuses to overwrite, record it in the report; do not `--force` unless the user asked.
3. **Ponytail flag (one paragraph, no extra rewrite):** from this session's diff plus `graphify god-nodes` or a query of the changed symbols, note any new helper that already exists on the graph. Put flags in the session report. Do **not** start a harmonize rewrite during wrap unless the user said `/graphify-ponytail` or "harmonize now".
4. Do **not** `git add` `graphify-out/` (local map) unless the user asked to pin it.
5. Patch the session report **Graphify Graph** and **Ponytail flags** lines with what actually ran.

## Step 3 — Follow-up promotion (interactive)

After the session report is saved (and the Graphify line filled), collect every actionable deferral from **§6 Deferred** and **§14 Follow-up Actions**. Present them as a numbered list (one line each).

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

## Multi-monolith / independent git repos (this workspace)

The sawtooth root is a **workspace**, *not* a single git repo.

Each majestic monolith (`winston_unit_test/`, `data_manager/`, `winston_v2/`, `winston/`, etc.) is its own independent git repository.

- `git` commands at the root will fail or see nothing ("no .git at root").
- Correct pattern: `cd <monolith> && git ...` **or** use `GIT_DIR=<monolith>/.git GIT_WORK_TREE=<monolith> git ...`
- When wrapping:
  1. The agent maintains the exact list of files it edited this session (from search_replace + write calls).
  2. Group those files by top-level monolith directory.
  3. For each monolith:
     - Attempt `cd <monolith> && git add <only the relative files from this session> && git commit ...`
     - If the terminal environment does not reflect the edits as dirty (common with container bind-mounts + agent FS layers), fall back to printing a clean "Run on your host shell" block with the precise commands.
  4. The `ecosystem/` tree (plans, reports, CONTEXT.md, etc.) sits outside the monolith gits. Wrap will always emit a separate note/command for committing reports/docs from the workspace/host shell.

Never do broad `git add .` or `git add -A`. Always use the precise per-session file list. Never add `graphify-out/` unless asked.

## Usage

```
/wrap
/wrap no-merge
```
