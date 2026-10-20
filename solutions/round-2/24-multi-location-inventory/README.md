# Multi-Location Inventory Reference Solution

## Reported behavior

Transfer lifecycle updates source stock and transfer status separately. A duplicate delivery or a receive/cancel race can create or destroy units unless each state transition is atomic and idempotent.

## Reproduce and investigate

From this folder, run:

```sh
python3 test_inventory_transfers.py
```

Start with `routes.py` to see the request boundary, then follow the call into `service.py` and the in-memory `repository.py`. Reproduce the reported scenario and inspect repository state before and after each operation. The starter tests include examples that pass and regressions that expose the issue.

## Fix

Reserve units at the source when a transfer starts, then atomically move the transfer from in_transit to received or cancelled. Receiving adds destination stock exactly once; cancellation restores source stock exactly once. Reject duplicate IDs, invalid quantities, same-location moves, and insufficient stock without partial writes.

## Regression coverage

The solution tests cover valid and invalid requests, state invariants, boundary conditions, repeated operations, and failure paths. They assert the data stored in the repository as well as returned results.

## Run the solution tests

```sh
python3 test_inventory_transfers.py
```
