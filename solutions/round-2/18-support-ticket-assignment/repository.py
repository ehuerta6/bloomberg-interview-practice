class TicketRepository:
    def __init__(self):
        self.tickets = {}
        self.agents = {"billing": ["Ava", "Ben"], "technical": ["Cal", "Dee"]}
        self.loads = {name: 0 for names in self.agents.values() for name in names}

    def save(self, ticket):
        self.tickets[ticket.ticket_id] = ticket

    def get(self, ticket_id):
        return self.tickets.get(ticket_id)
