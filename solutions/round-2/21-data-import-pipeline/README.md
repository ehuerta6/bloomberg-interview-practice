# Data Import Pipeline Reference Solution

## What was wrong

The row parser passed every amount through `int()`. That silently truncated a float such as `1.5` to `1` and treated `True` as `1`, allowing malformed amounts into storage.

## Reproduce and investigate

From the starter folder, run:

```sh
python3 test_data_import.py
```

Import rows with amounts `1.5` and `True`, then inspect the accepted IDs and repository records. Follow the call from `ImportRoutes.post` through `ImportService.import_rows` to `parse`. Check that an invalid row produces an error while valid neighboring rows still commit.

## Fix

Accept actual integers or base-10 integer strings, while explicitly excluding booleans and floats. Normalize email addresses, validate required fields and nonnegative amounts, and preserve the first valid occurrence of each external ID. Return row-level errors and continue processing independent rows.

## Regression tests

- `test_normalizes_email_and_rejects_invalid_numbers` covers normalization, a negative amount, and a float.
- `test_boolean_amount_is_not_an_integer_amount` prevents Python booleans from being treated as integers.
- `test_valid_rows_commit_independently_despite_bad_neighbor` checks partial success and error reporting.
- Other tests cover duplicate IDs in one file, duplicates already in storage, missing fields, and a non-list request body.

## Run the solution tests

```sh
python3 test_data_import.py
```
