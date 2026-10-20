class ModerationStore:
    def __init__(self):
        self.posts = {}
        self.audit = []

    def submit(self, post_id, author, content):
        from moderation_records import Post
        self.posts[post_id] = Post(post_id, author, content)

    def post(self, post_id):
        return self.posts.get(post_id)

    def audit_for(self, post_id):
        return [event for event in self.audit if event.post_id == post_id]
