import pygame


class fpsClock:
    # static variables
    clock = None

    def __init__(self):
        pass

    @staticmethod
    def get_clock():
        if fpsClock.clock is None:
            fpsClock.clock = pygame.time.Clock()

        return fpsClock.clock
