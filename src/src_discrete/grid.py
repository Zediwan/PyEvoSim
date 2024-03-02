from tiles.tile import Tile
import random
import pygame

class Grid():
    def __init__(self, rows : int, cols : int, tile_size : int):
        self.rows = rows
        self.cols = cols
        self.grid_size = tile_size
        self.cells = [[Tile(pygame.Rect(col * self.grid_size, row * self.grid_size, self.grid_size, self.grid_size), tile_size, value = random.randint(0, 10)) for col in range(cols)] for row in range(rows)]
    
    def update(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].update()
            
    def draw(self, screen : pygame.Surface):
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].draw(screen)