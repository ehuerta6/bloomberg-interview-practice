# 20 · Shipping Fee Calculator

**Round:** 1 · PR Review

**Difficulty:** Medium

## PR title

Calculate shipping by zone and weight

## Summary

A store needs predictable parcel charges for multiple shipping zones. Review its free-shipping cutoff and the arithmetic used to price each shipment.

## Input and output

`calculate_shipping(order, rates)` receives an order with `zone`, `subtotal`, and `weight_kg` fields. `rates` maps each zone to a rate containing `base`, `per_kg`, and `free_over`. The function returns the shipping fee as a number rounded to cents.

## Expected behavior, edge cases, and invariants

- Reject unknown zones, missing fields, negative values, and nonnumeric amounts with `ValueError`; booleans are not valid numeric amounts.
- A subtotal equal to or above the zone's `free_over` threshold receives free shipping regardless of weight.
- Below the threshold, charge `base + weight_kg * per_kg` and round only the final fee to two decimal places.
- Do not mutate the order or rate table.

## Review task

Compare orders just below, exactly at, and above the threshold. Include fractional weights, invalid quantities, and input-preservation checks.

## Starter and solution

- [Starter code: `shipping.py`](../../round-1/20-shipping-fee-calculator/shipping.py)
- [Reference solution and explanation](../../solutions/round-1/20-shipping-fee-calculator/README.md)

Run the starter from its folder with `python3 shipping.py`.
