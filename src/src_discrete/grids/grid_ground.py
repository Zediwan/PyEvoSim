import random
import noise
from grids.grid_base import Grid
from config import *
from entities.animal import Animal
from tiles.tile_base import Tile
from tiles.tile_grass import GrassTile
from tiles.tile_water import WaterTile

class GridGround(Grid):
    """
    The GridGround class represents a grid of ground tiles in a game environment.

    Attributes:
        rows (int): The number of rows in the grid.
        cols (int): The number of columns in the grid.
        tile_size (int): The size of each tile in pixels.

    Methods:
        __init__(self, rows: int, cols: int, tile_size: int): Initializes a new instance of the GridGround class.
        create_tile(self, col: int, row: int) -> Tile: Creates a new ground tile at the specified column and row.
        generate_noise_value(self, row: int, col: int) -> float: Generates a noise value for the specified row and column.
    """
    def __init__(self, rows: int, cols: int, tile_size: int):
        super().__init__(rows, cols, tile_size)
    
    
    def create_tile(self, col: int, row: int) -> Tile:
        """
        Creates a new ground tile at the specified column and row.

        Args:
            col (int): The column index of the tile.
            row (int): The row index of the tile.

        Returns:
            Tile: The newly created ground tile.
        """
        rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
        n = self.generate_noise_value(row, col)
        is_border = self.is_border_tile(col, row)
    
        if SURROUNDED_BY_WATER and is_border:
            tile : Tile = WaterTile(rect, self.tile_size, 10)
        elif n <= WATER_PERCENTAGE:
            tile : Tile = WaterTile(rect, self.tile_size, random.randint(0,10))
        else:
            tile : Tile = GrassTile(rect, self.tile_size, random.randint(0,10))
            if random.random() <= STARTING_ANIMAL_PERCENTAGE:
                Animal(tile)
            
        tile.is_border_tile = is_border 
        return tile

    def generate_noise_value(self, row: int, col: int) -> float:
        """
        Generates a noise value for the specified row and column.

        Args:
            row (int): The row index of the tile.
            col (int): The column index of the tile.

        Returns:
            float: The generated noise value.

        Raises:
            None
        """
        match(WORLD_GENERATION_MODE):
            case "Perlin":
                return noise.pnoise2(row / 20.0, col / 24.0)
            case "Random":
                return random.random()
            case _:
                return noise.pnoise2(row / 20.0, col / 24.0)