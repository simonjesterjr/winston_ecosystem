# Variance Investigation Template

```markdown
---
status: Under investigation
date_opened: YYYY-MM-DD
environment: <environment>
baseline: <version/run>
candidate: <version/run>
scope: <entity keys and input artifact>
adversarial_review: <mode, artifact/link, verdict, confidence>
---

# <What differs, for which scope>

## Summary

State the observed difference, primary classification, and recommended action in one paragraph.

## Comparison contract

- Governing requirement or contract:
- Shared input and time reference:
- Baseline version/configuration:
- Candidate version/configuration:

## Target comparison

| Field | Baseline | Candidate | Contract/notes |
|---|---|---|---|
| | | | |

## Dependency or contention scope

| Peer | Processing order | Baseline outcome | Candidate outcome | Classification |
|---|---:|---|---|---|
| | | | | Same / different selection / different value / baseline-only / candidate-only / cross-scope / artifact |

## Invariant and conservation checks

- Strict-scope result:
- Aggregate-scope result:
- Exclusions and authority:
- Independently recomputed units/date intervals:

## Executable trace

### Baseline

Cite entry point and each load-bearing branch with file:line or deployed-object evidence.

### Candidate

Cite entry point and each load-bearing branch with file:line.

## Classification

Choose one: Candidate defect / Baseline defect; candidate correct / Intentional contract change / Representation or time/calendar-rule difference / Contention-driven; candidate internally consistent / Capture or data artifact / Undetermined.

Explain why competing classifications do not fit.

## Recommendation

State the smallest action justified by the evidence. Link a ticket when action remains.

## Adversarial verification

- Mode: independent / self-skeptical
- Verdict: holds / holds with caveats / broken
- Claims re-derived:
- Corrections made:
- Remaining uncertainty:

## Cross-references

- Requirements:
- Known differences:
- Related issues/tickets/ADRs:
- Raw artifacts:
```
