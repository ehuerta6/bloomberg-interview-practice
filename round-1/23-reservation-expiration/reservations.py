"""Expire elapsed reservations."""

from datetime import datetime
import unittest


def expire_reservations(reservations, now):
    """Return copied records with elapsed pending reservations expired."""
    updated = []
    expired_ids = []
    for reservation in reservations:
        record = reservation.copy()
        expires_at = datetime.fromisoformat(record["expires_at"])
        if record["status"] == "pending" and expires_at < now:
            record["status"] = "expired"
            expired_ids.append(record["reservation_id"])
        updated.append(record)
    return {"reservations": updated, "expired_ids": expired_ids}


class ReservationTests(unittest.TestCase):
    def test_elapsed_pending_reservation_expires(self):
        rows = [{"reservation_id": "r1", "status": "pending", "expires_at": "2025-01-01T11:59:00"}]
        self.assertEqual(expire_reservations(rows, datetime(2025, 1, 1, 12))["expired_ids"], ["r1"])

    def test_exact_deadline_is_expired(self):
        rows = [{"reservation_id": "r1", "status": "pending", "expires_at": "2025-01-01T12:00:00"}]
        self.assertEqual(expire_reservations(rows, datetime(2025, 1, 1, 12))["reservations"][0]["status"], "expired")

    def test_future_reservation_remains_pending(self):
        rows = [{"reservation_id": "r1", "status": "pending", "expires_at": "2025-01-01T12:01:00"}]
        self.assertEqual(expire_reservations(rows, datetime(2025, 1, 1, 12))["expired_ids"], [])

    def test_confirmed_reservation_is_not_expired(self):
        rows = [{"reservation_id": "r1", "status": "confirmed", "expires_at": "2025-01-01T11:00:00"}]
        self.assertEqual(expire_reservations(rows, datetime(2025, 1, 1, 12))["reservations"][0]["status"], "confirmed")

    def test_expired_ids_preserve_input_order(self):
        rows = [{"reservation_id": "a", "status": "pending", "expires_at": "2025-01-01T00:00:00"}, {"reservation_id": "b", "status": "pending", "expires_at": "2025-01-01T00:00:00"}]
        self.assertEqual(expire_reservations(rows, datetime(2025, 1, 1))["expired_ids"], ["a", "b"])

    def test_input_records_are_not_mutated(self):
        rows = [{"reservation_id": "r1", "status": "pending", "expires_at": "2025-01-01T00:00:00"}]
        original = [row.copy() for row in rows]
        expire_reservations(rows, datetime(2025, 1, 1, 1))
        self.assertEqual(rows, original)

    def test_already_expired_record_is_not_reported_twice(self):
        rows = [{"reservation_id": "r1", "status": "expired", "expires_at": "2025-01-01T00:00:00"}]
        result = expire_reservations(rows, datetime(2025, 1, 1, 1))
        self.assertEqual(result["expired_ids"], [])

    def test_naive_and_aware_times_are_not_mixed(self):
        rows = [{"reservation_id": "r1", "status": "pending", "expires_at": "2025-01-01T00:00:00+00:00"}]
        with self.assertRaises(ValueError):
            expire_reservations(rows, datetime(2025, 1, 1))


if __name__ == "__main__":
    unittest.main()
