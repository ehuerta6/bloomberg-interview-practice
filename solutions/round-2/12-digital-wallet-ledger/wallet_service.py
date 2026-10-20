from wallet_entry import Entry


class WalletService:
    def __init__(self, store):
        self.store = store

    def transfer(self, transaction_id, source, destination, amount):
        prior = self.store.entries_for(transaction_id)
        if prior:
            same_transfer = (len(prior) == 2 and prior[0].wallet_id == source
                             and prior[0].amount == -amount and prior[1].wallet_id == destination
                             and prior[1].amount == amount)
            return type("Result", (), {"status": "posted" if same_transfer else "conflict"})()
        if amount <= 0 or source == destination or source not in self.store.opening or destination not in self.store.opening:
            return type("Result", (), {"status": "rejected"})()
        if self.store.balance(source) < amount:
            return type("Result", (), {"status": "rejected"})()
        self.store.post_pair(Entry(transaction_id, source, -amount), Entry(transaction_id, destination, amount))
        return type("Result", (), {"status": "posted"})()
