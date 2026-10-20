# Request Rate Limiter — Reference Solution

## What broke

The draft kept one shared request list for every user. It also counted attempts that had already been rejected and handled the window cutoff as an inclusive boundary.

## Reproduce the issue

Run `python3 rate_limiter.py` in the starter folder. Interleave users, reject a request, and retry at the exact window cutoff. Run the corrected independent suite with `python3 rate_limiter.py` here.

## Investigation approach

For each user, write down accepted timestamps and the active window after each request. The active interval is open on the left and closed on the right: `(now - window_seconds, now]`. Then check which events should be removed and whether a denied attempt should remain in history.

## Correction

The solution stores a deque per user, validates positive limits, finite windows and timestamps, and requires per-user timestamps to be nondecreasing. It removes timestamps at or before the cutoff and records only accepted requests.

## Regression tests

Tests cover per-user isolation, sliding expiration, exact cutoff behavior, rejected attempts, timestamp order, and invalid configuration. Run them with `python3 rate_limiter.py`.
