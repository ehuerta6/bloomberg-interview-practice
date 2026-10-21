import unittest
from datetime import datetime, timedelta
from reset_repository import ResetRepository
from reset_service import ResetService

class PasswordResetTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2030, 1, 1, 12)
        self.repo = ResetRepository()
        self.service = ResetService(self.repo, clock=lambda: self.now, ttl=timedelta(minutes=20))

    def test_new_token_can_be_used_once(self):
        token = self.service.issue("u1", "t1")
        self.assertTrue(self.service.reset("t1", "new-hash"))
        self.assertEqual(self.repo.password_hash("u1"), "new-hash")
        self.assertFalse(self.service.reset("t1", "other-hash"))
        self.assertEqual(self.repo.password_hash("u1"), "new-hash")

    def test_expired_token_does_not_change_password(self):
        self.service.issue("u1", "t1")
        self.now += timedelta(minutes=20)
        self.assertFalse(self.service.reset("t1", "new-hash"))
        self.assertIsNone(self.repo.password_hash("u1"))

    def test_retry_invalidates_older_token_for_same_user(self):
        self.service.issue("u1", "first")
        self.service.issue("u1", "second")
        self.assertFalse(self.service.reset("first", "old-path"))
        self.assertTrue(self.service.reset("second", "new-path"))
        self.assertEqual(self.repo.password_hash("u1"), "new-path")

    def test_unknown_token_is_safe(self):
        self.assertFalse(self.service.reset("missing", "hash"))
        self.assertIsNone(self.repo.password_hash("u1"))

    def test_tokens_for_different_users_are_independent(self):
        self.service.issue("u1", "t1")
        self.service.issue("u2", "t2")
        self.assertTrue(self.service.reset("t1", "hash-one"))
        self.assertTrue(self.service.reset("t2", "hash-two"))
        self.assertEqual(self.repo.password_hash("u1"), "hash-one")
        self.assertEqual(self.repo.password_hash("u2"), "hash-two")


    def test_token_is_valid_immediately_before_expiration(self):
        self.service.issue("u1", "t1")
        self.now += timedelta(minutes=19, seconds=59)
        self.assertTrue(self.service.reset("t1", "new-hash"))

if __name__ == "__main__": unittest.main()
