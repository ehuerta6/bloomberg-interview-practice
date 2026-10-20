from dataclasses import dataclass

@dataclass(frozen=True)
class ImportRow:
    external_id: str
    email: str
    amount: int
