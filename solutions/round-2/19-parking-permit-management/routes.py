class PermitRoutes:
    def __init__(self, service): self.service=service
    def issue(self, *args):
        try: return {"status":201,"permit":self.service.issue(*args)}
        except ValueError as exc: return {"status":409,"error":str(exc)}
    def renew(self,*args):
        try: return {"status":200,"permit":self.service.renew(*args)}
        except ValueError as exc: return {"status":409,"error":str(exc)}
