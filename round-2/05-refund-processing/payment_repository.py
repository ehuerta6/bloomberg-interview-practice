from payment_models import Payment

class PaymentRepository:
    def __init__(self):
        self.payments = {}
        self.refunds = {}

    def add_payment(self, payment_id, amount, state):
        self.payments[payment_id] = Payment(payment_id, amount, state)

    def payment(self, payment_id):
        return self.payments.get(payment_id)

    def payment_state(self, payment_id):
        payment = self.payment(payment_id)
        return payment.state if payment else None

    def refunds_for(self, payment_id):
        return [row for row in self.refunds.values() if row["payment_id"] == payment_id]

    def refunded_total(self, payment_id):
        return sum(row["amount"] for row in self.refunds_for(payment_id))

    def refund(self, refund_id):
        return self.refunds.get(refund_id)

    def record_refund(self, refund_id, payment_id, amount):
        self.refunds[refund_id] = {"payment_id": payment_id, "amount": amount}
        payment = self.payment(payment_id)
        payment.state = "refunded" if self.refunded_total(payment_id) == payment.amount else "partially_refunded"
