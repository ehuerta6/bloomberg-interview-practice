class DeliveryStore:
    def __init__(self):
        self.records = {}

    def get(self, event_id):
        return self.records.get(event_id)

    def save(self, record):
        self.records[record.event_id] = record
