from dataclasses import dataclass


@dataclass
class Invoice:
    id: str
    total_cents: int
    paid_cents: int = 0
    status: str = "open"
