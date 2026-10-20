# Log Filtering — Reference Solution

## What broke

The draft treated time bounds as exclusive and assumed every entry had usable timestamp and severity fields. A malformed record could interrupt filtering instead of being skipped.

## Reproduce the issue

Run `python3 log_filter.py` in the starter folder. Include entries exactly at the requested bounds and an entry with missing or malformed fields. Run the corrected independent suite with `python3 log_filter.py` here.

## Investigation approach

Check severity ranking separately from time filtering. Confirm whether the endpoints belong in the range, then pass malformed records through the same filtering path and decide which failures should be ignored versus rejected as invalid filter arguments.

## Correction

The solution validates filter arguments, normalizes severity names case-insensitively, and includes entries from both time endpoints. Malformed entries and unknown severities are skipped while valid entries retain their original order.

## Regression tests

Tests cover severity thresholds, case handling, inclusive and open-ended ranges, malformed records, invalid filters, ordering, and empty input. Run them with `python3 log_filter.py`.
