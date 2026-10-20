from dataclasses import dataclass

@dataclass
class Shipment:
    order_id: str
    shipped: dict
    backorder: dict
    state: str
