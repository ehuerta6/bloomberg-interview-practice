class ImportRoutes:
    def __init__(self,service): self.service=service
    def post(self,rows):
        if not isinstance(rows,list): return {"status":400,"error":"rows must be a list"}
        result=self.service.import_rows(rows)
        return {"status":207 if result["errors"] else 201,**result}
