import pygame

from tile import Tile
from mode import Mode
from grid import Grid
from settings import *


class StartMode(Mode):

    def __init__(self, grid: Grid):
        super().__init__(grid)
        self.name = "Start Mode"

    def left_click(self):
        tile = self.get_tile()
        self.set_tile(tile)

    def right_click(self):
        tile = self.get_tile()
        self.reset_tile(tile)

    def set_tile(self, tile: Tile):
        super().remove_tile_from_special_groups(tile)
        if not self.grid.start_tile:
            # lawn green: (124, 252, 0)
            tile.set_colour(START_TILE_COLOUR)
            self.grid.start_tile.add(tile)

    def reset_tile(self, tile: Tile):
        if tile in self.grid.start_tile:
            tile.set_colour(BLANK_TILE_COLOUR)
            self.grid.start_tile.remove(tile)

    def __str__(self) -> str:
        return str(self.name)
