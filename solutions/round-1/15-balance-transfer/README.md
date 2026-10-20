# Balance Transfer — Reference Solution

## What broke

The draft debited the source before confirming that the transfer could finish. An insufficient-funds error could leave account state changed, and several invalid amounts were not checked before arithmetic.

## Reproduce the issue

Run `python3 transfers.py` in the starter folder. Try an amount larger than the source balance and compare the accounts before and after. Run the corrected independent suite with `python3 transfers.py` here.

## Investigation approach

Treat the transfer as one state change. Validate the mapping, account IDs, amount, and balances first. Check sufficient funds before writing either balance, then verify the total is conserved.

## Correction

The solution requires a mutable mapping of nonnegative integer-cent balances, distinct known accounts, and a positive integer-cent amount. It returns `False` without mutation when funds are insufficient; otherwise it debits and credits the accounts and returns `True`.

## Regression tests

Tests cover successful transfers, exact-balance transfers, insufficient funds, invalid account/amount/balance data, atomicity, and conservation. Run them with `python3 transfers.py`.
