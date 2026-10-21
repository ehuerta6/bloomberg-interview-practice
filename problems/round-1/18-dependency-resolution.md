# PR #18 — Dependency Resolution

**Difficulty:** Hard

**PR title:** Resolve package dependencies into installation order

## Summary

A package installer receives a graph of prerequisites and needs a deterministic sequence that places every dependency before the package that uses it. Review ordering, graph validation, and cycle handling.

## Input and output

`resolve_dependencies(graph)` accepts a mapping from nonblank package names to collections of dependencies. Every dependency must also be defined as a package key. It returns a list of package names in installation order.

## Expected behavior and invariants
- Every dependency appears before its dependent, and every package appears exactly once.
- Repeated dependency edges do not add duplicate package entries.
- At each step, choose the lexicographically smallest package among those whose dependencies have all been emitted.
- Reject blank or non-string package names, invalid dependency collections or names, and references to undefined packages with `ValueError`.
- If the graph contains a cycle, raise `ValueError` instead of returning a partial order.
- An empty graph returns an empty list.

## Review task

Trace a chain, a shared prerequisite, and several simultaneously ready packages. Then test duplicate edges, missing package definitions, a self-cycle, and a multi-node cycle.

## Starter Code

[View starter code](../../round-1/18-dependency-resolution/)

## Reference Solution

[View solution](../../solutions/round-1/18-dependency-resolution/)
