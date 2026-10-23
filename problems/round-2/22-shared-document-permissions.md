# Ticket #22 — Shared Document Permissions

**Difficulty:** Hard

## Context

You maintain sharing for documents inside nested folders. A direct grant is on
the document; an inherited grant comes from its folder or a parent folder.
A viewer may read, an editor may read and edit, and the document owner may also
share. Revocation denies a user access at a specified scope.

## Practice report

Create folder `root`, its child `child`, and document `d` in `child`, owned by
`owner`. Grant `sam` editor access on `root` and viewer access directly on `d`.
Revoke `sam` on `d`, then ask for `role("d", "sam")` and read access.

| Observation | Current starter | Expected |
| --- | --- | --- |
| Resolved role | `viewer` | `None` |
| Read route status | 200 | 403 |

The document revocation must hold despite the two existing grant sources.

## Acceptance Criteria

- The immutable document owner always resolves as `owner` and cannot be revoked.
  Owner, editor, and viewer capabilities follow the read/edit/share levels above.
- A document revocation denies direct and inherited grants until an explicit
  document regrant clears it. Revocation must not change another user's access.
- Otherwise, a document grant wins over inherited grants. Without a document
  grant, use the nearest applicable folder grant while walking toward the root.
- A folder revocation blocks inherited access through that scope. A direct
  document grant can still provide access; it is distinct from inheritance.
- Resolve by scope, independently of grant insertion order. Folder traversal
  must terminate even if the supplied folder graph contains a cycle.
- Unknown documents and unsupported actions are denied. Invalid grants and
  attempts to revoke an owner do not change existing permissions.

## Out of Scope

Keep the existing grant/revoke APIs, role set, and folder graph. Login,
organization-wide policies, new actions such as deletion, and redesigning folder
storage are outside this ticket.

## Investigation

Reproduce the revocation report and compare direct, nearest-folder, and
parent-folder grants. Add tests for document and folder revocation, explicit
regrant, owner protection, and unsupported actions. Assert both the resolved role and
route result after each permission change.

## Starter Code

[View starter code](../../round-2/22-shared-document-permissions/)

## Reference Solution

[View solution](../../solutions/round-2/22-shared-document-permissions/)
