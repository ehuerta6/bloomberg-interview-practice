# PR #19 — Feature Flag Evaluation

**Difficulty:** Medium

## PR title

Evaluate feature rollouts consistently

## Summary

A rollout service releases a feature to selected users before enabling it for everyone. A feature flag is the policy describing that release: a global switch, explicit exceptions, and an optional percentage of users. You are reviewing evaluation so a user receives the same decision on repeated calls and explicit exclusions keep their priority.

## Input and output

`evaluate_flag(flag, user)` receives a flag dictionary with `enabled`, optional `allowlist`, optional `denylist`, and optional `rollout_percent` fields. The user dictionary supplies a stable `user_id`. The function returns a boolean.

If rollout is used, the percentage must be numeric and between 0 and 100. A missing user ID is treated as off.

## Expected behavior, edge cases, and invariants
- A globally disabled flag is always off.
- A denylisted user is off even if also allowlisted. An allowlisted user is on unless denied.
- Other users receive a stable bucket from 0 through 99 based on SHA-256 of their user ID string. Enable the user when the bucket is strictly less than `rollout_percent`.
- A percentage of 0 enables no rollout users; 100 enables every user with an ID. Invalid percentages are rejected.

## Contract examples

Evaluate these policies for `user={"user_id": "u1"}`:

| Flag fields | Expected return |
| --- | --- |
| `{"enabled": False, "allowlist": ["u1"]}` | `False` |
| `{"enabled": True, "allowlist": ["u1"], "denylist": ["u1"]}` | `False` |
| `{"enabled": True, "allowlist": ["u1"]}` | `True` |
| `{"enabled": True, "rollout_percent": 0}` | `False` |
| `{"enabled": True, "rollout_percent": 100}` | `True` |

A percentage rollout assigns each identified user a repeatable bucket, numbered 0 through 99. A user without an ID is off even at 100 percent. An enabled flag with `rollout_percent="50"` is invalid: a numeric-looking string is not a numeric percentage.

## Review task

Compare the evaluator and its assertions with global disable, direct exclusions, direct inclusion, and rollout decisions. Correct discrepancies and add tests for the exact bucket boundary, repeated calls for one user, missing IDs, and invalid percentages. Explain which assertions establish precedence and which establish repeatability.

## Starter Code

[View starter code](../../round-1/19-feature-flag-evaluation/)

## Reference Solution

[View solution](../../solutions/round-1/19-feature-flag-evaluation/)
