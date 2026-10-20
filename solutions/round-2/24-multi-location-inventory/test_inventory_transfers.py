import unittest
from repository import InventoryRepository
from service import TransferService
from routes import TransferRoutes

class TransferTests(unittest.TestCase):
    def setUp(self):
        self.repo=InventoryRepository({("east","book"):8,("west","book"):2}); self.routes=TransferRoutes(TransferService(self.repo))
    def test_start_then_receive_moves_stock_once(self):
        self.routes.start("t1","book","east","west",3)
        self.assertEqual((self.repo.quantity("east","book"),self.repo.quantity("west","book")),(5,2))
        self.routes.receive("t1")
        self.assertEqual((self.repo.quantity("east","book"),self.repo.quantity("west","book")),(5,5))
        self.assertEqual(self.repo.transfer("t1").status,"received")
    def test_receive_twice_is_rejected_without_duplication(self):
        self.routes.start("t1","book","east","west",3); self.routes.receive("t1")
        self.assertEqual(self.routes.receive("t1")["status"],409); self.assertEqual(self.repo.quantity("west","book"),5)
    def test_cancel_restores_source_and_cannot_be_received(self):
        self.routes.start("t1","book","east","west",3); self.routes.cancel("t1")
        self.assertEqual((self.repo.quantity("east","book"),self.repo.quantity("west","book")),(8,2))
        self.assertEqual(self.routes.receive("t1")["status"],409)
    def test_failed_start_has_no_partial_state(self):
        self.assertEqual(self.routes.start("bad","book","east","west",99)["status"],409)
        self.assertEqual(self.repo.quantity("east","book"),8); self.assertNotIn("bad",self.repo.transfers)
    def test_duplicate_id_and_same_location_are_rejected(self):
        self.routes.start("t1","book","east","west",1)
        self.assertEqual(self.routes.start("t1","book","east","west",1)["status"],409)
        self.assertEqual(self.routes.start("t2","book","east","east",1)["status"],409)

class AdditionalTransferTests(unittest.TestCase):
    def test_conservation_holds_across_multiple_in_transit_transfers(self):
        repo=InventoryRepository({("a","sku"):10,("b","sku"):0,("c","sku"):0}); svc=TransferService(repo)
        svc.start("x","sku","a","b",4); svc.start("y","sku","a","c",3)
        def accounted_units():
            on_hand = sum(repo.stock.values())
            in_transit = sum(t.quantity for t in repo.transfers.values() if t.status == "in_transit")
            return on_hand + in_transit
        self.assertEqual(accounted_units(),10)
        svc.receive("x"); svc.cancel("y")
        self.assertEqual(accounted_units(),10)
    def test_cannot_cancel_after_receive(self):
        repo=InventoryRepository({("a","sku"):2}); svc=TransferService(repo); svc.start("x","sku","a","b",1); svc.receive("x")
        with self.assertRaises(ValueError): svc.cancel("x")

if __name__=="__main__": unittest.main()
