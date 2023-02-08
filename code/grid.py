import pygame
from settings import *
from tile import Tile


class Grid:
    def __init__(self, dimensions: tuple[int, int]):
        self.tiles = pygame.sprite.Group()
        self.wall_tiles = pygame.sprite.Group()
        self.start_tile = pygame.sprite.GroupSingle()
        self.end_tile = pygame.sprite.GroupSingle()
        self.width, self.height = dimensions
        self.display_surface = pygame.display.get_surface()

        # populate grid
        self.add_tiles()

    def add_tiles(self):
        for x in range(0, self.width, TILE_WIDTH):
            for y in range(0, self.height, TILE_HEIGHT):
                Tile((x, y), self.tiles)

    def draw(self):
        for tile in self.tiles:
            pygame.draw.rect(self.display_surface, GRID_LINE_COLOUR ,
                             pygame.Rect((tile.x, tile.y), (TILE_WIDTH, TILE_HEIGHT)))
            offset = -2
            pygame.draw.rect(self.display_surface, tile.get_colour(), tile.rect.inflate(offset, offset))

    def run(self):
        pass

