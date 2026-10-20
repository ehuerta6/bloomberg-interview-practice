# URL Query Parameter Parser — Reference Solution

## What broke

The draft separated key/value pairs but returned the encoded text as-is. That misses the URL query rules for percent escapes and plus signs, which represent spaces in form-style query strings.

## Reproduce the issue

Run `python3 query_params.py` in the starter folder. Encoded keys and values show the mismatch. The solution has its own runnable tests: `python3 query_params.py`.

## Investigation approach

Use examples with repeated keys, empty values, encoded characters, and values containing equals signs. Check whether each input form is decoded once and whether key order and repeated-value order survive parsing.

## Correction

The solution uses `urllib.parse.parse_qsl` from the standard library, retains blank values, and accumulates repeated decoded keys in encounter order.

## Regression tests

Tests cover optional leading question marks, repeated values, bare keys, empty values, encoded keys and values, plus-as-space, empty segments, and invalid input types. Run them with `python3 query_params.py`.
