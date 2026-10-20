"""Move integer-cent balances between accounts atomically."""

from collections.abc import MutableMapping
import unittest


def _valid_cents(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def transfer(accounts, source, destination, amount_cents):
    """Transfer funds in place; return False without mutation if funds are short.

    Invalid account data or a nonpositive/non-integer amount raises
    ``ValueError``. All validation and the sufficient-funds check happen before
    either account is changed.
    """
    if not isinstance(accounts, MutableMapping):
        raise ValueError("accounts must be a mutable mapping")
    if any(not isinstance(account_id, str) or not account_id.strip() for account_id in accounts):
        raise ValueError("account IDs must be nonblank strings")
    if not isinstance(source, str) or not source.strip() or not isinstance(destination, str) or not destination.strip():
        raise ValueError("source and destination IDs must be nonblank strings")
    if source not in accounts or destination not in accounts or source == destination:
        raise ValueError("source and destination must be different known accounts")
    if isinstance(amount_cents, bool) or not isinstance(amount_cents, int) or amount_cents <= 0:
        raise ValueError("amount_cents must be a positive integer")
    if any(not _valid_cents(balance) for balance in accounts.values()):
        raise ValueError("account balances must be nonnegative integer cents")
    if accounts[source] < amount_cents:
        return False

    accounts[source] -= amount_cents
    accounts[destination] += amount_cents
    return True


class BalanceTransferTests(unittest.TestCase):
    def test_successful_transfer_moves_cents(self):
        accounts = {"a": 1000, "b": 200}
        self.assertTrue(transfer(accounts, "a", "b", 250))
        self.assertEqual(accounts, {"a": 750, "b": 450})

    def test_zero_balance_can_transfer_exact_balance(self):
        accounts = {"a": 300, "b": 0}
        self.assertTrue(transfer(accounts, "a", "b", 300))
        self.assertEqual(accounts, {"a": 0, "b": 300})

    def test_insufficient_funds_returns_false_without_mutation(self):
        accounts = {"a": 50, "b": 100}
        before = accounts.copy()
        self.assertFalse(transfer(accounts, "a", "b", 80))
        self.assertEqual(accounts, before)

    def test_unknown_account_is_rejected_atomically(self):
        accounts = {"a": 100}
        with self.assertRaises(ValueError):
            transfer(accounts, "a", "missing", 10)
        self.assertEqual(accounts, {"a": 100})

    def test_same_account_is_rejected_without_mutation(self):
        accounts = {"a": 100}
        with self.assertRaises(ValueError):
            transfer(accounts, "a", "a", 10)
        self.assertEqual(accounts, {"a": 100})

    def test_amount_must_be_positive_integer_cents(self):
        for amount in (0, -1, 1.5, True):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                transfer({"a": 100, "b": 0}, "a", "b", amount)

    def test_invalid_existing_balances_are_rejected_before_mutation(self):
        accounts = {"a": -1, "b": 0}
        with self.assertRaises(ValueError):
            transfer(accounts, "a", "b", 1)
        self.assertEqual(accounts, {"a": -1, "b": 0})

    def test_invalid_account_mapping_is_rejected(self):
        with self.assertRaises(ValueError):
            transfer([("a", 100), ("b", 0)], "a", "b", 1)

    def test_invalid_account_ids_are_rejected(self):
        for accounts, source, destination in (({"": 100, "b": 0}, "", "b"), ({"a": 100, "b": 0}, [], "b")):
            with self.subTest(accounts=accounts, source=source), self.assertRaises(ValueError):
                transfer(accounts, source, destination, 1)

    def test_total_balance_is_conserved(self):
        accounts = {"a": 75, "b": 25, "c": 200}
        before_total = sum(accounts.values())
        transfer(accounts, "c", "a", 125)
        self.assertEqual(sum(accounts.values()), before_total)


if __name__ == "__main__":
    unittest.main()
