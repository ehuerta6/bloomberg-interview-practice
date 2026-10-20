class RenewalStore:
    def __init__(self):
        self.subscriptions = {}
        self.invoices = {}

    def add(self, sub_id, member_id, monthly_cents, next_due):
        from subscription import Subscription
        self.subscriptions[sub_id] = Subscription(sub_id, member_id, monthly_cents, next_due)

    def get(self, sub_id):
        return self.subscriptions.get(sub_id)

    def invoice_status(self, invoice_id):
        return self.invoices.get(invoice_id)

    def save_invoice(self, invoice_id, status):
        self.invoices[invoice_id] = status
