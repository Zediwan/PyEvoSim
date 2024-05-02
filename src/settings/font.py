import pygame
from settings.config import TILE_SIZE

# TODO add all the fonts
# TODO is this still needed?
pygame.font.init()
font_size = int(1.2 * TILE_SIZE)
font: pygame.font.Font = pygame.font.Font(None, font_size) 