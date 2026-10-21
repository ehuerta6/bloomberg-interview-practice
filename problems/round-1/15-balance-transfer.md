# PR #15 — Balance Transfer

**Difficulty:** Medium

**PR title:** Transfer integer-cent balances between accounts

## Summary

A wallet service moves funds between two accounts. Review the validation and state changes as one transaction so invalid or unsuccessful transfers do not leave partial updates.

## Input and output

`transfer(accounts, source, destination, amount_cents)` mutates a mutable account-to-balance mapping. It returns `True` after a successful transfer and `False` when the source lacks funds.

## Expected behavior and invariants
- Account balances are nonnegative integer cents; booleans are not valid integers for this contract.
- Account IDs are nonblank strings. Source and destination must be distinct existing IDs. The amount must be a positive integer number of cents.
- Invalid account data, IDs, or amounts raise `ValueError` without changing any balance.
- If the source has insufficient funds, return `False` and leave the complete mapping unchanged.
- On success, subtract from the source and add the same amount to the destination. The total balance remains constant.

## Review task

Compare state before and after success, insufficient funds, and invalid input. Check the exact-balance case, same-account transfers, boolean amounts, and whether every unsuccessful call preserves all accounts.

## Starter Code

[View starter code](../../round-1/15-balance-transfer/)

## Reference Solution

[View solution](../../solutions/round-1/15-balance-transfer/)
