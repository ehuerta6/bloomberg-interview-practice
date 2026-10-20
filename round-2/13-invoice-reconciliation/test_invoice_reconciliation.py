import unittest

from invoice_service import InvoiceService
from invoice_store import InvoiceStore


class InvoiceReconciliationTests(unittest.TestCase):
    def build(self):
        store = InvoiceStore()
        store.add_invoice("inv-1", 10000)
        return store, InvoiceService(store)

    def test_partial_payments_accumulate_and_close_invoice(self):
        store, service = self.build()
        self.assertEqual(service.apply_payment("pay-1", "inv-1", 4000).status, "partial")
        result = service.apply_payment("pay-2", "inv-1", 6000)
        self.assertEqual(result.status, "paid")
        self.assertEqual(store.invoice("inv-1").paid_cents, 10000)

    def test_duplicate_payment_reference_is_applied_once(self):
        store, service = self.build()
        service.apply_payment("pay-3", "inv-1", 4000)
        service.apply_payment("pay-3", "inv-1", 4000)
        self.assertEqual(store.invoice("inv-1").paid_cents, 4000)
        self.assertEqual(len(store.payments_for("inv-1")), 1)

    def test_overpayment_is_rejected_without_mutation(self):
        store, service = self.build()
        result = service.apply_payment("pay-4", "inv-1", 12000)
        self.assertEqual(result.status, "rejected")
        self.assertEqual(store.invoice("inv-1").paid_cents, 0)


if __name__ == "__main__":
    unittest.main()
