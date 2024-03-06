from __future__ import annotations
import pygame

WIDTH, HEIGHT = 3000, 1000
TILE_SIZE = 20

MIN_ORGANISM_HEALTH, MAX_ORGANISM_HEALTH = 0, 100
MIN_ORGANISM_ENERGY, MAX_ORGANISM_ENERGY = 0, 100
MIN_ANIMAL_HEALHT, MAX_ANIMAL_HEALTH = 0, 100
MIN_ANIMAL_ENERGY, MAX_ANIMAL_ENERGY = 0, 100

BASE_ORGANISM_HEALHT = MAX_ORGANISM_HEALTH
BASE_ORGANISM_ENERGY = MAX_ORGANISM_ENERGY

BASE_ANIMAL_HEALHT = MAX_ANIMAL_HEALTH - 50
BASE_ANIMAL_ENERGY = MAX_ANIMAL_ENERGY - 50

MIN_WATER_VALUE, MAX_WATER_VALUE= 0, 10
MIN_GRASS_VALUE, MAX_GRASS_VALUE = 0, 10

# Settings
LAND_PERCENTAGE = .9
STARTING_ANIMAL_PERCENTAGE = .05
DRAW_WATER_LEVEL = True
SURROUNDED_BY_WATER = True
MIN_TILE_SIZE = 4

tile_outline_thickness = 1

# Alpha values for grids
ground_alpha = 255
ground_font_alpha = 100
surface_alpha = 255
sky_alpha = 100

# Colors
tile_border_color = pygame.Color("black")
dirt_color = pygame.Color(155, 118, 83, ground_alpha)
min_grass_color = pygame.Color(235, 242, 230, ground_alpha)
max_grass_color = pygame.Color(76, 141, 29, ground_alpha)
min_water_color = pygame.Color(204, 229, 233, ground_alpha)
max_water_color = pygame.Color(26, 136, 157, ground_alpha)
ANIMAL_COLOR = pygame.Color("black")

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