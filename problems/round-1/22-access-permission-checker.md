# PR #22 — Access Permission Checker

**Difficulty:** Hard

## PR title

Enforce access rule precedence

## Summary

A document service decides whether a user can read, write, or perform another named action on a resource. Roles provide shared grants, direct user rules provide exceptions, and ownership grants a limited read permission. You are reviewing the permission PR so conflicting rules produce a predictable access decision. An access-control list (ACL) is the policy data supplied to this decision.

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

## Contract example

Use this policy:

```python
{
    "users": {"u1": {"allow": {"docs": ["write"]}, "deny": {"docs": ["write"]}}},
    "roles": {"reader": {"*": ["read"]}},
    "owners": {"private": ["u2"]},
}
```

| User | Action | Resource | Expected return |
| --- | --- | --- | --- |
| `{"id": "u1", "roles": []}` | `"write"` | `"docs"` | `False` |
| `{"id": "u1", "roles": ["reader"]}` | `"read"` | `"docs"` | `True` |
| `{"id": "u2", "roles": []}` | `"read"` | `"private"` | `True` |
| `{"id": "u2", "roles": []}` | `"write"` | `"private"` | `False` |

The `"*"` resource key means the role's read grant applies to any resource. Owning a resource alone does not authorize editing it.

## Review task

Review permission decisions and tests for direct-rule conflicts, role grants, wildcard resources, and owner reads. Correct discrepancies and add cases where two policy sources disagree, as well as missing IDs and actions with no matching grant. Explain which rule determines each expected result.

## Starter Code

[View starter code](../../round-1/22-access-permission-checker/)

## Reference Solution

[View solution](../../solutions/round-1/22-access-permission-checker/)
