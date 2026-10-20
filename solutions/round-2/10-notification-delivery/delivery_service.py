from delivery_record import Delivery


class DeliveryService:
    def __init__(self, store, provider, max_attempts=3):
        self.store, self.provider, self.max_attempts = store, provider, max_attempts

    def deliver(self, event_id, recipient, message):
        record = self.store.get(event_id)
        if record is None:
            record = Delivery(event_id, recipient, message)
        elif (record.recipient, record.message) != (recipient, message):
            raise ValueError("event key reused for different content")
        if record.status == "sent":
            return record
        return self._attempt(record, self.max_attempts)

    def retry(self, event_id):
        record = self.store.get(event_id)
        if record is None:
            raise KeyError(event_id)
        if record.status == "sent":
            return record
        return self._attempt(record, self.max_attempts)

    def _attempt(self, record, limit):
        for _ in range(limit):
            record.attempts += 1
            record.status = "sending"
            self.store.save(record)
            if self.provider.send(record.recipient, record.message):
                record.status = "sent"
                self.store.save(record)
                return record
        record.status = "failed"
        self.store.save(record)
        return record
