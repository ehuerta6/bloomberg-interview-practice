from moderation_records import AuditEvent


class ModerationService:
    def __init__(self, store):
        self.store = store

    def review(self, post_id, reviewer, decision, note):
        post = self.store.post(post_id)
        if post is None or decision not in ("approve", "reject"):
            return type("Result", (), {"status": "invalid"})()
        if post.status != "pending":
            return type("Result", (), {"status": "conflict"})()
        post.status = "published" if decision == "approve" else "rejected"
        self.store.audit.append(AuditEvent(post_id, reviewer, decision, note))
        return type("Result", (), {"status": post.status})()
