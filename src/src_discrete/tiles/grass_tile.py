import pygame
from tile import Tile

class GrassTile(Tile):
    grass_color = pygame.Color(96, 153, 54)
    
    def __init__(self, rect: pygame.Rect, cell_size: int, value: int = 0):
        super().__init__(rect, cell_size, value, color = self.grass_color)
        
    #def update(self):
        