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

    def test_new_invoice_attempt_can_collect_after_decline(self):
        store, gateway, service = self.build(approved=False)
        self.assertEqual(service.renew("sub-1", "invoice-3", "2026-10-01").status, "declined")
        gateway.approved = True
        self.assertEqual(service.renew("sub-1", "invoice-4", "2026-10-02").status, "paid")
        self.assertEqual(store.get("sub-1").next_due, "2026-11-01")
        self.assertEqual(gateway.charges, [("invoice-3", 1200), ("invoice-4", 1200)])

    def test_early_renewal_does_not_charge(self):
        store, gateway, service = self.build()
        result = service.renew("sub-1", "invoice-early", "2026-09-30")
        self.assertEqual(result.status, "not_due")
        self.assertEqual(gateway.charges, [])


    def test_early_renewal_does_not_call_gateway_or_change_state(self):
        store, gateway, service = self.build()
        result = service.renew("sub-1", "invoice-early", "2026-09-30")
        self.assertEqual(result.status, "not_due")
        self.assertEqual(gateway.charges, [])
        self.assertEqual(store.get("sub-1").next_due, "2026-10-01")


    def test_renewal_preserves_month_end_schedule(self):
        store, _, service = self.build()
        store.get("sub-1").next_due = "2026-01-31"
        self.assertEqual(service.renew("sub-1", "invoice-jan", "2026-01-31").status, "paid")
        self.assertEqual(store.get("sub-1").next_due, "2026-02-28")


    def test_canceled_subscription_is_not_charged(self):
        store, gateway, service = self.build()
        store.get("sub-1").status = "canceled"
        self.assertEqual(service.renew("sub-1", "invoice-canceled", "2026-10-01").status, "not_due")
        self.assertEqual(gateway.charges, [])


    def test_missing_subscription_does_not_create_invoice_or_charge(self):
        store, gateway, service = self.build()
        self.assertEqual(service.renew("missing", "invoice-x", "2026-10-01").status, "missing")
        self.assertEqual(store.invoices, {})
        self.assertEqual(gateway.charges, [])

    def test_declined_invoice_replay_does_not_charge_again(self):
        store, gateway, service = self.build(approved=False)
        first = service.renew("sub-1", "invoice-declined", "2026-10-01")
        gateway.approved = True
        replay = service.renew("sub-1", "invoice-declined", "2026-10-01")
        self.assertEqual(first.status, "declined")
        self.assertEqual(replay.status, "declined")
        self.assertEqual(gateway.charges, [("invoice-declined", 1200)])
        self.assertEqual(store.get("sub-1").next_due, "2026-10-01")

if __name__ == "__main__":
    unittest.main()
