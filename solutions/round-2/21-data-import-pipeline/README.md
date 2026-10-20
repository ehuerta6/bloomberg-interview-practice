# Data Import Pipeline Reference Solution

## Reported behavior

The row parser converts values with `int()`, which silently truncates floats and treats booleans as amounts. Those values can enter storage as valid records.

## Reproduce and investigate

From this folder, run:

```sh
python3 test_data_import.py
```

Start with `routes.py` to see the request boundary, then follow the call into `service.py` and the in-memory `repository.py`. Reproduce the reported scenario and inspect repository state before and after each operation. The starter tests include examples that pass and regressions that expose the issue.

## Fix

Validate each row’s required fields and integer amount, normalize email, preserve the first occurrence of each external ID, skip duplicates against both the file and repository, and continue importing valid rows while returning row-level errors.

## Regression coverage

The solution tests cover valid and invalid requests, state invariants, boundary conditions, repeated operations, and failure paths. They assert the data stored in the repository as well as returned results.

## Run the solution tests

```sh
python3 test_data_import.py
```
