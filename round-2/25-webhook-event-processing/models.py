from dataclasses import dataclass

@dataclass(frozen=True)
class WebhookEvent:
    event_id: str
    order_id: str
    sequence: int
    status: str
