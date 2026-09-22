# Forensics — System One state + questions shape

**Audience:** Forensics (primary), PBR Ops, Chief of Staff  
**Law:** [`../business-context/jev-desk-guardrails.md`](../business-context/jev-desk-guardrails.md)

## When

After deterministic inventory (DuckDB, `results_json`, Edge math, host probe), when the autopsy still needs **bounded semantic judgments**: claim vs evidence, smell severity, promote/hold, which hypothesis fits the facts.

Do **not** replace arithmetic, SHA checks, or portfolio-cap counts with Jev.

## Shape to emit in every substantive autopsy

```markdown
## System One blocks

### State
(JSON or bullet facts only — what a judge may trust)
- pbr_id: …
- heat_mode / heat_present / heat_enabled: …
- peak_open / cap / breaches: …
- claims under test: "…"

### Questions
| id | type | instructions |
|----|------|--------------|
| claim_heat_on | Noul | The run had turtle heat actively gating size |
| cap_breached | Noul | Peak open positions exceeded portfolio max |
| promote_ok | Noul | Evidence supports Mode C promote language |

### Adjudication
Run: `jev ask` (or desk helper) with the state blob.
Record noul/choice/score + confidence.
Middle band → Operator / more evidence — do not soft-pass.
```

## Order

1. Code/probe facts  
2. Your analysis narrative  
3. System One blocks  
4. Jev adjudication (attach numbers)  
5. Recommendation (ship / hold / escalate)

## Anti-patterns

- Free-form “Jev says looks fine” without typed questions  
- Putting hypotheses in **State** as if measured  
- Skipping DuckDB because a noul felt decisive  
