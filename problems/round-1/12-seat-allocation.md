# PR #12 — Seat Allocation

**Difficulty:** Hard

**PR title:** Allocate prioritized groups to available seats

## Summary

An event team must seat each party together while respecting priority and accessible-seat requests. A party that cannot fit must be reported rather than split across rows. You are reviewing the allocation PR; the venue map is a caller-owned snapshot, and the function returns a seating proposal without changing it.

## Input and output

`allocate_seats(rows, groups)` receives an insertion-ordered mapping of row names to seat dictionaries and a list of group requests. Each seat has a positive number, an accessibility flag, and an availability flag. Each group has an ID, positive size, optional numeric priority, and optional accessibility requirement. The result contains an assignment mapping and the IDs that could not be seated.

## Expected behavior and invariants
- Process higher numeric priority first; preserve input order for groups with equal priority.
- Assign a group only to a whole, consecutive block of available seats in one row. Never split groups or reuse seats.
- When accessibility is requested, every seat in the group's block must be accessible.
- Among eligible blocks, choose the row with the least available capacity left after placement. Break ties by row insertion order, then lowest seat number.
- Keep the supplied venue data unchanged. Report every unseated group in processing order.
- Reject malformed rows or groups, nonpositive or boolean sizes, and repeated group IDs with `ValueError`.

## Contract example

The venue has these rows in insertion order. Each listed seat is available and has `accessible=False`:

| Row key | Seat numbers |
| --- | --- |
| `"A"` | `1, 2, 3, 4` |
| `"B"` | `1, 2` |

Each seat is represented as `{"number": n, "accessible": False, "available": True}`. For `groups=[{"group_id": "g", "size": 2}]`, the expected result is:

```python
{
    "assigned": {"g": [{"row": "B", "seat": 1}, {"row": "B", "seat": 2}]},
    "unassigned": [],
}
```

Row B leaves no unused available seats after the placement, while row A would leave two. The input seats must still be marked available after the call. In a separate venue with only two available seats, a size-2 group at priority 5 is seated before a size-1 group at priority 1, even when the smaller group appears first in `groups`.

## Review task

Review whether the allocation and assertions satisfy request priority, whole-party placement, and the specified row choice. Add layouts that distinguish accessible from mixed blocks, occupied from free seats, and equal choices from impossible requests. Check the returned assignments, unassigned order, and unchanged venue snapshot, then explain the evidence for each constraint.

## Starter Code

[View starter code](../../round-1/12-seat-allocation/)

## Reference Solution

[View solution](../../solutions/round-1/12-seat-allocation/)
