# Ticket: Rootless Podman NVIDIA CDI cleanup (ollama)

**Status:** Proposed  
**Date:** 2026-09-16  
**Priority:** P3 — Nice-to-have / cleanup  
**Source:** Session `docs/session-reports/2026-09-16-1955-rtx3090-ollama-cuda.md`

## Problem

NVIDIA Container Toolkit CDI is installed and generates a valid spec (`sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml`; `nvidia-ctk cdi list` → `nvidia.com/gpu=0|UUID|all`). Rootless Podman **5.8.0** still fails with:

`setting up CDI devices: unresolvable CDI devices nvidia.com/gpu=all`

Tried: `enable_cdi = true`, explicit `cdi_spec_dirs` (`/etc/cdi`, `/var/run/cdi`, `~/.cdi`), copies under `$XDG_RUNTIME_DIR/cdi`. Spec still not resolved at `podman run --device nvidia.com/gpu=all`.

## Current workaround (shipped)

Host `sawtooth/compose.yml` `ollama` service (mirrored at `deployment/workspace-compose.yml`):

- `devices:` `/dev/nvidia0`, `nvidiactl`, `nvidia-uvm`, `nvidia-uvm-tools`, `nvidia-modeset`
- Bind-mount host driver libs + `nvidia-smi` (versioned `.so.595.91.07` paths)
- Env: `NVIDIA_VISIBLE_DEVICES=all`, `NVIDIA_DRIVER_CAPABILITIES=compute,utility`

Verified: Ollama logs `inference compute … library=CUDA … RTX 3090 … 24.0 GiB`; probe offloaded 37/37 layers (~3.6 GiB VRAM).

## Why cleanup matters

1. Driver upgrades rename `/usr/lib/.../libcuda.so.595.*` → compose mounts break until paths are updated.
2. CDI is the supported long-term path for Podman + NVIDIA.
3. Classic mounts are more brittle under SELinux / read_only hardening.

## Scope

- [ ] Diagnose why Podman 5.8 rootless does not load `/etc/cdi/nvidia.yaml` (parse error? tags? cdiVersion 0.7.0? socket service not seeing user conf?)
- [ ] Prefer fix: `podman run --device nvidia.com/gpu=all` works without manual `.so` mounts
- [ ] Switch `ollama` compose from classic devices+lib binds → CDI device only
- [ ] Re-verify GPU discovery + layer offload
- [ ] Update `deployment/README.md` + `ai/README.md`; refresh `deployment/workspace-compose.yml` mirror
- [ ] Note driver-upgrade checklist if any residual binds remain

## Out of scope

- Switching Cromwell default model size (separate decision)
- Docker Engine / rootful Podman migration

## Acceptance

- [ ] `podman run --rm --device nvidia.com/gpu=all …` resolves CDI
- [ ] `ollama` compose no longer hard-codes driver soname paths
- [ ] Docs match the CDI path

## Related

- Hardware ticket (superseded by install): `docs/tickets/archive/2026-07-09-thelio-discrete-gpu-for-ollama.md`
- Compose versioning: `docs/tickets/2026-07-17-version-workspace-compose-yml.md`
- Ops: `deployment/README.md` · mirror `deployment/workspace-compose.yml`
