# PR #03 — Cappy's Snack Inventory

**Difficulty:** Easy

**PR title:** Manage Cappy's snack inventory

## Summary

Cappy keeps snacks for Coding Interview Club meetings. A member may reserve snacks only when enough are available, and a failed request must leave the stock available to others. You are reviewing the `SnackInventory` class and its `restock(snack, quantity)` and `reserve(snack, quantity)` operations, each of which returns a success boolean.

## Expected behavior
- Quantities are nonnegative integers; invalid quantities are rejected consistently.
- Restocking a positive quantity increases available stock.
- A successful reservation decreases stock by the requested quantity.
- A reservation that cannot be fulfilled leaves inventory unchanged.
- Invalid operations must not corrupt inventory state.

## Contract example

Start with `SnackInventory({"bars": 2})` and perform these operations in order:

| Operation | Expected return | Stock of `bars` afterward |
| --- | --- | ---: |
| `restock("bars", 3)` | `True` | 5 |
| `reserve("bars", 2)` | `True` | 3 |
| `reserve("bars", 4)` | `False` | 3 |

A fractional restock such as `1.5` is invalid and leaves the existing stock unchanged.

## Review task

Review each operation's return value and inventory state against the reservation contract. Correct inconsistent assertions as well as implementation defects. Add regression cases that distinguish a completed reservation, insufficient stock, and invalid quantities, with state assertions after rejected operations.

## Starter Code

[View starter code](../../round-1/03-snack-inventory/)

## Reference Solution

[View solution](../../solutions/round-1/03-snack-inventory/)
