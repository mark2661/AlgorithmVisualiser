import sys
import time
import pygame
from grid import Grid
from debug import debug
from wallMode import WallMode
from startMode import StartMode
from endMode import EndMode


class EventHandler:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.modes = [WallMode(self.grid), StartMode(self.grid), EndMode(self.grid)]
        self.mode_index = 0
        self.mode = self.modes[self.mode_index]

    def process_event(self, event: pygame.event):
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_TAB]:
                self._change_mode()
                time.sleep(1)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            left_button, center_button, right_button = pygame.mouse.get_pressed()
            if left_button:
                self.mode.left_click()

            elif right_button:
                self.mode.right_click()

    def _change_mode(self):
        self.mode_index = (self.mode_index + 1) % len(self.modes)
        self.mode = self.modes[self.mode_index]
