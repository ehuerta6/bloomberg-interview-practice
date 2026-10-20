class InvoiceStore:
    def __init__(self):
        self.invoices = {}
        self.payments = {}

    def add_invoice(self, invoice_id, total_cents):
        from invoice import Invoice
        self.invoices[invoice_id] = Invoice(invoice_id, total_cents)

    def invoice(self, invoice_id):
        return self.invoices.get(invoice_id)

    def payment(self, payment_id):
        return self.payments.get(payment_id)

    def payments_for(self, invoice_id):
        return [p for p in self.payments.values() if p[0] == invoice_id]

    def record_payment(self, payment_id, invoice_id, amount):
        self.payments[payment_id] = (invoice_id, amount)
