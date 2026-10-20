"""Reference in-memory session-token registry with regression tests."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import unittest


@dataclass(frozen=True)
class Token:
    token_id: str
    issued_at: datetime
    expires_at: datetime


def _is_aware(value):
    return isinstance(value, datetime) and value.tzinfo is not None and value.utcoffset() is not None


class TokenRegistry:
    def __init__(self):
        self.tokens = {}
        self.revoked = set()

    def issue(self, token_id, issued_at, expires_at):
        if not isinstance(token_id, str) or not token_id.strip() or token_id in self.tokens:
            raise ValueError("token id must be new and non-empty")
        if not _is_aware(issued_at) or not _is_aware(expires_at):
            raise ValueError("timestamps must include a timezone")
        if expires_at <= issued_at:
            raise ValueError("expiration must follow issue time")
        self.tokens[token_id] = Token(token_id, issued_at, expires_at)

    def revoke(self, token_id):
        if token_id not in self.tokens:
            return False
        self.revoked.add(token_id)
        return True

    def is_valid(self, token_id, now):
        token = self.tokens.get(token_id)
        if token is None or token_id in self.revoked:
            return False
        if not _is_aware(now):
            raise ValueError("current time must include a timezone")
        return token.issued_at <= now < token.expires_at


class SessionTokenTests(unittest.TestCase):
    def setUp(self):
        self.registry = TokenRegistry()
        self.start = datetime(2030, 1, 1, tzinfo=timezone.utc)
        self.end = self.start + timedelta(hours=1)
        self.registry.issue("s-1", self.start, self.end)

    def test_token_is_valid_between_issue_and_expiration(self):
        self.assertTrue(self.registry.is_valid("s-1", self.start + timedelta(minutes=2)))

    def test_unknown_token_is_invalid(self):
        self.assertFalse(self.registry.is_valid("missing", self.start))

    def test_revoked_token_is_invalid(self):
        self.registry.revoke("s-1")
        self.assertFalse(self.registry.is_valid("s-1", self.start + timedelta(minutes=2)))

    def test_expiration_instant_is_not_valid(self):
        self.assertFalse(self.registry.is_valid("s-1", self.end))

    def test_token_is_invalid_before_issue_time(self):
        self.assertFalse(self.registry.is_valid("s-1", self.start - timedelta(seconds=1)))

    def test_unknown_revocation_does_not_create_a_revoked_record(self):
        self.assertFalse(self.registry.revoke("missing"))
        self.assertNotIn("missing", self.registry.revoked)

    def test_duplicate_token_id_is_rejected(self):
        with self.assertRaises(ValueError):
            self.registry.issue("s-1", self.start, self.end)

    def test_naive_timestamps_are_rejected(self):
        with self.assertRaises(ValueError):
            self.registry.issue("s-2", datetime(2030, 1, 1), self.end)

    def test_naive_clock_is_rejected_for_existing_token(self):
        with self.assertRaises(ValueError):
            self.registry.is_valid("s-1", datetime(2030, 1, 1))


if __name__ == "__main__":
    unittest.main()
