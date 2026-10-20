from warehouse_models import Shipment

class ShipmentService:
    def __init__(self, repository):
        self.repository = repository

    def fulfill(self, order_id, lines, allow_partial=False):
        if not order_id or not lines or any(not isinstance(q, int) or q <= 0 for q in lines.values()):
            return "rejected"
        existing = self.repository.shipment(order_id)
        if existing:
            return "already_shipped" if existing.state in {"shipped", "partially_shipped"} else existing.state
        reserved = {}
        backorder = {}
        for sku, requested in lines.items():
            quantity = min(requested, self.repository.available(sku)) if allow_partial else requested
            if quantity and self.repository.reserve(sku, quantity):
                reserved[sku] = quantity
            elif not allow_partial:
                self.repository.save_shipment(Shipment(order_id, {}, dict(lines), "backordered"))
                return "backordered"
            if requested > quantity:
                backorder[sku] = requested - quantity
        for sku, quantity in reserved.items():
            self.repository.commit(sku, quantity)
        state = "partially_shipped" if backorder else "shipped"
        self.repository.save_shipment(Shipment(order_id, dict(reserved), backorder, state))
        return state
