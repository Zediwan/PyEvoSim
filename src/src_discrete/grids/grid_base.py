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
        self.tiles = [[self.create_tile(col, row) for col in range(self.cols)] for row in range(self.rows)]
        self.add_cell_neighbours()
    
    def update(self):
        # Create a list of all tiles
        tiles_list = [tile for row in self.tiles for tile in row]
        
        # Shuffle the list
        random.shuffle(tiles_list)
        
        # Update each tile
        for tile in tiles_list:
            tile.update()
            
    def draw(self, screen : pygame.Surface):
        for row in range(self.rows):
            for col in range(self.cols):
                self.tiles[row][col].draw(screen)
                
    @abstractmethod
    def create_tile(self, col, row) -> Tile:
        pass
    
    def add_cell_neighbours(self):
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.tiles[row][col]
                if row > 0:
                    tile.add_neighbor(Direction.NORTH, self.tiles[row - 1][col])
                if col < self.cols - 1:
                    tile.add_neighbor(Direction.EAST, self.tiles[row][col + 1])
                if row < self.rows - 1:
                    tile.add_neighbor(Direction.SOUTH, self.tiles[row + 1][col])
                if col > 0:
                    tile.add_neighbor(Direction.WEST, self.tiles[row][col - 1])