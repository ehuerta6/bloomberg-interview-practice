class InvitationRoutes:
    def __init__(self,service): self.service=service
    def invite(self,*args):
        try: return {"status":201,"invitation":self.service.invite(*args)}
        except ValueError as exc: return {"status":409,"error":str(exc)}
    def accept(self,*args):
        try: return {"status":200,"invitation":self.service.accept(*args)}
        except ValueError as exc: return {"status":409,"error":str(exc)}
