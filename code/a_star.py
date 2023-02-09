import heapq
from tile import Tile
from grid import Grid


def heuristic(a, b):
    # Manhattan distance
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def a_start(grid: Grid, start: Tile, end: Tile):
    heap = [(0, start)]
    cost = {start: 0}
    parent = {start: None}
    visited = set()

    while heap:
        f, current = heapq.heappop(heap)
        if current == end:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]

        visited.add(current)
        for neighbour in grid.get_valid_neighbours(current):
            if neighbour not in visited:
                g = cost[current] + 1
                f = g + heuristic(end.rect.center, neighbour.rect.center)
                heapq.heappush(heap, (f, neighbour))
                parent[neighbour] = current

    return None
