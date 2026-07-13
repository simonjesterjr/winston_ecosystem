# Session Report — Cromwell Telegram `path/to/file.txt` Incident

**Date:** 2026-07-13
**Time:** ~11:50–12:16 MDT
**Duration:** ~25m
**Project:** Sawtooth ecosystem (Cromwell / nanobot runtime diagnosis)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` (ecosystem)
**Model:** Grok
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Explain a Telegram message seen at 9:12 AM: file `path/to/file.txt` not found; decide if it needs resolution, next steps, ticket.

**Outcome:** Delivered

**One-line summary:** Root-caused the 9:12 AM Sawtooth Main message to a Cromwell market-snapshot cron LLM death spiral after output truncation (placeholder `read_file`, not a missing ops file); filed Open issue with evidence and remediations.

---

## 2. Work Completed

- Matched Telegram text to nanobot session + container logs at **15:12 UTC / 09:12 MDT**
- Traced full failure stack for `market-snapshot-hourly` (MCP OK → truncation → 8× `path/to/file.txt` → human-facing ask)
- Noted secondary `dream` path bugs and same-day hallucinated hourly “completions” without tool calls
- Filed issue via `/record` (user chose issue over ticket/both)
- Documented that no capital/mutation path was involved

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md` | added | Open issue — forensic trace + remediation list |
| `docs/session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md` | added | This report |

### Commits

- `1a97a63` — docs: file Cromwell path/to/file.txt cron hallucination issue and tickets

### Branch / PR state at sign-off

- Branch: `ecosystem` `main` — clean after wrap push
- Pushed: yes (`origin/main` @ `1a97a63`)
- PR: not opened (direct main workflow)

---

## 4. Decisions Made

### Decision 1: File as issue, not ticket
- **Choice:** `docs/issues/` with **Open** status; full root-cause trace
- **Why:** One-line test “Something is wrong; here's the trace.” User selected Issue over Ticket only / Both
- **Alternatives considered:** Ticket-only backlog item; issue + hardening ticket
- **Reversibility:** easy (can spawn ticket from issue later)
- **Promote to ADR?** no

### Decision 2: No emergency filesystem fix
- **Choice:** Do not create or chase `path/to/file.txt`
- **Why:** Literal LLM placeholder after truncation; MCP snapshot already succeeded
- **Alternatives considered:** Treat as missing workspace file
- **Reversibility:** n/a
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- **Cron “completed” ≠ duty done:** nanobot marks jobs complete even when the agent abandoned the required MCP format path.
- **Truncation recovery is a failure mode** on `cromwell-qwen2.5:3b`: after `Output truncated on turn 1`, the model looped on docs-style paths instead of summarizing tool output.
- **Memory poison:** idle compact wrote the placeholder error as permanent history (`history.jsonl` cursor 61).
- **Same-day quality regression:** 10:00 and 11:00 MT hourlies posted “stable market” with **no** `wv2_market_snapshot` tool call.
- **Dream paths still brittle:** tries workspace-root `MEMORY.md` though truth is `memory/MEMORY.md`; invents `ECOSYSTEM_STATUS.md`.

---

## 6. Issues & Tickets

### Resolved this session
- Investigation complete; filed `docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md` (**Open**)

### Deferred
- Memory scrub of cursor-61 / placeholder permanent facts — See: `docs/tickets/2026-07-13-cromwell-scrub-placeholder-path-memory.md`
- Circuit-break / require MCP / no path-asks on cron — See: `docs/tickets/2026-07-13-cromwell-cron-hallucination-hardening.md`
- Dream path hygiene — See: `docs/tickets/2026-07-13-cromwell-dream-memory-path-hygiene.md`
- Observe next natural hourlies — See: `docs/tickets/2026-07-13-observe-cromwell-market-snapshot-hourlies.md`
- Align Jul 9 timeout ticket acceptance with this incident — See: `docs/tickets/2026-07-13-extend-cron-llm-timeout-acceptance.md`
- Related open quality tickets still open:
  - `docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`
  - `docs/tickets/2026-07-09-cromwell-cpu-only-llm-tuning.md`

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Telegram message origin | Session JSONL + `podman logs nanobot_cromwell` | ✅ Matched 09:12 MDT |
| MCP call at 09:00 | Logs: `mcp_winston_wv2_market_snapshot({})` | ✅ Invoked |
| Placeholder loop | 8× `read_file path/to/file.txt` in logs + session | ✅ Confirmed |
| Memory poison | `history.jsonl` cursor 61 | ✅ Confirmed |
| Later hourlies tool-free | Logs 16:00 / 17:00 UTC — Response with no Tool call | ✅ Confirmed |
| Fix applied | — | ❌ Investigation only |

