from dataclasses import dataclass

@dataclass
class Transfer:
    transfer_id: str
    sku: str
    source: str
    destination: str
    quantity: int
    status: str = "in_transit"
