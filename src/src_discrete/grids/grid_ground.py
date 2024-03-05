import random
from grids.grid_base import Grid
from config import *
from tiles.tile_base import Tile
from tiles.tile_grass import GrassTile
from tiles.tile_water import WaterTile

class GridGround(Grid):
    def __init__(self, rows : int, cols : int, tile_size : int):
        super().__init__(rows, cols, tile_size)
    
    def create_tile(self, col, row) -> Tile:
        rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
        
        if SURROUNDED_BY_WATER and (row == 0 or col == 0 or row == self.rows - 1 or col == self.cols - 1):
            tile : Tile = WaterTile(rect, self.tile_size, random.randint(0,10))
        elif random.random() >= LAND_PERCENTAGE:
            tile : Tile = WaterTile(rect, self.tile_size, random.randint(0,10))
        else:
            tile : Tile = GrassTile(rect, self.tile_size, random.randint(0,10))
        return tile