import pygame

import settings.screen

# TODO add all the fonts
# TODO is this still needed?
font_size = int(1.2 * settings.screen.TILE_SIZE)
font: pygame.font.Font = pygame.font.Font(None, font_size)


def get_centered_text_coordinates(
    rect: pygame.Rect, text: pygame.Surface
) -> tuple[int, int]:
    return rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2
