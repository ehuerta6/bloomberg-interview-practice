# PR #10 — CSV Import Parser

**Difficulty:** Medium

## Practice Metadata

- **Interview format:** PR review / focused debugging.
- **Primary skills:** CSV parsing, malformed input, import correctness.
- **Expected duration:** 45–60 minutes.
- **AI assistance:** Allowed in guided practice mode for explanations, hypotheses, test ideas, and focused hints; the candidate owns and explains every change.
- **Candidate objective:** Compare the proposed change and its tests with the observable contract, then make a targeted correction and regression test.
- **Interviewer evaluation:** Clarifying questions, code investigation, root-cause reasoning, maintainable changes, testing, and communication. See the [shared interviewer rubric](../../docs/editorial/interviewer-rubric.md).

**PR title:** Import normalized account records from CSV

## Summary

An account service imports user records from a CSV export. The export can contain quoted fields, mixed-case values, and blank lines, but each accepted row must identify one user and an explicit active state. You are reviewing the PR that turns this document into normalized account dictionaries before import.

## Input and output

`parse_users(text)` accepts CSV text with the header `user_id,email,active`. It returns a list of dictionaries with string IDs, normalized email strings, and boolean active flags.

## Expected behavior and invariants
- Use CSV field boundaries, including quoted fields, rather than assuming every comma separates columns.
- Ignore blank lines and surrounding whitespace in header names and field values.
- Each nonblank data row has exactly three fields. IDs and emails are required, IDs are unique, and email values contain an `@`.
- Accept only case-insensitive `true` and `false` for the active field, and return the corresponding Python boolean.
- Reject missing or incorrect headers, malformed CSV, invalid rows, and duplicate IDs with `ValueError`.

## Contract example

Input CSV:

```csv
user_id,email,active
7,ADA@EXAMPLE.COM,true
8,"lee, jr@example.com",false
```

Expected return:

```python
[
    {"user_id": "7", "email": "ada@example.com", "active": True},
    {"user_id": "8", "email": "lee, jr@example.com", "active": False},
]
```

The quoted comma belongs to the second email field. A second nonblank row with ID `"7"` makes the document invalid and raises `ValueError`.

## Review task

Review the parser and its tests against the document and field contracts. Correct discrepancies, then add assertions for normalized output, both allowed active values, quoted fields, duplicate IDs, and malformed rows. Explain which tests establish acceptance of valid CSV and which establish rejection of an invalid document.

## Starter Code

[View starter code](../../round-1/10-csv-import-parser/)

## Reference Solution

[View solution](../../solutions/round-1/10-csv-import-parser/)
