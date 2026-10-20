from wallet_entry import Entry


class WalletService:
    def __init__(self, store):
        self.store = store

    def transfer(self, transaction_id, source, destination, amount):
        if amount <= 0 or source == destination or source not in self.store.opening or destination not in self.store.opening:
            return type("Result", (), {"status": "rejected"})()
        if self.store.balance(source) < amount:
            return type("Result", (), {"status": "rejected"})()
        self.store.post_pair(Entry(transaction_id, source, -amount), Entry(transaction_id, destination, amount))
        return type("Result", (), {"status": "posted"})()
