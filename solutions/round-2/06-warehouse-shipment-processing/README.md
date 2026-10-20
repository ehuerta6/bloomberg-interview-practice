# Warehouse Shipment Processing Reference Solution

## What Was Broken?

An all-or-nothing order could fail on a later SKU after earlier inventory had already been reserved.

## Reproduce the Behavior

From this folder, run `python3 test_shipments.py`; `test_failed_order_releases_every_reservation` requests 3 units of `sku-a` and 3 of `sku-b`, while only 2 units of `sku-b` exist. The starter leaves the 3 units it reserved for `sku-a` held after it returns `backordered`.

## Investigation

Trace each SKU through reservation, commit, and backorder recording. Inspect inventory and reservations at the point a later line fails; then compare all-or-nothing and partial fulfillment results. The tests check the stored records and state totals so the failure is visible at the domain boundary.

## Fix

The service tracks each reservation made during an all-or-nothing attempt and releases all of them if a later line cannot be reserved. Partial fulfillment commits only available quantities and stores only positive remainders as backorders.

## Regression Tests

The corrected suite covers the reported failure, normal success, rejected and repeated requests, and state invariants. It also checks boundary or retry behavior with deterministic clocks and in-memory repositories. All assertions inspect returned results and persisted state.

## Run the Corrected Tests

```sh
python3 test_shipments.py
```
