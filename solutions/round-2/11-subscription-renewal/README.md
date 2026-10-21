# Subscription Renewal Reference Solution

## What Was Broken

When the payment gateway declined a renewal, the starter stored a `declined` invoice but left the subscription `active`. Account views could therefore report a member as current even though the renewal remained unpaid.

## Reproduce and Investigate

From this folder, run `python3 test_subscription_renewal.py`. Configure the fake gateway to decline, renew on the due date, and compare the invoice record with the subscription status and due date. Then replay that invoice and verify it does not call the gateway again; a later collection attempt must use a new invoice ID.

Trace the route through `RenewalService`, `RenewalStore`, and the fake gateway. Check early renewal, declined renewal, successful renewal, and replay paths independently so a status update does not accidentally charge or advance the date.

## The Fix

A decline now marks the subscription `past_due`, records the declined invoice, and preserves the existing due date. Any invoice ID with a recorded outcome is idempotent, so both paid and declined replays return the saved outcome without another gateway call. A later collection uses a new invoice ID. A successful charge advances from the scheduled due date by one month, clamps month-end dates to the last valid day, and returns the subscription to `active`.

## Regression Tests

The corrected suite checks that a decline leaves the due date unchanged and sets `past_due`; replaying that declined invoice after the gateway recovers does not charge again; a new invoice ID can collect the balance; successful replays charge once; early attempts make no gateway call; month-end dates clamp correctly; canceled and missing subscriptions do not create charges or invoices.

## Run

```sh
python3 test_subscription_renewal.py
```
