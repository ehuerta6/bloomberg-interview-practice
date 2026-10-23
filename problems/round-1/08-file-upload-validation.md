# PR #08 — File Upload Validation

**Difficulty:** Easy

**PR title:** Validate document upload metadata

## Summary

A profile service accepts PDF documents and PNG images. Before metadata reaches storage, it needs a filename, declared media type, and byte count that agree with the upload policy. You are reviewing `validate_upload(filename, content_type, size_bytes)`; this task validates metadata, not the contents of the uploaded file.

## Expected behavior
- `validate_upload(filename, content_type, size_bytes)` returns a metadata dictionary or raises `ValueError`.
- Only plain leaf filenames are accepted. Reject empty or padded names, slash or backslash path components, NUL/control characters, and extension-only names.
- Accept final extensions `.pdf` and `.png` case-insensitively. The media type must match the extension; normalize media type whitespace and case.
- Size must be a non-boolean integer from 1 through 5,000,000 bytes inclusive.
- Return the original filename, normalized media type, and original byte count.

## Contract examples

`validate_upload("chart.PNG", " IMAGE/PNG ", 300)` returns:

```python
{"filename": "chart.PNG", "content_type": "image/png", "size_bytes": 300}
```

| Filename | Media type | Bytes | Expected outcome |
| --- | --- | ---: | --- |
| `"large.pdf"` | `"application/pdf"` | 5000000 | Metadata accepted |
| `"large.pdf"` | `"application/pdf"` | 5000001 | `ValueError` |
| `"photo.png"` | `"application/pdf"` | 10 | `ValueError` |
| `"../private.pdf"` | `"application/pdf"` | 10 | `ValueError` |

A leaf filename means a filename alone, without directory components.

## Review task

Compare the implementation and tests with the filename, media-type, and size contract. Correct discrepancies and add regression cases that check the full returned metadata on success and rejection at both size boundaries. Include invalid metadata types without assuming that a permitted extension proves the file's contents.

## Starter Code

[View starter code](../../round-1/08-file-upload-validation/)

## Reference Solution

[View solution](../../solutions/round-1/08-file-upload-validation/)
