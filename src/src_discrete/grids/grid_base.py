import random
import pygame
from abc import ABC, abstractmethod
from entities.organism import Organism
from tiles.tile_base import Tile
from config import *

class Grid(ABC):
    def __init__(self, rows : int, cols : int, tile_size : int):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.tiles = [self.create_tile(col, row) for row in range(self.rows) for col in range(self.cols)]
        self.add_cell_neighbours()
    
    def update(self):
        random.shuffle(self.tiles)
        for tile in self.tiles:
            tile.update()
            
    def draw(self, screen : pygame.Surface):
        temp_surface = pygame.Surface((self.cols * self.tile_size, self.rows * self.tile_size), pygame.SRCALPHA)
        for tile in self.tiles:
            tile.draw(temp_surface)
        screen.blit(temp_surface, (0, 0))
                
    @abstractmethod
    def create_tile(self, col, row) -> Tile:
        pass
    
    def add_cell_neighbours(self):
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.tiles[row * self.cols + col]
                neighbours = {}
                if row > 0:
                    neighbours[Direction.NORTH] = self.tiles[(row - 1) * self.cols + col]
                if col < self.cols - 1:
                    neighbours[Direction.EAST] = self.tiles[row * self.cols + col + 1]
                if row < self.rows - 1:
                    neighbours[Direction.SOUTH] = self.tiles[(row + 1) * self.cols + col]
                if col > 0:
                    neighbours[Direction.WEST] = self.tiles[row * self.cols + col - 1]
                tile.neighbours = neighbours
    
    def is_border_tile(self, row: int, col: int) -> bool:
        return (row == 0 or col == 0 or row == self.rows - 1 or col == self.cols - 1)