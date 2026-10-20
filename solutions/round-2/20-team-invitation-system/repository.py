class InvitationRepository:
    def __init__(self): self.invitations={}; self.members={}
    def get(self, invite_id): return self.invitations.get(invite_id)
    def for_email(self,email): return [i for i in self.invitations.values() if i.email==email]
    def save(self, invitation): self.invitations[invitation.invite_id]=invitation
