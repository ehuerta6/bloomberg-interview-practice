"""Expire pending reservations at or before a supplied instant."""

from datetime import datetime
import unittest


def expire_reservations(reservations, now):
    """Return new records and IDs newly transitioned from pending to expired."""
    if not isinstance(now, datetime):
        raise ValueError("now must be a datetime")
    updated = []
    expired_ids = []
    for reservation in reservations:
        try:
            record = reservation.copy()
            expires_at = datetime.fromisoformat(record["expires_at"])
            reservation_id = record["reservation_id"]
            status = record["status"]
        except (AttributeError, KeyError, TypeError, ValueError) as error:
            raise ValueError("reservation is missing a valid field") from error
        if (expires_at.tzinfo is None) != (now.tzinfo is None):
            raise ValueError("now and expiration timestamps must use matching timezone styles")
        if status == "pending" and expires_at <= now:
            record["status"] = "expired"
            expired_ids.append(reservation_id)
        updated.append(record)
    return {"reservations": updated, "expired_ids": expired_ids}


class ReservationTests(unittest.TestCase):
    def test_elapsed_pending_reservation_expires(self):
        rows = [{"reservation_id": "r1", "status": "pending", "expires_at": "2025-01-01T11:59:00"}]
        self.assertEqual(expire_reservations(rows, datetime(2025, 1, 1, 12))["expired_ids"], ["r1"])

    def test_exact_deadline_is_expired(self):
        rows = [{"reservation_id": "r1", "status": "pending", "expires_at": "2025-01-01T12:00:00"}]
        result = expire_reservations(rows, datetime(2025, 1, 1, 12))
        self.assertEqual(result["reservations"][0]["status"], "expired")
        self.assertEqual(result["expired_ids"], ["r1"])

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
