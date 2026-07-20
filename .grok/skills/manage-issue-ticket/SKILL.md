---
name: manage-issue-ticket
description: Use this skill when a newly discovered defect or investigation needs a standardized repository issue ticket, or when an existing ticket under docs/issues needs confirmed evidence, corrections, clarification, or status updates. Investigate known repository information and possible duplicates before asking grouped clarifying questions. Do not use for ordinary feature planning, implement the fix, or invent missing facts.
---

# Create or update an issue ticket

## Objective

Turn incomplete reports, observations, logs, screenshots, or an existing ticket into a durable, evidence-grounded issue under `docs/issues/` that is ready for investigation or implementation without forcing the developer to repeat known information.

## Inputs

- The developer's current description and answers from this interaction.
- An existing issue path, issue ID, title, or search terms when this is an update.
- Relevant logs, screenshots, stack traces, test failures, commits, diffs, specifications, ADRs, code, and related issue tickets available in the repository.
- Repository issue policy from `.agent-harness/policy.yaml` when present.
- The issue template and conventions in `docs/issues/` when present.

## Allowed changes

- Create one new Markdown issue under `docs/issues/`, or update the one existing issue identified by the developer or repository evidence.
- When running inside a harness run, write `issue-ticket-result.md` in the active run directory.
- Do not modify production code, tests, schemas, dependencies, CI, specifications, or unrelated tickets.

## Operating rules

- Investigate available evidence before asking questions.
- Never ask for information already supplied in the conversation, existing ticket, repository, or linked artifact.
- Separate confirmed facts, user-reported observations, hypotheses, and unknowns.
- Do not state a suspected root cause as fact without evidence.
- Preserve the repository's existing issue naming and structure when one is established.
- Preserve meaningful history when updating. Correct current sections, but record what changed and why in `History`.
- After a `safe-bug-fix` terminal report, update the issue lifecycle from that evidence: verified `PASS` with a durable commit or repository-defined landing event may become `resolved`; an uncommitted verified candidate remains `in-progress`; blocked or failed work must record the condition required to resume.
- Do not silently create a duplicate issue when an existing ticket appears to cover the same behavior.
- A ticket may be saved as `triage` with explicit unknowns. It may be marked `ready` only when the readiness rules below are satisfied.

## Procedure

### 1. Determine create or update mode

1. Honor an explicit issue path or ID.
2. For an update without an exact path, search `docs/issues/` by ID, title, error text, affected component, and observable behavior.
3. For a new issue, search open or active tickets for likely duplicates before allocating an identity.
4. When exactly one strong match exists, propose updating it rather than creating a duplicate.
5. When several plausible matches exist, ask the developer to select one. Do not guess.
6. When the developer explicitly requested an update but no ticket can be found, return `ISSUE_NOT_FOUND`; create a new ticket only with explicit authorization.

### 2. Build the known-information inventory

Inspect the available sources and record:

- Observable symptom or requested outcome.
- Actual behavior and expected behavior.
- Reproduction steps, frequency, and preconditions.
- Environment, version, branch, commit, device, browser, service, account role, or data conditions when relevant.
- Impact, affected users or workflows, severity signals, and workarounds.
- Logs, screenshots, stack traces, failing tests, paths, commits, and other evidence.
- Related tickets, specifications, ADRs, and prior fixes.
- Behaviors and interfaces that must remain unchanged.
- Confirmed exclusions and out-of-scope work.
- Suspected causes or approaches, clearly labeled as hypotheses.

Prefer repository evidence over memory. Cite repository paths, commands, commit hashes, or artifact names in the ticket whenever available.

### 3. Identify gaps and ask clarifying questions

Classify gaps as either:

- **Blocking:** needed to distinguish the defect, state expected behavior, identify the correct ticket, avoid a harmful assumption, or define testable acceptance criteria.
- **Non-blocking:** useful for priority, ownership, labels, additional examples, or implementation convenience.

Ask one concise, grouped set of blocking questions after investigation. Include non-blocking questions only when they are likely to materially improve the ticket. Follow these rules:

1. Ask no more than the policy limit, defaulting to seven questions in one round.
2. Put the highest-value questions first.
3. Offer answer choices when they reduce ambiguity.
4. State any safe default that will be used if a non-blocking question is unanswered.
5. Do not ask for a proposed implementation unless the developer already has one or the ticket type is an investigation.
6. Ask a follow-up round only when an answer reveals a new contradiction or leaves a blocking ambiguity.

Use this response shape when questions are required:

```markdown
I found [brief inventory of confirmed information and likely matching ticket, if any].

Blocking questions
1. [Question with choices when useful.]

Useful but non-blocking
2. [Question and safe default if unanswered.]

After these answers, the ticket will be [created/updated] at `docs/issues/...`.
```

When the developer is unavailable or explicitly requests immediate capture, save a `triage` ticket with unanswered items under `Unknowns and clarifying questions` rather than inventing answers.

### 4. Assign identity, type, status, and priority

For a new issue:

1. Follow the existing convention in `docs/issues/` if one exists.
2. Otherwise use `YYYY-MM-DD-short-kebab-title.md` and the identifier `ISSUE-YYYYMMDD-short-kebab-title`.
3. If the same slug is already used on that date, append the smallest unused numeric suffix, such as `-2`.
4. Recheck that the ID and path are unused immediately before writing.

Use these default classifications unless repository policy overrides them:

- `type`: `bug`, `regression`, or `investigation`. Route ordinary features and future work to `docs/tickets/`.
- `status`: `triage`, `ready`, `in-progress`, `blocked`, `resolved`, or `closed`.
- `priority`: `critical`, `high`, `medium`, `low`, or `unset`.

