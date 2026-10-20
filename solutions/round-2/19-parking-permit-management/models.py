from dataclasses import dataclass

@dataclass
class Permit:
    permit_id: str
    resident_id: str
    zone: str
    expires_day: int
    active: bool = True
