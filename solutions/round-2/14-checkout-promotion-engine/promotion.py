from dataclasses import dataclass


@dataclass
class Promotion:
    code: str
    kind: str
    value: int
    minimum_cents: int
    eligible_skus: set
