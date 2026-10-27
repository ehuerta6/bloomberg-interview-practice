# PR #20 — Shipping Minimum Charge

**Difficulty:** Medium

## Practice Metadata

- **Interview format:** PR review / focused debugging.
- **Primary skills:** pricing arithmetic, rounding, threshold behavior.
- **Expected duration:** 45–60 minutes.
- **AI assistance:** Allowed in guided practice mode for explanations, hypotheses, test ideas, and focused hints; the candidate owns and explains every change.
- **Candidate objective:** Compare the proposed change and its tests with the observable contract, then make a targeted correction and regression test.
- **Interviewer evaluation:** Clarifying questions, code investigation, root-cause reasoning, maintainable changes, testing, and communication. See the [shared interviewer rubric](../../docs/editorial/interviewer-rubric.md).

**PR title:** Enforce the carrier minimum on discounted shipping quotes

## Summary

The checkout page shows a shipping quote before an order is placed. The local carrier charges a base amount plus a per-kilogram rate, with a $5 minimum. A percentage promotion can reduce the quote, while orders at or above $75 receive free shipping. Support reports that some light parcels show a charge below the carrier's minimum after a promotion.

## Input and output

`calculate_shipping(order, rates)` returns a `Decimal` in dollars rounded to cents. An order supplies `zone`, `subtotal`, and `weight_kg`; the discount is optional and defaults to zero. Each zone supplies `base_fee`, `per_kg`, `minimum_fee`, and `free_over`.

## Expected behavior

- For a paid shipping order, calculate `base_fee + weight_kg * per_kg`, apply the percentage discount, then charge at least the zone's `minimum_fee`.
- The minimum applies after the discount.
- A subtotal equal to or greater than `free_over` receives free shipping.
- Round the final charge to cents using half-up rounding.

## Reproduction

With local rates `{ "base_fee": "3.00", "per_kg": "1.25", "minimum_fee": "5.00", "free_over": "75.00" }`, a one-kilogram order with subtotal `$20` and a 50% shipping discount has a calculated discounted amount below $5. The expected quote is `Decimal("5.00")`. At a `$75` subtotal, the expected quote is `Decimal("0.00")`.

## Review task

Trace the quote calculation and compare the returned amount with the minimum and free-shipping contract. Add a focused regression assertion for the discounted light parcel and explain why the free-shipping threshold takes precedence over the minimum.

## Starter Code

[View starter code](../../round-1/20-shipping-fee-calculator/)

## Reference Solution

[View solution](../../solutions/round-1/20-shipping-fee-calculator/)
