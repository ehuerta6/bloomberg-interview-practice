import unittest

from wallet_service import WalletService
from wallet_store import WalletStore


class WalletLedgerTests(unittest.TestCase):
    def build(self):
        store = WalletStore()
        store.open_wallet("w-1", 5000)
        store.open_wallet("w-2", 1000)
        return store, WalletService(store)

    def test_transfer_writes_balanced_entries_and_moves_money(self):
        store, service = self.build()
        transfer = service.transfer("tx-1", "w-1", "w-2", 1250)
        self.assertEqual(transfer.status, "posted")
        self.assertEqual(store.balance("w-1"), 3750)
        self.assertEqual(store.balance("w-2"), 2250)
        entries = store.entries_for("tx-1")
        self.assertEqual(sum(entry.amount for entry in entries), 0)
        self.assertEqual(len(entries), 2)

    def test_replaying_transfer_does_not_duplicate_ledger_entries(self):
        store, service = self.build()
        service.transfer("tx-2", "w-1", "w-2", 300)
        service.transfer("tx-2", "w-1", "w-2", 300)
        self.assertEqual(store.balance("w-1"), 4700)
        self.assertEqual(len(store.entries_for("tx-2")), 2)

    def test_insufficient_funds_leave_both_wallets_and_ledger_unchanged(self):
        store, service = self.build()
        result = service.transfer("tx-3", "w-1", "w-2", 6000)
        self.assertEqual(result.status, "rejected")
        self.assertEqual(store.balance("w-1"), 5000)
        self.assertEqual(store.entries_for("tx-3"), [])


    def test_same_wallet_transfer_is_rejected_without_entries(self):
        store, service = self.build()
        self.assertEqual(service.transfer("tx-self", "w-1", "w-1", 100).status, "rejected")
        self.assertEqual(store.balance("w-1"), 5000)
        self.assertEqual(store.entries_for("tx-self"), [])


    def test_invalid_amount_is_rejected_without_entries(self):
        store, service = self.build()
        for amount in (0, -1):
            self.assertEqual(service.transfer("tx-invalid", "w-1", "w-2", amount).status, "rejected")
        self.assertEqual(store.balance("w-1"), 5000)
        self.assertEqual(store.entries, [])


    def test_transaction_id_cannot_be_reused_for_different_transfer(self):
        store, service = self.build()
        service.transfer("tx-4", "w-1", "w-2", 100)
        self.assertEqual(service.transfer("tx-4", "w-1", "w-2", 200).status, "conflict")
        self.assertEqual(store.balance("w-1"), 4900)
        self.assertEqual(len(store.entries_for("tx-4")), 2)

if __name__ == "__main__":
    unittest.main()
