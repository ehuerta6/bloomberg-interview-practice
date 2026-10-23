# Ticket #21 — Data Import Pipeline

**Difficulty:** Medium

## Context

You maintain an operations tool that receives a partner's already-decoded CSV
rows as a list of dictionaries. Each partner ID identifies one stored customer
record. The import should save valid independent rows and report errors by their
1-based row number, so an operator can correct the input without losing good rows.

## Practice report

Start with an empty repository and post these rows through `ImportRoutes.post`:

```python
[
    {"id": "a", "email": "a@x.test", "amount": True},
    {"id": "b", "email": "b@x.test", "amount": "4"},
]
```

| Observation | Current starter | Expected |
| --- | --- | --- |
| Accepted IDs | `["a", "b"]` | `["b"]` |
| Error row numbers | `[]` | `[1]` |
| Persisted records | `a` with amount 1; `b` with amount 4 | Only `b` with amount 4 |

The boolean is malformed input; it must not become a financial amount.

## Acceptance Criteria

- Accept a nonnegative integer amount supplied as an integer or a base-10
  integer string. Reject booleans, floats, negative amounts, missing fields,
  blank trimmed IDs, and emails without `@`.
- Trim IDs and emails and store emails in lowercase. Return accepted IDs and
  errors in input order, with the original 1-based row number for each error.
- An invalid row changes no record; continue to save valid independent rows.
- Within one batch, the first valid row for an ID wins. Report later duplicates
  without replacing it, and never overwrite a preexisting stored ID.
- A non-list top-level body returns 400 without persistence effects. A list
  with errors returns 207; a fully accepted list returns 201.

## Out of Scope

Work with parsed row dictionaries and the existing in-memory repository. Reading
CSV bytes, file uploads, all-or-nothing batch transactions, and changing customer
IDs are outside this ticket.

## Investigation

Trace the two-row report through the route, parser, and store. Add mixed-batch
cases with a float, bad email, duplicate ID, existing ID, and later valid row.
Assert row numbers, normalized records, and preserved existing values.

## Starter Code

[View starter code](../../round-2/21-data-import-pipeline/)

## Reference Solution

[View solution](../../solutions/round-2/21-data-import-pipeline/)
