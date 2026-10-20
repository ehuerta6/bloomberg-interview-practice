import unittest
from repository import InvitationRepository
from service import InvitationService
from routes import InvitationRoutes

class InvitationTests(unittest.TestCase):
    def setUp(self): self.repo=InvitationRepository(); self.service=InvitationService(self.repo); self.routes=InvitationRoutes(self.service)
    def invite(self,ident="i1",email="new@example.com",role="viewer",now=10,ttl=5): return self.routes.invite(ident,email,role,now,ttl)
    def test_role_is_granted_only_after_acceptance(self):
        self.invite(role="editor"); self.assertNotIn("new@example.com",self.repo.members)
        self.routes.accept("i1",11); self.assertEqual(self.repo.members["new@example.com"],"editor")
    def test_invitation_expires_after_inclusive_deadline(self):
        self.invite(); self.assertEqual(self.routes.accept("i1",15)["status"],200)
        self.invite("i2","late@example.com",now=10,ttl=2)
        self.assertEqual(self.routes.accept("i2",13)["status"],409)
        self.assertEqual(self.repo.get("i2").status,"expired")
    def test_active_pending_invite_prevents_duplicate_but_expired_does_not(self):
        self.invite(); self.assertEqual(self.invite("i2")["status"],409)
        self.service.expire(16)
        self.assertEqual(self.invite("i3")["status"],201)
    def test_cancelled_invite_cannot_be_accepted_or_cancelled_twice(self):
        self.invite(); self.service.cancel("i1")
        self.assertEqual(self.routes.accept("i1",11)["status"],409)
        with self.assertRaises(ValueError): self.service.cancel("i1")
    def test_invalid_role_and_duplicate_member_are_rejected(self):
        self.assertEqual(self.invite(role="owner")["status"],409)
        self.invite(); self.routes.accept("i1",11)
        self.assertEqual(self.invite("i2")["status"],409)

class AdditionalInvitationTests(unittest.TestCase):
    def test_cancelled_address_can_receive_new_invite(self):
        repo=InvitationRepository(); service=InvitationService(repo)
        service.invite("a","x@y.test","viewer",1,3); service.cancel("a")
        self.assertEqual(service.invite("b","x@y.test","admin",2,3).role,"admin")
    def test_expiry_sweep_returns_only_newly_expired_ids(self):
        repo=InvitationRepository(); service=InvitationService(repo); service.invite("a","x@y.test","viewer",1,1)
        self.assertEqual(service.expire(3),["a"]); self.assertEqual(service.expire(3),[])

if __name__=="__main__": unittest.main()
