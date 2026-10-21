# Ticket #14 — Checkout Promotion Engine

**Difficulty:** Medium

## Problem

### Reported symptom

Some shoppers receive a discount for products the promotion excludes, and the displayed tax and final total do not agree with the cart.

### Scenario

A cart can contain eligible and ineligible products. Promotions have minimum spend rules, while checkout calculates discount, tax, and the amount due in integer cents.

## Acceptance Criteria
- Promotion eligibility and minimum subtotal determine whether a discount applies.
- The discount cannot exceed the eligible amount; tax is calculated after the discount and the final total never becomes negative.
- Invalid requests must leave persisted state unchanged.

## State Invariants

The discount cannot exceed the eligible amount; tax is calculated after the discount and the final total never becomes negative.

## Investigation

Trace line validation, promotion eligibility, and the order of subtotal, discount, and tax calculations. Compare mixed carts to carts containing only eligible items. Add regression coverage for the behavior you reproduce.

## Starter Code

[View starter code](../../round-2/14-checkout-promotion-engine/)

## Reference Solution

[View solution](../../solutions/round-2/14-checkout-promotion-engine/)
