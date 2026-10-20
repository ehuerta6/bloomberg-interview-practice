"""Track accepted requests against a per-user rolling time window."""

import unittest


class RequestRateLimiter:
    def __init__(self, limit, window_seconds):
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests = []

    def allow(self, user_id, timestamp):
        cutoff = timestamp - self.window_seconds
        self.requests = [seen for seen in self.requests if seen[1] < cutoff]
        if len(self.requests) >= self.limit:
            self.requests.append((user_id, timestamp))
            return False
        self.requests.append((user_id, timestamp))
        return True


class RateLimiterTests(unittest.TestCase):
    def test_requests_within_limit_are_allowed(self):
        limiter = RequestRateLimiter(2, 10)
        self.assertTrue(limiter.allow("u1", 0))
        self.assertTrue(limiter.allow("u1", 1))

    def test_users_have_independent_limits(self):
        limiter = RequestRateLimiter(1, 10)
        self.assertTrue(limiter.allow("a", 0))
        self.assertTrue(limiter.allow("b", 0))

    def test_request_outside_the_window_expires(self):
        limiter = RequestRateLimiter(1, 10)
        self.assertTrue(limiter.allow("a", 0))
        self.assertTrue(limiter.allow("a", 10.1))

    def test_exact_cutoff_is_outside_the_sliding_window(self):
        limiter = RequestRateLimiter(1, 10)
        self.assertTrue(limiter.allow("a", 0))
        self.assertTrue(limiter.allow("a", 10))

    def test_rejected_attempt_does_not_consume_a_slot(self):
        limiter = RequestRateLimiter(2, 10)
        self.assertTrue(limiter.allow("a", 0))
        self.assertTrue(limiter.allow("a", 1))
        self.assertFalse(limiter.allow("a", 2))
        self.assertTrue(limiter.allow("a", 10))

    def test_limit_is_enforced_for_one_user(self):
        limiter = RequestRateLimiter(1, 10)
        self.assertTrue(limiter.allow("a", 0))
        self.assertFalse(limiter.allow("a", 1))

    def test_time_must_not_move_backwards_for_a_user(self):
        limiter = RequestRateLimiter(2, 10)
        limiter.allow("a", 5)
        with self.assertRaises(ValueError):
            limiter.allow("a", 4)

    def test_bad_configuration_and_timestamp_are_rejected(self):
        with self.assertRaises(ValueError):
            RequestRateLimiter(0, 10)
        limiter = RequestRateLimiter(1, 10)
        with self.assertRaises(ValueError):
            limiter.allow("a", float("nan"))


if __name__ == "__main__":
    unittest.main()
