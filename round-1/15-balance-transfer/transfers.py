"""Move integer-cent balances between accounts."""

import unittest


def transfer(accounts, source, destination, amount_cents):
    """Transfer funds and return True when it succeeds."""
    if source not in accounts or destination not in accounts or source == destination:
        raise ValueError("source and destination must be different known accounts")
    accounts[source] -= amount_cents
    if accounts[source] < 0:
        return False
    accounts[destination] += amount_cents
    return True


class BalanceTransferTests(unittest.TestCase):
    def test_successful_transfer_moves_cents(self):
        accounts = {"a": 1000, "b": 200}
        self.assertTrue(transfer(accounts, "a", "b", 250))
        self.assertEqual(accounts, {"a": 750, "b": 450})

    def test_zero_balance_can_transfer_exact_balance(self):
        accounts = {"a": 300, "b": 0}
        transfer(accounts, "a", "b", 300)
        self.assertEqual(accounts, {"a": 0, "b": 300})

    def test_insufficient_funds_fails_without_mutation(self):
        accounts = {"a": 50, "b": 100}
        before = accounts.copy()
        self.assertFalse(transfer(accounts, "a", "b", 80))
        self.assertEqual(accounts, before)

    def test_unknown_account_is_rejected_atomically(self):
        accounts = {"a": 100}
        with self.assertRaises(ValueError):
            transfer(accounts, "a", "missing", 10)
        self.assertEqual(accounts, {"a": 100})

    def test_same_account_is_rejected(self):
        with self.assertRaises(ValueError):
            transfer({"a": 100}, "a", "a", 10)

    def test_amount_must_be_positive_integer_cents(self):
        for amount in (0, -1, 1.5, True):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                transfer({"a": 100, "b": 0}, "a", "b", amount)

    def test_invalid_existing_balances_are_rejected(self):
        with self.assertRaises(ValueError):
            transfer({"a": -1, "b": 0}, "a", "b", 1)

    def test_unhashable_account_id_is_rejected(self):
        with self.assertRaises(ValueError):
            transfer({"a": 100, "b": 0}, [], "b", 1)

    def test_destination_is_credited_only_after_funds_are_available(self):
        accounts = {"a": 10, "b": 5}
        self.assertFalse(transfer(accounts, "a", "b", 11))
        self.assertEqual(accounts, {"a": 10, "b": 5})


if __name__ == "__main__":
    unittest.main()
