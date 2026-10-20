# Rolling Analytics Window — Reference Solution

## What broke

The draft compares timezone-aware and naive timestamps directly, leaking a TypeError instead of rejecting the malformed comparison through the documented ValueError interface.

## Reproduce the issue

Run `python3 rolling_window.py` in the starter folder. The focused regression case demonstrates the discrepancy. Run `python3 rolling_window.py` here to verify the corrected behavior.

## Investigation approach

Trace the implementation in policy order and compare each branch against the boundary conditions in the challenge. Use small inputs that isolate one decision at a time, then check state, ordering, and input preservation where they apply.

## Correction

The solution applies the challenge rules explicitly, checks invalid inputs before using them, and avoids unintended mutation or unstable decisions. The corrected behavior is implemented independently rather than importing starter code.

## Regression tests

The tests cover ordinary cases, the defect boundary, adjacent edge cases, and invariants. Run them with `python3 rolling_window.py`.
