# Ticket: Track AI runtime Containerfile + example config in git

**Status:** Proposed
**Context:** Session `docs/session-reports/2026-07-09-0736-cromwell-cron-telegram-fix.md` pinned `nanobot-ai==0.2.2` and added `tools.ssrf_whitelist` to the example config, but both live only under workspace `ai/` which has **no** `.git`. Only `ecosystem/ai/schedule/*` (and personas/skills) are versioned.

## Problem

Durable operator fixes (Containerfile pin, SSRF whitelist example) can be lost on machine rebuild or are invisible to other hosts. Live `ai/data/cromwell-bot/config.json` correctly stays local (Telegram token), but **example** + **Containerfile** should be recoverable.

## Acceptance criteria

- [ ] Decide home for versioned copies: e.g. `ecosystem/deployment/ai/` mirror, or a small tracked tree under `ecosystem/ai/runtime/`
- [ ] Commit `ai/nanobot/Containerfile` (or equivalent) with pinned `nanobot-ai` version
- [ ] Commit `ai/configs/nanobot-cromwell.example.json` with SSRF whitelist note (no secrets)
- [ ] Update `ecosystem/deployment/README.md` / `ai/README.md` seed path if paths move
- [ ] Explicitly keep `ai/data/cromwell-bot/config.json` untracked / gitignored

## Out of scope

- Committing real bot tokens or allowFrom production IDs
- Moving Cromwell workspace memory/sessions into git

## Related

- `docs/session-reports/2026-07-09-0736-cromwell-cron-telegram-fix.md`
- `ecosystem/deployment/README.md` (AI layer section)
- Workspace: `ai/nanobot/Containerfile`, `ai/configs/nanobot-cromwell.example.json`
