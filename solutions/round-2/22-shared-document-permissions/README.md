# Shared Document Permissions Reference Solution

## What was wrong

Permission resolution could return a direct document grant before checking the document’s revocation set. A user revoked at the document could therefore keep access through a grant on that document or an inherited folder grant.

## Reproduce and investigate

From the starter folder, run:

```sh
python3 test_document_permissions.py
```

Grant a user editor access from the root folder and a direct viewer grant on the document, then revoke that user at the document. Check `PermissionService.role` and `DocumentRoutes.access`. Follow the lookup order through ownership, document grants, and the parent-folder chain.

## Fix

Resolve the owner first, then reject a document-revoked user before considering direct or inherited grants. Otherwise use the document grant if present, then walk from the nearest folder toward its parents. A folder revocation blocks inherited access through that scope; an explicit document regrant clears the document revocation. Apply role levels consistently to read, edit, and share.

## Regression tests

- `test_document_revocation_overrides_direct_and_inherited_grants` checks that revocation denies access despite both grant sources.
- `test_folder_revocation_blocks_inherited_access_only` checks inherited denial and an explicit document grant.
- `test_nearest_inherited_grant_and_parent_inheritance` checks nested-folder precedence.
- Other tests cover owner access, editor capabilities, invalid actions and documents, owner revocation, and termination on a folder cycle.

## Run the solution tests

```sh
python3 test_document_permissions.py
```
