class InventoryRepository:
    def __init__(self,stock): self.stock=dict(stock); self.transfers={}
    def quantity(self,location,sku): return self.stock.get((location,sku),0)
    def set_quantity(self,location,sku,value): self.stock[(location,sku)]=value
    def transfer(self,transfer_id): return self.transfers.get(transfer_id)
