# PR #15 — Balance Transfer

**Difficulty:** Medium

**PR title:** Transfer integer-cent balances between accounts

## Summary

A wallet user transfers funds to another account. The service must either move the requested cents or leave every account unchanged; a failed transfer must not alter the balance shown to either user. You are reviewing the in-memory transfer PR and its tests for this complete state change.

## Input and output

`transfer(accounts, source, destination, amount_cents)` mutates a mutable account-to-balance mapping. It returns `True` after a successful transfer and `False` when the source lacks funds.

## Expected behavior and invariants
- Account balances are nonnegative integer cents; booleans are not valid integers for this contract.
- Account IDs are nonblank strings. Source and destination must be distinct existing IDs. The amount must be a positive integer number of cents.
- Invalid account data, IDs, or amounts raise `ValueError` without changing any balance.
- If the source has insufficient funds, return `False` and leave the complete mapping unchanged.
- On success, subtract from the source and add the same amount to the destination. The total balance remains constant.

## Contract examples

Each row begins with a fresh account mapping and transfers from `"a"` to `"b"`:

| Initial accounts | Amount in cents | Expected return | Accounts afterward |
| --- | ---: | --- | --- |
| `{"a": 1000, "b": 200}` | 250 | `True` | `{"a": 750, "b": 450}` |
| `{"a": 300, "b": 0}` | 300 | `True` | `{"a": 0, "b": 300}` |
| `{"a": 50, "b": 100}` | 80 | `False` | `{"a": 50, "b": 100}` |

An amount of `True` is invalid and raises `ValueError` without changing either balance. A successful transfer preserves the sum across all accounts, including accounts that did not participate.

## Review task

Compare return values and complete before/after mappings for successful, insufficient-funds, and invalid requests. Correct implementation or assertion discrepancies, then add regression cases for exact-balance transfers, invalid amounts and IDs, and conservation of the total. Explain how the state assertions rule out a partially applied transfer.

## Starter Code

[View starter code](../../round-1/15-balance-transfer/)

## Reference Solution

[View solution](../../solutions/round-1/15-balance-transfer/)
