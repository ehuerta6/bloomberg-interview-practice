# Ticket #12 — Digital Wallet Ledger

**Difficulty:** Hard

## Context

You maintain transfers between two digital wallets. Amounts are in cents.
The ledger is the saved history of movements: a debit is a negative entry in
the source wallet, and the matching credit is a positive entry in the destination.
A wallet balance is its opening funds plus all its entries.

## Practice report

Open `w-1` with 5000 cents and `w-2` with 1000 cents. Call
`transfer("tx-2", "w-1", "w-2", 300)` twice, representing a client retry.

| Observation | Current starter | Expected |
| --- | --- | --- |
| Source balance | 4400 | 4700 |
| Destination balance | 1600 | 1300 |
| Entries for `tx-2` | 4 | 2 |

The entries still sum to zero in the starter; the problem is the extra movement
for one transaction ID.

## Acceptance Criteria

- Each new posted transfer writes exactly one debit and one matching credit;
  those two amounts sum to zero and move the requested amount between wallets.
- A transfer needs a positive amount, distinct existing wallets, and sufficient
  source funds. A rejected transfer leaves both balances and all entries unchanged.
- An exact transaction-ID replay returns `posted` without moving funds or
  appending entries again.
- Reusing a transaction ID for a different source, destination, or amount returns
  `conflict` and preserves its original entries and wallet balances.
- No accepted new transfer overdraws the source wallet. Ledger history and
  derived balances must agree after each operation.

## Out of Scope

Use the local ledger and supplied numeric amounts. Bank settlement, fees,
currency conversion, transaction authentication, and distributed storage are
outside this ticket.

## Investigation

Reproduce the duplicate request and inspect transaction entries alongside both
balances. Add regression tests for exact replay, conflicting reuse, insufficient
funds, and the same-wallet case. Explain why balanced entries alone do not prove
that a transfer happened only once.

## Starter Code

[View starter code](../../round-2/12-digital-wallet-ledger/)

## Reference Solution

[View solution](../../solutions/round-2/12-digital-wallet-ledger/)
