import pygame

def draw_text(text: str, font: pygame.font.Font, color: pygame.Color, surface: pygame.Surface, x: int, y: int):
    text_obj: pygame.Surface = font.render(text, True, color)
    text_rect: pygame.Rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)