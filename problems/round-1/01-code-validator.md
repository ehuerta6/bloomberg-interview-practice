# PR #01 — Code Validator

**Difficulty:** Easy

**PR title:** Add student access code validation

## Summary

This change adds a small validator for student access codes before they are accepted by the club registration flow.

## Expected behavior
- A valid code is a string containing exactly six ASCII digits (`0` through `9`).
- Leading zeros are meaningful and valid.
- Every other value is invalid and returns `False`.
- Invalid strings are ordinary validation failures and do not raise an exception.

## Review task

Review the proposed implementation and tests against the contract. Correct the implementation and any tests that fail to express the expected behavior. Add regression cases and explain which cases give you confidence in the result.

## Starter Code

[View starter code](../../round-1/01-code-validator/)

## Reference Solution

[View solution](../../solutions/round-1/01-code-validator/)
