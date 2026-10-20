class StoreRepository:
    def __init__(self): self.orders={}; self.stock={}; self.returns={}
    def add_order(self,order_id,lines): self.orders[order_id]={line.line_id:line for line in lines}
    def line(self,order_id,line_id): return self.orders.get(order_id,{}).get(line_id)
    def returned(self,order_id,line_id): return sum(r.quantity for r in self.returns.values() if r.order_id==order_id and r.line_id==line_id)
