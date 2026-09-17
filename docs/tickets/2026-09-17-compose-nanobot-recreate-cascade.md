# Ticket: podman-compose recreate of nanobot cascades core stack

**Status:** Proposed  
**Date:** 2026-09-17  
**Priority:** P2  
**Origin:** Wrap follow-up. Session `docs/session-reports/2026-09-17-1700-cromwell-llm-desk-and-daily-state.md`

## Problem

On sawtooth-ai, `./bin/compose --profile ai up -d --force-recreate nanobot_cromwell` **and** `./bin/compose --profile ai up -d nanobot_cromwell` after `podman rm nanobot_cromwell` both **stopped Redis, Winston v2, data_manager, Ollama, and MCP**, then failed to recreate some of those names (`container name already in use` / dependent containers). The stack recovered after compose retried, but Ollama dropped the resident 8b (cold-load ~28s) and End of Day cron can fire during the hole.

`ecosystem/ai/README.md` already says prefer replacing only those containers; the command that looks like “just nanobot” still cascades under this podman-compose.

## Scope

1. Document the safe recreate path (e.g. `podman stop/rm nanobot_cromwell` is not enough if the next `compose up` still walks depends_on; find a command that does **not** stop Redis/Wv2).
2. Add a one-paragraph ops note in `ecosystem/ai/nanobot/README.md` and/or `ecosystem/deployment/README.md`.
3. Optional: wrapper in `bin/` that rebuilds/recreates **only** `nanobot_cromwell` without touching monoliths.

## Non-goals

- Changing compose depends_on so nanobot can start without Ollama/MCP (health is real)
- CDI / GPU device path

## Acceptance

- [ ] Proven command that updates nanobot image without stopping Redis / Wv2 / Ollama (or an explicit “this will bounce the stack” banner)
- [ ] Docs match the command
- [ ] Session report / L1 ship notes point here

## Related

- L1 ship notes: [`2026-09-17-cromwell-daily-state-verifier.md`](2026-09-17-cromwell-daily-state-verifier.md)
- Session: [`../session-reports/2026-09-17-1700-cromwell-llm-desk-and-daily-state.md`](../session-reports/2026-09-17-1700-cromwell-llm-desk-and-daily-state.md)
- `ecosystem/ai/README.md` rebuild paragraph
