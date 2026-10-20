from dataclasses import dataclass


@dataclass(frozen=True)
class Entry:
    transaction_id: str
    wallet_id: str
    amount: int
