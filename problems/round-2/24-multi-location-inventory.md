# Ticket 24: Multi-Location Inventory (Hard)

## Ticket

Multi-Location Inventory needs reliable state transitions.

## Reported symptom

Warehouse staff move goods between retail locations. Recent counts show phantom stock after repeated delivery scans and missing stock after cancelled shipments. The tool uses a local ledger and does not call shipping systems.

## Scenario

Trace a transfer through start, receive, repeat receive, and cancellation. Compare total stock across locations and inspect the transfer status at each step.

## Acceptance criteria

- Starting a transfer removes units from source stock and records one in-transit transfer.
- Receiving adds exactly the reserved units to destination stock once.
- Cancelling restores the source exactly once and prevents receipt.
- Invalid transfers change neither stock nor transfer history.
- Reject operations that do not match the transfer state.

## State invariants

- Across an in-transit transfer, total on-hand plus in-transit stock is conserved.
- Each transfer has exactly one terminal outcome.
- A terminal transfer cannot be received or cancelled again.

## Investigation task

Trace a normal operation, a boundary or failure case, and a repeated request across the route, service, and repository. Explain which state should change, which state must remain untouched, and how your regression tests demonstrate both outcomes. Keep the implementation in memory; no external services or frameworks are required.

## Run the starter tests

```sh
python3 test_inventory_transfers.py
```

## Exercise folders

- [Starter exercise](../../round-2/24-multi-location-inventory/)
- [Reference solution](../../solutions/round-2/24-multi-location-inventory/)
