class DocumentRoutes:
    def __init__(self,service): self.service=service
    def access(self,doc,user,action):
        try: return {"status":200 if self.service.can(doc,user,action) else 403,"allowed":self.service.can(doc,user,action)}
        except (KeyError,TypeError): return {"status":400,"allowed":False}
