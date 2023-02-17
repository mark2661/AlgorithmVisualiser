
import pygame

from .mode import Mode
from src.grid import Grid
from src.tile import Tile
from src.settings import *


class WallMode(Mode):

    def __init__(self, grid: Grid):
        super().__init__(grid)
        self.name = "Wall Mode"

    def left_click(self):
        tile = self.get_tile()
        self.set_tile(tile)

    def right_click(self):
        tile = self.get_tile()
        self.reset_tile(tile)

    def set_tile(self, tile: Tile):
        super().remove_tile_from_special_groups(tile)
        if tile not in self.grid.wall_tiles:
            tile.set_colour(WALL_TILE_COLOUR)
            self.grid.wall_tiles.add(tile)

    def reset_tile(self, tile: Tile):
        if tile in self.grid.wall_tiles:
            tile.set_colour(BLANK_TILE_COLOUR)
            self.grid.wall_tiles.remove(tile)

    def __str__(self) -> str:
        return str(self.name)

