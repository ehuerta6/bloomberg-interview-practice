# Product Returns & Exchanges Reference Solution

## What was wrong

The exchange path restored the returned SKU before checking replacement availability. If the replacement was out of stock, the request failed after increasing the original SKU’s stock, with no return case recorded. Return limits also need to include prior refunds and exchanges, scoped to the order line.

## Reproduce and investigate

From the starter folder, run:

```sh
python3 test_returns.py
```

Try to exchange one coat for a missing replacement SKU. Compare `repo.stock` and `repo.returns` before and after the failed request. Trace the request through `ReturnRoutes.post` and `ReturnService.process`, paying attention to when inventory changes relative to validation.

## Fix

Validate the return ID, order line, remaining returnable quantity, action, and replacement availability before changing stock. For a valid exchange, consume replacement stock and restore the original SKU, then record one return case. Track returned quantity across refunds and exchanges for the same order and line; reject duplicate request IDs.

## Regression tests

- `test_failed_exchange_is_atomic` verifies that an unavailable replacement changes neither stock nor the return ledger.
- `test_exchange_restores_returned_unit_and_consumes_replacement` checks both sides of a successful exchange.
- `test_combined_returns_cannot_exceed_purchased_quantity` combines refund and exchange quantities against the purchase limit.
- Other tests check exact refund amounts, invalid and duplicate requests, partial refunds, missing replacement SKUs, and line IDs shared by separate orders.

## Run the solution tests

```sh
python3 test_returns.py
```
