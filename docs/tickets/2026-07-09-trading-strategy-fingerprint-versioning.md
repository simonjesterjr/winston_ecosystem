# Ticket: TradingStrategy fingerprint payload versioning

**Status:** Proposed

**Date:** 2026-07-09

**Context:** Session [`2026-07-09-0833-trading-strategy-fingerprint-capture`](../session-reports/2026-07-09-0833-trading-strategy-fingerprint-capture.md). Fingerprint is SHA256 of canonical payload (implicit v1). **ADR-006** makes full fingerprint the Wv2 lineage match key — version bumps now also re-shard ops OP/TS pairs unless migrated.

## Problem

Adding fields to the fingerprint payload will re-shard identities (new hash for same real-world recipe), breaking “won on N portfolios” continuity and Wv2 same-fingerprint re-import matching unless versioned or migrated.

## Scope

1. Add `fingerprint_version` (or payload `"_v": 1`) into hashed material deliberately.
2. Document migration strategy when version bumps (rehash + merge policy, or dual-read) for WUT **and** Wv2 lineage rows.
3. Only implement when next payload schema change is planned — design now, code when needed.

## Acceptance

- Written policy for version bumps (lab + ops)
- Code path that stamps version on new captures (when implemented)

## Related

- `TradingStrategyFingerprintCapture`
- ADR-006; session [`2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill`](../session-reports/2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill.md)
