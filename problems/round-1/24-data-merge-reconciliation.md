# PR #24 — Data Merge Reconciliation

**Difficulty:** Medium

## PR title

Reconcile customer snapshots and tags

## Summary

A customer directory receives snapshots from two import feeds. A snapshot is a record of fields at its `updated_at` time, but customer tags collected by either feed must survive even when an older snapshot arrives. You are reviewing reconciliation so consumers get current fields, accumulated tags, and a predictable customer order without changing either feed's data.

## Input and output

`merge_records(existing, incoming)` accepts ordered lists of customer dictionaries. Each record has `customer_id` and an ISO-sortable `updated_at` value; `tags` is optional. The function returns a new ordered list of records.

## Expected behavior, edge cases, and invariants
- Keep existing customer order. Append new customers in the order they first appear in `incoming`.
- For a matched customer, newer ordinary fields replace older fields. Equal timestamps prefer incoming fields; older incoming snapshots do not replace current fields.
- Tags form a stable union: existing tags first, then unseen incoming tags, regardless of which snapshot supplies the winning ordinary fields.
- Do not mutate inputs or share mutable tag lists with the result.

## Contract example

Existing records:

```python
[{"customer_id": "c1", "name": "Current", "updated_at": "2025-01-02", "tags": ["vip", "beta"]}]
```

Incoming records:

```python
[
    {"customer_id": "c1", "name": "Older", "updated_at": "2025-01-01", "tags": ["beta", "priority"]},
    {"customer_id": "c2", "name": "New", "updated_at": "2025-01-03", "tags": []},
]
```

Expected output order is `c1`, then `c2`. The returned `c1` retains name `"Current"` and timestamp `"2025-01-02"`, with tags `["vip", "beta", "priority"]`. Changing that returned tag list afterward must not change either input list. If the incoming `c1` timestamp instead equals `"2025-01-02"`, its name `"Older"` wins the tie.

## Review task

Review field selection, tag retention, and assertions for newer, older, and tied snapshots. Correct discrepancies and add cases for customer order, repeated tags, and editing a returned tag list after the call. Explain which tests prove the selected field values and which prove isolation from caller-owned data.

## Starter Code

[View starter code](../../round-1/24-data-merge-reconciliation/)

## Reference Solution

[View solution](../../solutions/round-1/24-data-merge-reconciliation/)
