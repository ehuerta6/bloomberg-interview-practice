# Notification Delivery Reference Solution

## What Was Broken

`DeliveryService.deliver` sent the provider request every time the same event ID was submitted. The store already held a `sent` delivery, but the starter did not return it before trying the provider again. A caller retry after a successful send therefore created a duplicate notification.

## Reproduce and Investigate

From this folder, run `python3 test_notification_delivery.py`. The replay case sends `evt-1` twice and checks both the provider call count and the stored attempt count. Trace `deliver` into `DeliveryStore` and `RecordingProvider`: the store retains one delivery row, so provider calls reveal the duplicate side effect. The other tests exercise transient failure, exhausted attempts, and a later retry.

## The Fix

`deliver` now returns an already-sent record without contacting the provider. It also rejects reuse of an event ID for different recipient or message content. Before each provider call, the service saves the record with its incremented attempt count; it saves `sent` or `failed` after the outcome. `retry` resumes only deliveries that have not succeeded.

## Regression Tests

The suite verifies one provider call for a duplicate successful request, retries through two transient failures, persists failure after three attempts, resumes a failed delivery successfully, and rejects changed content under an existing event ID.

## Run

```sh
python3 test_notification_delivery.py
```
