import pygame
from config import *
from tiles.tile_base import Tile
from abc import abstractmethod

class GroundTile(Tile):
    def __init__(self, rect: pygame.Rect, cell_size: int,  color : pygame.Color = pygame.Color("white")):
        super().__init__(rect, cell_size)
        self.color = color
    
    def update(self):
        self.updateColor()
    
    @abstractmethod
    def updateColor(self):
        pass
    
    def draw(self, screen : pygame.Surface):
        super().draw(screen)
        
        temp_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, self.color, self.rect, ground_alpha)
        screen.blit(temp_surface, (self.rect.x, self.rect.y))