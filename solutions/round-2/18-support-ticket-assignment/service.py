from models import Ticket

class TicketService:
    def __init__(self, repository):
        self.repo = repository

    def submit(self, ticket_id, customer, category, priority=3):
        if not isinstance(ticket_id, str) or not ticket_id or not customer or category not in self.repo.agents:
            raise ValueError("invalid ticket")
        if type(priority) is not int or priority not in range(1, 6) or self.repo.get(ticket_id):
            raise ValueError("invalid priority or duplicate ticket")
        ticket = Ticket(ticket_id, customer, category, priority)
        self.repo.save(ticket)
        return ticket

    def assign_next(self, category):
        candidates = [t for t in self.repo.tickets.values() if t.category == category and t.status == "open"]
        if not candidates:
            return None
        ticket = max(candidates, key=lambda t: t.priority)
        agent = min(self.repo.agents[category], key=lambda name: self.repo.loads[name])
        ticket.assignee, ticket.status = agent, "assigned"
        self.repo.loads[agent] += 1
        return ticket

    def reassign(self, ticket_id, new_agent):
        ticket = self.repo.get(ticket_id)
        if not ticket or ticket.status != "assigned" or new_agent not in self.repo.agents[ticket.category]:
            raise ValueError("ticket cannot be reassigned")
        self.repo.loads[ticket.assignee] -= 1
        ticket.assignee = new_agent
        self.repo.loads[new_agent] += 1
        return ticket
