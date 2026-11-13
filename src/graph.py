
"""Dependency graph traversal and ASCII-tree output."""

from collections import deque


def build_graph_bfs_recursive(start_package, dependency_map):
    """Build the reachable graph using recursive BFS."""

    if start_package not in dependency_map:
        dependency_map = dict(dependency_map)
        dependency_map[start_package] = []

    graph = {}
    visited = set()
    queue = deque([(start_package, 0)])

    def process_queue():
        if not queue:
            return

        package, _depth = queue.popleft()

        if package in visited:
            process_queue()
            return

        visited.add(package)
        dependencies = dependency_map.get(package, [])
        graph[package] = list(dependencies)

        for dependency in dependencies:
            if dependency not in visited:
                queue.append((dependency, _depth + 1))

        process_queue()

    process_queue()

    # Include leaf packages as graph nodes.
    for dependencies in list(graph.values()):
        for dependency in dependencies:
            graph.setdefault(dependency, [])

    return graph


def build_reverse_dependency_map(dependency_map):
    """Build a map of packages that depend on each package."""

    reverse_map = {
        package: [] for package in dependency_map
    }

    for package, dependencies in dependency_map.items():
        for dependency in dependencies:
            reverse_map.setdefault(dependency, [])

            if package not in reverse_map[dependency]:
                reverse_map[dependency].append(package)

    return reverse_map


def print_ascii_tree(start_package, graph):
    """Print graph dependencies as an ASCII tree."""

    def visit(package, prefix, path):
        dependencies = graph.get(package, [])

        if not dependencies:
            return

        for index, dependency in enumerate(dependencies):
            is_last = index == len(dependencies) - 1
            branch = "└── " if is_last else "├── "

            print(prefix + branch + dependency)

            if dependency in path:
                cycle_prefix = (
                    "    " if is_last else "│   "
                )
                print(prefix + cycle_prefix + "└── [цикл]")
                continue

            next_prefix = prefix + (
                "    " if is_last else "│   "
            )
            visit(
                dependency,
                next_prefix,
                path | {dependency}
            )

    print(start_package)
    visit(start_package, "", {start_package})

