import pygame
from config import *

class Tile():
    MIN_TILE_SIZE = 4
    def __init__(self, rect : pygame.Rect, cell_size : int, value : int = 0, color : pygame.Color = pygame.Color(0, 0, 0)):
        assert cell_size >= 4, "Cell size is below minimum."
        self.cell_size = max(cell_size, self.MIN_TILE_SIZE)
        self.value = value
        self.color = color
        self.rect = rect
    
    def update(self):
        self.color = dirt_color.lerp(min_grass_color, self.value / 10).lerp(max_grass_color, self.value / 10)

    def draw(self, screen : pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value
        
    def change_value(self, change):
        self.value += change