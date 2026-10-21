# PR #19 — Feature Flag Evaluation

**Difficulty:** Medium

## PR title

Evaluate feature rollouts consistently

## Summary

A rollout service combines a global enable switch, explicit user lists, and deterministic percentage cohorts. Review whether precedence and rollout boundaries match the policy.

## Input and output

`evaluate_flag(flag, user)` receives a flag dictionary with `enabled`, optional `allowlist`, optional `denylist`, and optional `rollout_percent` fields. The user dictionary supplies a stable `user_id`. The function returns a boolean.

If rollout is used, the percentage must be numeric and between 0 and 100. A missing user ID is treated as off.

## Expected behavior, edge cases, and invariants
- A globally disabled flag is always off.
- A denylisted user is off even if also allowlisted. An allowlisted user is on unless denied.
- Other users receive a stable bucket from 0 through 99 based on SHA-256 of their user ID string. Enable the user when the bucket is strictly less than `rollout_percent`.
- A percentage of 0 enables no rollout users; 100 enables every user with an ID. Invalid percentages are rejected.

## Review task

Test precedence before rollout, exact bucket boundaries, stable results across calls, malformed percentages, and users without IDs.


## Starter Code

[View starter code](../../round-1/19-feature-flag-evaluation/)

## Reference Solution

[View solution](../../solutions/round-1/19-feature-flag-evaluation/)
