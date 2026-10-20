class PermitRepository:
    def __init__(self, quotas):
        self.quotas = dict(quotas)
        self.permits = {}
    def get(self, permit_id): return self.permits.get(permit_id)
    def save(self, permit): self.permits[permit.permit_id] = permit
    def active_in_zone(self, zone, day):
        return [p for p in self.permits.values() if p.zone == zone and p.active and p.expires_day >= day]
