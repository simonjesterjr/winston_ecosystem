# Ecosystem MCP layer

This directory is the **MCP access layer** for the Winston ecosystem (Cromwell / nanobot → monoliths).

It is intentionally named **`mcp`**, not `mcp_winston`: ecosystem AI is exercised through MCP as a whole. Winston-specific tools are one package inside that layer.

## What lives where

```text
ecosystem/ai/mcp/                 ← MCP layer (compose build context, this folder)
  Containerfile                   ← builds the winston_mcp service image
  pyproject.toml                  ← Python project metadata
  README.md                       ← you are here
  mcp_winston/                    ← Python package: Winston (Wv2/WUT/DM) tools
    __init__.py
    server.py                     ← tool surface + HTTP to /internal/*
    errors.py
    audit.py
    …
```

| Path | Meaning |
|------|---------|
| **`ecosystem/ai/mcp/`** | **MCP layer root** — image build context, packaging, docs. “The MCP layer for ecosystem + AI.” |
| **`mcp_winston/`** (inner) | **Importable package** for Winston monolith access (`import mcp_winston`). Tools that talk to Wv2, WUT, and DM. |
| **Service name `winston_mcp`** | Compose/container name for the running MCP process (historical name; still correct). |

So:

- **Layer** = `mcp` (this tree)
- **Winston access package** = `mcp_winston` (nested package)
- **Edit tools here:** `ecosystem/ai/mcp/mcp_winston/server.py`

The double path is deliberate, not a duplicate folder mistake: outer name = layer, inner name = Winston package.

## Build / run

```bash
# From sawtooth workspace root
./bin/compose --profile ai build winston_mcp
./bin/compose --profile ai up -d winston_mcp
```

Compose build context: `./ecosystem/ai/mcp` (see root `compose.yml`).

Image entrypoint runs: `uvicorn mcp_winston.server:asgi_app …` (the **package** name).

## Package layout (inner)

| Path | Role |
|------|------|
| `mcp_winston/server.py` | Tool surface + monolith HTTP |
| `mcp_winston/errors.py` | Structured MCP errors / retry guidance |
| `mcp_winston/audit.py` | Correlation + audit JSONL |
| `pyproject.toml` | Declares package `mcp_winston` |
| `Containerfile` | Image for compose service `winston_mcp` |

## Contract docs

Human/agent tool contracts: `ecosystem/interfaces/winston-mcp-tools.md`. Keep tool names in the package and that interface in sync.

## Dev notes

- Git home: this tree under `winston_ecosystem` (`ecosystem/ai/mcp/`).
- Optional live bind-mount: uncomment volume in `compose.yml` (`./ecosystem/ai/mcp:/app`).
- Workspace path `ai/mcp_winston/` is a legacy pointer only — do not edit code there.
