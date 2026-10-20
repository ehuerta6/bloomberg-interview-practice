class InvoiceService:
    def __init__(self, store):
        self.store = store

    def apply_payment(self, payment_id, invoice_id, amount):
        invoice = self.store.invoice(invoice_id)
        if invoice is None or amount <= 0:
            return type("Result", (), {"status": "rejected"})()
        prior = self.store.payment(payment_id)
        if prior:
            if prior != (invoice_id, amount):
                return type("Result", (), {"status": "conflict"})()
            return type("Result", (), {"status": invoice.status if invoice.status == "paid" else "partial"})()
        if invoice.status == "paid" or invoice.paid_cents + amount > invoice.total_cents:
            return type("Result", (), {"status": "rejected"})()
        self.store.record_payment(payment_id, invoice_id, amount)
        invoice.paid_cents += amount
        invoice.status = "paid" if invoice.paid_cents == invoice.total_cents else "partial"
        return type("Result", (), {"status": invoice.status})()
