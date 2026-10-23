# PR #01 — Code Validator

**Difficulty:** Easy

**PR title:** Add student access code validation

## Summary

You are reviewing a PR for the club registration flow. Students enter an access code as text, and a leading zero is part of the code. The PR adds `is_valid_access_code(code)` so the form can accept a valid code or report a validation failure without raising an exception.

## Expected behavior
- A valid code is a string containing exactly six ASCII digits (`0` through `9`).
- Leading zeros are meaningful and valid.
- Every other value is invalid and returns `False`.
- Invalid strings are ordinary validation failures and do not raise an exception.

## Contract examples

| Input to `is_valid_access_code` | Expected return |
| --- | --- |
| `"001234"` | `True` |
| `"12a456"` | `False` |
| `"12345"` | `False` |
| `123456` (an integer) | `False` |

The table states the required contract results.

## Review task

Compare the validator and its assertions with the six-character text contract. Correct discrepancies, add regression coverage for accepted and rejected inputs, and explain which assertions demonstrate that invalid input returns `False` without raising.

## Starter Code

[View starter code](../../round-1/01-code-validator/)

## Reference Solution

[View solution](../../solutions/round-1/01-code-validator/)
