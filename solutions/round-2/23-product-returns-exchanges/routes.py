class ReturnRoutes:
    def __init__(self,service): self.service=service
    def post(self,*args):
        try: return {"status":201,**self.service.process(*args)}
        except ValueError as exc: return {"status":409,"error":str(exc)}
