# Ticket 21: Data Import Pipeline (Medium)

## Ticket

Data Import Pipeline needs reliable state transitions.

## Reported symptom

An operations team imports a partner CSV through a small in-memory adapter. Bad rows must be reported without losing valid neighboring records, while duplicate partner IDs must never silently replace customer data.

## Scenario

Trace a mixed batch containing valid rows, malformed values, repeated IDs, and an ID already in storage. Inspect accepted IDs, error row numbers, and the stored record after each import.

## Acceptance criteria

- Return a row-level result for valid and invalid input rows.
- Do not let a duplicate overwrite an accepted or preexisting record.
- Continue after a bad row and commit valid independent rows.
- Accept nonnegative integer amounts supplied as integers or base-10 numeric strings; reject booleans and floats.
- Return 400 for a non-list request body.

## State invariants

- A stored external ID maps to at most one record.
- Within one batch, the first valid row for an ID wins.
- Invalid or duplicate rows have no persistence effect.

## Investigation task

Trace a normal operation, a boundary or failure case, and a repeated request across the route, service, and repository. Explain which state should change, which state must remain untouched, and how your regression tests demonstrate both outcomes. Keep the implementation in memory; no external services or frameworks are required.

## Run the starter tests

```sh
python3 test_data_import.py
```

## Exercise folders

- [Starter exercise](../../round-2/21-data-import-pipeline/)
- [Reference solution](../../solutions/round-2/21-data-import-pipeline/)