**Test command(s):**  
`podman logs --since "2026-07-13T14:50:00" --until "2026-07-13T16:00:00" nanobot_cromwell`  
`read` session files under `ai/data/cromwell-bot/workspace/sessions/`

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None changed
- **Services:** Observed existing stack (`nanobot_cromwell` Up 3 days); no restarts this session
- **Migrations:** None

---

## 9. Risks & Technical Debt

- Cron quality debt on small CPU model: timeouts (Jul 9 ticket) + post-truncation hallucination (this issue)
- Permanent memory pollution can bias future consolidations
- Trust erosion if Sawtooth Main keeps getting non-ops agent chatter

---

## 10. Open Questions

- **Should hardening be a new ticket or extend `2026-07-09-cromwell-cron-llm-timeout`?** — needs answer from: operator; blocks: backlog shape only
- **Is structured post-processing of snapshot JSON preferable to free-form LLM formatting?** — needs answer from: design session; blocks: longer-term fix scope

---

## 11. Handoff & Resume Notes

- **Where I left off:** Issue filed; wrap in progress
- **Next concrete step:** Promote deferred remediations to ticket(s) if desired; scrub Cromwell memory; watch next natural hourly for real tool call + clean text
- **Files to read first:**
  1. `ecosystem/docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md`
  2. `ai/data/cromwell-bot/workspace/sessions/telegram_-1003884714483.jsonl`
  3. `ecosystem/docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`

---

## 12. Stakeholder Communications

- Optional one-liner for team: “9:12 AM Telegram path error was Cromwell misbehaving after a truncated hourly snapshot — not a missing file; logged as open issue.”

---

## 13. Tools & Workflow Notes

- **Skills used:** `record`, `session-report` (via `/wrap`), `ask_user_question` for bucket choice
- **What worked well:** Runtime session JSONL + `podman logs` gave exact 9:12 match; memory cursor confirmed side effect
- **Friction points:** None material
- **Subagent usage:** None

---

## 14. Follow-up Actions

- [ ] Scrub permanent memory entry for `path/to/file.txt` — See: `docs/tickets/2026-07-13-cromwell-scrub-placeholder-path-memory.md`
- [ ] Harden cron against post-truncation hallucination — See: `docs/tickets/2026-07-13-cromwell-cron-hallucination-hardening.md`
- [ ] Fix dream routing to `memory/MEMORY.md` — See: `docs/tickets/2026-07-13-cromwell-dream-memory-path-hygiene.md`
- [ ] Observe next natural market-snapshot hourlies — See: `docs/tickets/2026-07-13-observe-cromwell-market-snapshot-hourlies.md`
- [ ] Extend Jul 9 cron LLM timeout acceptance criteria — See: `docs/tickets/2026-07-13-extend-cron-llm-timeout-acceptance.md`

---

## 15. Appendix (optional)

**Telegram message (verbatim):**

> It seems that the file path/to/file.txt was not found. Could you please provide the correct file path so I can attempt reading the file again?

**Key log lines (UTC 2026-07-13):**

```
15:00:00 Cron: executing job 'market-snapshot-hourly'
15:01:07 Tool call: mcp_winston_wv2_market_snapshot({})
15:02:37 Output truncated on turn 1 for telegram:-1003884714483 (1/3); continuing
15:03:44–15:11:32 Tool call: read_file({"path": "path/to/file.txt"})  # ×8
15:12:40 Response to telegram:cron: It seems that the file `path/to/file.txt` was not found...
15:12:40 Cron: job 'market-snapshot-hourly' completed
```
