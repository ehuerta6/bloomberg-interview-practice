"""Checkout coupon calculation and its pull-request review tests."""

import unittest


COUPONS = {
    "SAVE10": (10, 5000),
    "TAKE500": (500, 2500),
}


def calculate_total(subtotal_cents, coupon_code=None, first_order=False, employee=False):
    """Return the amount due after checkout promotions, in whole cents."""
    if not isinstance(subtotal_cents, int) or subtotal_cents < 0:
        raise ValueError("subtotal must be a non-negative number of cents")

    discount = 0
    if employee:
        discount = subtotal_cents // 5

    if first_order:
        discount = subtotal_cents * 15 // 100

    if coupon_code:
        code = coupon_code.strip().upper()
        if code not in COUPONS:
            raise ValueError("unknown coupon")
        amount, minimum = COUPONS[code]
        if subtotal_cents >= minimum:
            if code == "SAVE10":
                discount = subtotal_cents * amount // 100
            else:
                discount = amount

    return max(0, subtotal_cents - discount)


class CouponEligibilityTests(unittest.TestCase):
    def test_regular_order_without_promotions(self):
        self.assertEqual(calculate_total(3200), 3200)

    def test_coupon_is_case_insensitive_and_trimmed(self):
        self.assertEqual(calculate_total(6000, " save10 "), 5400)

    def test_coupon_minimum_uses_original_subtotal(self):
        self.assertEqual(calculate_total(4999, "SAVE10"), 4999)

    def test_fixed_discount_does_not_exceed_order_total(self):
        self.assertEqual(calculate_total(3000, "TAKE500"), 2500)

    def test_employee_discount_is_twenty_percent(self):
        self.assertEqual(calculate_total(10000, employee=True), 8000)

    def test_first_order_takes_precedence_over_employee_rate(self):
        self.assertEqual(calculate_total(10000, first_order=True, employee=True), 8500)

    def test_automatic_discount_cannot_be_stacked_with_coupon(self):
        self.assertEqual(calculate_total(10000, "SAVE10", first_order=True), 8500)

    def test_unknown_coupon_is_rejected_even_below_its_minimum(self):
        with self.assertRaises(ValueError):
            calculate_total(100, "NOT-A-COUPON")

    def test_boolean_is_not_a_valid_cent_amount(self):
        with self.assertRaises(ValueError):
            calculate_total(True)


if __name__ == "__main__":
    unittest.main()
