# Ticket #12 — Digital Wallet Ledger

**Difficulty:** Hard

## Problem

### Reported symptom

A wallet transfer is reflected twice in balances after a client retries, and the transaction history no longer balances.

### Scenario

Two users move funds between wallets. The API can receive a duplicate request after a timeout, and a transfer must appear as one debit and one matching credit in the ledger.

## Acceptance Criteria
- Every posted transfer has exactly two entries with equal and opposite amounts.
- A rejected or repeated transfer leaves balances and ledger history unchanged; a wallet cannot be overdrawn.
- Invalid requests must leave persisted state unchanged.

## State Invariants

A rejected or repeated transfer leaves balances and ledger history unchanged; a wallet cannot be overdrawn.

## Investigation

Follow a transfer from validation through both ledger entries. Inspect transaction-level totals as well as wallet balances after success, replay, and insufficient funds. Add regression coverage for the behavior you reproduce.

## Starter Code

[View starter code](../../round-2/12-digital-wallet-ledger/)

## Reference Solution

[View solution](../../solutions/round-2/12-digital-wallet-ledger/)
