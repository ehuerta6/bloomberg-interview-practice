# Ticket 22: Shared Document Permissions (Hard)

## Ticket

Shared Document Permissions needs reliable state transitions.

## Reported symptom

A product team stores shared documents inside nested folders. A former contractor can still open a file through an inherited folder grant after a revocation. The team needs explicit precedence across ownership, direct sharing, nested inheritance, and revocation.

## Scenario

Create a root folder, child folder, and document. Add grants at different levels, then revoke the same user at the document and folder levels. Check what permission source wins each time.

## Acceptance criteria

- The document owner always has owner access and cannot be revoked.
- The nearest folder grant wins when no document grant exists.
- Document revocation denies direct and inherited grants until an explicit regrant.
- Folder revocation blocks that user’s inherited access through that folder.
- Unknown actions and document IDs are denied.

## State invariants

- Owner is immutable and has full permissions.
- A revoked user cannot inherit access through the revoked scope.
- Role capabilities are monotonic: owner > editor > viewer.
- Access resolution is deterministic regardless of grant insertion order.

## Investigation task

Trace a normal operation, a boundary or failure case, and a repeated request across the route, service, and repository. Explain which state should change, which state must remain untouched, and how your regression tests demonstrate both outcomes. Keep the implementation in memory; no external services or frameworks are required.

## Run the starter tests

```sh
python3 test_document_permissions.py
```

## Exercise folders

- [Starter exercise](../../round-2/22-shared-document-permissions/)
- [Reference solution](../../solutions/round-2/22-shared-document-permissions/)
