import random
import noise
from grids.grid_base import Grid
from config import *
from entities.animal import Animal
from tiles.tile_base import Tile
from tiles.tile_grass import GrassTile
from tiles.tile_water import WaterTile

class GridGround(Grid):
    def __init__(self, rows: int, cols: int, tile_size: int):
        super().__init__(rows, cols, tile_size)
    
    def create_tile(self, col: int, row: int) -> Tile:
        rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
        
        match(WORLD_GENERATION_MODE):
            case "Perlin":
                n = noise.pnoise2(row / 20.0, col / 24.0)
            case "Random":
                n = random.random()
            case _:
                n = noise.pnoise2(row / 20.0, col / 24.0)
        
        
        if SURROUNDED_BY_WATER and self.is_border_tile(col, row):
            tile : Tile = WaterTile(rect, self.tile_size, 10)
        elif n <= WATER_PERCENTAGE:
            tile : Tile = WaterTile(rect, self.tile_size, random.randint(0,10))
        else:
            tile : Tile = GrassTile(rect, self.tile_size, random.randint(0,10))
            if random.random() <= STARTING_ANIMAL_PERCENTAGE:
                Animal(tile)
                
        tile.is_border_tile = self.is_border_tile(col, row) 
        return tile