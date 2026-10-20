from dataclasses import dataclass


@dataclass
class Delivery:
    event_id: str
    recipient: str
    message: str
    status: str = "queued"
    attempts: int = 0
