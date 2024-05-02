from __future__ import annotations
import pygame

JEREMY_BIG_SCREEN_SETTINGS = (5200, 1300, 20)
JEREMY_LAPTOP_SETTINGS = (1400, 800, 10)
SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE = JEREMY_LAPTOP_SETTINGS

# Settings
STARTING_ANIMAL_SPAWNING_CHANCE = .01
STARTING_PLANT_SPAWNING_CHANCE = .5

MIN_TILE_SIZE = 1

draw_height_level = False
draw_animal_energy = False
draw_animal_health = False
show_dead_organisms_stats = True

pygame.font.init()
font_size = int(1.2 * TILE_SIZE)
font: pygame.font.Font = pygame.font.Font(None, font_size) 