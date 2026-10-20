from dataclasses import dataclass

@dataclass
class OrderLine:
    line_id: str
    sku: str
    quantity: int
    unit_price: int

@dataclass
class ReturnCase:
    return_id: str
    order_id: str
    line_id: str
    quantity: int
    action: str
    replacement_sku: str | None = None
    status: str = "completed"
