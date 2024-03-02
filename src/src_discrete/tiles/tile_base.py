import pygame
from config import *

class Tile():
    MIN_TILE_SIZE = 4
    def __init__(self, rect : pygame.Rect, cell_size : int, color : pygame.Color = pygame.Color("white")):
        assert cell_size >= 4, "Cell size is below minimum."
        self.cell_size = max(cell_size, self.MIN_TILE_SIZE)
        self.color = color
        self.rect = rect
    
    def update(self):
        pass

    def draw(self, screen : pygame.Surface):
        pygame.draw.rect(screen, pygame.Color("black"), self.rect, tile_outline_thickness)
        pygame.draw.rect(screen, self.color, self.rect)