# Ticket #22 — Shared Document Permissions

**Difficulty:** Hard

## Practice Metadata

- **Interview format:** Engineering ticket / existing-code debugging.
- **Primary skills:** permission revocation, grant precedence, security regression testing.
- **Expected duration:** 50–60 minutes.
- **AI assistance:** Allowed in guided practice mode for explanations, hypotheses, test ideas, and focused hints; the candidate owns and explains every change.
- **Candidate objective:** Ensure a document revocation blocks existing grants and verify that explicit regrant restores only the affected user's access.
- **Interviewer evaluation:** Problem decomposition, code navigation, root-cause explanation, incremental implementation, and test evidence. See the [shared interviewer rubric](../../docs/editorial/interviewer-rubric.md).

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

## Core acceptance criteria

- A document-level revocation denies that user's document access even when
  direct or inherited grants already exist.
- An explicit document regrant clears the revocation for that user and document.
- Revoking one user's access does not change another user's resolved role.
- The immutable document owner retains owner access.

## Optional follow-ups

If the core regression is complete, discuss nearest-folder inheritance,
folder-level revocation, grant ordering, or cyclic folder data. Clarify the
intended precedence with the interviewer before implementing additional rules.

## Out of Scope

Keep the existing grant/revoke APIs, role set, and folder graph. Login,
organization-wide policies, new actions such as deletion, and redesigning folder
storage are outside this ticket.

## Investigation

Reproduce the document revocation report and trace the resolved role to the route response. Add a regression test for a denied user with existing grants, plus a focused check that explicit regrant restores only that user's access. Explain which other user's state remains unchanged.

## Starter Code

[View starter code](../../round-2/22-shared-document-permissions/)

## Reference Solution

[View solution](../../solutions/round-2/22-shared-document-permissions/)
