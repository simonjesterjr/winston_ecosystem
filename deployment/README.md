# Deployment & Podman for the Sawtooth Ecosystem

## Local Development (Current Target)
- Use podman (or podman-compose / podman compose).
- Root `sawtooth/compose.yml` (committed) defines the services: data_manager, winston_unit_test, redis (for Sidekiq), (later cromwell, winston_v2).
- Each monolith has a minimal Containerfile (or Dockerfile) in its directory or referenced from root.
- Volumes:
  - One (or more) for DM's `data/` parquet tree. WUT can mount it read-only for direct high-performance parquet access during dev.
  - Separate named volumes for each monolith's Postgres (metadata DBs are independent).
- Networking: containers can reach each other by service name for the internal APIs (e.g. WUT calls DM at http://data_manager:3000/... or the other way for discovery).
- Redis is shared (WUT already notes this in its docker-compose).

## Running
```bash
# From sawtooth/ root
podman compose up --build   # or podman-compose up
# In separate shells / detach as needed:
#   podman compose exec data_manager bin/rails console
#   podman compose exec data_manager bundle exec sidekiq
```

## Credentials & Config (EODHD Key etc.)
- User will supply the EODHD API key once this location exists.
- Place it according to the template below (or in per-app `config/credentials.yml.enc` / env files that the compose mounts).
- Never commit real keys. Use the templates in this directory.
- Inter-monolith tokens (for /api/internal/*) live in the same place or as compose secrets / env.

Example template file (create `eodhd.env.template` or similar and copy to a non-committed `eodhd.env`):

```
EODHD_API_KEY=your_key_here
# Also common ones:
# WUT_INTERNAL_API_TOKEN=...
# DM_INTERNAL_API_TOKEN=...
# REDIS_URL=redis://redis:6379/0
```

Compose can load these with `env_file:`.

## Data Volumes & Portability
- The parquet `data/` tree is the valuable artifact.
- In compose you can define a volume that maps to a host path if you want your real data to live outside containers.
- Reconciliation (in DM) + the fact that parquet is the source of truth means you can:
  - Stop everything
  - Drop or rsync parquet files into the volume
  - Bring DM back up (or run its reconcile rake)
  - PG metadata is now in sync; no unnecessary re-downloads.

## Production / Later
- Each monolith can be deployed independently (Fly, Render, k8s, etc.).
- The same principles apply: DM owns the parquet (object storage or persistent volume), exposes it, notifies Cromwell.
- Shared Redis or per-monolith Sidekiq + Redis is fine as long as the monoliths can reach each other for the internal APIs/webhooks.

## Relation to Existing Files
- `winston_unit_test/docker-compose.yml` is minimal and references a shared redis. It will be superseded / composed into the root `compose.yml`.
- DM will get its own Containerfile modeled on WUT's patterns.

See the approved data-manager plan and principles/ for more.
