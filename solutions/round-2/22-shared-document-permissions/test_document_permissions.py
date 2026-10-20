import unittest
from models import Folder,Document
from repository import DocumentRepository
from service import PermissionService
from routes import DocumentRoutes

class PermissionTests(unittest.TestCase):
    def setUp(self):
        self.repo=DocumentRepository(); self.repo.add_folder(Folder("root")); self.repo.add_folder(Folder("child","root")); self.repo.add_document(Document("d","child","owner")); self.service=PermissionService(self.repo); self.routes=DocumentRoutes(self.service)
    def test_owner_and_direct_grants(self):
        self.assertTrue(self.service.can("d","owner","share")); self.service.grant_document("d","lee","editor")
        self.assertTrue(self.service.can("d","lee","edit")); self.assertFalse(self.service.can("d","lee","share"))
    def test_nearest_inherited_grant_and_parent_inheritance(self):
        self.service.grant_folder("root","pat","viewer"); self.service.grant_folder("child","pat","editor")
        self.assertTrue(self.service.can("d","pat","edit"))
    def test_document_revocation_overrides_direct_and_inherited_grants(self):
        self.service.grant_folder("root","sam","editor"); self.service.grant_document("d","sam","viewer"); self.service.revoke("d","sam")
        self.assertIsNone(self.service.role("d","sam")); self.assertEqual(self.routes.access("d","sam","read"),{"status":403,"allowed":False})
    def test_folder_revocation_blocks_inherited_access_only(self):
        self.service.grant_folder("root","kim","viewer"); self.repo.folders["child"].revoked.add("kim")
        self.assertIsNone(self.service.role("d","kim"))
        self.service.grant_document("d","kim","editor"); self.assertEqual(self.service.role("d","kim"),"editor")
    def test_unknown_document_and_action_are_denied(self):
        self.assertFalse(self.service.can("missing","x","read")); self.assertFalse(self.service.can("d","owner","delete"))
    def test_owner_cannot_be_removed_by_revocation(self):
        with self.assertRaises(ValueError): self.service.revoke("d","owner")

class AdditionalPermissionTests(unittest.TestCase):
    def test_editor_can_edit_but_cannot_manage_shares(self):
        repo=DocumentRepository(); repo.add_folder(Folder("f")); repo.add_document(Document("d","f","o")); svc=PermissionService(repo)
        svc.grant_document("d","e","editor")
        self.assertTrue(svc.can("d","e","edit")); self.assertFalse(svc.can("d","e","share"))
    def test_parent_inheritance_walk_terminates_on_bad_cycle(self):
        repo=DocumentRepository(); repo.add_folder(Folder("a","b")); repo.add_folder(Folder("b","a")); repo.add_document(Document("d","a","o"))
        self.assertIsNone(PermissionService(repo).role("d","nobody"))

if __name__=="__main__": unittest.main()
