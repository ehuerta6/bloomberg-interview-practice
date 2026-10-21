# PR #24 — Data Merge Reconciliation

**Difficulty:** Medium

## PR title

Reconcile customer snapshots and tags

## Summary

Two import feeds provide customer snapshots while tags accumulate independently. Review how timestamps select ordinary fields and how metadata survives reconciliation.

## Input and output

`merge_records(existing, incoming)` accepts ordered lists of customer dictionaries. Each record has `customer_id` and an ISO-sortable `updated_at` value; `tags` is optional. The function returns a new ordered list of records.

## Expected behavior, edge cases, and invariants
- Keep existing customer order. Append new customers in the order they first appear in `incoming`.
- For a matched customer, newer ordinary fields replace older fields. Equal timestamps prefer incoming fields; older incoming snapshots do not replace current fields.
- Tags form a stable union: existing tags first, then unseen incoming tags, regardless of which snapshot supplies the winning ordinary fields.
- Do not mutate inputs or share mutable tag lists with the result.

## Review task

Compare newer, older, and tied snapshots. Exercise duplicate tags and verify both inputs and nested tag arrays remain isolated.


## Starter Code

[View starter code](../../round-1/24-data-merge-reconciliation/)

## Reference Solution

[View solution](../../solutions/round-1/24-data-merge-reconciliation/)
