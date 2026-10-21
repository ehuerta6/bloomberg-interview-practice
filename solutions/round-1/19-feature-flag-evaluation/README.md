# Feature Flag Evaluation — Reference Solution

## What broke

The draft hashes `str(None)` when `user_id` is missing, so a missing ID can enter a 100 percent rollout. It also uses `bucket <= percentage`; a user whose bucket equals the rollout percentage is enabled even though the policy requires `bucket < percentage`.

## Reproduce the issue

From `round-1/19-feature-flag-evaluation/`, run `python3 feature_flags.py`. `test_missing_user_does_not_get_rollout` and `test_rollout_bucket_uses_strict_percentage_boundary` fail: the first returns `True` for a user without an ID at 100 percent, and the second returns `True` when the rollout equals the user's bucket. Run `python3 feature_flags.py` in this solution folder to confirm the cases pass.

## Investigation approach

Follow `evaluate_flag` from the global `enabled` check through user-list handling to percentage rollout. Inspect what happens when `user.get("user_id")` returns `None`, then compute the deterministic SHA-256 bucket for `customer-42` and compare it with an equal percentage. This separates the missing-ID case from the off-by-one boundary.

## Correction

The solution returns `False` before list lookup or hashing when the ID is missing. It validates rollout values, handles 0 and 100 explicitly, and uses the strict comparison `bucket < percentage` for intermediate rollouts. The hash remains stable across processes because it uses SHA-256 rather than Python's randomized `hash()`.

## Regression tests

`test_missing_user_does_not_get_rollout` and `test_rollout_bucket_uses_strict_percentage_boundary` cover both defects. The suite also checks global disable, allow/deny precedence, 0 and 100 percent, dictionary-order independence, and invalid percentages. Run it with `python3 feature_flags.py`.
