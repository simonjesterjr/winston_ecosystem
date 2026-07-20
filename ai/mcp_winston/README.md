# Winston MCP server (`mcp_winston`)

Thin HTTP/SSE MCP delegator for Cromwell / nanobot. Calls DM, WUT, and Wv2 `/internal/*` over the compose network only — no direct DB.

**Git home:** `ecosystem/ai/mcp_winston` in `winston_ecosystem` (not a separate monolith).

## Build / run

```bash
# From sawtooth workspace root
./bin/compose --profile ai build winston_mcp
./bin/compose --profile ai up -d winston_mcp
```

Compose build context: `./ecosystem/ai/mcp_winston` (see root `compose.yml`).

## Package layout

| Path | Role |
|------|------|
| `mcp_winston/server.py` | Tool surface + monolith HTTP |
| `mcp_winston/errors.py` | Structured MCP errors / retry guidance |
| `mcp_winston/audit.py` | Correlation + audit JSONL |
| `pyproject.toml` | Package metadata |
| `Containerfile` | Image for `winston_mcp` service |

## Contract docs

Human/agent tool contracts live in `ecosystem/interfaces/winston-mcp-tools.md`. Keep server tool names and that interface in sync.

## Dev notes

- Prefer commits here over editing a host-only copy under workspace `ai/mcp_winston/` (deprecated path).
- Optional live bind-mount for debug: uncomment volume in `compose.yml` (`./ecosystem/ai/mcp_winston:/app`).
