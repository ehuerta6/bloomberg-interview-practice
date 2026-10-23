# PR #18 — Dependency Resolution

**Difficulty:** Hard

**PR title:** Resolve package dependencies into installation order

## Summary

A package installer needs a repeatable installation plan from a set of prerequisites. A package may be installed only after every package it depends on, and an invalid or cyclic graph must stop planning rather than produce an incomplete plan. You are reviewing the dependency-resolution PR. Lexicographic order here means ordinary string ordering among the package names that are ready at a given step.

## Input and output

`resolve_dependencies(graph)` accepts a mapping from nonblank package names to collections of dependencies. Every dependency must also be defined as a package key. It returns a list of package names in installation order.

## Expected behavior and invariants
- Every dependency appears before its dependent, and every package appears exactly once.
- Repeated dependency edges do not add duplicate package entries.
- At each step, choose the lexicographically smallest package among those whose dependencies have all been emitted.
- Reject blank or non-string package names, invalid dependency collections or names, and references to undefined packages with `ValueError`.
- If the graph contains a cycle, raise `ValueError` instead of returning a partial order.
- An empty graph returns an empty list.

## Contract examples

For this graph:

```python
{"root": ["z", "a"], "z": [], "a": [], "mid": ["a"]}
```

The expected installation list is `["a", "mid", "z", "root"]`. After `a` is included, `mid` becomes eligible and precedes `z` under the specified tie rule.

`{"app": ["core", "core"], "core": []}` returns `["core", "app"]`. The cycle `{"a": ["b"], "b": ["a"]}` raises `ValueError`, and so does `{"app": ["missing"]}` because `missing` has no package definition.

## Review task

Review the resolver and assertions against prerequisite order, one occurrence per package, and deterministic selection when several packages are ready. Correct discrepancies and add cases for a shared prerequisite, repeated edges, missing definitions, and cycles. Explain how tests distinguish a valid complete plan from a partial or invalid result.

## Starter Code

[View starter code](../../round-1/18-dependency-resolution/)

## Reference Solution

[View solution](../../solutions/round-1/18-dependency-resolution/)
