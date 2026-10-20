# 22 · Access Permission Checker

**Round:** 1 · PR Review

**Difficulty:** Hard

## PR title

Enforce access rule precedence

## Summary

A document service combines role grants, direct user overrides, and resource ownership. Incorrect precedence can expose protected data, so review every path that grants or denies access.

## Input and output

`has_permission(user, action, resource, acl)` returns a boolean. The user has an `id` and optional `roles` list. The ACL has:

- `users`: user IDs mapped to `allow` and `deny` dictionaries, each mapping a resource name to actions.
- `roles`: role names mapped to resource names and their granted actions.
- `owners`: resource names mapped to owner ID lists.

The resource key `"*"` matches any resource in direct rules or role grants.

## Expected behavior, edge cases, and invariants

- A direct user deny blocks an action even when a direct allow or role grant also matches.
- A direct allow grants access if no direct deny matches.
- Otherwise, any matching role grant allows the action. Role grants can target the resource or `"*"`.
- An owner may read their resource; ownership does not grant write or other actions. Missing or unknown user IDs are denied.

## Review task

Construct conflicting direct and role rules. Verify deny precedence for resource-specific and wildcard rules, then test ownership, unknown users, and unsupported actions.

## Starter and solution

- [Starter code: `permissions.py`](../../round-1/22-access-permission-checker/permissions.py)
- [Reference solution and explanation](../../solutions/round-1/22-access-permission-checker/README.md)

Run the starter from its folder with `python3 permissions.py`.
