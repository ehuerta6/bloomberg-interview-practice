class RefundService:
    def __init__(self, repository):
        self.repository = repository

    def refund(self, payment_id, refund_id, amount):
        payment = self.repository.payment(payment_id)
        if not payment or not refund_id or not isinstance(amount, int) or amount <= 0:
            return "rejected"
        prior = self.repository.refund(refund_id)
        if prior:
            if prior["payment_id"] == payment_id and prior["amount"] == amount:
                return "already_refunded"
            return "rejected"
        if self.repository.refunded_total(payment_id) + amount > payment.amount:
            return "rejected"
        self.repository.record_refund(refund_id, payment_id, amount)
        return "refunded"
