import heapq
import sys
import math
from tile import Tile
from settings import *
import pygame
import time
from clock import fpsClock


def heuristic(a, b):
    # Manhattan distance
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

    # Euclidian distance
    # return math.sqrt(pow(b[0] - a[0], 2) + pow(b[1] - a[1], 2))


def a_star(grid, start: Tile, end: Tile):
    heap_entry_count = 0
    heap = [(0, heap_entry_count, start)]
    g_score = {id(tile): sys.maxsize for tile in grid.tiles}
    g_score[id(start)] = 0
    f_score = {id(tile): sys.maxsize for tile in grid.tiles}
    f_score[id(start)] = heuristic(start.rect.center, end.rect.center)
    parent = {start: None}
    visited = set()
    visited.add(id(start))

    clock = fpsClock.get_clock()

    def draw_best_path(best_path: list[Tile]):
        time.sleep(2)
        grid.reset()
        grid.draw()
        pygame.display.update()

        for tile in best_path:
            tile.set_colour(SHORTEST_PATH_COLOUR)
            grid.draw()
            pygame.display.update()
            clock.tick(FPS//4)

    def draw():
        grid.draw()
        pygame.display.update()
        clock.tick(FPS)

    while heap:
        f, _, current = heapq.heappop(heap)
        if current == end:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            draw_best_path(path[::-1])
            break

        # change current tile to VISITED_TILE_COLOUR
        if current != start:
            current.set_colour(VISITED_TILE_COLOUR)
        visited.remove(id(current))

        for neighbour in grid.get_valid_neighbours(current):
            temp_g_score = g_score[id(current)] + 1

            # update cost
            if temp_g_score < g_score[id(neighbour)]:
                parent[neighbour] = current
                g_score[id(neighbour)] = temp_g_score
                f_score[id(neighbour)] = temp_g_score + heuristic(end.rect.center, neighbour.rect.center)
                if id(neighbour) not in visited:
                    # add neighbour to priority queue
                    heap_entry_count += 1
                    heapq.heappush(heap, (f, heap_entry_count, neighbour))
                    visited.add(id(neighbour))
                    # change frontier tile to FRONTIER_TILE_COLOUR
                    if neighbour != end:
                        neighbour.set_colour(FRONTIER_TILE_COLOUR)

        # update display
        draw()

    return None


