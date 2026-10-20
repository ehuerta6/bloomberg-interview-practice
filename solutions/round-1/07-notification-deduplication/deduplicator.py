"""Reference notification deduplication keyed by recipient and event."""

from datetime import datetime, timedelta, timezone
import unittest


class NotificationDeduplicator:
    def __init__(self, window=timedelta(minutes=10)):
        if window <= timedelta(0):
            raise ValueError("window must be positive")
        self.window = window
        self.last_sent = {}

    def should_send(self, recipient, event_id, now):
        if not isinstance(recipient, str) or not recipient.strip():
            raise ValueError("recipient is required")
        if not isinstance(event_id, str) or not event_id.strip():
            raise ValueError("event id is required")
        if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("now must be timezone-aware")

        key = (recipient, event_id)
        previous = self.last_sent.get(key)
        if previous is not None and (now <= previous or now - previous < self.window):
            return False
        self.last_sent[key] = now
        return True


class DeduplicatorTests(unittest.TestCase):
    def setUp(self):
        self.filter = NotificationDeduplicator()
        self.now = datetime(2030, 5, 1, 12, tzinfo=timezone.utc)

    def test_first_delivery_is_allowed(self):
        self.assertTrue(self.filter.should_send("u1", "e1", self.now))

    def test_repeat_for_same_recipient_is_suppressed(self):
        self.filter.should_send("u1", "e1", self.now)
        self.assertFalse(self.filter.should_send("u1", "e1", self.now + timedelta(minutes=2)))

    def test_same_event_for_another_recipient_is_allowed(self):
        self.filter.should_send("u1", "e1", self.now)
        self.assertTrue(self.filter.should_send("u2", "e1", self.now + timedelta(minutes=1)))

    def test_distinct_event_for_same_recipient_is_allowed(self):
        self.filter.should_send("u1", "e1", self.now)
        self.assertTrue(self.filter.should_send("u1", "e2", self.now + timedelta(minutes=1)))

    def test_exactly_at_window_boundary_is_allowed(self):
        self.filter.should_send("u1", "e1", self.now)
        self.assertTrue(self.filter.should_send("u1", "e1", self.now + timedelta(minutes=10)))

    def test_suppressed_retries_do_not_extend_the_window(self):
        self.filter.should_send("u1", "e1", self.now)
        self.assertFalse(self.filter.should_send("u1", "e1", self.now + timedelta(minutes=8)))
        self.assertTrue(self.filter.should_send("u1", "e1", self.now + timedelta(minutes=10)))

    def test_out_of_order_delivery_does_not_regress_last_successful_time(self):
        self.filter.should_send("u1", "e1", self.now + timedelta(minutes=5))
        self.assertFalse(self.filter.should_send("u1", "e1", self.now))
        self.assertFalse(self.filter.should_send("u1", "e1", self.now + timedelta(minutes=14)))

    def test_empty_identity_is_rejected(self):
        with self.assertRaises(ValueError):
            self.filter.should_send("", "e1", self.now)

    def test_naive_clock_is_rejected(self):
        with self.assertRaises(ValueError):
            self.filter.should_send("u1", "e1", self.now.replace(tzinfo=None))

    def test_window_must_be_positive(self):
        with self.assertRaises(ValueError):
            NotificationDeduplicator(timedelta(0))


if __name__ == "__main__":
    unittest.main()
