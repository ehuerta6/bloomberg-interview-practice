# Digital Wallet Ledger Reference Solution

## What Was Broken

The starter posted a debit and credit pair for every call, even when the transaction ID had already been used. A client retry could therefore move the money twice. The same ID could also be reused with different transfer details without being detected.

## Reproduce and Investigate

From this folder, run `python3 test_wallet_ledger.py`. In the replay test, inspect both wallet balances and the entries for `tx-2` after submitting the same transfer twice. Follow `WalletService.transfer` into `WalletStore`: balances are derived from opening funds plus ledger entries, so both views should agree.

## The Fix

Before posting, the service looks up entries for the transaction ID. An exact replay returns `posted` without adding entries; reusing that ID for a different debit or credit returns `conflict`. A new transfer must use a positive amount, distinct existing wallets, and sufficient source funds. The store appends the equal-and-opposite entries together only after those checks pass.

## Regression Tests

The suite checks that each transfer has two entries summing to zero, duplicate requests move funds once, a changed request under the same ID conflicts, and insufficient funds or a zero amount leave the ledger unchanged.

## Run

```sh
python3 test_wallet_ledger.py
```
