# Session Token Expiration — Reference Solution

## What was broken

The registry accepted tokens whose issue time was still in the future and treated the exact expiration instant as valid. Both errors come from checking only one side of the token's validity interval.

## Reproduce the issue

Run `python3 session_tokens.py` in the starter folder. The tests for a token queried before `issued_at` and exactly at `expires_at` fail. Since `is_valid` accepts `now`, each test controls time and is repeatable.

## Investigation approach

Translate “valid from issue time until expiration” into an interval: the left endpoint is included, while the right endpoint is excluded. Then inspect how revocation and malformed timestamps interact with that interval.

## Correction

`is_valid` now requires `issued_at <= now < expires_at`, after confirming the token exists, is not revoked, and the supplied clock is timezone-aware. Issue-time validation also rejects blank IDs, duplicate IDs, naive timestamps, and non-positive lifetimes.

## Regression tests

Tests cover a valid interior instant, one second before issue, the exact expiry instant, unknown and revoked tokens, duplicate IDs, naive timestamps, and deterministic clock injection.
