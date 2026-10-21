# PR #13 — LRU Cache

**Difficulty:** Medium

**PR title:** Add a bounded least-recently-used cache

## Summary

A small service cache stores up to a configured number of key/value pairs. Review how reads and writes affect the order used for eviction.

## Input and output

`LRUCache(capacity)` creates a cache. `put(key, value)` stores or updates a value, and `get(key, default=None)` returns a value or the default when the key is absent.

## Expected behavior and invariants
- Capacity is a nonnegative integer; boolean values are not valid capacities.
- A successful read and a write make the key most recently used.
- When a write exceeds capacity, evict the least recently used key.
- Updating an existing key replaces its value without creating a duplicate entry.
- A missing read returns the supplied default and does not change recency.
- Capacity zero stores no entries, and cached falsey values remain distinguishable from missing keys when a default is supplied.

## Review task

Track key order after each operation. Test a read between two writes, updating an existing key, missing reads, capacity boundaries, and falsey values. Check both returned values and which key is evicted.

## Starter Code

[View starter code](../../round-1/13-lru-cache/)

## Reference Solution

[View solution](../../solutions/round-1/13-lru-cache/)
