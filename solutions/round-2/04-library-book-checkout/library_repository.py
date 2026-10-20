from collections import defaultdict, deque

class LibraryRepository:
    def __init__(self):
        self.copies = {}
        self.loans = {}
        self.reservations = defaultdict(deque)

    def add_book(self, book_id, copies):
        self.copies[book_id] = copies

    def available_copies(self, book_id):
        active = sum(loan.book_id == book_id and not loan.returned for loan in self.loans.values())
        return self.copies.get(book_id, 0) - active

    def add_loan(self, loan):
        self.loans[loan.loan_id] = loan

    def loan(self, loan_id):
        return self.loans.get(loan_id)

    def reserve(self, book_id, reader_id):
        queue = self.reservations[book_id]
        if reader_id not in queue:
            queue.append(reader_id)

    def next_reservation(self, book_id):
        queue = self.reservations[book_id]
        return queue[0] if queue else None

    def claim_reservation(self, book_id, reader_id):
        queue = self.reservations[book_id]
        if queue and queue[0] == reader_id:
            queue.popleft()
