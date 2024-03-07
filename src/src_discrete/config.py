from __future__ import annotations
import pygame

WIDTH, HEIGHT = 4000, 1400
TILE_SIZE = 20

# Settings
WATER_PERCENTAGE = -.2
STARTING_ANIMAL_PERCENTAGE = .01
SURROUNDED_BY_WATER = False
WORLD_GENERATION_MODE = "Perlin"
MIN_TILE_SIZE = 4

draw_water_level: bool = False
draw_growth_level = False

pygame.font.init()
font: pygame.font.Font = pygame.font.Font(None, 24) 

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