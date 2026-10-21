"""Calculate shipping with weight bands, discounts, and a minimum charge."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import unittest

_CENT = Decimal("0.01")
_ZERO = Decimal("0")
_HUNDRED = Decimal("100")


def _amount(value, field):
    if isinstance(value, bool):
        raise ValueError(f"{field} must be a finite amount")
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as error:
        raise ValueError(f"{field} must be a finite amount") from error
    if not amount.is_finite():
        raise ValueError(f"{field} must be a finite amount")
    return amount


def _select_band(weight, brackets):
    if not isinstance(brackets, (list, tuple)) or not brackets:
        raise ValueError("weight_brackets must contain at least one band")
    previous_limit = _ZERO
    normalized = []
    for index, bracket in enumerate(brackets):
        try:
            upper_limit = bracket.get("up_to_kg")
            per_kg = _amount(bracket["per_kg"], "per_kg")
        except (AttributeError, KeyError, TypeError) as error:
            raise ValueError("each weight band needs a per_kg rate") from error
        if per_kg < _ZERO:
            raise ValueError("per_kg cannot be negative")
        if upper_limit is None:
            if index != len(brackets) - 1:
                raise ValueError("only the final weight band may be unbounded")
        else:
            upper_limit = _amount(upper_limit, "up_to_kg")
            if upper_limit <= previous_limit:
                raise ValueError("weight band limits must increase")
            previous_limit = upper_limit
        normalized.append((upper_limit, per_kg))
    if normalized[-1][0] is not None:
        raise ValueError("weight bands must end with an unbounded band")
    for upper_limit, per_kg in normalized:
        if upper_limit is None or weight <= upper_limit:
            return per_kg
    raise ValueError("weight bands must end with an unbounded band")


def calculate_shipping(order, rates):
    """Return a Decimal fee rounded to cents using half-up currency rounding.

    The order contains zone, subtotal, weight_kg, and optional
    shipping_discount_percent. A rate contains base_fee, minimum_fee,
    free_over, and ordered weight_brackets with per_kg rates.
    """
    try:
        zone = order["zone"]
        rate = rates[zone]
        subtotal = _amount(order["subtotal"], "subtotal")
        weight = _amount(order["weight_kg"], "weight_kg")
        base_fee = _amount(rate["base_fee"], "base_fee")
        minimum_fee = _amount(rate["minimum_fee"], "minimum_fee")
        free_over = _amount(rate["free_over"], "free_over")
        discount = _amount(order.get("shipping_discount_percent", 0), "shipping_discount_percent")
    except (KeyError, TypeError, AttributeError) as error:
        raise ValueError("order or rate is missing a required field") from error
    amounts = (subtotal, weight, base_fee, minimum_fee, free_over, discount)
    if any(amount < _ZERO for amount in amounts):
        raise ValueError("shipping amounts cannot be negative")
    if discount > _HUNDRED:
        raise ValueError("shipping discount must not exceed 100 percent")
    per_kg = _select_band(weight, rate.get("weight_brackets"))
    if subtotal >= free_over:
        return _ZERO.quantize(_CENT)
    raw_fee = base_fee + weight * per_kg
    discounted_fee = raw_fee * (_HUNDRED - discount) / _HUNDRED
    return max(discounted_fee, minimum_fee).quantize(_CENT, rounding=ROUND_HALF_UP)


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
        self.assertEqual(calculate_shipping(order, self.rates), Decimal("5.00"))

    def test_weight_band_boundary_moves_to_next_band(self):
        order = {"zone": "local", "subtotal": "20", "weight_kg": "2.01"}
        self.assertEqual(calculate_shipping(order, self.rates), Decimal("5.01"))

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
        self.assertEqual(calculate_shipping(order, self.rates), Decimal("5.00"))

    def test_decimal_rounding_uses_half_up(self):
        rates = {"local": {"base_fee": "0", "minimum_fee": "0", "free_over": "100", "weight_brackets": [{"up_to_kg": None, "per_kg": "1"}]}}
        order = {"zone": "local", "subtotal": "10", "weight_kg": "1.005"}
        self.assertEqual(calculate_shipping(order, rates), Decimal("1.01"))

    def test_invalid_weight_and_discount_are_rejected(self):
        with self.assertRaises(ValueError):
            calculate_shipping({"zone": "local", "subtotal": "20", "weight_kg": "-1"}, self.rates)
        with self.assertRaises(ValueError):
            calculate_shipping({"zone": "local", "subtotal": "20", "weight_kg": "1", "shipping_discount_percent": "101"}, self.rates)

    def test_unknown_zone_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_shipping({"zone": "moon", "subtotal": "20", "weight_kg": "1"}, self.rates)

    def test_boolean_amount_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_shipping({"zone": "local", "subtotal": True, "weight_kg": "1"}, self.rates)

    def test_free_shipping_does_not_hide_invalid_rate_configuration(self):
        rates = {"local": {"base_fee": "3", "minimum_fee": "0", "free_over": "75", "weight_brackets": [{"up_to_kg": "5", "per_kg": "1"}, {"up_to_kg": "2", "per_kg": "2"}, {"up_to_kg": None, "per_kg": "1"}]}}
        with self.assertRaises(ValueError):
            calculate_shipping({"zone": "local", "subtotal": "75", "weight_kg": "1"}, rates)


if __name__ == "__main__":
    unittest.main()
