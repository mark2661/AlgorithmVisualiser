from __future__ import annotations
import pygame
from src.settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], groups: pygame.sprite.Group,
                 colour: pygame.Color = BLANK_TILE_COLOUR):

        super().__init__(groups)
        self.x, self.y = pos
        self.colour = colour
        self.rect = pygame.Rect((self.x, self.y), (TILE_WIDTH, TILE_HEIGHT))

    def set_colour(self, newColour: pygame.Color):
        self.colour = newColour

    def get_colour(self) -> pygame.Color:
        return self.colour