Do not infer priority solely from emotional language. Record impact evidence and leave priority `unset` when authorization or business context is missing.

### 5. Apply readiness rules

A ticket can be `ready` only when it contains:

- A distinct observable problem or outcome.
- Expected behavior that does not conflict with authoritative requirements.
- A reproducible path, or for an investigation ticket, a bounded question and required evidence.
- Testable acceptance criteria.
- Relevant preservation constraints and known scope boundaries.
- No unresolved blocking contradiction.

Otherwise use `triage` or `blocked` and list what is still needed. Never mark a ticket `resolved` or `closed` from an unverified claim alone.

### 6. Create or merge the standardized ticket

For a new ticket, use the standard structure in `docs/issues/_template.md` when present.

For an update:

1. Preserve its ID, filename, original creation date, and valid manually entered context.
2. Update `updated` to the current date.
3. Merge new confirmed information into the relevant sections instead of appending an unstructured note dump.
4. Replace corrected current facts, then add a dated `History` entry describing the correction and its evidence.
5. Keep unresolved conflicting reports visible under `Unknowns and clarifying questions` or `Investigation notes`.
6. Do not remove acceptance criteria, preservation requirements, or evidence merely because a proposed solution changed.
7. Change status, type, priority, labels, or ownership only when the developer directs it or evidence and repository policy clearly justify it.

### 7. Validate the result

Before completion, verify that:

- The file is under `docs/issues/`.
- The ID and filename are unique.
- Required frontmatter fields and sections exist.
- Statements of fact have an identifiable source or are explicitly marked as reported.
- Hypotheses are not represented as confirmed causes.
- Acceptance criteria are observable and testable.
- Unknowns are explicit.
- An updated ticket contains a dated history entry.
- No unrelated repository file was changed.

## Required output

Create or update a ticket with this structure:

```markdown
---
id: ISSUE-YYYYMMDD-short-kebab-title
title: Concise observable problem
status: triage
type: bug
priority: unset
created: YYYY-MM-DD
updated: YYYY-MM-DD
labels: []
related: []
---

# Concise observable problem

## Summary
[Two or three sentences describing the user-visible or system-visible problem and why it matters.]

## Problem statement
[The problem without prescribing an implementation.]

## Current behavior
[What happens now.]

## Expected behavior
[What should happen instead.]

## Reproduction

### Preconditions
[Required state, account, data, configuration, or `Unknown`.]

### Steps
1. [Action.]
2. [Action.]

### Observed result
[Exact result, error, or failure signature.]

### Reproducibility
[Always, intermittent with known frequency, not yet reproduced, or investigation-specific condition.]

## Environment
[Versions, branch or commit, platform, browser, service, configuration, and data conditions. Use `Unknown` where necessary.]

## Evidence

| Evidence | Source | What it establishes |
|---|---|---|
| [Log, screenshot, command output, test, report] | [Path, commit, artifact, or reported by developer] | [Supported fact] |

## Impact and priority
[Affected users or workflows, severity evidence, workaround, and reason for assigned priority or `Priority remains unset`.]

## Scope and preservation requirements

### In scope
- [Authorized outcome.]

### Must preserve
- [Existing behavior, contract, data, security property, or performance characteristic.]

### Out of scope
- [Unauthorized refactor, dependency, API, schema, or product change.]

## Acceptance criteria
- [ ] Given [precondition], when [action], then [observable result].
- [ ] Existing [related behavior] continues to pass its current verification.

## Investigation notes
[Confirmed findings and clearly labeled hypotheses.]

## Unknowns and clarifying questions
- [ ] [Unanswered question, or `None`.]

## Dependencies and risks
[Related systems, tickets, migrations, compatibility, security, performance, or `None known`.]

## Verification plan
[Tests, commands, manual checks, environments, or evidence needed to close the ticket.]

## History
- YYYY-MM-DD — Created from [source].
```

When running inside a harness run, also create `issue-ticket-result.md` containing:

- Operation: `created` or `updated`.
- Ticket path and ID.
- Duplicate search result.
- Questions asked and answers incorporated.
- Remaining blocking and non-blocking unknowns.
- Resulting readiness status.
- Repository evidence inspected.

## Stop conditions

- Return `ISSUE_AMBIGUOUS` when multiple existing tickets could be the update target.
- Return `ISSUE_NOT_FOUND` when an update was requested but no target exists.
- Return `CONFLICTING_REQUIREMENTS` when authoritative expected behaviors conflict.
- Return `INSUFFICIENT_IDENTITY` when a new ticket cannot be distinguished from an existing report after clarification.
- Return `BLOCKED_QUESTIONS` when blocking questions remain and the developer did not authorize a triage ticket.
- Never resolve uncertainty by fabricating reproduction steps, impact, priority, ownership, or root cause.

## Handoff

- Pass a `ready` bug or regression ticket to `safe-bug-fix` by its exact repository path after it is committed through the repository's normal workflow. If it remains uncommitted, state that the clean-baseline gate will block.
- Pass a `ready` investigation ticket to the relevant bounded investigation workflow, not `safe-bug-fix`.
- After `safe-bug-fix` finishes, consume its terminal completion report to update status, verification evidence, and `History`; do not alter the completed candidate while recording this durable result.
- Pass a `triage` ticket to further investigation or a later explicit invocation of this skill.
- Pass an intentional requirements change to `change-behavior-intentionally` rather than disguising it as a defect.
