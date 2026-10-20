"""Order packages so every dependency precedes its dependent."""

import unittest


def resolve_dependencies(graph):
    """Return a topological ordering of the dependency mapping."""
    result = []
    visited = set()

    def visit(package):
        if package in visited:
            return
        for dependency in graph.get(package, []):
            visit(dependency)
        visited.add(package)
        result.append(package)

    for package in graph:
        visit(package)
    return result


class DependencyResolverTests(unittest.TestCase):
    def test_dependency_precedes_dependent(self):
        self.assertEqual(resolve_dependencies({"app": ["core"], "core": []}), ["core", "app"])

    def test_chain_is_ordered_from_leaf_to_root(self):
        result = resolve_dependencies({"app": ["ui", "core"], "ui": ["core"], "core": []})
        self.assertLess(result.index("core"), result.index("ui"))
        self.assertLess(result.index("ui"), result.index("app"))

    def test_independent_nodes_have_deterministic_order(self):
        self.assertEqual(resolve_dependencies({"z": [], "a": [], "m": []}), ["a", "m", "z"])

    def test_shared_dependency_appears_once(self):
        result = resolve_dependencies({"app": ["core", "ui"], "ui": ["core"], "core": []})
        self.assertEqual(result.count("core"), 1)

    def test_duplicate_edges_do_not_duplicate_packages(self):
        self.assertEqual(resolve_dependencies({"app": ["core", "core"], "core": []}).count("core"), 1)

    def test_cycle_is_reported(self):
        try:
            resolve_dependencies({"a": ["b"], "b": ["a"]})
        except RecursionError:
            self.fail("cycle should be reported as ValueError instead of recursing")
        else:
            self.fail("cycle should be reported as ValueError")

    def test_unknown_dependencies_are_rejected(self):
        with self.assertRaises(ValueError):
            resolve_dependencies({"app": ["missing"]})

    def test_invalid_graph_shape_is_rejected(self):
        with self.assertRaises(ValueError):
            resolve_dependencies([("app", [])])


if __name__ == "__main__":
    unittest.main()
