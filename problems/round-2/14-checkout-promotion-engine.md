# Ticket #14 — Checkout Promotion Engine

**Difficulty:** Medium

## Context

You maintain price quotes for a campus shop. A cart line is `(sku, quantity,
unit_price_cents)`; a SKU identifies one product. Promotions may apply to a set
of eligible SKUs and require a minimum whole-cart subtotal. A quote returns
`subtotal`, `discount`, `tax`, and `total`, all in cents.

## Practice report

Configure `SAVE10` as 10 percent off books, with a 5000-cent minimum. Quote one
6000-cent `book` and one excluded 4000-cent `pen`, with tax rate 0.

| Observation | Current starter | Expected |
| --- | --- | --- |
| Cart subtotal | 10000 | 10000 |
| Discount | 1000 | 600 |
| Total | 9000 | 9400 |

The customer should receive the promotion only on eligible merchandise.

## Acceptance Criteria

- Validate line quantities and prices: quantities must be positive and unit
  prices nonnegative; an invalid line raises `ValueError` without changing the
  promotion store.
- Determine minimum spend from the full cart subtotal. A missing/unknown code,
  insufficient spend, or a cart with no eligible products gives no discount.
- Percentage promotions apply to the eligible subtotal, using the existing
  whole-cent floor calculation. Fixed promotions cannot exceed that eligible
  subtotal; an empty eligible-SKU set means all products are eligible.
- Subtract the discount before calculating tax, retaining the existing
  `round(taxable_amount * tax_rate)` behavior. Total equals taxable amount plus tax
  and cannot become negative for the supplied valid promotion/tax inputs.
- Quotes do not modify the cart or saved promotions. A 6000-cent eligible cart
  with a 600-cent discount and tax rate 0.1 yields tax 540 and total 5940.

## Out of Scope

Keep the quote API, existing rounding, and configured promotion data. Promotion
stacking, shipping charges, tax jurisdiction rules, and new rate-validation
policies are outside this ticket.

## Investigation

Reproduce the mixed cart, then compare it with eligible-only and excluded-only
carts. Add regression assertions for every quote field, minimum spend, and a
fixed discount larger than the eligible value. Explain how the results satisfy
the pricing contract without changing rounding behavior.

## Starter Code

[View starter code](../../round-2/14-checkout-promotion-engine/)

## Reference Solution

[View solution](../../solutions/round-2/14-checkout-promotion-engine/)
