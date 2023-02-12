import sys
import pygame
from settings import *
from grid import Grid
from eventHandler import EventHandler
from debug import debug
from clock import FpsClock


class Game:
    clock = FpsClock.get_clock()

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.grid = Grid((WIDTH, HEIGHT))
        self.event_handler = EventHandler(self.grid)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                self.event_handler.process_event(event)

            self.screen.fill("black")
            self.grid.draw()
            debug(self.event_handler.mode)

            pygame.display.update()
            Game.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
