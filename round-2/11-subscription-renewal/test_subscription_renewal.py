import unittest

from renewal_service import RenewalService
from renewal_store import RenewalStore
from payment_gateway import FakePaymentGateway


class SubscriptionRenewalTests(unittest.TestCase):
    def build(self, approved=True):
        store = RenewalStore()
        store.add("sub-1", "member-1", 1200, "2026-10-01")
        gateway = FakePaymentGateway(approved)
        return store, gateway, RenewalService(store, gateway)

    def test_success_charges_once_and_advances_from_due_date(self):
        store, gateway, service = self.build()
        first = service.renew("sub-1", "invoice-1", "2026-10-01")
        replay = service.renew("sub-1", "invoice-1", "2026-10-01")
        self.assertEqual(first.status, "paid")
        self.assertEqual(replay.status, "paid")
        self.assertEqual(store.get("sub-1").next_due, "2026-11-01")
        self.assertEqual(gateway.charges, [("invoice-1", 1200)])

    def test_declined_renewal_keeps_due_date_and_marks_past_due(self):
        store, _, service = self.build(approved=False)
        result = service.renew("sub-1", "invoice-2", "2026-10-01")
        self.assertEqual(result.status, "declined")
        self.assertEqual(store.get("sub-1").status, "past_due")
        self.assertEqual(store.get("sub-1").next_due, "2026-10-01")


if __name__ == "__main__":
    unittest.main()
