# Feature Flag Evaluation — Reference Solution

## What broke

The draft turns on a user with no ID at 100 percent rollout and includes the bucket exactly equal to the configured percentage, although rollout membership is defined by a strict less-than comparison.

## Reproduce the issue

Run `python3 feature_flags.py` in the starter folder. The focused regression case demonstrates the discrepancy. Run `python3 feature_flags.py` here to verify the corrected behavior.

## Investigation approach

Trace the implementation in policy order and compare each branch against the boundary conditions in the challenge. Use small inputs that isolate one decision at a time, then check state, ordering, and input preservation where they apply.

## Correction

The solution applies the challenge rules explicitly, checks invalid inputs before using them, and avoids unintended mutation or unstable decisions. The corrected behavior is implemented independently rather than importing starter code.

## Regression tests

The tests cover ordinary cases, the defect boundary, adjacent edge cases, and invariants. Run them with `python3 feature_flags.py`.
