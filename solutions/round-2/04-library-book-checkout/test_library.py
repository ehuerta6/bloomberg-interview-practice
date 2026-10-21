import unittest
from library_repository import LibraryRepository
from library_service import LibraryService

class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.repo = LibraryRepository()
        self.repo.add_book("b1", copies=1)
        self.service = LibraryService(self.repo)

    def test_checkout_creates_loan_and_uses_last_copy(self):
        loan = self.service.checkout("b1", "reader-a", "l1")
        self.assertEqual(loan, "l1")
        self.assertEqual(self.repo.available_copies("b1"), 0)
        self.assertIsNone(self.service.checkout("b1", "reader-b", "l2"))

    def test_return_releases_copy_and_cannot_be_repeated(self):
        self.service.checkout("b1", "reader-a", "l1")
        self.assertTrue(self.service.return_book("l1"))
        self.assertEqual(self.repo.available_copies("b1"), 1)
        self.assertFalse(self.service.return_book("l1"))

    def test_reservation_gets_copy_before_walk_in(self):
        self.assertTrue(self.service.reserve("b1", "reader-a"))
        self.assertIsNone(self.service.checkout("b1", "reader-b", "l1"))
        self.assertEqual(self.service.checkout("b1", "reader-a", "l2"), "l2")

    def test_returned_book_goes_to_next_reservation(self):
        self.service.checkout("b1", "reader-a", "l1")
        self.service.reserve("b1", "reader-b")
        self.service.reserve("b1", "reader-c")
        self.assertTrue(self.service.return_book("l1"))
        self.assertEqual(self.service.checkout("b1", "reader-b", "l2"), "l2")
        self.assertIsNone(self.service.checkout("b1", "reader-c", "l3"))

    def test_unknown_book_cannot_be_reserved_or_checked_out(self):
        self.assertFalse(self.service.reserve("missing", "reader-a"))
        self.assertIsNone(self.service.checkout("missing", "reader-a", "l1"))
        self.assertNotIn("l1", self.repo.loans)


    def test_duplicate_loan_id_does_not_replace_active_loan(self):
        self.service.checkout("b1", "reader-a", "l1")
        self.assertIsNone(self.service.checkout("b1", "reader-b", "l1"))
        self.assertEqual(self.repo.loan("l1").reader_id, "reader-a")
        self.assertEqual(self.repo.available_copies("b1"), 0)

if __name__ == "__main__": unittest.main()
