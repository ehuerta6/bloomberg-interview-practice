from dataclasses import dataclass


@dataclass
class Subscription:
    id: str
    member_id: str
    monthly_cents: int
    next_due: str
    status: str = "active"
