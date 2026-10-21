import unittest
from payment_repository import PaymentRepository
from refund_service import RefundService

class RefundTests(unittest.TestCase):
    def setUp(self):
        self.repo = PaymentRepository()
        self.repo.add_payment("p1", amount=5000, state="captured")
        self.service = RefundService(self.repo)

    def test_refund_changes_payment_state_and_records_amount(self):
        self.assertEqual(self.service.refund("p1", "rf1", 1500), "refunded")
        self.assertEqual(self.repo.payment_state("p1"), "partially_refunded")
        self.assertEqual(self.repo.refunded_total("p1"), 1500)

    def test_same_refund_retry_is_idempotent(self):
        self.service.refund("p1", "rf1", 1500)
        self.assertEqual(self.service.refund("p1", "rf1", 1500), "already_refunded")
        self.assertEqual(self.repo.refunded_total("p1"), 1500)

    def test_over_refund_is_rejected_without_state_change(self):
        self.assertEqual(self.service.refund("p1", "rf1", 5001), "rejected")
        self.assertEqual(self.repo.payment_state("p1"), "captured")
        self.assertEqual(self.repo.refunded_total("p1"), 0)

    def test_uncaptured_or_unknown_payment_cannot_be_refunded(self):
        self.repo.add_payment("p2", amount=900, state="authorized")
        self.assertEqual(self.service.refund("p2", "rf2", 100), "rejected")
        self.assertEqual(self.service.refund("missing", "rf3", 100), "rejected")
        self.assertEqual(self.repo.refunded_total("p2"), 0)

    def test_distinct_refunds_cannot_exceed_captured_amount(self):
        self.service.refund("p1", "rf1", 3000)
        self.assertEqual(self.service.refund("p1", "rf2", 2500), "rejected")
        self.assertEqual(self.repo.refunded_total("p1"), 3000)

    def test_full_refund_marks_payment_fully_refunded(self):
        self.assertEqual(self.service.refund("p1", "rf1", 5000), "refunded")
        self.assertEqual(self.repo.payment_state("p1"), "refunded")
        self.assertEqual(self.repo.refunded_total("p1"), 5000)


    def test_refund_reference_cannot_be_reused_for_different_amount(self):
        self.service.refund("p1", "rf1", 1000)
        self.assertEqual(self.service.refund("p1", "rf1", 2000), "rejected")
        self.assertEqual(self.repo.refunded_total("p1"), 1000)

if __name__ == "__main__": unittest.main()
