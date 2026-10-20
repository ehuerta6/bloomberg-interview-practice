"""In-memory session-token registry and pull-request review tests."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import unittest


@dataclass(frozen=True)
class Token:
    token_id: str
    issued_at: datetime
    expires_at: datetime


class TokenRegistry:
    def __init__(self):
        self.tokens = {}
        self.revoked = set()

    def issue(self, token_id, issued_at, expires_at):
        if not token_id or token_id in self.tokens:
            raise ValueError("token id must be new and non-empty")
        if issued_at.tzinfo is None or expires_at.tzinfo is None:
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
        return now <= token.expires_at


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


if __name__ == "__main__":
    unittest.main()
