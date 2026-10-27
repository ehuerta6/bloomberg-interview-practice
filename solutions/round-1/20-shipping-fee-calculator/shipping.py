"""Calculate a store's flat-rate shipping quote."""

from decimal import Decimal, ROUND_HALF_UP
import unittest


def calculate_shipping(order, rates):
    """Return shipping in dollars after discount and the carrier minimum."""
    try:
        rate = rates[order["zone"]]
        weight = Decimal(str(order["weight_kg"]))
        subtotal = Decimal(str(order["subtotal"]))
        discount = Decimal(str(order.get("shipping_discount_percent", 0)))
        base = Decimal(str(rate["base_fee"]))
        per_kg = Decimal(str(rate["per_kg"]))
        minimum = Decimal(str(rate["minimum_fee"]))
        free_over = Decimal(str(rate["free_over"]))
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("invalid order or rate") from error
    if subtotal >= free_over:
        return Decimal("0.00")
    fee = base + weight * per_kg
    fee -= fee * discount / Decimal("100")
    return max(fee, minimum).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class ShippingTests(unittest.TestCase):
    def setUp(self):
        self.rates = {"local": {"base_fee": "3.00", "per_kg": "1.25", "minimum_fee": "5.00", "free_over": "75.00"}}

    def quote(self, weight="1", subtotal="20", **extra):
        return calculate_shipping({"zone": "local", "weight_kg": weight, "subtotal": subtotal, **extra}, self.rates)

    def test_minimum_fee_applies_when_calculated_price_is_lower(self):
        self.assertEqual(self.quote(weight="1"), Decimal("5.00"))

    def test_calculated_price_above_minimum_is_preserved(self):
        self.assertEqual(self.quote(weight="2"), Decimal("5.50"))

    def test_discount_is_applied_before_minimum(self):
        self.assertEqual(self.quote(weight="1", shipping_discount_percent="50"), Decimal("5.00"))

    def test_free_shipping_threshold_is_inclusive(self):
        self.assertEqual(self.quote(subtotal="75.00"), Decimal("0.00"))

    def test_just_below_free_shipping_threshold_is_charged(self):
        self.assertEqual(self.quote(subtotal="74.99"), Decimal("5.00"))


if __name__ == "__main__":
    unittest.main()
