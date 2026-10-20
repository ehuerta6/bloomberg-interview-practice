"""Reference checkout coupon calculation with regression tests."""

import unittest


COUPONS = {
    "SAVE10": ("percent", 10, 5000),
    "TAKE500": ("fixed", 500, 2500),
}


def calculate_total(subtotal_cents, coupon_code=None, first_order=False, employee=False):
    """Return the amount due after the highest-priority eligible promotion."""
    if isinstance(subtotal_cents, bool) or not isinstance(subtotal_cents, int) or subtotal_cents < 0:
        raise ValueError("subtotal must be a non-negative integer number of cents")

    if employee:
        discount = subtotal_cents * 20 // 100
    elif first_order:
        discount = subtotal_cents * 15 // 100
    elif coupon_code is not None:
        if not isinstance(coupon_code, str):
            raise ValueError("coupon must be text")
        code = coupon_code.strip().upper()
        if not code:
            return subtotal_cents
        if code not in COUPONS:
            raise ValueError("unknown coupon")
        kind, value, minimum = COUPONS[code]
        if subtotal_cents < minimum:
            discount = 0
        elif kind == "percent":
            discount = subtotal_cents * value // 100
        else:
            discount = value
    else:
        discount = 0

    return subtotal_cents - min(subtotal_cents, discount)


class CouponEligibilityTests(unittest.TestCase):
    def test_regular_order_without_promotions(self):
        self.assertEqual(calculate_total(3200), 3200)

    def test_coupon_is_case_insensitive_and_trimmed(self):
        self.assertEqual(calculate_total(6000, " save10 "), 5400)

    def test_coupon_minimum_uses_original_subtotal(self):
        self.assertEqual(calculate_total(4999, "SAVE10"), 4999)

    def test_fixed_discount_applies_at_minimum(self):
        self.assertEqual(calculate_total(2500, "TAKE500"), 2000)

    def test_employee_discount_is_twenty_percent(self):
        self.assertEqual(calculate_total(10000, employee=True), 8000)

    def test_employee_discount_has_precedence_over_first_order_and_coupon(self):
        self.assertEqual(calculate_total(10000, "SAVE10", True, True), 8000)

    def test_first_order_takes_precedence_over_coupon(self):
        self.assertEqual(calculate_total(10000, "SAVE10", first_order=True), 8500)

    def test_unknown_coupon_is_rejected_even_below_its_minimum(self):
        with self.assertRaises(ValueError):
            calculate_total(100, "NOT-A-COUPON")

    def test_blank_coupon_means_no_coupon(self):
        self.assertEqual(calculate_total(2500, "  "), 2500)

    def test_boolean_is_not_a_valid_cent_amount(self):
        with self.assertRaises(ValueError):
            calculate_total(True)


if __name__ == "__main__":
    unittest.main()
