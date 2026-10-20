from wallet_entry import Entry


class WalletStore:
    def __init__(self):
        self.opening = {}
        self.entries = []

    def open_wallet(self, wallet_id, opening_cents):
        self.opening[wallet_id] = opening_cents

    def balance(self, wallet_id):
        return self.opening[wallet_id] + sum(e.amount for e in self.entries if e.wallet_id == wallet_id)

    def entries_for(self, transaction_id):
        return [e for e in self.entries if e.transaction_id == transaction_id]

    def post_pair(self, debit, credit):
        self.entries.extend((debit, credit))
