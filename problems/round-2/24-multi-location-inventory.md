# Ticket #24 — Multi-Location Inventory

**Difficulty:** Hard

## Problem

### Reported symptom

Warehouse staff move goods between retail locations. Recent counts show phantom stock after repeated delivery scans and missing stock after cancelled shipments. The tool uses a local ledger and does not call shipping systems.

### Scenario

Trace a transfer through start, receive, repeat receive, and cancellation. Compare total stock across locations and inspect the transfer status at each step.

## Acceptance Criteria
- Starting a transfer removes units from source stock and records one in-transit transfer.
- Receiving adds exactly the reserved units to destination stock once.
- Cancelling restores the source exactly once and prevents receipt.
- Invalid transfers change neither stock nor transfer history.
- Reject operations that do not match the transfer state.

## State Invariants
- Across an in-transit transfer, total on-hand plus in-transit stock is conserved.
- Each transfer has exactly one terminal outcome.
- A terminal transfer cannot be received or cancelled again.

## Investigation

Follow one transfer from start through receive, repeated receive, and cancellation attempts. Run a second transfer through cancellation before receipt. Reconcile source stock, destination stock, in-transit units, and transfer state after every transition.

## Starter Code

[View starter code](../../round-2/24-multi-location-inventory/)

## Reference Solution

[View solution](../../solutions/round-2/24-multi-location-inventory/)
