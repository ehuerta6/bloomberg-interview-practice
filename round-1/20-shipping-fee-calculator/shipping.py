"""Calculate a shipping charge from the selected weight band."""

from decimal import Decimal
import unittest


def calculate_shipping(order, rates):
    """Return a shipping amount in dollars for one order."""
    try:
        rate = rates[order["zone"]]
        weight = Decimal(str(order["weight_kg"]))
        subtotal = Decimal(str(order["subtotal"]))
    except (KeyError, TypeError) as error:
        raise ValueError("order or zone is invalid") from error

    if subtotal >= Decimal(str(rate["free_over"])):
        return Decimal("0.00")

    per_kg = None
    for bracket in rate["weight_brackets"]:
        limit = bracket["up_to_kg"]
        if limit is None or weight < Decimal(str(limit)):
            per_kg = Decimal(str(bracket["per_kg"]))
            break
    if per_kg is None:
        per_kg = Decimal(str(rate["weight_brackets"][-1]["per_kg"]))
    fee = Decimal(str(rate["base_fee"])) + weight * per_kg
    discount = Decimal(str(order.get("shipping_discount_percent", 0)))
    fee -= fee * discount / Decimal("100")
    return fee.quantize(Decimal("0.01"))


class ShippingTests(unittest.TestCase):
    def setUp(self):
        self.rates = {
            "local": {
                "base_fee": "3.00",
                "minimum_fee": "5.00",
                "free_over": "75.00",
                "weight_brackets": [
                    {"up_to_kg": "2", "per_kg": "1.25"},
                    {"up_to_kg": "5", "per_kg": "1.00"},
                    {"up_to_kg": None, "per_kg": "0.80"},
                ],
            }
        }

    def test_uses_first_band_that_contains_total_weight(self):
        order = {"zone": "local", "subtotal": "20", "weight_kg": "1.5"}
        self.assertEqual(calculate_shipping(order, self.rates), Decimal("4.88"))

    def test_weight_band_boundary_moves_to_next_band(self):
        order = {"zone": "local", "subtotal": "20", "weight_kg": "2.01"}
        self.assertEqual(calculate_shipping(order, self.rates), Decimal("5.01"))

    def test_exact_weight_limit_stays_in_current_band(self):
        order = {"zone": "local", "subtotal": "20", "weight_kg": "2"}
        self.assertEqual(calculate_shipping(order, self.rates), Decimal("5.50"))

    def test_heaviest_band_has_no_upper_bound(self):
        order = {"zone": "local", "subtotal": "20", "weight_kg": "6"}
        self.assertEqual(calculate_shipping(order, self.rates), Decimal("7.80"))

    def test_percentage_discount_applies_before_minimum_fee(self):
        order = {"zone": "local", "subtotal": "20", "weight_kg": "1", "shipping_discount_percent": "50"}
        self.assertEqual(calculate_shipping(order, self.rates), Decimal("5.00"))

    def test_discount_does_not_reduce_below_minimum(self):
        order = {"zone": "local", "subtotal": "20", "weight_kg": "6", "shipping_discount_percent": "25"}
        self.assertEqual(calculate_shipping(order, self.rates), Decimal("5.85"))

    def test_free_shipping_threshold_is_inclusive(self):
        order = {"zone": "local", "subtotal": "75.00", "weight_kg": "10"}
        self.assertEqual(calculate_shipping(order, self.rates), Decimal("0.00"))

    def test_just_below_free_threshold_is_charged(self):
        order = {"zone": "local", "subtotal": "74.99", "weight_kg": "1"}
        self.assertGreater(calculate_shipping(order, self.rates), Decimal("0.00"))

    def test_decimal_inputs_are_not_rounded_before_final_charge(self):
        rates = {"local": {"base_fee": "3", "minimum_fee": "0", "free_over": "100", "weight_brackets": [{"up_to_kg": None, "per_kg": "1.25"}]}}
        order = {"zone": "local", "subtotal": "20", "weight_kg": "1.234", "shipping_discount_percent": "12.5"}
        self.assertEqual(calculate_shipping(order, rates), Decimal("3.97"))

    def test_invalid_weight_and_discount_are_rejected(self):
        with self.assertRaises(ValueError):
            calculate_shipping({"zone": "local", "subtotal": "20", "weight_kg": "-1"}, self.rates)
        with self.assertRaises(ValueError):
            calculate_shipping({"zone": "local", "subtotal": "20", "weight_kg": "1", "shipping_discount_percent": "101"}, self.rates)

    def test_unknown_zone_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_shipping({"zone": "moon", "subtotal": "20", "weight_kg": "1"}, self.rates)


if __name__ == "__main__":
    unittest.main()
