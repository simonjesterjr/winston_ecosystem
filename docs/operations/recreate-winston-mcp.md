# Recreate `winston_mcp` after tool schema changes

## When

MCP tools were added/renamed/removed, `tools_schema.py` or server wiring changed, or compose shows stale tools / missing ops demo tools. Also after large `ecosystem/ai/mcp/` edits.

## Why

The MCP container does not always pick up schema changes from a soft restart. Operators have hit “tool missing” and off-duty tool noise when the process still runs an old registry.

## Steps (local compose)

From sawtooth root:

```bash
# 1. Ensure code/assets are current (seed if Cromwell workspace also changed)
bin/seed-cromwell-workspace   # if skills/schedule/allowlist changed

# 2. Recreate MCP (name may vary — confirm with compose ps)
bin/compose ps | grep -i mcp
bin/compose up -d --force-recreate winston_mcp
# If the service name differs in compose.yml, use that name.

# 3. Health
bin/compose ps
# optional:
bin/test-mcp-audit-smoke
```

If the image embeds the MCP package rather than a bind mount, **rebuild** the image before recreate:

```bash
bin/compose build winston_mcp
bin/compose up -d --force-recreate winston_mcp
```

## Verify

- Tool list includes the expected new tools and excludes removed ones.
- A forbidden cron tool still fails closed when allowlist is in play (`ecosystem/ai/schedule/cron-tool-allowlist.json`).
- Audit JSONL still receives `correlation_id` (ADR-004) — `bin/test-mcp-audit-smoke`.

## Related

- Tickets: MCP recreate / ops demo tools (see `docs/tickets/` and archive)
- Skill: `ship-to-test`
- Interface: `interfaces/winston-mcp-tools.md`
