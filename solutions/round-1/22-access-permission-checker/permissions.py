"""Resolve direct, role, and ownership access rules."""

import unittest


def has_permission(user, action, resource, acl):
    """Apply explicit user deny, direct allow, roles, then read ownership."""
    user_id = user.get("id")
    if user_id is None:
        return False
    direct = acl.get("users", {}).get(user_id, {})
    denied = direct.get("deny", {})
    if action in denied.get(resource, ()) or action in denied.get("*", ()):
        return False
    allowed = direct.get("allow", {})
    if action in allowed.get(resource, ()) or action in allowed.get("*", ()):
        return True
    for role in user.get("roles", ()):
        grants = acl.get("roles", {}).get(role, {})
        if action in grants.get(resource, ()) or action in grants.get("*", ()):
            return True
    if user_id in acl.get("owners", {}).get(resource, ()):
        return action == "read"
    return False


class PermissionTests(unittest.TestCase):
    def setUp(self):
        self.acl = {
            "roles": {"reader": {"*": ["read"]}, "editor": {"docs": ["write"]}},
            "users": {"u1": {"allow": {}, "deny": {}}},
            "owners": {"private": ["u2"]},
        }

    def test_role_grant(self):
        self.assertTrue(has_permission({"id": "u1", "roles": ["reader"]}, "read", "docs", self.acl))

    def test_resource_specific_role_grant(self):
        self.assertTrue(has_permission({"id": "u1", "roles": ["editor"]}, "write", "docs", self.acl))

    def test_role_does_not_grant_other_action(self):
        self.assertFalse(has_permission({"id": "u1", "roles": ["editor"]}, "delete", "docs", self.acl))

    def test_direct_deny_overrides_role(self):
        self.acl["users"]["u1"]["deny"] = {"docs": ["read"]}
        self.assertFalse(has_permission({"id": "u1", "roles": ["reader"]}, "read", "docs", self.acl))

    def test_direct_deny_overrides_direct_allow(self):
        self.acl["users"]["u1"] = {"allow": {"docs": ["write"]}, "deny": {"docs": ["write"]}}
        self.assertFalse(has_permission({"id": "u1", "roles": []}, "write", "docs", self.acl))

    def test_direct_allow_can_grant_without_role(self):
        self.acl["users"]["u1"]["allow"] = {"docs": ["write"]}
        self.assertTrue(has_permission({"id": "u1", "roles": []}, "write", "docs", self.acl))

    def test_owner_can_read_owned_resource(self):
        self.assertTrue(has_permission({"id": "u2", "roles": []}, "read", "private", self.acl))

    def test_owner_does_not_automatically_write(self):
        self.assertFalse(has_permission({"id": "u2", "roles": []}, "write", "private", self.acl))

    def test_unknown_user_has_no_permission(self):
        self.assertFalse(has_permission({"id": "outsider", "roles": []}, "read", "docs", self.acl))


if __name__ == "__main__":
    unittest.main()
