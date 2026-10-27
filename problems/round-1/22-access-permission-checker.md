# PR #22 — Access Permission Checker

**Difficulty:** Hard

## Practice Metadata

- **Interview format:** PR review / focused debugging.
- **Primary skills:** permission revocation, authorization precedence, least privilege.
- **Expected duration:** 45–60 minutes.
- **AI assistance:** Allowed in guided practice mode for explanations, hypotheses, test ideas, and focused hints; the candidate owns and explains every change.
- **Candidate objective:** Compare the proposed change and its tests with the observable contract, then make a targeted correction and regression test.
- **Interviewer evaluation:** Clarifying questions, code investigation, root-cause reasoning, maintainable changes, testing, and communication. See the [shared interviewer rubric](../../docs/editorial/interviewer-rubric.md).

## PR title

Enforce access rule precedence

## Summary

A document service grants project-wide read access to members of the `reader` role. A user-specific revocation was added after an account lost access, but the user can still read one document through the shared role. You are reviewing the authorization change. An access-control list (ACL) is the policy data supplied to the decision.

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

Reproduce a revoked user request that still receives access through a role. Correct the precedence decision and add a regression test asserting that the denied request remains denied even when the role grants it. Explain why missing and unrelated grants should stay closed.

## Starter Code

[View starter code](../../round-1/22-access-permission-checker/)

## Reference Solution

[View solution](../../solutions/round-1/22-access-permission-checker/)
