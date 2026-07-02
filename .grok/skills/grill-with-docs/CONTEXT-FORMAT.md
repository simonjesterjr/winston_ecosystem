# CONTEXT.md Format

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A concise description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

## Relationships

- An **Order** produces one or more **Invoices**

## Example dialogue

> **Dev:** "When a **Customer** places an **Order**, do we create the **Invoice** immediately?"
> **Domain expert:** "No — an **Invoice** is only generated once fulfillment is confirmed."

## Flagged ambiguities

- "account" was used to mean both **Customer** and **User** — resolved: these are distinct concepts.
```

## Rules

- **Be opinionated.** Pick one canonical term; list aliases to avoid.
- **Flag conflicts explicitly** in "Flagged ambiguities".
- **One sentence max** per definition. Define what it IS.
- **Glossary only** — no implementation details, no specs, no code paths.
- **Project-specific terms only** — not general programming concepts.
- **Example dialogue** — show how terms interact in conversation.

## Sawtooth locations

| Scope | File |
|-------|------|
| Ecosystem (cross-monolith) | `ecosystem/CONTEXT.md` |
| Monolith-specific (if needed) | `{repo}/CONTEXT.md` |
| Multi-context (rare) | `CONTEXT-MAP.md` at repo root |

Create files lazily — only when the first term is resolved.