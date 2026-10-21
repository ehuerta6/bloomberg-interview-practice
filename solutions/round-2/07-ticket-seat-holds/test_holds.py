import unittest
from datetime import datetime, timedelta
from seat_repository import SeatRepository
from hold_service import HoldService

class HoldTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2030, 1, 1, 12)
        self.repo = SeatRepository(["A1", "A2"])
        self.service = HoldService(self.repo, clock=lambda: self.now, ttl=timedelta(minutes=5))

    def test_active_hold_prevents_second_customer_from_taking_seat(self):
        self.assertTrue(self.service.hold("A1", "buyer-a", "h1"))
        self.assertFalse(self.service.hold("A1", "buyer-b", "h2"))

    def test_expired_hold_releases_seat(self):
        self.service.hold("A1", "buyer-a", "h1")
        self.now += timedelta(minutes=5)
        self.assertTrue(self.service.hold("A1", "buyer-b", "h2"))
        self.assertEqual(self.repo.hold_for_seat("A1").customer_id, "buyer-b")

    def test_same_hold_cannot_be_used_to_claim_another_seat(self):
        self.assertTrue(self.service.hold("A1", "buyer-a", "h1"))
        self.assertFalse(self.service.hold("A2", "buyer-a", "h1"))
        self.assertIsNone(self.repo.hold_for_seat("A2"))

    def test_confirmation_requires_owner_and_active_hold(self):
        self.service.hold("A1", "buyer-a", "h1")
        self.assertFalse(self.service.confirm("h1", "buyer-b"))
        self.assertTrue(self.service.confirm("h1", "buyer-a"))
        self.assertFalse(self.service.hold("A1", "buyer-b", "h2"))

    def test_hold_expiring_at_now_is_available_to_another_buyer(self):
        self.service.hold("A1", "buyer-a", "h1")
        self.now += timedelta(minutes=5)
        self.assertTrue(self.service.hold("A1", "buyer-b", "h2"))
        self.assertEqual(self.repo.hold_for_seat("A1").hold_id, "h2")


    def test_confirmed_hold_remains_unavailable_after_deadline(self):
        self.service.hold("A1", "buyer-a", "h1")
        self.assertTrue(self.service.confirm("h1", "buyer-a"))
        self.now += timedelta(minutes=10)
        self.assertFalse(self.service.hold("A1", "buyer-b", "h2"))
        self.assertEqual(self.repo.hold_for_seat("A1").hold_id, "h1")

if __name__ == "__main__": unittest.main()
