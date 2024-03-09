from __future__ import annotations
import pygame

JEREMY_BIG_SCREEN = (5200, 1300, 20)
JEREMY_LAPTOP = (1400, 1000, 10)
WIDTH, HEIGHT, TILE_SIZE = JEREMY_LAPTOP
 

# Settings
WATER_PERCENTAGE = 0
STARTING_ANIMAL_PERCENTAGE = .01
STARTING_LAND_ANIMAL_PERCENTAGE = .0005
STARTING_WATER_ANIMAL_PERCENTAGE = .005
SURROUNDED_BY_WATER = False

WORLD_GENERATION_MODE = "Perlin"
#WORLD_GENERATION_PARAMS = 20, 24
WORLD_GENERATION_PARAMS = None, None
WORLD_GENERATION_PARAM1 = WORLD_GENERATION_PARAMS[0]
WORLD_GENERATION_PARAM2 = WORLD_GENERATION_PARAMS[1]

MIN_TILE_SIZE = 4

draw_water_level: bool = False
draw_growth_level = False
draw_height_level = False
draw_height_lines = False

pygame.font.init()
font_size = int(1.2 * TILE_SIZE)
font: pygame.font.Font = pygame.font.Font(None, font_size) 

tile_outline_thickness = 1

# Alpha values for grids
ground_alpha = 255
ground_font_alpha = 100
surface_alpha = 255
sky_alpha = 100

# Colors
tile_border_color = pygame.Color("black")

from enum import Enum

class ExtendedEnum(Enum):
    @classmethod
    def get_options(cls):
        return list(map(lambda c: c.value, cls))

class Direction(ExtendedEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    
    @staticmethod
    def is_valid_direction(direction : Direction) -> bool:
        return direction in Direction.get_options()