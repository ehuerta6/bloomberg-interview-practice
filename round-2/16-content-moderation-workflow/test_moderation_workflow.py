import unittest

from moderation_service import ModerationService
from moderation_store import ModerationStore


class ModerationWorkflowTests(unittest.TestCase):
    def build(self):
        store = ModerationStore()
        store.submit("post-1", "author-1", "A new discussion")
        return store, ModerationService(store)

    def test_reviewer_approval_records_audit_and_publishes(self):
        store, service = self.build()
        result = service.review("post-1", "reviewer-1", "approve", "safe")
        self.assertEqual(result.status, "published")
        self.assertEqual(store.post("post-1").status, "published")
        self.assertEqual(store.audit_for("post-1")[0].actor, "reviewer-1")

    def test_author_cannot_review_own_post(self):
        store, service = self.build()
        result = service.review("post-1", "author-1", "approve", "self review")
        self.assertEqual(result.status, "forbidden")
        self.assertEqual(store.post("post-1").status, "pending")
        self.assertEqual(store.audit_for("post-1"), [])

    def test_already_reviewed_post_cannot_be_decided_again(self):
        store, service = self.build()
        service.review("post-1", "reviewer-1", "reject", "policy")
        second = service.review("post-1", "reviewer-2", "approve", "changed mind")
        self.assertEqual(second.status, "conflict")
        self.assertEqual(store.post("post-1").status, "rejected")
        self.assertEqual(len(store.audit_for("post-1")), 1)


    def test_rejection_records_actor_and_note(self):
        store, service = self.build()
        self.assertEqual(service.review("post-1", "reviewer-2", "reject", "spam").status, "rejected")
        event = store.audit_for("post-1")[0]
        self.assertEqual((event.actor, event.decision, event.note), ("reviewer-2", "reject", "spam"))


    def test_invalid_decision_does_not_change_post_or_audit(self):
        store, service = self.build()
        self.assertEqual(service.review("post-1", "reviewer-1", "hide", "reason").status, "invalid")
        self.assertEqual(store.post("post-1").status, "pending")
        self.assertEqual(store.audit_for("post-1"), [])


    def test_missing_post_does_not_create_audit_event(self):
        store, service = self.build()
        self.assertEqual(service.review("missing", "reviewer-1", "approve", "safe").status, "invalid")
        self.assertEqual(store.audit, [])

if __name__ == "__main__":
    unittest.main()
