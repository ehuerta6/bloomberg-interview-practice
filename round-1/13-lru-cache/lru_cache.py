"""A small least-recently-used cache."""

from collections import OrderedDict
import unittest


class LRUCache:
    def __init__(self, capacity):
        if not isinstance(capacity, int) or capacity < 0:
            raise ValueError("capacity must be a nonnegative integer")
        self.capacity = capacity
        self._items = OrderedDict()

    def get(self, key, default=None):
        """Return a cached value or the supplied default."""
        return self._items.get(key, default)

    def put(self, key, value):
        """Insert or replace a value, evicting the least-recently-used item."""
        if self.capacity == 0:
            return
        self._items[key] = value
        self._items.move_to_end(key)
        if len(self._items) > self.capacity:
            self._items.popitem(last=False)


class LRUCacheTests(unittest.TestCase):
    def test_missing_key_returns_default(self):
        self.assertEqual(LRUCache(2).get("missing", -1), -1)

    def test_put_and_get(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        self.assertEqual(cache.get("a"), 1)

    def test_oldest_entry_is_evicted_after_capacity_is_exceeded(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        self.assertIsNone(cache.get("a"))
        self.assertEqual(cache.get("b"), 2)

    def test_successful_get_makes_entry_most_recent(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")
        cache.put("c", 3)
        self.assertEqual(cache.get("a"), 1)
        self.assertIsNone(cache.get("b"))

    def test_updating_key_replaces_value(self):
        cache = LRUCache(1)
        cache.put("a", 1)
        cache.put("a", 2)
        self.assertEqual(cache.get("a"), 2)

    def test_capacity_zero_stores_nothing(self):
        cache = LRUCache(0)
        cache.put("a", 1)
        self.assertIsNone(cache.get("a"))

    def test_invalid_capacity_is_rejected(self):
        with self.assertRaises(ValueError):
            LRUCache(-1)

    def test_falsey_values_are_still_cached(self):
        cache = LRUCache(2)
        cache.put("zero", 0)
        self.assertEqual(cache.get("zero"), 0)


if __name__ == "__main__":
    unittest.main()
