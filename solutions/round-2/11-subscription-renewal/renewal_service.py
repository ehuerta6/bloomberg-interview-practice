import calendar
from datetime import date


class RenewalService:
    def __init__(self, store, gateway):
        self.store, self.gateway = store, gateway

    def renew(self, sub_id, invoice_id, today):
        subscription = self.store.get(sub_id)
        if subscription is None:
            return type("Result", (), {"status": "missing"})()
        prior = self.store.invoice_status(invoice_id)
        if prior:
            return type("Result", (), {"status": prior})()
        if subscription.status not in ("active", "past_due") or today < subscription.next_due:
            return type("Result", (), {"status": "not_due"})()
        if not self.gateway.charge(invoice_id, subscription.monthly_cents):
            subscription.status = "past_due"
            self.store.save_invoice(invoice_id, "declined")
            return type("Result", (), {"status": "declined"})()
        due = date.fromisoformat(subscription.next_due)
        month = due.month % 12 + 1
        year = due.year + (due.month == 12)
        day = min(due.day, calendar.monthrange(year, month)[1])
        subscription.next_due = date(year, month, day).isoformat()
        subscription.status = "active"
        self.store.save_invoice(invoice_id, "paid")
        return type("Result", (), {"status": "paid"})()
