# Winston topology poster — DSL sketch

**Source of intended nodes:** `ecosystem/ecosystem_view/catalog/runtime.yaml`  
**Canonical compose:** repo-root `compose.yml` (not `ecosystem/deployment/compose.yml`)  
**Render:** `docs/poster/winston-topology.svg` (Isoflow-style isometric cuboids on a diamond grid)  
**Viewer:** `docs/poster/index.html` (pan / zoom)  
**FossFLOW import:** `docs/poster/winston-topology.fossflow.json`  
**Served on Wv2:** `winston_v2/public/ecosystem/winston-topology.svg` via `/operations/ecosystem`  
**Regenerate:** `python3 ecosystem/ecosystem_view/bin/render_poster`  
**Not live metrics.** Regen when topology or ADRs change.

```
poster winston {
  island dm  "data_manager"   port=3001 {
    box postgres          image=postgres:16  host=5432
    box data_manager      rails              host=3001
    box data_manager_sidekiq  sidekiq        redis_db=0
    volume parquet        sawtooth_dm_data
  }
  island wut "winston_unit_test" port=3000 {
    box wut_postgres      image=postgres:16  host=5433
    box winston_unit_test rails              host=3000
    box winston_unit_test_sidekiq sidekiq    redis_db=1
  }
  island wv2 "winston_v2" port=3002 {
    box wv2_postgres      image=postgres:16  host=5434
    box winston_v2        rails              host=3002
    box winston_v2_sidekiq sidekiq           redis_db=2
  }
  island bg  "broker_gateway" port=3003 {
    box bg_postgres       image=postgres:16  host=5435
    box broker_gateway    rails              host=3003
    box broker_gateway_sidekiq sidekiq       redis_db=3
    volume evidence       sawtooth_bg_evidence
  }
  infra redis redis:7-alpine host=6379
  host  ibkr_cpgw            :5000   # not a container
  vendor eodhd  owner=dm
  vendor quiver owner=dm   # env template; not a compose service
  vendor schwab owner=bg   # adapter; no compose service
  wing ai profile=ai {
    ollama
    winston_mcp           expose=8088
    nanobot_cromwell      host=127.0.0.1:18790
    open-webui            host=127.0.0.1:8080
  }

  edge dm --> eodhd          http     adr=ADR-002
  edge dm --> parquet        file     adr=ADR-002
  edge dm --> wut            webhook  data_ready
  edge dm --> wv2            webhook  data_ready
  edge wut --> wv2           file     portfolio_configs
  edge wut --> wv2           http     PCS snapshots adr=ADR-007
  edge wv2 --> bg            http     Confirmation Intake fail-closed adr=ADR-009
  edge bg  --> ibkr_cpgw     http
  edge bg  --> schwab        http
  edge wv2 --> winston_mcp   http     /internal
  edge winston_mcp --> nanobot_cromwell sse
}

absent: hdf5, s3, otel_collector, codescene, dragonruby, fossflow, k8s
```

ADR chips on edges: **decided** (001, 002, 003, 006, 007, 009, 012, 013) | **superseded** (none for these edges).
