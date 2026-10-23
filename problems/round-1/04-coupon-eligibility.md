# PR #04 — Coupon Eligibility

**Difficulty:** Medium

**PR title:** Apply checkout promotions

## Summary

Checkout shows a customer the amount due before an order is placed. Employee pricing, a first-order offer, and a coupon can all be present on the request, but only the highest-priority eligible promotion applies. You are reviewing the PR that calculates this quote in whole cents.

## Expected behavior
- `calculate_total(subtotal_cents, coupon_code=None, first_order=False, employee=False)` returns an integer amount in cents and rejects negative, non-integer, or boolean subtotals.
- Employee pricing is a 20% discount and takes precedence over all other promotions. Otherwise, a first-order discount is 15% and takes precedence over a coupon.
- With no automatic promotion, `SAVE10` removes 10% when the original subtotal is at least 5000 cents; `TAKE500` removes 500 cents when it is at least 2500 cents.
- Coupon codes ignore surrounding whitespace and letter case. An unknown nonblank code is rejected. A known coupon below its minimum gives no discount.
- Discounts use whole-cent floor rounding and cannot reduce the amount due below zero.

## Contract examples

Each row is an independent quote. `10000` cents is $100.00.

| Subtotal | Coupon | First order | Employee | Expected amount due |
| ---: | --- | --- | --- | ---: |
| 4999 | `"SAVE10"` | `False` | `False` | 4999 |
| 5000 | `"SAVE10"` | `False` | `False` | 4500 |
| 10000 | `"SAVE10"` | `True` | `True` | 8000 |
| 2500 | `" take500 "` | `False` | `False` | 2000 |

A quote for 100 cents with the unknown code `"NOT-A-COUPON"` raises `ValueError`.

## Review task

Compare the quote results and tests with the promotion priority and original-subtotal minimums. Correct misleading assertions and implementation defects, then add tests for competing promotions, threshold boundaries, whole-cent rounding, and invalid money input. Explain how the assertions establish that a quote applies only one promotion.

## Starter Code

[View starter code](../../round-1/04-coupon-eligibility/)

## Reference Solution

[View solution](../../solutions/round-1/04-coupon-eligibility/)
