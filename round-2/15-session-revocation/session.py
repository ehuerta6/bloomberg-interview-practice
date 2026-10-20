from dataclasses import dataclass


@dataclass
class Session:
    id: str
    user_id: str
    device: str
    revoked_at: str = None
