"""Dependency graph traversal and ASCII-tree output."""


def build_graph_bfs_recursive(start_package, dependency_map):
    """Build the reachable dependency graph using recursive BFS.

    The queue is processed recursively. The visited set prevents infinite
    traversal when the repository contains cycles.
    """
    if start_package not in dependency_map:
        # A package may exist as a leaf without its own dependency entry.
        dependency_map = dict(dependency_map)
        dependency_map[start_package] = []

    graph = {}
    visited = set()
    queue = [(start_package, 0)]

    def process_queue():
        if not queue:
            return

        package, _depth = queue.pop(0)
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

    # Include leaf packages in the graph as nodes with no outgoing edges.
    for dependencies in list(graph.values()):
        for dependency in dependencies:
            graph.setdefault(dependency, [])

    return graph


def print_ascii_tree(start_package, graph):
    """Print graph dependencies as an ASCII tree and avoid cycle loops."""
    def visit(package, prefix, path):
        dependencies = graph.get(package, [])
        if not dependencies:
            return

        for index, dependency in enumerate(dependencies):
            is_last = index == len(dependencies) - 1
            branch = "└── " if is_last else "├── "
            print(prefix + branch + dependency)

            if dependency in path:
                print(prefix + ("    " if is_last else "│   ") + "└── [цикл]")
                continue

            next_prefix = prefix + ("    " if is_last else "│   ")
            visit(dependency, next_prefix, path | {dependency})

    print(start_package)
    visit(start_package, "", {start_package})
