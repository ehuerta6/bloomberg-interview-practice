class TicketRoutes:
    def __init__(self, service): self.service = service
    def create(self, *args, **kwargs):
        try: return {"status": 201, "ticket": self.service.submit(*args, **kwargs)}
        except ValueError as exc: return {"status": 409, "error": str(exc)}
    def assign(self, category):
        ticket = self.service.assign_next(category)
        return {"status": 200 if ticket else 204, "ticket": ticket}
    def reassign(self, ticket_id, agent):
        try: return {"status": 200, "ticket": self.service.reassign(ticket_id, agent)}
        except ValueError as exc: return {"status": 409, "error": str(exc)}
