# Seat Allocation — Reference Solution

## What broke

The draft assigned groups in input order and selected the first row with a fitting block. It could use a partly accessible block for a group that requires accessible seating, and it could consume a tight row while a roomier row was available.

## Reproduce the issue

Run `python3 seat_allocation.py` in the starter folder. Priority, accessibility, and row-selection cases show where allocations diverge from the policy. Run the corrected implementation independently with `python3 seat_allocation.py` here.

## Investigation approach

Model allocation as a sequence of constraints: rank requests, find a whole consecutive available block in one row, enforce accessibility across the block, then compare all eligible blocks using the stated tie-break rules. Track availability separately so input data remains unchanged.

## Correction

The solution validates rows and requests, processes groups by descending priority with stable ties, and uses a best-fit row followed by insertion order and seat number. It marks availability in a private working map and returns assignments plus unassigned group IDs.

## Regression tests

Tests cover contiguous blocks, occupied seats, groups that cannot fit, accessibility, priority, best-fit choice, deterministic ties, non-mutation, and invalid requests. Run them with `python3 seat_allocation.py`.
