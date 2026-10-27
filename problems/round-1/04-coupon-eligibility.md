# PR #04 — Coupon Eligibility

**Difficulty:** Medium

**PR title:** Apply checkout promotions

## Summary

Checkout shows a customer the amount due before an order is placed. Employee pricing and a coupon can both be present on the request. The quote must apply employee pricing first; otherwise it may apply one eligible coupon. You are reviewing the PR that calculates the amount due in whole cents.

## Expected behavior
- `calculate_total(subtotal_cents, coupon_code=None, employee=False)` returns an integer amount in cents and rejects negative, non-integer, or boolean subtotals.
- Employee pricing is a 20% discount and takes precedence over a coupon.
- Without employee pricing, coupon `SAVE10` removes 10% when the original subtotal is at least 5000 cents.
- Coupon codes ignore surrounding whitespace and letter case. An unknown nonblank code is rejected. A known coupon below its minimum gives no discount. A blank coupon means no coupon.
- Discounts use whole-cent floor rounding and cannot reduce the amount due below zero.

## Contract examples

Each row is an independent quote. `10000` cents is $100.00.

| Subtotal | Coupon | Employee | Expected amount due |
| ---: | --- | --- | ---: |
| 4999 | `"SAVE10"` | `False` | 4999 |
| 5000 | `"SAVE10"` | `False` | 4500 |
| 10000 | `"SAVE10"` | `True` | 8000 |

A quote for 100 cents with the unknown code `"NOT-A-COUPON"` raises `ValueError`.

## Review task

Compare quote results and tests with the employee-pricing priority and coupon threshold. Correct the contradictory assertion and implementation defect, then verify the threshold immediately below and at 5000 cents. Explain which evidence shows that only one promotion applies.

## Starter Code

[View starter code](../../round-1/04-coupon-eligibility/)

## Reference Solution

[View solution](../../solutions/round-1/04-coupon-eligibility/)
