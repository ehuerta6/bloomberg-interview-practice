"""Reserve one seat in an in-memory booking snapshot."""

import unittest


def reserve_seat(reservations, seat_id, customer_id):
    """Reserve an unclaimed seat and report whether the reservation succeeded."""
    if seat_id in reservations:
        reservations[seat_id] = customer_id
        return True
    reservations[seat_id] = customer_id
    return True


class SeatReservationTests(unittest.TestCase):
    def test_first_customer_can_reserve_an_open_seat(self):
        reservations = {}
        self.assertTrue(reserve_seat(reservations, "A-12", "customer-1"))
        self.assertEqual(reservations, {"A-12": "customer-1"})

    def test_existing_reservation_is_preserved(self):
        reservations = {"A-12": "customer-1"}
        self.assertFalse(reserve_seat(reservations, "A-12", "customer-2"))
        self.assertEqual(reservations, {"A-12": "customer-1"})

    def test_another_seat_can_be_reserved_after_a_conflict(self):
        reservations = {"A-12": "customer-1"}
        self.assertTrue(reserve_seat(reservations, "A-13", "customer-2"))
        self.assertEqual(reservations, {"A-12": "customer-1", "A-13": "customer-2"})


if __name__ == "__main__":
    unittest.main()
