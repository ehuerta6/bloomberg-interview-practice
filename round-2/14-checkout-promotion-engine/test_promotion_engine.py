import unittest

from checkout_service import CheckoutService
from checkout_store import CheckoutStore
from promotion_engine import PromotionEngine


class PromotionEngineTests(unittest.TestCase):
    def build(self):
        store = CheckoutStore()
        store.add_promotion("SAVE10", "percent", 10, minimum_cents=5000, eligible_skus={"book"})
        store.add_promotion("SHIP5", "fixed", 500, eligible_skus={"book"})
        return store, CheckoutService(store, PromotionEngine(store))

    def test_percent_discount_uses_eligible_subtotal_before_tax(self):
        _, service = self.build()
        quote = service.quote([("book", 2, 3000)], "SAVE10", tax_rate=0.1)
        self.assertEqual(quote.subtotal, 6000)
        self.assertEqual(quote.discount, 600)
        self.assertEqual(quote.tax, 540)
        self.assertEqual(quote.total, 5940)

    def test_ineligible_or_below_minimum_promotion_is_not_applied(self):
        _, service = self.build()
        quote = service.quote([("pen", 1, 3000)], "SAVE10")
        self.assertEqual(quote.discount, 0)
        self.assertEqual(quote.total, 3000)

    def test_fixed_discount_never_makes_total_negative(self):
        _, service = self.build()
        quote = service.quote([("book", 1, 200)], "SHIP5")
        self.assertEqual(quote.discount, 200)
        self.assertEqual(quote.total, 0)

    def test_percent_discount_only_counts_eligible_lines_in_mixed_cart(self):
        _, service = self.build()
        quote = service.quote([("book", 1, 6000), ("pen", 1, 4000)], "SAVE10")
        self.assertEqual(quote.discount, 600)
        self.assertEqual(quote.total, 9400)


    def test_unknown_promotion_code_leaves_cart_undiscounted(self):
        _, service = self.build()
        quote = service.quote([("book", 1, 2000)], "MISSING")
        self.assertEqual(quote.discount, 0)
        self.assertEqual(quote.total, 2000)


    def test_fixed_discount_is_limited_to_eligible_subtotal(self):
        _, service = self.build()
        quote = service.quote([("book", 1, 300), ("pen", 1, 5000)], "SHIP5")
        self.assertEqual(quote.discount, 300)
        self.assertEqual(quote.total, 5000)

if __name__ == "__main__":
    unittest.main()
