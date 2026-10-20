from session import Session


class SessionService:
    def __init__(self, store):
        self.store = store

    def login(self, session_id, user_id, device):
        if self.store.get(session_id):
            raise ValueError("session id already exists")
        self.store.save(Session(session_id, user_id, device))

    def logout(self, session_id, at):
        session = self.store.get(session_id)
        if session is None:
            return False
        if session.revoked_at is None:
            session.revoked_at = at
        return True

    def is_authorized(self, session_id):
        session = self.store.get(session_id)
        return session is not None
