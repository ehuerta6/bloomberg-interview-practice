# PR #20 — Shipping Fee Calculator

**Difficulty:** Medium

**PR title:** Calculate discounted, zone-based shipping fees

## Summary

A store shows the shipping charge before checkout. The carrier prices parcels by destination and total weight, while the store offers shipping discounts and a free-shipping threshold. You are reviewing the pricing PR so the quote follows the carrier minimum and produces a predictable dollar amount rounded to cents.

## Input and output

`calculate_shipping(order, rates)` receives an order with `zone`, `subtotal`, `weight_kg`, and optional `shipping_discount_percent` fields. The discount defaults to zero. `rates` maps each zone to `base_fee`, `minimum_fee`, `free_over`, and an ordered `weight_brackets` list. Each band has an inclusive `up_to_kg` limit and `per_kg` rate; the final band uses `None` for an unbounded limit. The function returns a `Decimal` fee in dollars rounded to cents.

## Expected behavior and invariants
- Reject unknown zones, missing fields, malformed or non-finite amounts, booleans, negative amounts, discounts over 100 percent, and invalid weight-band ordering with `ValueError`.
- A subtotal equal to or above the zone's `free_over` threshold receives free shipping regardless of weight or minimum fee.
- Otherwise select the first band whose upper limit is greater than or equal to the parcel's weight; use the final unbounded band for heavier parcels.
- Calculate `base_fee + weight_kg * per_kg`, apply the percentage shipping discount, then enforce `minimum_fee`.
- Round only the final fee to two decimal places using half-up currency rounding.
- Do not mutate the order or rate table.

## Contract example

Use this rate table:

```python
{
    "local": {
        "base_fee": "3.00",
        "minimum_fee": "5.00",
        "free_over": "75.00",
        "weight_brackets": [
            {"up_to_kg": "2", "per_kg": "1.25"},
            {"up_to_kg": "5", "per_kg": "1.00"},
            {"up_to_kg": None, "per_kg": "0.80"},
        ],
    }
}
```

Each row is an independent order in zone `"local"`:

| Subtotal in dollars | Weight in kg | Shipping discount | Expected `Decimal` fee |
| ---: | ---: | ---: | --- |
| `"20"` | `"2"` | 0 | `Decimal("5.50")` |
| `"20"` | `"2.01"` | 0 | `Decimal("5.01")` |
| `"20"` | `"1"` | 50 | `Decimal("5.00")` |
| `"75.00"` | `"10"` | 0 | `Decimal("0.00")` |

The 50 percent discount on the one-kilogram parcel would fall below the carrier minimum, so the fee is $5.00. An order at the free-shipping threshold pays zero even when a carrier minimum exists.

## Review task

Review the quote and assertions against inclusive weight bands, discounts, the carrier minimum, and free shipping. Correct misleading expectations and implementation defects, then add cases on both sides of the boundaries and at a half-cent rounding point. Check the final fee and unchanged order/rate inputs, and explain the evidence for the pricing order.

## Starter Code

[View starter code](../../round-1/20-shipping-fee-calculator/)

## Reference Solution

[View solution](../../solutions/round-1/20-shipping-fee-calculator/)
