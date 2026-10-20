class WarehouseRepository:
    def __init__(self):
        self.stock = {}
        self.reservations = {}
        self.shipments = {}

    def set_stock(self, sku, quantity):
        self.stock[sku] = quantity
        self.reservations.setdefault(sku, 0)

    def on_hand(self, sku):
        return self.stock.get(sku, 0)

    def reserved(self, sku):
        return self.reservations.get(sku, 0)

    def available(self, sku):
        return self.on_hand(sku) - self.reserved(sku)

    def reserve(self, sku, quantity):
        if quantity < 0 or quantity > self.available(sku):
            return False
        self.reservations[sku] = self.reserved(sku) + quantity
        return True

    def release(self, sku, quantity):
        self.reservations[sku] -= quantity

    def commit(self, sku, quantity):
        self.release(sku, quantity)
        self.stock[sku] -= quantity

    def save_shipment(self, shipment):
        self.shipments[shipment.order_id] = shipment

    def shipment(self, order_id):
        return self.shipments.get(order_id)

    def backorder(self, order_id):
        shipment = self.shipment(order_id)
        return shipment.backorder if shipment else {}
