class ResetRepository:
    def __init__(self):
        self.tokens = {}
        self.passwords = {}

    def add_token(self, token):
        self.tokens[token.token_id] = token

    def token(self, token_id):
        return self.tokens.get(token_id)

    def invalidate_for_user(self, user_id):
        for token in self.tokens.values():
            if token.user_id == user_id and not token.used:
                token.invalidated = True

    def set_password(self, user_id, password_hash):
        self.passwords[user_id] = password_hash

    def password_hash(self, user_id):
        return self.passwords.get(user_id)
