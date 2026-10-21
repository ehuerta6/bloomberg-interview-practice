# Ticket #21 — Data Import Pipeline

**Difficulty:** Medium

## Problem

### Reported symptom

An operations team imports a partner CSV through a small in-memory adapter. Bad rows must be reported without losing valid neighboring records, while duplicate partner IDs must never silently replace customer data.

### Scenario

Trace a mixed batch containing valid rows, malformed values, repeated IDs, and an ID already in storage. Inspect accepted IDs, error row numbers, and the stored record after each import.

## Acceptance Criteria
- Return a row-level result for valid and invalid input rows.
- Do not let a duplicate overwrite an accepted or preexisting record.
- Continue after a bad row and commit valid independent rows.
- Accept nonnegative integer amounts supplied as integers or base-10 numeric strings; reject booleans and floats.
- Return 400 for a non-list request body.

## State Invariants
- A stored external ID maps to at most one record.
- Within one batch, the first valid row for an ID wins.
- Invalid or duplicate rows have no persistence effect.

## Investigation

Run a mixed import containing valid rows, malformed amounts, duplicate IDs within the batch, and IDs already stored. Compare row numbers and per-row outcomes, confirm valid independent rows persist, and inspect state after a non-list request body.

## Starter Code

[View starter code](../../round-2/21-data-import-pipeline/)

## Reference Solution

[View solution](../../solutions/round-2/21-data-import-pipeline/)
