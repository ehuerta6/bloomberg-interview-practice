from models import WebhookEvent

class WebhookService:
    ALLOWED={"created","paid","shipped","delivered","cancelled"}
    def __init__(self,repo): self.repo=repo
    def receive(self,event_id,order_id,sequence,status):
        if not all((event_id,order_id)) or type(sequence) is not int or sequence<1 or status not in self.ALLOWED: raise ValueError("invalid event")
        if event_id in self.repo.processed: return "duplicate"
        if order_id not in self.repo.orders: raise ValueError("unknown order")
        prior=self.repo.history[order_id]
        if prior and sequence<=prior[-1][0]:
            self.repo.processed.add(event_id)
            return "stale"
        self.repo.orders[order_id]=status
        prior.append((sequence,event_id,status))
        self.repo.processed.add(event_id)
        return "applied"
