from abc import ABC, abstractmethod
from tile import Tile

import pygame

from grid import Grid


class Mode(ABC):
    def __init__(self, grid: Grid):
        self.grid = grid

    @abstractmethod
    def left_click(self):
        pass

    @abstractmethod
    def right_click(self):
        pass

    @abstractmethod
    def set_tile(self, tile: Tile):
        pass

    @abstractmethod
    def reset_tile(self, tile: Tile):
        pass

    def get_tile(self):
        mouse_pos = pygame.mouse.get_pos()
        for tile in self.grid.tiles:
            if self._cursor_on_tile(mouse_pos, tile):
                return tile

    def remove_tile_from_special_groups(self, tile: Tile):
        # remove tile from all groups
        tile.kill()
        # add tile back to tile group
        self.grid.tiles.add(tile)

    def _cursor_on_tile(self, mouse_pos: tuple[float, float], tile: Tile):
        return tile.rect.left <= mouse_pos[0] <= tile.rect.right \
               and tile.rect.top <= mouse_pos[1] <= tile.rect.bottom

    @abstractmethod
    def __str__(self) -> str:
        str(self)
