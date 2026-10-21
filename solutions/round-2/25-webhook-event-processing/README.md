# Webhook Event Processing Reference Solution

## What was wrong

The receiver deduplicated repeated event IDs, but it applied every new event ID regardless of sequence. A delayed event with a lower or equal sequence could overwrite the order’s newer status and append out-of-order history.

## Reproduce and investigate

From the starter folder, run:

```sh
python3 test_webhook_events.py
```

Send sequence 2 with status `shipped`, then send a different event ID at sequence 1 with status `paid`. Inspect the order status and history. Follow validation and deduplication in `WebhookService.receive`, then check whether it compares the new sequence with the latest applied one.

## Fix

Keep event-ID deduplication, then compare the sequence with the last applied sequence for that order. Apply only strictly newer events. Record stale event IDs as processed so their retries remain duplicates, without changing status or adding history.

## Regression tests

- `test_out_of_order_event_does_not_regress_state` verifies that a delayed lower-sequence event does not replace `shipped`.
- `test_same_sequence_conflict_is_stale_and_idempotent` checks that equal-sequence events are ignored and their retries are duplicates.
- `test_duplicate_event_id_applies_once` covers retry deduplication; `test_newer_events_advance_status_and_keep_history` checks ordered progress.
- Other tests cover malformed events, unknown orders, and independent sequence histories for separate orders.

## Run the solution tests

```sh
python3 test_webhook_events.py
```
