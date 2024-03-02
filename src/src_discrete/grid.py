from tiles.tile import Tile
from config import *
from wfc.ClassStack import Stack
import random
import pygame

class Grid():
    def __init__(self, rows : int, cols : int, tile_size : int):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        
        self.generate_tiles()
        self.add_cell_neighbours()
    
    def update(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.tiles[row][col].update()
            
    def draw(self, screen : pygame.Surface):
        for row in range(self.rows):
            for col in range(self.cols):
                self.tiles[row][col].draw(screen)
    
    # Getter & Setter
    def generate_tiles(self):
        self.tiles = [[Tile(pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size), self.tile_size, value = random.randint(1, 10)) for col in range(self.cols)] for row in range(self.rows)]
           
    def add_cell_neighbours(self):
        for y in range(self.rows):
            for x in range(self.cols):
                tile = self.tiles[y][x]
                if y > 0:
                    tile.addNeighbour(NORTH, self.tiles[y - 1][x])
                if x < self.cols - 1:
                    tile.addNeighbour(EAST, self.tiles[y][x + 1])
                if y < self.rows - 1:
                    tile.addNeighbour(SOUTH, self.tiles[y + 1][x])
                if x > 0:
                    tile.addNeighbour(WEST, self.tiles[y][x - 1])