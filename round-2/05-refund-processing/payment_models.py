from dataclasses import dataclass

@dataclass
class Payment:
    payment_id: str
    amount: int
    state: str
