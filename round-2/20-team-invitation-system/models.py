from dataclasses import dataclass

@dataclass
class Invitation:
    invite_id: str
    email: str
    role: str
    expires_at: int
    status: str = "pending"
