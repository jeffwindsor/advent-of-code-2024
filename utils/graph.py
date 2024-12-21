from collections import defaultdict, deque
from typing import DefaultDict, List, TypeAlias, TypeVar

T = TypeVar("T")  # Generic Graph type alias
Graph: TypeAlias = DefaultDict[T, List[T]]


def create_graph() -> Graph[T]:
    return defaultdict(list)


def add_edge(graph: Graph[T], node1: T, node2: T, directed: bool = False):
    graph[node1].append(node2)
    if not directed:
        graph[node2].append(node1)


def bfs(graph: DefaultDict[T, List[T]], start: T) -> List[T]:
    visited = set()
    queue = deque([start])  # Use deque for better performance
    order = []

    while queue:
        node = queue.popleft()  # Dequeue the first element in O(1) time
        if node not in visited:
            visited.add(node)
            order.append(node)
            # Enqueue all unvisited neighbors
            queue.extend(
                neighbor for neighbor in graph[node] if neighbor not in visited
            )

    return order
