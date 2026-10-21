# PR #04 — Coupon Eligibility

**Difficulty:** Medium

**PR title:** Apply checkout promotions

## Summary

This change adds coupon and automatic-promotion handling to the checkout quote. The caller passes a subtotal in whole cents and receives the amount due.

## Expected behavior
- `calculate_total(subtotal_cents, coupon_code=None, first_order=False, employee=False)` returns an integer amount in cents and rejects negative, non-integer, or boolean subtotals.
- Employee pricing is a 20% discount and takes precedence over all other promotions. Otherwise, a first-order discount is 15% and takes precedence over a coupon.
- With no automatic promotion, `SAVE10` removes 10% when the original subtotal is at least 5000 cents; `TAKE500` removes 500 cents when it is at least 2500 cents.
- Coupon codes ignore surrounding whitespace and letter case. An unknown nonblank code is rejected. A known coupon below its minimum gives no discount.
- Discounts use whole-cent floor rounding and cannot reduce the amount due below zero.

## Review task

Trace every combination of employee, first-order, and coupon inputs. Compare the order of the implementation branches with the promotion precedence, then inspect whether the tests prove promotions cannot be stacked. Correct misleading tests and add regression coverage for boundaries and invalid input.

## Starter Code

[View starter code](../../round-1/04-coupon-eligibility/)

## Reference Solution

[View solution](../../solutions/round-1/04-coupon-eligibility/)
