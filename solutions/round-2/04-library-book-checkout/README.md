# Library Book Checkout Reference Solution

## What Was Broken?

Returning a copy did not make it available to another reader because its loan still counted as active.

## Reproduce the Behavior

From this folder, run `python3 test_library.py`; in `test_return_releases_copy_and_cannot_be_repeated`, check out the only copy as `l1`, return it, then query `available_copies("b1")`. The starter still counts the loan as active, so the next reader cannot check it out.

## Investigation

Trace checkout and return through the loan repository, then compare available-copy counts before checkout, during the loan, and after return. Check the reservation queue as well: a returning copy should be offered to its next reader, and a different reader must not bypass that reservation.

## Fix

A successful return marks the loan closed, so active-loan counts release that copy. Checkout respects the head of the reservation queue, consumes the reservation only for its owner, and rejects repeated loan identifiers.

## Regression Tests

The tests cover checkout and return, rejection of a repeated return, reservation priority, duplicate loan IDs, and the active-loan count after each transition. They assert repository state so the returned success value cannot hide a copy that remains incorrectly checked out.

## Run the Corrected Tests

```sh
python3 test_library.py
```
