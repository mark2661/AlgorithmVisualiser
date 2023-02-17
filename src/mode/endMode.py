import pygame

from src.tile import Tile
from src.mode import Mode
from src.grid import Grid
from src.settings import *


class EndMode(Mode):

    def __init__(self, grid: Grid):
        super().__init__(grid)
        self.name = "End Mode"

    def left_click(self):
        tile = self.get_tile()
        self.set_tile(tile)

    def right_click(self):
        tile = self.get_tile()
        self.reset_tile(tile)

    def set_tile(self, tile: Tile):
        super().remove_tile_from_special_groups(tile)
        if not self.grid.end_tile:
            tile.set_colour(END_TILE_COLOUR)
            self.grid.end_tile.add(tile)

    def reset_tile(self, tile: Tile):
        if tile in self.grid.end_tile:
            tile.set_colour(BLANK_TILE_COLOUR)
            self.grid.end_tile.remove(tile)

    def __str__(self) -> str:
        return str(self.name)