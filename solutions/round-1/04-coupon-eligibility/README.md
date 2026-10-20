# Coupon Eligibility — Reference Solution

## What was broken

The draft calculated an employee discount, then replaced it with a first-order discount, and finally replaced either result with a coupon. That made promotion order depend on which `if` statements ran last. A customer could stack promotions the PR says are mutually exclusive, and an employee could lose the employee rate.

## Reproduce the issue

From this folder, run `python3 coupon_eligibility.py`. The starter's combined employee/first-order/coupon case returns 9000 cents for a 10000-cent order; the rules require the employee rate to win and return 8000 cents.

## Investigation approach

Write the precedence rules as an ordered decision table before reading the branches: employee, first order, eligible coupon, then no discount. Check the threshold against the original subtotal and use cents throughout so rounding is explicit.

## Correction

The reference implementation validates integer cents (excluding `bool`), chooses exactly one promotion in priority order, normalizes coupon text, and applies minimums before calculating the discount. The final subtraction is capped at the subtotal, so a fixed discount can never create a negative amount due.

## Regression tests

The starter also contains an assertion that says first-order pricing beats employee pricing. That assertion contradicts the PR's precedence rule and passes the buggy branch order, so the reference tests replace it with the required employee-first behavior. The expanded suite covers each promotion alone, employee precedence over both other offers, first-order precedence over a coupon, threshold boundaries, an unknown code below its minimum, blank input, and invalid boolean money input.
