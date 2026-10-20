from models import ReturnCase

class ReturnService:
    def __init__(self,repo): self.repo=repo
    def process(self,return_id,order_id,line_id,quantity,action,replacement_sku=None):
        if not return_id or return_id in self.repo.returns: raise ValueError("duplicate return")
        line=self.repo.line(order_id,line_id)
        if not line or type(quantity) is not int or quantity<=0 or action not in {"refund","exchange"}: raise ValueError("invalid return")
        if self.repo.returned(order_id,line_id)+quantity>line.quantity: raise ValueError("quantity exceeds purchase")
        if action=="exchange" and not replacement_sku: raise ValueError("replacement required")
        if action=="refund":
            amount=line.unit_price*quantity
            self.repo.stock[line.sku]=self.repo.stock.get(line.sku,0)+quantity
        else:
            amount=0
            if self.repo.stock.get(replacement_sku,0)<quantity: raise ValueError("replacement unavailable")
            self.repo.stock[replacement_sku]-=quantity
            self.repo.stock[line.sku]=self.repo.stock.get(line.sku,0)+quantity
        case=ReturnCase(return_id,order_id,line_id,quantity,action,replacement_sku)
        self.repo.returns[return_id]=case
        return {"case":case,"refund_cents":amount}
