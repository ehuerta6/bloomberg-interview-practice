"""Calculate a parcel shipping fee."""

import unittest


def calculate_shipping(order, rates):
    """Return base plus weight charge, waived at the inclusive threshold."""
    try:
        zone = order["zone"]
        subtotal = order["subtotal"]
        weight = order["weight_kg"]
        rate = rates[zone]
        base, per_kg, free_over = rate["base"], rate["per_kg"], rate["free_over"]
    except (KeyError, TypeError) as error:
        raise ValueError("order or rate is missing a required field") from error
    numbers = (subtotal, weight, base, per_kg, free_over)
    if any(not isinstance(value, (int, float)) or isinstance(value, bool) for value in numbers):
        raise ValueError("shipping amounts must be numeric")
    if subtotal < 0 or weight < 0 or base < 0 or per_kg < 0 or free_over < 0:
        raise ValueError("shipping amounts cannot be negative")
    if subtotal >= free_over:
        return 0.0
    return round(base + weight * per_kg, 2)


class ShippingTests(unittest.TestCase):
    def setUp(self):
        self.rates = {"local": {"base": 4.0, "per_kg": 1.5, "free_over": 50.0}}

    def test_base_and_weight_fee(self):
        self.assertEqual(calculate_shipping({"zone": "local", "subtotal": 20, "weight_kg": 2}, self.rates), 7.0)

    def test_free_threshold_is_inclusive(self):
        self.assertEqual(calculate_shipping({"zone": "local", "subtotal": 50, "weight_kg": 2}, self.rates), 0.0)

    def test_below_threshold_still_has_base_fee(self):
        self.assertEqual(calculate_shipping({"zone": "local", "subtotal": 49.99, "weight_kg": 0}, self.rates), 4.0)

    def test_unknown_zone_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_shipping({"zone": "moon", "subtotal": 10, "weight_kg": 1}, self.rates)

    def test_rounds_only_final_fee_to_cents(self):
        self.assertEqual(calculate_shipping({"zone": "local", "subtotal": 10, "weight_kg": 1.01}, self.rates), 5.52)

    def test_free_shipping_does_not_depend_on_weight(self):
        self.assertEqual(calculate_shipping({"zone": "local", "subtotal": 60, "weight_kg": 100}, self.rates), 0.0)

    def test_negative_weight_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_shipping({"zone": "local", "subtotal": 10, "weight_kg": -1}, self.rates)

    def test_order_is_not_mutated(self):
        order = {"zone": "local", "subtotal": 20, "weight_kg": 2}
        original = order.copy()
        calculate_shipping(order, self.rates)
        self.assertEqual(order, original)

    def test_boolean_amount_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_shipping({"zone": "local", "subtotal": True, "weight_kg": 2}, self.rates)


if __name__ == "__main__":
    unittest.main()
