# Shared Document Permissions Reference Solution

## Reported behavior

Access checks can fall through to a direct or inherited grant after a collaborator has been revoked at the document. A revoked collaborator can retain access through a parent folder, so revocation precedence needs to be explicit.

## Reproduce and investigate

From this folder, run:

```sh
python3 test_document_permissions.py
```

Start with `routes.py` to see the request boundary, then follow the call into `service.py` and the in-memory `repository.py`. Reproduce the reported scenario and inspect repository state before and after each operation. The starter tests include examples that pass and regressions that expose the issue.

## Fix

Resolve ownership first, then apply document-specific revocation, direct grant, and folder inheritance from nearest parent outward. A folder revocation blocks inherited access at that folder boundary while a document-level direct grant can explicitly regrant access. Apply role levels consistently to read, edit, and share.

## Regression coverage

The solution tests cover valid and invalid requests, state invariants, boundary conditions, repeated operations, and failure paths. They assert the data stored in the repository as well as returned results.

## Run the solution tests

```sh
python3 test_document_permissions.py
```
