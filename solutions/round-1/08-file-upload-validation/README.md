# File Upload Validation — Reference Solution

## What was broken

The draft checked whether a name ended in an allowed suffix but accepted directory paths and allowed a PDF extension paired with a PNG MIME type. It also treated `True` as a one-byte file because Python booleans are integers.

## Reproduce the issue

Run `python3 upload_validation.py` in the starter folder. Path traversal, mismatched type, and boolean-size cases are accepted by the draft even though the endpoint contract rejects them.

## Investigation approach

Treat upload metadata as three related inputs: the client filename must be a plain leaf name, the final extension must map to the declared media type, and the byte count must be an integer within the inclusive size range. Validate each before returning normalized metadata.

## Correction

The solution rejects path separators, NUL/control characters, blank or padded names, and extension-only hidden filenames. It matches the final supported suffix to a normalized MIME type and accepts sizes from 1 through 5,000,000 bytes, excluding booleans.

## Regression tests

Tests cover PDF and case-insensitive PNG success, whitespace normalization of MIME type, the inclusive upper limit, Unix and Windows path components, mismatched type, double extensions, hidden names, and invalid sizes.
