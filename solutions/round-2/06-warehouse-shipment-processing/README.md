# Warehouse Shipment Processing Reference Solution

## What Was Broken?

An all-or-nothing order could fail on a later SKU after earlier inventory had already been reserved.

## Reproduce the Behavior

From this folder, run `python3 test_shipments.py`; `test_failed_order_releases_every_reservation` requests 3 units of `sku-a` and 3 of `sku-b`, while only 2 units of `sku-b` exist. The starter leaves the 3 units it reserved for `sku-a` held after it returns `backordered`.

## Investigation

Trace each order line through reservation, shipment commit, and backorder recording. Use an order where an early SKU is available but a later SKU is short, then inspect both on-hand quantities and reservation records after the failed all-or-nothing attempt. Compare that result with the explicitly partial-fulfillment path.

## Fix

The service tracks each reservation made during an all-or-nothing attempt and releases all of them if a later line cannot be reserved. Partial fulfillment commits only available quantities and stores only positive remainders as backorders.

## Regression Tests

The tests cover successful full shipment, rollback after a later SKU fails, partial shipment with a recorded remainder, duplicate shipment IDs, and invalid quantities. They assert that failure leaves no orphan reservations and that committed shipment quantities reconcile with inventory.

## Run the Corrected Tests

```sh
python3 test_shipments.py
```
