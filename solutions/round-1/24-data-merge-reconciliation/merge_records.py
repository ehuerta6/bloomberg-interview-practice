"""Reconcile customer records by timestamp and union their tags."""

import unittest


def merge_records(existing, incoming):
    """Return records in stable order, retaining every source's tags."""
    merged = {}
    order = []
    for record in existing:
        customer_id = record["customer_id"]
        if customer_id in merged:
            raise ValueError("duplicate customer in existing records")
        merged[customer_id] = {**record, "tags": list(record.get("tags", []))}
        order.append(customer_id)
    for update in incoming:
        customer_id = update["customer_id"]
        if customer_id not in merged:
            merged[customer_id] = {**update, "tags": list(update.get("tags", []))}
            order.append(customer_id)
            continue
        current = merged[customer_id]
        old_tags = list(current.get("tags", []))
        new_tags = list(update.get("tags", []))
        if update["updated_at"] >= current["updated_at"]:
            merged[customer_id] = {**current, **update}
        merged[customer_id]["tags"] = list(dict.fromkeys(old_tags + new_tags))
    return [merged[customer_id] for customer_id in order]


class MergeTests(unittest.TestCase):
    def test_newer_snapshot_replaces_fields(self):
        rows = merge_records([{"customer_id": "c1", "name": "Old", "updated_at": "2025-01-01T00:00:00"}], [{"customer_id": "c1", "name": "New", "updated_at": "2025-01-02T00:00:00"}])
        self.assertEqual(rows[0]["name"], "New")

    def test_older_snapshot_is_ignored(self):
        rows = merge_records([{"customer_id": "c1", "name": "New", "updated_at": "2025-01-02T00:00:00"}], [{"customer_id": "c1", "name": "Old", "updated_at": "2025-01-01T00:00:00"}])
        self.assertEqual(rows[0]["name"], "New")

    def test_equal_timestamp_prefers_incoming_snapshot(self):
        rows = merge_records([{"customer_id": "c1", "name": "Old", "updated_at": "2025-01-01T00:00:00"}], [{"customer_id": "c1", "name": "New", "updated_at": "2025-01-01T00:00:00"}])
        self.assertEqual(rows[0]["name"], "New")

    def test_new_customers_append_in_incoming_order(self):
        rows = merge_records([], [{"customer_id": "c2", "updated_at": "2025-01-01"}, {"customer_id": "c1", "updated_at": "2025-01-01"}])
        self.assertEqual([r["customer_id"] for r in rows], ["c2", "c1"])

    def test_existing_order_is_preserved(self):
        rows = merge_records([{"customer_id": "b", "updated_at": "2025-01-01"}, {"customer_id": "a", "updated_at": "2025-01-01"}], [])
        self.assertEqual([r["customer_id"] for r in rows], ["b", "a"])

    def test_tags_are_union_of_both_sources(self):
        rows = merge_records([{"customer_id": "c1", "updated_at": "2025-01-01", "tags": ["vip", "beta"]}], [{"customer_id": "c1", "updated_at": "2025-01-02", "tags": ["beta", "priority"]}])
        self.assertEqual(rows[0]["tags"], ["vip", "beta", "priority"])

    def test_inputs_are_not_mutated(self):
        old = [{"customer_id": "c1", "updated_at": "2025-01-01", "tags": ["a"]}]
        new = [{"customer_id": "c1", "updated_at": "2025-01-02", "tags": ["b"]}]
        before = ({**old[0], "tags": old[0]["tags"].copy()}, {**new[0], "tags": new[0]["tags"].copy()})
        merge_records(old, new)
        self.assertEqual((old[0], new[0]), before)

    def test_result_records_do_not_share_tag_lists_with_inputs(self):
        old = [{"customer_id": "c1", "updated_at": "2025-01-01", "tags": ["a"]}]
        result = merge_records(old, [])
        result[0]["tags"].append("later")
        self.assertEqual(old[0]["tags"], ["a"])


if __name__ == "__main__":
    unittest.main()
