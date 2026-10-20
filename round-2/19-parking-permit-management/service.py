from models import Permit

class PermitService:
    def __init__(self, repo): self.repo = repo
    def issue(self, permit_id, resident_id, zone, day, duration):
        if not permit_id or not resident_id or zone not in self.repo.quotas or type(day) is not int or type(duration) is not int or duration <= 0 or self.repo.get(permit_id):
            raise ValueError("invalid permit")
        if len(self.repo.active_in_zone(zone, day)) >= self.repo.quotas[zone]: raise ValueError("zone quota reached")
        permit = Permit(permit_id, resident_id, zone, day + duration - 1)
        self.repo.save(permit); return permit
    def renew(self, permit_id, day, duration):
        permit = self.repo.get(permit_id)
        if not permit or not permit.active or type(day) is not int or type(duration) is not int or duration <= 0: raise ValueError("invalid renewal")
        if len(self.repo.active_in_zone(permit.zone, day)) > self.repo.quotas[permit.zone]: raise ValueError("zone quota reached")
        permit.expires_day = max(day, permit.expires_day + 1) + duration - 1
        return permit
    def expire(self, day):
        changed=[]
        for permit in self.repo.permits.values():
            if permit.active and permit.expires_day < day: permit.active=False; changed.append(permit.permit_id)
        return changed
