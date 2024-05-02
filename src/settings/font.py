import pygame

import settings.config

# TODO add all the fonts
# TODO is this still needed?
font_size = int(1.2 * settings.config.TILE_SIZE)
font: pygame.font.Font = pygame.font.Font(None, font_size)
