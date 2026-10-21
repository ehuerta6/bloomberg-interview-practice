# Access Permission Checker — Reference Solution

## What broke

The draft checks the user's `allow` rule first and returns immediately. If the same user is both allowed and denied `write` on `docs`, `has_permission` returns `True`; the explicit deny should take precedence.

## Reproduce the issue

From `round-1/22-access-permission-checker/`, run `python3 permissions.py`. `test_direct_deny_overrides_direct_allow` fails because the conflicting rules grant access. Run it in this solution folder to confirm the deny wins.

## Investigation approach

Trace `has_permission` in branch order. The direct allow branch returns before the code reads `deny`, so role checks and ownership are never reached for a direct match. Test a user with both rules and no roles to isolate that precedence defect; then separately check how role grants and owner reads behave.

## Correction

The solution checks resource-specific and wildcard direct denies first and returns `False` on a match. It then checks direct allows, role grants, and finally read-only ownership. This ordering lets a deny override every grant while keeping role and owner behavior available when no direct deny matches.

## Regression tests

`test_direct_deny_overrides_direct_allow` reproduces the defect. The suite also covers a deny overriding a role grant, direct and role grants, unsupported actions, owner read-only access, and an unknown user. Run it with `python3 permissions.py`.
