from dataclasses import dataclass

@dataclass
class Loan:
    loan_id: str
    book_id: str
    reader_id: str
    returned: bool = False
