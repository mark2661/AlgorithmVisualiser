import time
import pygame
from grid import Grid
from src.mode import WallMode
from src.mode import StartMode
from src.mode import EndMode


class EventHandler:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.modes = [WallMode(self.grid), StartMode(self.grid), EndMode(self.grid)]
        self.mode_index = 0
        self.mode = self.modes[self.mode_index]

    def process_event(self, event: pygame.event):
        left_button, center_button, right_button = pygame.mouse.get_pressed()

        if event.type == pygame.QUIT:
            # sys.exit()
            pass
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_TAB]:
                self._change_mode()
                time.sleep(1)

            elif keys[pygame.K_SPACE]:
                self.grid.run()

        elif left_button:
            self.mode.left_click()

        elif right_button:
            self.mode.right_click()

    def _change_mode(self):
        self.mode_index = (self.mode_index + 1) % len(self.modes)
        self.mode = self.modes[self.mode_index]
