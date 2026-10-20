from models import Transfer

class TransferService:
    def __init__(self,repo): self.repo=repo
    def start(self,transfer_id,sku,source,destination,quantity):
        if not transfer_id or self.repo.transfer(transfer_id) or not sku or not source or not destination or source==destination or type(quantity) is not int or quantity<=0: raise ValueError("invalid transfer")
        available=self.repo.quantity(source,sku)
        if available<quantity: raise ValueError("insufficient source stock")
        self.repo.set_quantity(source,sku,available-quantity)
        transfer=Transfer(transfer_id,sku,source,destination,quantity)
        self.repo.transfers[transfer_id]=transfer
        return transfer
    def receive(self,transfer_id):
        transfer=self.repo.transfer(transfer_id)
        if not transfer or transfer.status!="in_transit": raise ValueError("transfer unavailable")
        dest=self.repo.quantity(transfer.destination,transfer.sku)
        self.repo.set_quantity(transfer.destination,transfer.sku,dest+transfer.quantity)
        transfer.status="received"
        return transfer
    def cancel(self,transfer_id):
        transfer=self.repo.transfer(transfer_id)
        if not transfer or transfer.status!="in_transit": raise ValueError("transfer unavailable")
        current=self.repo.quantity(transfer.source,transfer.sku)
        self.repo.set_quantity(transfer.source,transfer.sku,current+transfer.quantity)
        transfer.status="cancelled"
        return transfer
