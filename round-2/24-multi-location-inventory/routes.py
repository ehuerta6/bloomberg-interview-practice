class TransferRoutes:
    def __init__(self,service): self.service=service
    def start(self,*args):
        try: return {"status":201,"transfer":self.service.start(*args)}
        except ValueError as exc: return {"status":409,"error":str(exc)}
    def receive(self,transfer_id):
        try: return {"status":200,"transfer":self.service.receive(transfer_id)}
        except ValueError as exc: return {"status":409,"error":str(exc)}
    def cancel(self,transfer_id):
        try: return {"status":200,"transfer":self.service.cancel(transfer_id)}
        except ValueError as exc: return {"status":409,"error":str(exc)}
