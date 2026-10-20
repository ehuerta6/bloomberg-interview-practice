from dataclasses import dataclass
from datetime import datetime

@dataclass
class SeatHold:
    hold_id: str
    seat_id: str
    customer_id: str
    expires_at: datetime
    confirmed: bool = False
