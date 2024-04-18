import pygame

class Custom_Group(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(sprites)
    
    def draw(
        self, surface, bgsurf=None, special_flags=0
    ):
        sprites = self.sprites()
        for s in sprites:
            s.draw(surface)