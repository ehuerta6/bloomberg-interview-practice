class CustomerRepository:
    def __init__(self): self.records={}
    def get(self,external_id): return self.records.get(external_id)
    def save(self,record): self.records[record.external_id]=record
