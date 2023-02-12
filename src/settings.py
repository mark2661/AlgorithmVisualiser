import pygame

WIDTH = 1500
HEIGHT = 800
TILE_WIDTH = 25
TILE_HEIGHT = 25
GRID_LINE_COLOUR = pygame.Color(0, 0, 0)
# BLANK_TILE_COLOUR = pygame.Color(0, 0, 0)
BLANK_TILE_COLOUR = pygame.Color(255, 255, 255)
# WALL_TILE_COLOUR = pygame.Color(255, 255, 255)
WALL_TILE_COLOUR = pygame.Color(80, 80, 80) # grey
START_TILE_COLOUR = pygame.Color(0, 255, 0) # green
END_TILE_COLOUR = pygame.Color(255, 0, 0) # red
FRONTIER_TILE_COLOUR = pygame.Color(102, 0, 255) # purple
VISITED_TILE_COLOUR = pygame.Color(255, 51, 204) # pink
SHORTEST_PATH_COLOUR = pygame.Color(255, 215, 0) # gold


FPS = 120