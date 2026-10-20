from models import Invitation

class InvitationService:
    ROLES={"viewer","editor","admin"}
    def __init__(self,repo): self.repo=repo
    def invite(self,invite_id,email,role,now,ttl):
        if not invite_id or "@" not in email or role not in self.ROLES or type(now) is not int or type(ttl) is not int or ttl<=0 or self.repo.get(invite_id): raise ValueError("invalid invitation")
        if email in self.repo.members: raise ValueError("already a member")
        if any(i.email==email and i.status=="pending" and i.expires_at>=now for i in self.repo.invitations.values()): raise ValueError("pending invite exists")
        invite=Invitation(invite_id,email,role,now+ttl); self.repo.save(invite); return invite
    def accept(self,invite_id,now):
        invite=self.repo.get(invite_id)
        if not invite or invite.status!="pending": raise ValueError("invitation unavailable")
        if invite.expires_at<now:
            invite.status="expired"
            raise ValueError("invitation unavailable")
        invite.status="accepted"; self.repo.members[invite.email]=invite.role; return invite
    def cancel(self,invite_id):
        invite=self.repo.get(invite_id)
        if not invite or invite.status!="pending": raise ValueError("invitation unavailable")
        invite.status="cancelled"; return invite
    def expire(self,now):
        changed=[]
        for invite in self.repo.invitations.values():
            if invite.status=="pending" and invite.expires_at<now:
                invite.status="expired"
                changed.append(invite.invite_id)
        return changed
