class OrderRepository:
    def __init__(self): self.orders={}; self.processed=set(); self.history={}
    def add_order(self,order_id,status="created"):
        self.orders[order_id]=status; self.history[order_id]=[]
    def status(self,order_id): return self.orders.get(order_id)
