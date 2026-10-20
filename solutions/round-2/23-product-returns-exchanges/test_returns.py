import unittest
from models import OrderLine
from repository import StoreRepository
from service import ReturnService
from routes import ReturnRoutes

class ReturnTests(unittest.TestCase):
    def setUp(self):
        self.repo=StoreRepository(); self.repo.add_order("o1",[OrderLine("l1","coat",3,2500)]); self.repo.stock={"coat":1,"shirt":4}; self.routes=ReturnRoutes(ReturnService(self.repo))
    def test_refund_restores_stock_and_refunds_exact_amount(self):
        result=self.routes.post("r1","o1","l1",2,"refund")
        self.assertEqual(result["refund_cents"],5000); self.assertEqual(self.repo.stock["coat"],3)
    def test_exchange_restores_returned_unit_and_consumes_replacement(self):
        result=self.routes.post("r1","o1","l1",1,"exchange","shirt")
        self.assertEqual(result["refund_cents"],0); self.assertEqual(self.repo.stock,{"coat":2,"shirt":3})
    def test_combined_returns_cannot_exceed_purchased_quantity(self):
        self.routes.post("r1","o1","l1",2,"refund")
        self.assertEqual(self.routes.post("r2","o1","l1",2,"exchange","shirt")["status"],409)
        self.assertEqual(self.repo.stock,{"coat":3,"shirt":4})
    def test_failed_exchange_is_atomic(self):
        result=self.routes.post("r1","o1","l1",1,"exchange","missing")
        self.assertEqual(result["status"],409); self.assertEqual(self.repo.stock,{"coat":1,"shirt":4}); self.assertEqual(self.repo.returns,{})
    def test_bad_quantity_and_duplicate_request_have_no_second_effect(self):
        self.assertEqual(self.routes.post("r1","o1","l1",True,"refund")["status"],409)
        self.routes.post("r1","o1","l1",1,"refund")
        self.assertEqual(self.routes.post("r1","o1","l1",1,"refund")["status"],409)
        self.assertEqual(self.repo.stock["coat"],2)

class AdditionalReturnTests(unittest.TestCase):
    def test_two_partial_refunds_preserve_exact_remainder(self):
        repo=StoreRepository(); repo.add_order("o",[OrderLine("l","sku",3,700)]); svc=ReturnService(repo)
        self.assertEqual(svc.process("r1","o","l",1,"refund")["refund_cents"],700)
        self.assertEqual(svc.process("r2","o","l",2,"refund")["refund_cents"],1400)
        self.assertEqual(repo.stock["sku"],3)
    def test_exchange_requires_replacement_sku(self):
        repo=StoreRepository(); repo.add_order("o",[OrderLine("l","sku",1,700)]); repo.stock["sku"]=0
        with self.assertRaises(ValueError): ReturnService(repo).process("r","o","l",1,"exchange")

    def test_line_identifiers_are_scoped_to_the_order(self):
        repo=StoreRepository(); repo.add_order("o1",[OrderLine("l1","coat",3,2500)])
        repo.add_order("o2",[OrderLine("l1","shirt",2,1000)])
        routes=ReturnRoutes(ReturnService(repo))
        routes.post("r1","o1","l1",3,"refund")
        result=routes.post("r2","o2","l1",2,"refund")
        self.assertEqual(result["status"],201)
        self.assertEqual(result["refund_cents"],2000)

if __name__=="__main__": unittest.main()
