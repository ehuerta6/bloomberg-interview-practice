"""Resolve dependency graphs into deterministic installation order."""

import heapq
from collections.abc import Mapping
import unittest


def resolve_dependencies(graph):
    """Return deterministic topological order or raise ``ValueError``.

    ``graph`` maps each package name to the packages it depends on. Every
    referenced dependency must be defined as a key. Among packages that are
    ready at the same step, the lexicographically smallest name is selected.
    """
    if not isinstance(graph, Mapping):
        raise ValueError("dependency graph must be a mapping")
    normalized = {}
    for package, dependencies in graph.items():
        if not isinstance(package, str) or not package.strip():
            raise ValueError("package names must be nonblank strings")
        if not isinstance(dependencies, (list, tuple, set, frozenset)):
            raise ValueError("each package must map to a dependency collection")
        unique_dependencies = set()
        for dependency in dependencies:
            if not isinstance(dependency, str) or not dependency.strip():
                raise ValueError("dependency names must be nonblank strings")
            unique_dependencies.add(dependency)
        normalized[package] = unique_dependencies

    for dependencies in normalized.values():
        if not dependencies <= normalized.keys():
            raise ValueError("every dependency must be defined in the graph")

    indegree = {package: len(dependencies) for package, dependencies in normalized.items()}
    dependents = {package: [] for package in normalized}
    for package, dependencies in normalized.items():
        for dependency in dependencies:
            dependents[dependency].append(package)
    ready = [package for package, count in indegree.items() if count == 0]
    heapq.heapify(ready)

    order = []
    while ready:
        package = heapq.heappop(ready)
        order.append(package)
        for dependent in sorted(dependents[package]):
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                heapq.heappush(ready, dependent)
    if len(order) != len(normalized):
        raise ValueError("dependency graph contains a cycle")
    return order


class DependencyResolverTests(unittest.TestCase):
    def test_dependency_precedes_dependent(self):
        self.assertEqual(resolve_dependencies({"app": ["core"], "core": []}), ["core", "app"])

    def test_chain_is_ordered_from_leaf_to_root(self):
        result = resolve_dependencies({"app": ["ui", "core"], "ui": ["core"], "core": []})
        self.assertEqual(result, ["core", "ui", "app"])

    def test_independent_nodes_have_deterministic_order(self):
        self.assertEqual(resolve_dependencies({"z": [], "a": [], "m": []}), ["a", "m", "z"])

    def test_ready_nodes_are_selected_lexicographically_at_each_step(self):
        graph = {"root": ["z", "a"], "z": [], "a": [], "mid": ["a"]}
        self.assertEqual(resolve_dependencies(graph), ["a", "mid", "z", "root"])

    def test_shared_and_duplicate_dependencies_appear_once(self):
        result = resolve_dependencies({"app": ["core", "ui", "core"], "ui": ["core"], "core": []})
        self.assertEqual(result, ["core", "ui", "app"])

    def test_cycle_is_reported(self):
        for graph in ({"a": ["b"], "b": ["a"]}, {"a": ["a"]}):
            with self.subTest(graph=graph), self.assertRaises(ValueError):
                resolve_dependencies(graph)

    def test_unknown_dependencies_are_rejected(self):
        with self.assertRaises(ValueError):
            resolve_dependencies({"app": ["missing"]})

    def test_invalid_graph_shapes_and_names_are_rejected(self):
        for graph in ([("app", [])], {"app": "core"}, {" ": []}, {"app": [""]}):
            with self.subTest(graph=graph), self.assertRaises(ValueError):
                resolve_dependencies(graph)

    def test_empty_graph_returns_empty_order(self):
        self.assertEqual(resolve_dependencies({}), [])


if __name__ == "__main__":
    unittest.main()
