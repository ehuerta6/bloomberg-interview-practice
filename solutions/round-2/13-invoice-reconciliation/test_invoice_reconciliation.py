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

    def test_duplicate_reference_with_changed_amount_does_not_change_original_payment(self):
        store, service = self.build()
        service.apply_payment("pay-5", "inv-1", 2500)
        service.apply_payment("pay-5", "inv-1", 7000)
        self.assertEqual(store.invoice("inv-1").paid_cents, 2500)
        self.assertEqual(store.payment("pay-5"), ("inv-1", 2500))

    def test_same_reference_cannot_be_reassigned_to_another_invoice(self):
        store, service = self.build()
        store.add_invoice("inv-2", 5000)
        service.apply_payment("pay-6", "inv-1", 1000)
        self.assertEqual(service.apply_payment("pay-6", "inv-2", 1000).status, "conflict")
        self.assertEqual(store.invoice("inv-2").paid_cents, 0)


    def test_payment_reference_reused_for_other_amount_is_conflict(self):
        store, service = self.build()
        service.apply_payment("pay-5", "inv-1", 1000)
        self.assertEqual(service.apply_payment("pay-5", "inv-1", 2000).status, "conflict")
        self.assertEqual(store.invoice("inv-1").paid_cents, 1000)


    def test_unknown_invoice_does_not_record_payment(self):
        store, service = self.build()
        self.assertEqual(service.apply_payment("pay-missing", "missing", 100).status, "rejected")
        self.assertIsNone(store.payment("pay-missing"))


    def test_zero_payment_is_rejected_without_mutation(self):
        store, service = self.build()
        self.assertEqual(service.apply_payment("pay-zero", "inv-1", 0).status, "rejected")
        self.assertEqual(store.invoice("inv-1").paid_cents, 0)
        self.assertIsNone(store.payment("pay-zero"))

if __name__ == "__main__":
    unittest.main()
