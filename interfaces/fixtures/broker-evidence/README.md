# Winston Broker Evidence Standard — L1 contract fixtures

**Version:** aligned with `interfaces/winston-broker-evidence-standard.md` **v0.1**  
**Live broker:** none — these are static JSON for Wv2 ↔ Broker Gateway contract tests.

| File | Use |
|------|-----|
| `auth-status.json` | `auth.status` heartbeat (not match fuel) |
| `trade-executed-exact.json` | Equity/ETF fill for exact/soft match |
| `trade-executed-orphan.json` | Fill with no Winston intent |
| `trade-executed-extra-modal.json` | Signal underlying IBM, fill OCC LEAP |
| `order-canceled.json` | Order lifecycle (not auto-book) |
| `page-multi-event.json` | Pull API page: two events + `next_cursor` |
| `refresh-ok.json` | `POST …/refresh` success envelope |
| `refresh-auth-failed.json` | Fail-closed auth |

Consumers: `winston_v2` Confirmation Intake specs (copies under `spec/fixtures/broker-evidence`); Broker Gateway dummy_sim emits the same envelope at runtime.

Vendor-shaped Schwab JSON (before normalize) lives in [`../schwab/`](../schwab/) and `broker_gateway/lib/adapters/schwab/fixtures/`.  
Vendor-shaped Interactive Brokers JSON lives in [`../ibkr/`](../ibkr/) and `broker_gateway/lib/adapters/ibkr/fixtures/`.

Run (from `winston_v2/`):

```bash
bundle exec rspec spec/services/broker_gateway spec/services/confirmation_intake spec/requests/operations_confirmation_intake_spec.rb spec/requests/operations_desk_workflow_evidence_spec.rb
```
