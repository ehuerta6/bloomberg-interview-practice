# LRU Cache — Reference Solution

## What broke

The draft inserted and evicted entries in order, but a successful read did not refresh that entry's recency. A recently used entry could therefore be evicted as if it were still the oldest.

## Reproduce the issue

Run `python3 lru_cache.py` in the starter folder. The access-then-insert sequence shows the wrong eviction. The corrected version is independently runnable with `python3 lru_cache.py` here.

## Investigation approach

Write down the recency order after each operation. Insert two entries, read the older one, then insert a third and check which key remains. Also check updates, missing reads, zero capacity, and values such as `0` or `None`.

## Correction

The solution uses `OrderedDict` to move a present key to the newest position on reads and writes. A missing read leaves the order alone; inserting beyond capacity removes the oldest key.

## Regression tests

Tests cover hit and miss behavior, read recency, update recency, eviction, zero and one capacity, invalid capacities, falsey values, and cache size. Run them with `python3 lru_cache.py`.
