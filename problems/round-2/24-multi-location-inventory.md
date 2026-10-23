# Ticket #24 — Multi-Location Inventory

**Difficulty:** Hard

## Context

You maintain stock transfers between shop locations. **On-hand** stock can be
sold at a location. **In-transit** units have left the source but have not yet
been received by the destination. The local ledger tracks each transfer ID
through one terminal outcome: `received` or `cancelled`.

## Practice report

Start with 8 books at `east` and 2 at `west`. Call
`start("t1", "book", "east", "west", 3)`, then receive `t1` once.

| Observation after receipt | Current starter | Expected |
| --- | --- | --- |
| East on-hand books | 5 | 5 |
| West on-hand books | 8 | 5 |
| Transfer state | `received` | `received` |

On a fresh repository, start and cancel the same transfer instead. The expected
final stock is the original 8 and 2, with the transfer marked `cancelled`.

## Acceptance Criteria

- Starting a valid transfer removes units from source on-hand stock and records
  exactly one `in_transit` transfer. Destination on-hand stock is unchanged until receipt.
- Receipt adds the transfer's units to destination stock once and changes it to
  `received`. Cancellation instead restores source stock once and changes it to
  `cancelled` without a destination credit.
- Only an in-transit transfer can be received or cancelled. Repeated receipt,
  repeated cancellation, and crossing from one terminal outcome to the other
  are rejected without further effects.
- Reject missing IDs/SKU/locations, duplicate transfer IDs, same source and
  destination, invalid nonpositive/non-integer quantities, booleans, and
  insufficient source stock without changing stock or transfer history.
- Across all transfers of a SKU, on-hand units plus in-transit units are
  conserved. Each transfer has exactly one terminal outcome.

## Out of Scope

Use the in-memory ledger and supplied location names. Carrier tracking,
shipping systems, damaged goods, and partial receipts are outside this ticket.

## Investigation

Trace start, receive, and cancellation through the two scenarios described
above. Add assertions for both locations before and after each transition,
terminal-state rejection, and conservation with several transfers in transit.

## Starter Code

[View starter code](../../round-2/24-multi-location-inventory/)

## Reference Solution

[View solution](../../solutions/round-2/24-multi-location-inventory/)
