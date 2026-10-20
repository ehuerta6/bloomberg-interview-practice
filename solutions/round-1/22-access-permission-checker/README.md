# Access Permission Checker — Reference Solution

## What broke

The draft returns immediately for a direct allow before checking a conflicting direct deny, granting access against the explicit user block.

## Reproduce the issue

Run `python3 permissions.py` in the starter folder. The focused regression case demonstrates the discrepancy. Run `python3 permissions.py` here to verify the corrected behavior.

## Investigation approach

Trace the implementation in policy order and compare each branch against the boundary conditions in the challenge. Use small inputs that isolate one decision at a time, then check state, ordering, and input preservation where they apply.

## Correction

The solution applies the challenge rules explicitly, checks invalid inputs before using them, and avoids unintended mutation or unstable decisions. The corrected behavior is implemented independently rather than importing starter code.

## Regression tests

The tests cover ordinary cases, the defect boundary, adjacent edge cases, and invariants. Run them with `python3 permissions.py`.
