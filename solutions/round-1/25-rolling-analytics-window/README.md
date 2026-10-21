# Rolling Analytics Window — Reference Solution

## What broke

The draft's generator compares each parsed event timestamp with `cutoff` and `now` immediately. If the event timestamp includes a UTC offset but `now` is naive (or vice versa), Python raises `TypeError` instead of the documented `ValueError`.

## Reproduce the issue

From `round-1/25-rolling-analytics-window/`, run `python3 rolling_window.py`. `test_aware_and_naive_timestamps_cannot_be_compared` errors when the generator compares the aware event timestamp with naive `now`. Run it in this solution folder to confirm the mismatch is rejected with `ValueError`.

## Investigation approach

Follow the starter's generator condition: it parses `timestamp`, then performs `cutoff <= timestamp <= now` without first checking timezone styles. Compare the aware timestamp in the regression input with the naive reference datetime. Then verify the normal interval itself is closed at both ends and excludes both old and future events.

## Correction

The solution validates the reference time and window, parses each event inside a guarded block, and checks aware-versus-naive compatibility before comparison. It validates each event value and adds it only when `cutoff <= timestamp <= now`, preserving the specified closed interval.

## Regression tests

`test_aware_and_naive_timestamps_cannot_be_compared` covers the exception-type defect. The suite also checks the inclusive cutoff, just-before-cutoff and future exclusion, empty input, negative event values, and a zero-length window. The solution adds a boolean-window validation case. Run it with `python3 rolling_window.py`.
