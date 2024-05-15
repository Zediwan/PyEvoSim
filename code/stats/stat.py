import pygame

class Stat(pygame.sprite.Sprite):
    def __init__(self, name: str, value, rect: pygame.Rect) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.name: str = name
        self.value = value
        self.rect: pygame.Rect = rect
        self.image: pygame.Surface = pygame.Surface(self.rect.size)