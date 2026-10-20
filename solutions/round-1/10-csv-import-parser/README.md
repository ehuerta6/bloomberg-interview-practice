# CSV Import Parser — Reference Solution

## What broke

The draft split each line at every comma, so quoted fields were not treated as one field. It also converted any nonempty active value to `True`, including the text `false`, and did not reject repeated IDs.

## Reproduce the issue

Run `python3 csv_import.py` in the starter folder. The quoted-field, boolean, and duplicate-ID cases expose the problems. Run the corrected, independent suite with `python3 csv_import.py` here.

## Investigation approach

Compare the input as a CSV document rather than a list of comma-separated strings. Check header and row width, then validate normalized identity fields and the allowed boolean vocabulary before constructing a user record.

## Correction

The solution uses Python's standard-library `csv` reader, accepts quoted fields and blank lines, normalizes IDs and email values, accepts only `true` or `false`, and rejects malformed rows and duplicate IDs.

## Regression tests

Tests cover normalization, both boolean values, quoted commas and quotes, whitespace, blank lines, header and width errors, duplicates, CRLF, embedded newlines, and malformed quoting. Run them with `python3 csv_import.py`.
