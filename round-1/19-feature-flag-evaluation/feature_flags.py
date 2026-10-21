"""Evaluate a feature flag for a user."""

import hashlib
import unittest


def evaluate_flag(flag, user):
    """Return whether a flag is active for a user."""
    if not flag.get("enabled", False):
        return False
    user_id = user.get("user_id")
    if user_id in flag.get("denylist", []):
        return False
    if user_id in flag.get("allowlist", []):
        return True
    percentage = flag.get("rollout_percent", 0)
    if percentage <= 0:
        return False
    bucket = int(hashlib.sha256(str(user_id).encode()).hexdigest()[:8], 16) % 100
    return bucket <= percentage


class FeatureFlagTests(unittest.TestCase):
    def test_disabled_flag_is_off(self):
        self.assertFalse(evaluate_flag({"enabled": False, "allowlist": ["u1"]}, {"user_id": "u1"}))

    def test_enabled_allowlisted_user_is_on(self):
        self.assertTrue(evaluate_flag({"enabled": True, "allowlist": ["u1"]}, {"user_id": "u1"}))

    def test_denylist_overrides_allowlist(self):
        flag = {"enabled": True, "allowlist": ["u1"], "denylist": ["u1"]}
        self.assertFalse(evaluate_flag(flag, {"user_id": "u1"}))

    def test_zero_percent_is_off(self):
        self.assertFalse(evaluate_flag({"enabled": True, "rollout_percent": 0}, {"user_id": "u1"}))

    def test_one_hundred_percent_is_on(self):
        self.assertTrue(evaluate_flag({"enabled": True, "rollout_percent": 100}, {"user_id": "u1"}))

    def test_rollout_bucket_uses_strict_percentage_boundary(self):
        user = {"user_id": "customer-42"}
        bucket = int(hashlib.sha256(b"customer-42").hexdigest()[:8], 16) % 100
        self.assertTrue(evaluate_flag({"enabled": True, "rollout_percent": bucket + 1}, user))
        self.assertFalse(evaluate_flag({"enabled": True, "rollout_percent": bucket}, user))

    def test_rollout_is_independent_of_dict_insertion_order(self):
        a = {"enabled": True, "rollout_percent": 40}
        b = {"rollout_percent": 40, "enabled": True}
        user = {"user_id": "stable"}
        self.assertEqual(evaluate_flag(a, user), evaluate_flag(b, user))

    def test_missing_user_does_not_get_rollout(self):
        self.assertFalse(evaluate_flag({"enabled": True, "rollout_percent": 100}, {}))

    def test_invalid_percentage_is_not_hidden_by_allowlist(self):
        flag = {"enabled": True, "allowlist": ["u"], "rollout_percent": "50"}
        with self.assertRaises(ValueError):
            evaluate_flag(flag, {"user_id": "u"})


if __name__ == "__main__":
    unittest.main()
