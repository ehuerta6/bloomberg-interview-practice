# Session Revocation Reference Solution

## What Was Broken

Logout saved `revoked_at`, but the starter’s authorization check only tested whether the session record existed. A revoked session therefore continued to authorize access. The stored revocation timestamp had no effect on requests.

## Reproduce and Investigate

From this folder, run `python3 test_session_revocation.py`. The first test logs one user in on two devices, logs out session `s-1`, then checks authorization for both IDs. Compare `SessionService.is_authorized` with the `revoked_at` value held by `SessionStore`.

## The Fix

Authorization now requires a stored session whose `revoked_at` is still unset. Logout records the first revocation time and leaves it unchanged on repeated calls. Because sessions are stored separately, revoking one device does not revoke another; an unknown session is never authorized.

## Regression Tests

The suite checks logout on one of two sessions, repeated logout preserving the original timestamp, and rejection of an unknown session ID.

## Run

```sh
python3 test_session_revocation.py
```
