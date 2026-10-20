from datetime import timedelta
from reset_models import ResetToken

class ResetService:
    def __init__(self, repository, clock, ttl=timedelta(minutes=20)):
        self.repository = repository
        self.clock = clock
        self.ttl = ttl

    def issue(self, user_id, token_id):
        if not user_id or not token_id or self.repository.token(token_id):
            return None
        token = ResetToken(token_id, user_id, self.clock() + self.ttl)
        self.repository.add_token(token)
        return token

    def reset(self, token_id, password_hash):
        token = self.repository.token(token_id)
        now = self.clock()
        if (token is None or token.used or token.invalidated or
                token.expires_at <= now or not password_hash):
            return False
        token.used = True
        self.repository.set_password(token.user_id, password_hash)
        return True
