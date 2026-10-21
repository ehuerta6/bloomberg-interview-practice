# PR #10 — CSV Import Parser

**Difficulty:** Medium

**PR title:** Import normalized account records from CSV

## Summary

A service imports user records from a CSV export. Review how it reads rows, validates fields, and turns the source values into normalized account dictionaries.

## Input and output

`parse_users(text)` accepts CSV text with the header `user_id,email,active`. It returns a list of dictionaries with string IDs, normalized email strings, and boolean active flags.

## Expected behavior and invariants
- Use CSV field boundaries, including quoted fields, rather than assuming every comma separates columns.
- Ignore blank lines and surrounding whitespace in header names and field values.
- Each nonblank data row has exactly three fields. IDs and emails are required, IDs are unique, and email values contain an `@`.
- Accept only case-insensitive `true` and `false` for the active field, and return the corresponding Python boolean.
- Reject missing or incorrect headers, malformed CSV, invalid rows, and duplicate IDs with `ValueError`.

## Review task

Review parsing at both the document and field levels. Try quoted commas, whitespace, blank rows, malformed widths, duplicate identities, and each allowed active value. Add tests that check the parsed data, not just whether a call completes.

## Starter Code

[View starter code](../../round-1/10-csv-import-parser/)

## Reference Solution

[View solution](../../solutions/round-1/10-csv-import-parser/)
