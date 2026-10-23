# PR #13 — LRU Cache

**Difficulty:** Medium

**PR title:** Add a bounded least-recently-used cache

## Summary

A service reuses recently requested key/value pairs to avoid repeated work, but it can retain only a fixed number. The least recently used (LRU) entry is the one that must leave when a new write exceeds that capacity. You are reviewing the cache PR, including how an existing value is used or replaced.

## Input and output

`LRUCache(capacity)` creates a cache. `put(key, value)` stores or updates a value, and `get(key, default=None)` returns a value or the default when the key is absent.

## Expected behavior and invariants
- Capacity is a nonnegative integer; boolean values are not valid capacities.
- A successful read and a write make the key most recently used.
- When a write exceeds capacity, evict the least recently used key.
- Updating an existing key replaces its value without creating a duplicate entry.
- A missing read returns the supplied default and does not change recency.
- Capacity zero stores no entries, and cached falsey values remain distinguishable from missing keys when a default is supplied.

## Contract example

Start with `cache = LRUCache(2)` and perform these operations in order:

| Operation | Required observation |
| --- | --- |
| `cache.put("a", 1)` | `a` is stored |
| `cache.put("b", 2)` | `a` and `b` are stored |
| `cache.get("a")` | Returns `1` |
| `cache.put("c", 3)` | `b` is evicted; `a` and `c` remain |
| `cache.get("b", -1)` | Returns `-1` |

A separate `LRUCache(0)` stores no value after a `put`. Storing `0` in a cache with room must return `0` on a later read, even when that read supplies another default.

## Review task

Review the cache and tests against the meaning of a successful use, a replacement, and a miss. Correct discrepancies and add sequences that verify both returned values and the eventual eviction after reads or updates. Include capacity zero and cached values that Python treats as false, such as `0`, so a hit cannot be confused with a missing key.

## Starter Code

[View starter code](../../round-1/13-lru-cache/)

## Reference Solution

[View solution](../../solutions/round-1/13-lru-cache/)
