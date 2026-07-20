---
name: investigate-system-variance
description: Root-cause and classify behavioral or data differences between a baseline and a candidate system, implementation, release, replay, or environment. Use for one-case parity failures, migration discrepancies, legacy-versus-rewrite output differences, unexplained regression rows, or stakeholder reports that two systems disagree. Produces an evidence-backed issue record, an action ticket when needed, and an adversarial verification pass. Do not use for undifferentiated bulk drift before a representative case has been selected.
---

# Investigate System Variance

Treat a difference as an observation, not a defect. Determine what should happen, reproduce the same scope on both sides, trace the governing paths, classify the cause, and preserve the evidence.

## Load project context

Read, in order:

1. `AGENTS.md` and `PROJECT_PROFILE.md` for safety, ownership, commands, and environments.
2. `CONTEXT.md` for canonical domain terms.
3. The current requirements and compatibility contract.
4. The replay or validation runbook.
5. `references/project-notes.md` if an installed project has created it.

Never inherit server names, thresholds, exclusions, source tables, or credential locations from an example. Resolve them from the current project.

## Procedure

### 1. Define one target and its comparison contract

State the smallest identity that reproduces the difference: entity keys, input snapshot, time reference, configuration, baseline version, candidate version, and environment.

Write the observed fields side by side before explaining them. Identify which requirement, schema, API contract, or compatibility promise governs each field. If intended behavior is ambiguous, stop classification and record a decision question.

### 2. Check known differences before tracing code

Search current runbooks, issues, ADRs, project notes, compatibility exceptions, and accepted debt by symptom and field name. Verify that a matching exception still applies to the exact versions and scope.

Do not rediscover and relabel a deliberate change as a regression. Do not use a documented exception as a blanket excuse for a superficially similar case.

### 3. Collect equivalent inputs and outputs

Prefer immutable on-disk artifacts. If fresh capture is necessary:

- use the same logical source, time boundary, scope, flags, and configuration;
- record source environment and capture time;
- default external systems to read-only;
- parameterize queries;
- redact credentials and sensitive values before output reaches chat or documentation.

For large captures, produce `summary.json`, `preview.tsv`, and a searchable `full.jsonl` or equivalent. Read the summary first and query the full artifact on demand.

### 4. Expand to the shared contention or dependency scope

Do not reason from the target row alone when rows share mutable supply, quotas, ordering, locks, caches, parent aggregation, or upstream state.

Build:

- Table A: every relevant field for the target on baseline and candidate.
- Table B: every peer that can affect the target, in actual processing order, with the resource or state each consumes.

Classify every Table B row as same, different selection, different quantity/value, baseline-only, candidate-only, cross-scope reference, or capture artifact. Adapt labels to the domain but do not leave peers unclassified.

### 5. Check conservation and invariants two ways

When a limited resource is involved, total consumption at the strict scope and at the aggregate scope. Strict scope catches illegal cross-boundary use; aggregate scope distinguishes a mapping error from true over-consumption.

Exclude synthetic or cosmetic rows only when the current contract explicitly says they do not consume the resource. Cite the exclusion.

Recompute units and date intervals independently. Verify whether a reported duration means elapsed, calendar, business, working, or wall-clock time.

### 6. Trace both executable paths

Start at the entry point and follow the actual branches for the target through ordering, selection, calculation, post-processing, persistence, and presentation. Cite file and line for every load-bearing code claim.

- Verify which implementation is invoked; do not cite dead, test-only, or historical variants as runtime behavior.
- Treat comments, names, and old decisions as leads. The executing code proves current behavior; current requirements prove intended behavior.
- For deployed database routines or configuration, verify the deployed artifact when repository copies can drift.
- Include adapter or capture transformations when a difference may be introduced before core logic.

### 7. Classify the result

Use exactly one primary classification:

1. `Candidate defect` — candidate violates the current contract.
2. `Baseline defect; candidate correct` — baseline behavior is wrong and need not be replicated.
3. `Intentional contract change` — candidate deliberately implements a newer requirement.
4. `Representation or time/calendar-rule difference` — equivalent intent differs because of formatting, rounding, time/calendar rules, or post-processing.
5. `Contention-driven; candidate internally consistent` — shared-state ordering or baseline over-consumption explains the target.
6. `Capture or data artifact` — timing, stale input, normalization, environment, or data quality invalidates direct comparison.
7. `Undetermined` — evidence is insufficient or the governing requirement is unresolved.

If the evidence does not fit, keep investigating. Do not force a confident label.

### 8. Write the durable record

Use `references/investigation-report-template.md`. Save under the project's issue/investigation folder and update its index if one exists.

Include the target table, peer classification, invariant checks, executable trace, cited authority, classification, and recommendation. Write facts before interpretation.

Create a separate ticket only when action remains: fix, instrumentation, runbook change, requirements decision, data correction, or escalation. Link it instead of duplicating the investigation.

### 9. Run adversarial verification

Give a fresh reviewer the issue artifact and primary sources, not the desired conclusion. Ask it to disconfirm supply/state claims, recalculate totals, re-read cited code, locate omitted peers, challenge the governing requirement, and test whether the recommendation follows.

If independent review is unavailable, perform a structured self-skeptical pass and label it as self-review. Re-derive every load-bearing fact without trusting the first pass.

Revise falsified or weak claims and repeat verification until the verdict is stable. Record mode, verdict, important caveats, and confidence in the issue.

## Completion contract

Complete the investigation only when all are true:

- one reproducible target and comparison contract are recorded;
- known differences were checked first;
- the full dependency/contention scope was classified;
- relevant invariants were independently recomputed;
- both executable paths were traced from primary sources;
- one primary classification is justified;
- the durable issue exists and any action has a linked ticket;
- adversarial or labeled self-verification has been incorporated.

## Red flags

Stop and reconsider when you are about to:

- call a difference a regression from one row;
- quote a summary field without verifying its unit;
- trust a repository routine known to differ from deployment;
- include virtual rows in physical conservation totals;
- cite a comment instead of the executing branch;
- skip known-difference search or adversarial review;
- write the only investigation record to a temporary directory;
- query or mutate a production system without explicit authority.
