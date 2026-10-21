# PR #20 — Shipping Fee Calculator

**Difficulty:** Medium

**PR title:** Calculate discounted, zone-based shipping fees

## Summary

A store is adding a new carrier and loyalty discounts to its parcel-pricing service. The change must select a weight band, apply shipping discounts, and honor carrier minimums while keeping currency arithmetic predictable.

## Input and output

`calculate_shipping(order, rates)` receives an order with `zone`, `subtotal`, `weight_kg`, and optional `shipping_discount_percent` fields. The discount defaults to zero. `rates` maps each zone to `base_fee`, `minimum_fee`, `free_over`, and an ordered `weight_brackets` list. Each band has an inclusive `up_to_kg` limit and `per_kg` rate; the final band uses `None` for an unbounded limit. The function returns a `Decimal` fee in dollars rounded to cents.

## Expected behavior and invariants
- Reject unknown zones, missing fields, malformed or non-finite amounts, booleans, negative amounts, discounts over 100 percent, and invalid weight-band ordering with `ValueError`.
- A subtotal equal to or above the zone's `free_over` threshold receives free shipping regardless of weight or minimum fee.
- Otherwise select the first band whose upper limit is greater than or equal to the parcel's weight; use the final unbounded band for heavier parcels.
- Calculate `base_fee + weight_kg * per_kg`, apply the percentage shipping discount, then enforce `minimum_fee`.
- Round only the final fee to two decimal places using half-up currency rounding.
- Do not mutate the order or rate table.

## Review task

Trace an order through zone lookup, weight-band selection, the shipping discount, minimum fee, and free-shipping threshold. Compare just-below, exactly-at, and above-boundary cases. Include fractional weights, a half-cent rounding case, malformed rates, and inputs that reveal whether a free order is incorrectly charged a minimum.

## Starter Code

[View starter code](../../round-1/20-shipping-fee-calculator/)

## Reference Solution

[View solution](../../solutions/round-1/20-shipping-fee-calculator/)
