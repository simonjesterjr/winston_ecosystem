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
2. **Commit** — Stage only files this session actually touched (never `git add .` — avoids secrets and build artefacts). Commit with a clear message.
3. **Push** — Push the branch. If a PR is open, push to it; otherwise ask before opening a new one.
4. **Merge (unless `no-merge`)** — If the user passed `no-merge`, stop after push. Otherwise follow the repo's branching conventions in `CONTRIBUTING.md` or `AGENTS.md`.
5. **Cleanup** — If using a worktree, remove it and delete the local branch after merge. Confirm `git worktree list` and `git branch` are clean.
6. **Final state** — Report in three lines: branch status, worktree status, what is on the target branch.

## Guardrails

- If there is uncommitted or unpushed work you cannot account for, STOP and show `git status` before deleting branches or worktrees.
- Never delete the branch you are currently on without switching first.
- Cross-monolith work: commit in each repo that was touched; session report goes in `ecosystem/docs/session-reports/`.

## Usage

```
/wrap
/wrap no-merge
```