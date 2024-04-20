from __future__ import annotations

import pygame

JEREMY_BIG_SCREEN = (5200, 1300, 20)
JEREMY_LAPTOP = (1400, 1000, 8)
WIDTH, HEIGHT, TILE_SIZE = JEREMY_LAPTOP
 

# Settings
WATER_PERCENTAGE = 0
STARTING_ANIMAL_PERCENTAGE = .01
STARTING_PLANT_PERCENTAGE = .5
STARTING_LAND_ANIMAL_PERCENTAGE = .5
STARTING_WATER_ANIMAL_PERCENTAGE = .5
SURROUNDED_BY_WATER = False

WORLD_GENERATION_MODE = "Simplex Summation Normalised"
#WORLD_GENERATION_PARAMS = 20, 24
WORLD_GENERATION_PARAMS = None, None
WORLD_GENERATION_PARAM1 = WORLD_GENERATION_PARAMS[0]
WORLD_GENERATION_PARAM2 = WORLD_GENERATION_PARAMS[1]

MIN_TILE_SIZE = 4

draw_water_level: bool = False
draw_growth_level = False
draw_height_level = False
draw_height_lines = False
draw_water_sources = False
draw_temperature_level = False
draw_wind_speed = False
draw_wind_direction = False

pygame.font.init()
font_size = int(1.2 * TILE_SIZE)
font: pygame.font.Font = pygame.font.Font(None, font_size) 

# Alpha values for grids
ground_alpha = 255
ground_font_alpha = 100
surface_alpha = 255
sky_alpha = 100

freq_x1 = 1
freq_y1 = 1
freq_x2 = 2
freq_y2 = 2
freq_x3 = 4
freq_y3 = 4
scale_1 = 1
scale_2 = .5
scale_3 = .25
offset_x1 = 0
offset_y1 = 0
offset_x2 = 4.7
offset_y2 = 2.3
offset_x3 = 19.1
offset_y3 = 16.6