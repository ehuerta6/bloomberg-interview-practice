from datetime import timedelta
from seat_models import SeatHold

class HoldService:
    def __init__(self, repository, clock, ttl=timedelta(minutes=5)):
        self.repository = repository
        self.clock = clock
        self.ttl = ttl

    def _active(self, hold):
        return hold.confirmed or hold.expires_at > self.clock()

    def hold(self, seat_id, customer_id, hold_id):
        if seat_id not in self.repository.seats or not customer_id or not hold_id:
            return False
        same_id = self.repository.hold(hold_id)
        if same_id and self._active(same_id):
            return False
        if same_id:
            self.repository.remove(hold_id)
        current = self.repository.hold_for_seat(seat_id)
        if current and self._active(current):
            return False
        if current:
            self.repository.remove(current.hold_id)
        hold = SeatHold(hold_id, seat_id, customer_id, self.clock() + self.ttl)
        self.repository.save_hold(hold)
        return True

    def confirm(self, hold_id, customer_id):
        hold = self.repository.hold(hold_id)
        if hold is None or hold.customer_id != customer_id or hold.confirmed or hold.expires_at <= self.clock():
            return False
        hold.confirmed = True
        return True
