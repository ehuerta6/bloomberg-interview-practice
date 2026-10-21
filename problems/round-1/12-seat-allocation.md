# PR #12 — Seat Allocation

**Difficulty:** Hard

**PR title:** Allocate prioritized groups to available seats

## Summary

An event team needs to assign each party to an available block in a venue. Review the allocator against its prioritization, adjacency, accessibility, and deterministic selection rules.

## Input and output

`allocate_seats(rows, groups)` receives an insertion-ordered mapping of row names to seat dictionaries and a list of group requests. Each seat has a positive number, an accessibility flag, and an availability flag. Each group has an ID, positive size, optional numeric priority, and optional accessibility requirement. The result contains an assignment mapping and the IDs that could not be seated.

## Expected behavior and invariants
- Process higher numeric priority first; preserve input order for groups with equal priority.
- Assign a group only to a whole, consecutive block of available seats in one row. Never split groups or reuse seats.
- When accessibility is requested, every seat in the group's block must be accessible.
- Among eligible blocks, choose the row with the least available capacity left after placement. Break ties by row insertion order, then lowest seat number.
- Keep the supplied venue data unchanged. Report every unseated group in processing order.
- Reject malformed rows or groups, nonpositive or boolean sizes, and repeated group IDs with `ValueError`.

## Review task

Build small venue layouts that force competing choices. Trace the order of requests and candidate blocks, then test accessibility across the full block, occupied seats, ties, impossible groups, and input immutability.

## Starter Code

[View starter code](../../round-1/12-seat-allocation/)

## Reference Solution

[View solution](../../solutions/round-1/12-seat-allocation/)
