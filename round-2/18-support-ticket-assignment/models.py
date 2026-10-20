from dataclasses import dataclass

@dataclass
class Ticket:
    ticket_id: str
    customer: str
    category: str
    priority: int
    status: str = "open"
    assignee: str | None = None
