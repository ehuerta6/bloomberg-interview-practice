class FakePaymentGateway:
    def __init__(self, approved=True):
        self.approved = approved
        self.charges = []

    def charge(self, invoice_id, amount_cents):
        self.charges.append((invoice_id, amount_cents))
        return self.approved
