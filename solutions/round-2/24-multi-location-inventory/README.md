# Multi-Location Inventory Reference Solution

## What was wrong

Starting a transfer deducted units from the source and also credited the destination immediately. Receiving the in-transit transfer credited the destination a second time; cancelling it restored the source but left the premature destination credit behind.

## Reproduce and investigate

From the starter folder, run:

```sh
python3 test_inventory_transfers.py
```

Start a transfer from east to west and inspect both quantities before receiving it. Then receive it and compare the destination quantity with the requested transfer. Also start and cancel a separate transfer, checking that the source is restored and the destination is unchanged. Trace each transition through `TransferService.start`, `receive`, and `cancel`.

## Fix

Deduct the source quantity when the transfer enters `in_transit`, but leave destination stock unchanged until receipt. A successful receipt credits the destination once and marks the transfer received. Cancellation restores the source once and marks the transfer cancelled. Reject duplicate IDs and operations that do not match the current transfer state.

## Regression tests

- `test_start_then_receive_moves_stock_once` checks the destination before and after receipt.
- `test_receive_twice_is_rejected_without_duplication` checks repeat delivery.
- `test_cancel_restores_source_and_cannot_be_received` verifies cancellation’s stock effects and terminal state.
- Other tests cover invalid starts, duplicate IDs, same-location transfers, conservation including in-transit units, and cancellation after receipt.

## Run the solution tests

```sh
python3 test_inventory_transfers.py
```
