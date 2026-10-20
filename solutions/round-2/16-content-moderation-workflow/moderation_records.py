from dataclasses import dataclass


@dataclass
class Post:
    id: str
    author: str
    content: str
    status: str = "pending"


@dataclass
class AuditEvent:
    post_id: str
    actor: str
    decision: str
    note: str
