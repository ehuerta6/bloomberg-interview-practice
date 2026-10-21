# PR #08 — File Upload Validation

**Difficulty:** Easy

**PR title:** Validate document upload metadata

## Summary

A small profile service accepts PDF documents and PNG images. This change validates the filename, declared media type, and byte size before passing upload metadata to storage.

## Expected behavior
- `validate_upload(filename, content_type, size_bytes)` returns a metadata dictionary or raises `ValueError`.
- Only plain leaf filenames are accepted. Reject empty or padded names, slash or backslash path components, NUL/control characters, and extension-only names.
- Accept final extensions `.pdf` and `.png` case-insensitively. The media type must match the extension; normalize media type whitespace and case.
- Size must be a non-boolean integer from 1 through 5,000,000 bytes inclusive.
- Return the original filename, normalized media type, and original byte count.

## Review task

Review what the extension check actually establishes. Try path-like names, a supported suffix with an unrelated media type, and Python values that are technically integers but should not represent byte counts. Add tests for the accepted boundary and rejected metadata.

## Starter Code

[View starter code](../../round-1/08-file-upload-validation/)

## Reference Solution

[View solution](../../solutions/round-1/08-file-upload-validation/)
