# Dependency Resolution — Reference Solution

## What broke

The draft recursively walked dependencies in mapping order without tracking an active traversal path. Cycles could recurse indefinitely, while independent packages had no specified deterministic tie-break.

## Reproduce the issue

Run `python3 dependency_resolver.py` in the starter folder. Try a cycle, an undefined package, and independent packages in a different insertion order. Run the corrected independent suite with `python3 dependency_resolver.py` here.

## Investigation approach

Treat each package as a node and each dependency as a prerequisite edge. A package is ready only after all its dependencies are emitted. Track the number of prerequisites, detect when progress stops before all nodes are emitted, and choose ready nodes deterministically.

## Correction

The solution validates graph shapes and referenced names, removes duplicate dependency edges, and uses a min-heap of ready package names for deterministic topological ordering. If not every package can be emitted, it raises `ValueError` for a cycle.

## Regression tests

Tests cover chains, shared and repeated edges, independent ready nodes, deterministic ordering, missing dependencies, cycles, and invalid graph shapes. Run them with `python3 dependency_resolver.py`.
