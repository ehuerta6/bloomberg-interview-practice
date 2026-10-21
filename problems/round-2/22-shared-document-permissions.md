# Ticket #22 — Shared Document Permissions

**Difficulty:** Hard

## Problem

### Reported symptom

A product team stores shared documents inside nested folders. A former contractor can still open a file through an inherited folder grant after a revocation. The team needs explicit precedence across ownership, direct sharing, nested inheritance, and revocation.

### Scenario

Create a root folder, child folder, and document. Add grants at different levels, then revoke the same user at the document and folder levels. Check what permission source wins each time.

## Acceptance Criteria
- The document owner always has owner access and cannot be revoked.
- The nearest folder grant wins when no document grant exists.
- Document revocation denies direct and inherited grants until an explicit regrant.
- Folder revocation blocks that user’s inherited access through that folder.
- Unknown actions and document IDs are denied.

## State Invariants
- Owner is immutable and has full permissions.
- A revoked user cannot inherit access through the revoked scope.
- Role capabilities are monotonic: owner > editor > viewer.
- Access resolution is deterministic regardless of grant insertion order.

## Investigation

Resolve access in a root folder, nested folder, and document while grants exist at several levels. Compare direct grants with nearest inherited grants, then revoke at the document and folder scopes; verify owner access remains stable and resolution does not depend on insertion order.

## Starter Code

[View starter code](../../round-2/22-shared-document-permissions/)

## Reference Solution

[View solution](../../solutions/round-2/22-shared-document-permissions/)
