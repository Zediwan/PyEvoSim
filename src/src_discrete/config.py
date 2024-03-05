import pygame

MIN_WATER_VALUE = 0
MAX_WATER_VALUE = 10

# Settings
LAND_PERCENTAGE = .9
DRAW_WATER_LEVEL = True
SURROUNDED_BY_WATER = True

tile_outline_thickness = 1

# Colors
dirt_color = pygame.Color(155, 118, 83)
min_grass_color = pygame.Color(235, 242, 230)
max_grass_color = pygame.Color(76, 141, 29)
min_water_color = pygame.Color(204, 229, 233)
max_water_color = pygame.Color(26, 136, 157)

# Directions
NORTH = 0
EAST  = 1
SOUTH = 2
WEST  = 3