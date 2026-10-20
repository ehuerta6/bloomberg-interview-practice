from dataclasses import dataclass


@dataclass
class Job:
    id: str
    kind: str
    payload: dict
    status: str = "queued"
    attempts: int = 0
    lease_owner: str = None
    lease_until: int = 0
    last_error: str = None
