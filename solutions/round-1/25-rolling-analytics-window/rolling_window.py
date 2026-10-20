"""Sum event values in a validated rolling time window."""

from datetime import datetime, timedelta
import unittest


def rolling_total(events, now, window_seconds):
    """Sum events in [now - window, now], requiring comparable timestamps."""
    if not isinstance(now, datetime):
        raise ValueError("now must be a datetime")
    if not isinstance(window_seconds, (int, float)) or isinstance(window_seconds, bool) or window_seconds < 0:
        raise ValueError("window_seconds must be nonnegative")
    cutoff = now - timedelta(seconds=window_seconds)
    total = 0
    for event in events:
        try:
            timestamp = datetime.fromisoformat(event["timestamp"])
            value = event["value"]
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("event must have a valid timestamp and value") from error
        if (timestamp.tzinfo is None) != (now.tzinfo is None):
            raise ValueError("event and reference times must use matching timezone styles")
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("event value must be numeric")
        if cutoff <= timestamp <= now:
            total += value
    return total


class RollingWindowTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2025, 1, 1, 12)

    def test_in_window_events_are_summed(self):
        events = [{"timestamp": "2025-01-01T11:59:00", "value": 2}, {"timestamp": "2025-01-01T11:58:00", "value": 3}]
        self.assertEqual(rolling_total(events, self.now, 180), 5)

    def test_cutoff_instant_is_included(self):
        events = [{"timestamp": "2025-01-01T11:57:00", "value": 7}]
        self.assertEqual(rolling_total(events, self.now, 180), 7)

    def test_event_before_cutoff_is_excluded(self):
        events = [{"timestamp": "2025-01-01T11:56:59", "value": 7}]
        self.assertEqual(rolling_total(events, self.now, 180), 0)

    def test_future_event_is_excluded(self):
        events = [{"timestamp": "2025-01-01T12:00:01", "value": 9}]
        self.assertEqual(rolling_total(events, self.now, 60), 0)

    def test_empty_input_is_zero(self):
        self.assertEqual(rolling_total([], self.now, 60), 0)

    def test_negative_values_are_counted(self):
        events = [{"timestamp": "2025-01-01T11:59:00", "value": -3}]
        self.assertEqual(rolling_total(events, self.now, 60), -3)

    def test_zero_window_includes_only_events_at_now(self):
        events = [{"timestamp": "2025-01-01T12:00:00", "value": 4}, {"timestamp": "2025-01-01T11:59:59", "value": 3}]
        self.assertEqual(rolling_total(events, self.now, 0), 4)

    def test_aware_and_naive_timestamps_cannot_be_compared(self):
        events = [{"timestamp": "2025-01-01T11:59:00+00:00", "value": 2}]
        with self.assertRaises(ValueError):
            rolling_total(events, self.now, 60)

    def test_boolean_window_is_rejected(self):
        with self.assertRaises(ValueError):
            rolling_total([], self.now, True)


if __name__ == "__main__":
    unittest.main()
