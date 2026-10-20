"""Track accepted requests against per-user sliding time windows."""

from collections import deque
import math
import unittest


def _finite_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


class RequestRateLimiter:
    def __init__(self, limit, window_seconds):
        if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
            raise ValueError("limit must be a positive integer")
        if not _finite_number(window_seconds) or window_seconds <= 0:
            raise ValueError("window_seconds must be a positive finite number")
        self.limit = limit
        self.window_seconds = window_seconds
        self._requests = {}
        self._last_time = {}

    def allow(self, user_id, timestamp):
        """Return whether a request is accepted and record only accepted requests.

        Each user's active window is ``(timestamp - window_seconds, timestamp]``.
        Per-user timestamps must be nondecreasing.
        """
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("user_id must be a nonblank string")
        if not _finite_number(timestamp):
            raise ValueError("timestamp must be a finite number")
        previous = self._last_time.get(user_id)
        if previous is not None and timestamp < previous:
            raise ValueError("timestamps must be nondecreasing for each user")
        self._last_time[user_id] = timestamp

        history = self._requests.setdefault(user_id, deque())
        cutoff = timestamp - self.window_seconds
        while history and history[0] <= cutoff:
            history.popleft()
        if len(history) >= self.limit:
            return False
        history.append(timestamp)
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

    def test_configuration_timestamps_and_user_ids_are_validated(self):
        for limit, window in ((0, 10), (True, 10), (2, 0), (2, float("inf"))):
            with self.subTest(limit=limit, window=window), self.assertRaises(ValueError):
                RequestRateLimiter(limit, window)
        limiter = RequestRateLimiter(1, 10)
        for user_id, timestamp in (("a", float("nan")), (" ", 0), ("a", True)):
            with self.subTest(user_id=user_id, timestamp=timestamp), self.assertRaises(ValueError):
                limiter.allow(user_id, timestamp)

    def test_rejected_attempts_do_not_extend_window(self):
        limiter = RequestRateLimiter(1, 5)
        self.assertTrue(limiter.allow("a", 0))
        self.assertFalse(limiter.allow("a", 4))
        self.assertTrue(limiter.allow("a", 5))

    def test_other_users_can_advance_time_independently(self):
        limiter = RequestRateLimiter(1, 5)
        self.assertTrue(limiter.allow("a", 10))
        self.assertTrue(limiter.allow("b", 1))


if __name__ == "__main__":
    unittest.main()
