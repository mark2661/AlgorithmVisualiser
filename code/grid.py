import sys
import pygame
from memory_profiler import profile
import cProfile
import pstats
from settings import *
from tile import Tile
from a_star import a_star


class Grid:
    def __init__(self, dimensions: tuple[int, int]):
        self.tiles = pygame.sprite.Group()
        self.wall_tiles = pygame.sprite.Group()
        self.start_tile = pygame.sprite.GroupSingle()
        self.end_tile = pygame.sprite.GroupSingle()
        self.width, self.height = dimensions
        self.display_surface = pygame.display.get_surface()
        self.tile_map = dict()

        # populate grid
        self.add_tiles()

    def add_tiles(self):
        for x in range(0, self.width, TILE_WIDTH):
            for y in range(0, self.height, TILE_HEIGHT):
                new_tile = Tile((x, y), self.tiles)
                # map the tile center coords to the tile object for fast lookup
                self.tile_map[new_tile.rect.center] = new_tile

    def get_valid_neighbours(self, tile: Tile) -> list[Tile]:
        center_x, center_y = tile.rect.center
        valid_neighbours = []

        # up neighbour
        up_neighbour_center_coords = (center_x , center_y + TILE_HEIGHT)
        valid_neighbours.append(self.get_tile(up_neighbour_center_coords))

        # down neighbour
        down_neighbour_center_coords = (center_x , center_y - TILE_HEIGHT)
        valid_neighbours.append(self.get_tile(down_neighbour_center_coords))

        # left neighbour
        left_neighbour_center_coords = (center_x - TILE_WIDTH, center_y)
        valid_neighbours.append(self.get_tile(left_neighbour_center_coords))

        # right neighbour
        right_neighbour_center_coords = (center_x + TILE_WIDTH, center_y)
        valid_neighbours.append(self.get_tile(right_neighbour_center_coords))

        # return non wall neighbours only
        return [neighbour for neighbour in valid_neighbours if neighbour is not None and neighbour not in self.wall_tiles]

    def get_tile(self, center_pos: tuple[float, float]) -> Tile:
        return self.tile_map.get(center_pos, None)

    def reset(self, include_wall_tiles: bool = False):
        for tile in self.tiles:
            if include_wall_tiles:
                tile.set_colour(BLANK_TILE_COLOUR)
            else:
                if tile not in self.wall_tiles:
                    tile.set_colour(BLANK_TILE_COLOUR)

    def draw(self):
        for tile in self.tiles:
            pygame.draw.rect(self.display_surface, GRID_LINE_COLOUR,
                             pygame.Rect((tile.x, tile.y), (TILE_WIDTH, TILE_HEIGHT)))
            offset = -2
            pygame.draw.rect(self.display_surface, tile.get_colour(), tile.rect.inflate(offset, offset))

    def run(self):
        a_star(self, self.start_tile.sprite, self.end_tile.sprite)







