import pygame
from config import *
from tiles.tile_base import Tile
from abc import abstractmethod

class GroundTile(Tile):
    color: pygame.Color
    
    def __init__(self, rect: pygame.Rect, cell_size: int):
        super().__init__(rect, cell_size)
        self.temp_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
    
    def update(self):
        super().update()
    
    @abstractmethod
    def updateColor(self):
        pass
    
    def draw(self, screen : pygame.Surface):
        super().draw(screen)
        
        if self.organism:
            if self.organism.is_alive():
                self.organism.draw(screen)
        else:
            self.updateColor()
            self.temp_surface.fill(self.color)
        screen.blit(self.temp_surface, (self.rect.left, self.rect.top))