"""Plan delays for retry attempts."""

import unittest


def retry_delays(max_retries, base_delay, multiplier=2, max_delay=None):
    """Return one delay per retry after the initial attempt."""
    delays = []
    delay = base_delay
    for _ in range(max_retries):
        delays.append(delay)
        delay *= multiplier
    if max_delay is not None:
        delays = [min(value, max_delay) for value in delays]
    return delays


class RetryPlanTests(unittest.TestCase):
    def test_exponential_schedule(self):
        self.assertEqual(retry_delays(4, 1), [1, 2, 4, 8])

    def test_zero_retries_has_no_waits(self):
        self.assertEqual(retry_delays(0, 1), [])

    def test_custom_multiplier(self):
        self.assertEqual(retry_delays(3, 2, multiplier=3), [2, 6, 18])

    def test_cap_applies_to_each_wait(self):
        self.assertEqual(retry_delays(5, 2, max_delay=5), [2, 4, 5, 5, 5])

    def test_cap_does_not_change_earlier_delays(self):
        self.assertEqual(retry_delays(3, 1, multiplier=2, max_delay=3), [1, 2, 3])

    def test_fractional_delays_are_preserved(self):
        self.assertEqual(retry_delays(3, 0.25), [0.25, 0.5, 1.0])

    def test_negative_retry_count_is_rejected(self):
        with self.assertRaises(ValueError):
            retry_delays(-1, 1)

    def test_invalid_multiplier_is_rejected(self):
        with self.assertRaises(ValueError):
            retry_delays(3, 1, multiplier=0)


if __name__ == "__main__":
    unittest.main()
