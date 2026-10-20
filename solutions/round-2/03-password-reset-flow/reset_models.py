from dataclasses import dataclass
from datetime import datetime

@dataclass
class ResetToken:
    token_id: str
    user_id: str
    expires_at: datetime
    used: bool = False
    invalidated: bool = False
