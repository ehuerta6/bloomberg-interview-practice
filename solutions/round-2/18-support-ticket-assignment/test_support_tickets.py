import unittest
from repository import TicketRepository
from service import TicketService
from routes import TicketRoutes

class TicketTests(unittest.TestCase):
    def setUp(self):
        self.repo=TicketRepository(); self.service=TicketService(self.repo); self.routes=TicketRoutes(self.service)
    def make(self, ident, priority=3, category="technical"):
        return self.routes.create(ident, "Morgan", category, priority)
    def test_priority_then_balanced_routing(self):
        self.make("low", 1); self.make("urgent", 5); self.make("mid", 3)
        urgent=self.routes.assign("technical")["ticket"]
        self.assertEqual(urgent.ticket_id, "urgent")
        self.assertEqual(urgent.assignee, "Cal")
        next_ticket=self.routes.assign("technical")["ticket"]
        self.assertEqual(next_ticket.ticket_id, "mid")
        self.assertEqual(next_ticket.assignee, "Dee")
    def test_reassignment_moves_load_exactly_once(self):
        self.make("t"); ticket=self.routes.assign("technical")["ticket"]
        self.routes.reassign("t", "Dee")
        self.assertEqual((ticket.assignee, self.repo.loads["Cal"], self.repo.loads["Dee"]), ("Dee", 0, 1))
    def test_empty_queue_and_bad_requests(self):
        self.assertEqual(self.routes.assign("billing")["status"], 204)
        self.assertEqual(self.make("bad", 9)["status"], 409)
        self.assertEqual(self.routes.reassign("missing", "Cal")["status"], 409)
    def test_priority_ties_are_fifo(self):
        self.make("first", 4); self.make("second", 4)
        self.assertEqual(self.routes.assign("technical")["ticket"].ticket_id, "first")

class AdditionalTicketTests(unittest.TestCase):
    def test_billing_queue_is_independent_and_reassignment_rejects_wrong_team(self):
        repo=TicketRepository(); service=TicketService(repo); routes=TicketRoutes(service)
        routes.create("b","Client","billing",5); routes.create("t","Client","technical",1)
        self.assertEqual(routes.assign("billing")["ticket"].ticket_id,"b")
        with self.assertRaises(ValueError): service.reassign("b","Cal")
    def test_assigned_ticket_is_not_dispatched_twice(self):
        repo=TicketRepository(); service=TicketService(repo); service.submit("x","C","technical",2)
        service.assign_next("technical")
        self.assertIsNone(service.assign_next("technical"))



if __name__ == "__main__": unittest.main()
