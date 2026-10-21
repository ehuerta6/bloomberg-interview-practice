# Checkout Promotion Engine Reference Solution

## What Was Broken

For percentage promotions with SKU restrictions, the starter calculated the discount from the whole cart subtotal instead of the eligible lines. A cart containing books and pens could therefore discount the pens even when the promotion applied only to books. Fixed discounts could also exceed the eligible subtotal when the rest of the cart contained excluded products.

## Reproduce and Investigate

From this folder, run `python3 test_promotion_engine.py`. The mixed-cart test applies `SAVE10` to a $60 eligible book and a $40 ineligible pen; inspect the quote’s discount and total. The fixed-discount case checks a $5 promotion against a $2 eligible item beside an excluded $10 item. Trace `quote` through `PromotionEngine.discount` and compare cart subtotal with the eligible subtotal.

## The Fix

The engine sums only eligible lines for the discount and caps both percentage and fixed discounts at that eligible amount. It still checks minimum spend against the full cart subtotal. Checkout subtracts the discount before calculating tax, then adds tax to produce the total.

## Regression Tests

The suite covers percentage math and post-discount tax, an ineligible cart, minimum spend, mixed eligible and excluded lines, and a fixed discount capped at eligible value so the total stays nonnegative.

## Run

```sh
python3 test_promotion_engine.py
```
