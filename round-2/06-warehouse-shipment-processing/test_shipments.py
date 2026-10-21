import unittest
from warehouse_repository import WarehouseRepository
from shipment_service import ShipmentService

class ShipmentTests(unittest.TestCase):
    def setUp(self):
        self.repo = WarehouseRepository()
        self.repo.set_stock("sku-a", 4)
        self.repo.set_stock("sku-b", 2)
        self.service = ShipmentService(self.repo)

    def test_fulfillment_deducts_complete_order_once(self):
        self.assertEqual(self.service.fulfill("o1", {"sku-a": 2, "sku-b": 1}), "shipped")
        self.assertEqual(self.repo.on_hand("sku-a"), 2)
        self.assertEqual(self.repo.on_hand("sku-b"), 1)
        self.assertEqual(self.service.fulfill("o1", {"sku-a": 2, "sku-b": 1}), "already_shipped")
        self.assertEqual(self.repo.on_hand("sku-a"), 2)

    def test_failed_order_releases_every_reservation(self):
        self.assertEqual(self.service.fulfill("o1", {"sku-a": 3, "sku-b": 3}), "backordered")
        self.assertEqual(self.repo.reserved("sku-a"), 0)
        self.assertEqual(self.repo.reserved("sku-b"), 0)
        self.assertEqual(self.repo.available("sku-a"), 4)

    def test_partial_fulfillment_preserves_remainder_for_later(self):
        self.assertEqual(self.service.fulfill("o1", {"sku-a": 3, "sku-b": 3}, allow_partial=True), "partially_shipped")
        self.assertEqual(self.repo.on_hand("sku-a"), 1)
        self.assertEqual(self.repo.on_hand("sku-b"), 0)
        self.assertEqual(self.repo.backorder("o1"), {"sku-b": 1})

    def test_invalid_quantity_does_not_reserve_stock(self):
        self.assertEqual(self.service.fulfill("o1", {"sku-a": 0}), "rejected")
        self.assertEqual(self.repo.reserved("sku-a"), 0)
        self.assertEqual(self.repo.on_hand("sku-a"), 4)

    def test_existing_reservations_reduce_available_stock(self):
        self.repo.reserve("sku-a", 3)
        self.assertEqual(self.service.fulfill("o1", {"sku-a": 2}), "backordered")
        self.assertEqual(self.repo.reserved("sku-a"), 3)
    def test_partial_fulfillment_is_idempotent_on_order_retry(self):
        lines = {"sku-a": 3, "sku-b": 3}
        self.assertEqual(self.service.fulfill("o1", lines, allow_partial=True), "partially_shipped")
        self.assertEqual(self.service.fulfill("o1", lines, allow_partial=True), "already_shipped")
        self.assertEqual(self.repo.on_hand("sku-a"), 1)
        self.assertEqual(self.repo.on_hand("sku-b"), 0)

    def test_unknown_sku_is_backordered_without_consuming_known_stock(self):
        self.assertEqual(self.service.fulfill("o1", {"sku-a": 1, "missing": 1}), "backordered")
        self.assertEqual(self.repo.on_hand("sku-a"), 4)
        self.assertEqual(self.repo.reserved("sku-a"), 0)


if __name__ == "__main__": unittest.main()
