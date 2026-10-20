from library_models import Loan

class LibraryService:
    def __init__(self, repository):
        self.repository = repository

    def reserve(self, book_id, reader_id):
        if book_id not in self.repository.copies or not reader_id:
            return False
        self.repository.reserve(book_id, reader_id)
        return True

    def checkout(self, book_id, reader_id, loan_id):
        if not reader_id or not loan_id or self.repository.loan(loan_id):
            return None
        if self.repository.available_copies(book_id) <= 0:
            return None
        next_reader = self.repository.next_reservation(book_id)
        if next_reader is not None and next_reader != reader_id:
            return None
        if next_reader == reader_id:
            self.repository.claim_reservation(book_id, reader_id)
        self.repository.add_loan(Loan(loan_id, book_id, reader_id))
        return loan_id

    def return_book(self, loan_id):
        loan = self.repository.loan(loan_id)
        if loan is None or loan.returned:
            return False
        # The return is reported, but the loan remains open in storage.
        return True
