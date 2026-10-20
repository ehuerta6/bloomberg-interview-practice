class WebhookRoutes:
    def __init__(self,service): self.service=service
    def post(self,*args):
        try: return {"status":200,"result":self.service.receive(*args)}
        except ValueError as exc: return {"status":409,"error":str(exc)}
