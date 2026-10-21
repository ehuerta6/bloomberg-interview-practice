# Password Reset Flow Reference Solution

## What Was Broken?

An older reset link remained usable after a newer request for the same account.

## Reproduce the Behavior

From this folder, run `python3 test_password_reset.py`; `test_retry_invalidates_older_token_for_same_user` issues `first` and then `second` for `u1`. Try both links and inspect `password_hash("u1")`. The starter accepts the old link and stores `old-path`, even though the newer link was issued.

## Investigation

Trace token creation and password updates through the service and token repository. After issuing two tokens for one account, inspect both records and attempt each token. Also check the exact expiry instant and confirm invalid or reused tokens leave the stored password unchanged.

## Fix

A new token invalidates earlier unused tokens for the same user before it is saved. Reset validates existence, invalidation, single-use state, expiry, and input before changing the password; it marks the token used as part of the successful transition.

## Regression Tests

The tests cover a successful reset, invalidation of an older token, exact expiry, unknown tokens, one-time use, and invalid replacement passwords. Assertions verify both token state and the account's stored password after rejected requests.

## Run the Corrected Tests

```sh
python3 test_password_reset.py
```
