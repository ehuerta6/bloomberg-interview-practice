import unittest

from session_service import SessionService
from session_store import SessionStore


class SessionRevocationTests(unittest.TestCase):
    def build(self):
        store = SessionStore()
        return store, SessionService(store)

    def test_logout_revokes_only_the_target_session(self):
        store, service = self.build()
        service.login("s-1", "alice", "device-a")
        service.login("s-2", "alice", "device-b")
        service.logout("s-1", "2026-10-20T10:00:00Z")
        self.assertFalse(service.is_authorized("s-1"))
        self.assertTrue(service.is_authorized("s-2"))
        self.assertEqual(store.get("s-1").revoked_at, "2026-10-20T10:00:00Z")

    def test_repeated_logout_is_safe_and_keeps_original_revocation_time(self):
        store, service = self.build()
        service.login("s-3", "bob", "laptop")
        service.logout("s-3", "10:00")
        service.logout("s-3", "10:05")
        self.assertFalse(service.is_authorized("s-3"))
        self.assertEqual(store.get("s-3").revoked_at, "10:00")

    def test_active_session_is_authorized_before_logout(self):
        _, service = self.build()
        service.login("s-4", "alice", "tablet")
        self.assertTrue(service.is_authorized("s-4"))

    def test_unknown_session_is_not_authorized(self):
        _, service = self.build()
        self.assertFalse(service.is_authorized("missing"))

    def test_logout_of_unknown_session_is_safe(self):
        store, service = self.build()
        self.assertFalse(service.logout("missing", "10:00"))
        self.assertEqual(store.sessions, {})

    def test_duplicate_session_id_cannot_replace_existing_user(self):
        store, service = self.build()
        service.login("s-5", "alice", "phone")
        with self.assertRaises(ValueError):
            service.login("s-5", "mallory", "phone")
        self.assertEqual(store.get("s-5").user_id, "alice")


if __name__ == "__main__":
    unittest.main()
