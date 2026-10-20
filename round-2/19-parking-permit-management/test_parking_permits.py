import unittest
from repository import PermitRepository
from service import PermitService
from routes import PermitRoutes

class PermitTests(unittest.TestCase):
    def setUp(self):
        self.repo=PermitRepository({"north":2}); self.service=PermitService(self.repo); self.routes=PermitRoutes(self.service)
    def issue(self, ident, day=1, duration=3): return self.routes.issue(ident,"r-"+ident,"north",day,duration)
    def test_quota_counts_only_unexpired_active_permits(self):
        self.issue("a"); self.issue("b")
        self.assertEqual(self.issue("c")["status"],409)
        self.assertEqual(self.issue("c", day=4)["status"],201)
    def test_expiration_is_exclusive_and_idempotent(self):
        self.issue("a",day=1,duration=2)
        self.assertEqual(self.service.expire(2),[])
        self.assertEqual(self.service.expire(3),["a"])
        self.assertEqual(self.service.expire(4),[])
    def test_renewal_extends_from_later_of_today_or_current_expiry(self):
        permit=self.issue("a",day=1,duration=3)["permit"]
        self.assertEqual(self.routes.renew("a",2,2)["permit"].expires_day,5)
        self.assertEqual(self.routes.renew("a",4,2)["permit"].expires_day,7)
    def test_invalid_issue_does_not_consume_quota(self):
        self.assertEqual(self.routes.issue("bad","r","north",1,0)["status"],409)
        self.assertEqual(self.issue("ok")["status"],201)
    def test_expired_permit_cannot_be_renewed(self):
        self.issue("a",1,1)
        self.assertEqual(self.routes.renew("a",2,5)["status"],409)

class AdditionalPermitTests(unittest.TestCase):
    def test_revoke_frees_quota_immediately(self):
        repo=PermitRepository({"n":1}); service=PermitService(repo)
        permit=service.issue("a","r1","n",1,5); permit.active=False
        self.assertEqual(service.issue("b","r2","n",2,2).permit_id,"b")
    def test_invalid_duration_never_changes_existing_expiry(self):
        repo=PermitRepository({"n":1}); service=PermitService(repo); p=service.issue("a","r","n",1,4)
        with self.assertRaises(ValueError): service.renew("a",2,0)
        self.assertEqual(p.expires_day,4)


if __name__=="__main__": unittest.main()
