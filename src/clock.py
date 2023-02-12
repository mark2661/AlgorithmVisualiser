import pygame


class FpsClock:
    # static variables
    clock = None

    def __init__(self):
        pass

    @staticmethod
    def get_clock():
        if FpsClock.clock is None:
            FpsClock.clock = pygame.time.Clock()

        return FpsClock.clock
