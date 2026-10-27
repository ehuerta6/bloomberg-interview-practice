# PR #19 — Feature Flag Evaluation

**Difficulty:** Medium

## Practice Metadata

- **Interview format:** PR review / focused debugging.
- **Primary skills:** stable rollout cohorts, percentage boundaries, regression testing.
- **Expected duration:** 45–60 minutes.
- **AI assistance:** Allowed in guided practice mode for explanations, hypotheses, test ideas, and focused hints; the candidate owns and explains every change.
- **Candidate objective:** Compare the proposed change and its tests with the observable contract, then make a targeted correction and regression test.
- **Interviewer evaluation:** Clarifying questions, code investigation, root-cause reasoning, maintainable changes, testing, and communication. See the [shared interviewer rubric](../../docs/editorial/interviewer-rubric.md).

## PR title

Evaluate feature rollouts consistently

## Summary

A checkout team is expanding a new payment flow to a percentage of customers. The rollout service hashes each stable user ID into a bucket so the same customer keeps the same decision across requests. A support report says one customer at the configured rollout boundary received the feature even though the rollout percentage was meant to include only lower-numbered buckets. You are reviewing the flag evaluator.

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

Reproduce the reported customer decision from the bucket rule. Correct the boundary behavior and add a regression assertion that checks both the exact boundary and repeatability for the same user. Explain the limits of a deterministic local test for a production rollout.

## Starter Code

[View starter code](../../round-1/19-feature-flag-evaluation/)

## Reference Solution

[View solution](../../solutions/round-1/19-feature-flag-evaluation/)
