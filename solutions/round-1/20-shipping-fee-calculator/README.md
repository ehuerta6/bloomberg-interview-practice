# Shipping Fee Calculator — Reference Solution

## What was broken

The starter always used the first rate and never read the minimum fee. It also ignored the shipping discount, selected the wrong band as weight increased, and did not validate negative or malformed amounts. Its use of binary floating-point followed by the default rounding mode also made cent calculations harder to reason about.

## Why it was wrong

A charge based on the wrong weight band can underprice heavier parcels. Applying a percentage discount without a minimum can violate the carrier's minimum charge. Rounding each intermediate calculation can shift the final customer charge by a cent. These are contract and billing errors even if ordinary sample orders look correct.

## Reproduce the issue

Run `python3 shipping.py` from the starter directory. The initial tests cover several ordinary orders, but boundary, discount, minimum, and invalid-input cases expose defects. From this directory, run `python3 shipping.py` to run the corrected regression suite.

## Investigation approach

Trace the inputs from zone lookup through band selection and charge calculation. Write down the order of operations from the ticket: free-shipping threshold, weight band, base plus weight charge, percentage discount, minimum charge, and final currency rounding. Then probe just below, at, and above each band boundary.

## Correction

The solution parses amounts through `Decimal`, rejects booleans, invalid values, and non-finite numbers, and checks that weight bands are increasing with only the final band unbounded. It chooses the first band whose upper limit contains the total weight. For a non-free order, it computes base plus weight charge, applies the percentage discount, enforces the minimum fee, and rounds once to cents with `ROUND_HALF_UP`. An inclusive free-shipping threshold returns zero before the minimum is applied, as the ticket requires.

## Regression tests

The suite covers weight-band transitions and the unbounded final band; a discount that would fall below the minimum; a discount that remains above it; inclusive free shipping; half-up rounding at a half-cent; unknown zones; and invalid amount/discount values. These tests exercise both precedence and numeric behavior instead of checking only a typical order.
