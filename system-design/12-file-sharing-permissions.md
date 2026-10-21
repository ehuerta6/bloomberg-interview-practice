# Problem 12 — File Sharing & Permissions

**Difficulty:** Medium

## Scenario

A campus research group needs a simple place to upload project files and share selected files with collaborators. Files may be large, so the application should not keep their bytes in its relational database. Some collaborators should only view a file; others may download it. Owners need to revoke access and must be able to tell who owns each file.

Design a first version for authenticated campus users. Folders and real-time collaboration are not required.

## Functional Requirements

- A user can upload a file, provide a display name, list their files, download a file, and soft-delete a file they own.
- The system stores file bytes in private object storage and stores file metadata and the opaque storage key in the application database.
- An owner can grant another user `viewer` or `editor` access to an individual file and can revoke that grant.
- Viewers can read metadata and download. Editors can also update the display name, including through an editor share link. Only the owner can grant/revoke access or delete the file.
- Every download and metadata change must check current authorization. Knowing a storage key or URL must not be sufficient to access a private object.
- A completed file cannot be overwritten by reusing an upload authorization issued for a pending upload.
- The owner can create an optional share link with a selected `viewer` or `editor` permission and an expiration time. The owner can revoke it. A link that is expired, revoked, or tied to a deleted file grants no access.
- Uploads have a maximum size and an allowed content-type list supplied by application configuration. Failed or abandoned uploads must not create a visible completed file record.

## Constraints & Assumptions

- Assume account authentication already exists. A share link acts as a bearer capability; explain the risks and limit what a link can do.
- Store a hash of a high-entropy link token rather than its raw value. The object bucket is private; downloads are mediated by the application or by a short-lived signed URL issued after an authorization check.
- Upload can use a two-step flow: create pending metadata, upload bytes, then finalize. Clarify how failed finalization and orphaned objects are cleaned up.
- No virus scanning, version history, folder hierarchy, or public search is required in the initial design.
- State whether editors can reshare. For this version, only the owner manages access grants and links.

## Your Task

Design the upload, download, sharing, and revocation flows. Identify which data belongs in the relational database and which belongs in object storage. Explain how each request is authorized, including the difference between a user grant and a bearer share link. Walk through what happens if upload bytes succeed but finalization fails, and how access revocation affects previously issued download URLs.

## Interviewer Follow-Ups

- A signed download URL remains usable briefly after the owner revokes access. What policy choices are available?
- Users need nested folders and inherited permissions. How would you model inheritance and revocation?
- A user overwrites a file with a new version. How would you prevent a partially uploaded version from replacing the last good one?

## Reference Solution

[View the reference solution](../solutions/system-design/12-file-sharing-permissions.md)
