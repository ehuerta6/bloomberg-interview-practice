import unittest
from repository import OrderRepository
from service import WebhookService
from routes import WebhookRoutes

class WebhookTests(unittest.TestCase):
    def setUp(self):
        self.repo=OrderRepository(); self.repo.add_order("o1"); self.routes=WebhookRoutes(WebhookService(self.repo))
    def post(self,event,seq,status): return self.routes.post(event,"o1",seq,status)
    def test_duplicate_event_id_applies_once(self):
        self.assertEqual(self.post("e1",1,"paid")["result"],"applied")
        self.assertEqual(self.post("e1",1,"paid")["result"],"duplicate")
        self.assertEqual(self.repo.history["o1"],[(1,"e1","paid")])
    def test_out_of_order_event_does_not_regress_state(self):
        self.post("e2",2,"shipped"); result=self.post("e1",1,"paid")
        self.assertEqual(result["result"],"stale"); self.assertEqual(self.repo.status("o1"),"shipped")
    def test_newer_events_advance_status_and_keep_history(self):
        self.post("e1",1,"paid"); self.post("e2",2,"shipped"); self.post("e3",3,"delivered")
        self.assertEqual(self.repo.status("o1"),"delivered"); self.assertEqual(len(self.repo.history["o1"]),3)
    def test_invalid_or_unknown_events_do_not_mutate(self):
        self.assertEqual(self.post("bad",0,"paid")["status"],409)
        self.assertEqual(self.routes.post("x","missing",1,"paid")["status"],409)
        self.assertEqual(self.repo.history["o1"],[]); self.assertEqual(self.repo.status("o1"),"created")
    def test_same_sequence_conflict_is_stale_and_idempotent(self):
        self.post("e1",1,"paid"); result=self.post("e2",1,"cancelled")
        self.assertEqual(result["result"],"stale"); self.assertEqual(self.repo.status("o1"),"paid")
        self.assertEqual(self.post("e2",1,"cancelled")["result"],"duplicate")

class AdditionalWebhookTests(unittest.TestCase):
    def test_event_ids_are_global_across_orders(self):
        repo=OrderRepository(); repo.add_order("a"); repo.add_order("b"); svc=WebhookService(repo)
        svc.receive("event","a",1,"paid")
        self.assertEqual(svc.receive("event","b",1,"paid"),"duplicate")
        self.assertEqual(repo.status("b"),"created")
    def test_independent_orders_have_independent_sequences(self):
        repo=OrderRepository(); repo.add_order("a"); repo.add_order("b"); svc=WebhookService(repo)
        svc.receive("a2","a",2,"shipped")
        self.assertEqual(svc.receive("b1","b",1,"paid"),"applied")


if __name__=="__main__": unittest.main()
