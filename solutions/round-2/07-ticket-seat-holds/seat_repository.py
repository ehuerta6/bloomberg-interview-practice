class SeatRepository:
    def __init__(self, seats):
        self.seats = set(seats)
        self.holds = {}

    def hold_for_seat(self, seat_id):
        return next((hold for hold in self.holds.values() if hold.seat_id == seat_id), None)

    def hold(self, hold_id):
        return self.holds.get(hold_id)

    def save_hold(self, hold):
        self.holds[hold.hold_id] = hold

    def remove(self, hold_id):
        self.holds.pop(hold_id, None)
