import math
from pygame import sprite, Surface
from tile import Tile
from config import *
import random
from noise import pnoise2
from direction import Direction

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class World(sprite.Sprite):
    """
    The World class represents a game world in a game environment.

    Attributes:
        height (int): The height of the game world.
        width (int): The width of the game world.
        tile_size (int): The size of each tile in pixels.
        ground (GridGround): The grid of ground tiles in the game world.

    Methods:
        __init__(self, height: int, width: int, tile_size: int): Initializes a new instance of the World class.
        update(self): Updates the game world.
        draw(self, screen: pygame.Surface): Draws the game world on the screen.
        adjust_dimensions(height, width, tile_size): Adjusts the given height and width to be divisible by the tile size.
    """
    
    def __init__(self, height : int, width : int, tile_size : int):
        sprite.Sprite.__init__(self)
        self.tile_size = tile_size
        self.height, self.width = World.adjust_dimensions(height, width, self.tile_size)
        self.rows = math.floor(self.height / self.tile_size)
        self.cols = math.floor(self.width / self.tile_size)
        
        self.generate_world_parameters()
        
        self.tiles = [self.create_tile(col, row) for row in range(self.rows) for col in range(self.cols)]
        self.add_cell_neighbours()
   
    def update(self):
        random.shuffle(self.tiles)
        for tile in self.tiles:
            tile.update()
        
    def draw(self, screen : Surface):
        temp_surface = Surface((self.cols * self.tile_size, self.rows * self.tile_size), pygame.SRCALPHA)
        for tile in self.tiles:
            tile.draw(temp_surface)
            
        screen.blit(temp_surface, (0, 0))  
    
    def create_tile(self, col: int, row: int) -> Tile:
        rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
                
        height = self.generate_noise_value(row, col, self.world_gen_param1, self.world_gen_param2)
    
        return Tile(rect, self.tile_size, height=height)
    
    def add_cell_neighbours(self):
        for row in range(self.rows):
            for col in range(self.cols):
                tile: Tile = self.tiles[row * self.cols + col]
                if row > 0:
                    tile.add_neighbor(Direction.NORTH, self.tiles[(row - 1) * self.cols + col])
                if col < self.cols - 1:
                    tile.add_neighbor(Direction.EAST, self.tiles[row * self.cols + col + 1])
                if row < self.rows - 1:
                    tile.add_neighbor(Direction.SOUTH, self.tiles[(row + 1) * self.cols + col])
                if col > 0:
                    tile.add_neighbor(Direction.WEST, self.tiles[row * self.cols + col - 1])  
    
    def generate_world_parameters(self, seed=None):
        if seed is not None:
            random.seed(seed)  # Initialize the random number generator with the seed

        RANDOM_VALUE_RANGE = (-150, 150)
        MIN_PARAM_VALUE_THRESHOLD = 40

        if WORLD_GENERATION_PARAM1 is not None:
            self.world_gen_param1: int = WORLD_GENERATION_PARAM1
        else:
            self.world_gen_param1 = random.randint(*RANDOM_VALUE_RANGE) 
            while True:
                if abs(self.world_gen_param1) >= MIN_PARAM_VALUE_THRESHOLD:
                    break
                self.world_gen_param1 = random.randint(*RANDOM_VALUE_RANGE) 
                
        if WORLD_GENERATION_PARAM2 is not None:
            self.world_gen_param2: int = WORLD_GENERATION_PARAM2
        else:
            self.world_gen_param2  = 100 - abs(self.world_gen_param1)  # Inversely proportional example
            while True:
                if abs(self.world_gen_param2) >= MIN_PARAM_VALUE_THRESHOLD:
                    break
                self.world_gen_param2  = random.randint(*RANDOM_VALUE_RANGE) 

        logging.info(f"Perlin noise parameters: [{self.world_gen_param1}, {self.world_gen_param2}]")
    
    def generate_noise_value(self, row: int, col: int, param1: int, param2: int) -> int:
        match(WORLD_GENERATION_MODE):
            case "Perlin":
                value = pnoise2(row / param1, col / param1)
            case "Perlin Summation":
                base_noise = pnoise2(row / param1, col / param2)
                detail_noise = pnoise2(row / (param1 * 0.5), col / (param2 * 0.5)) * 0.5  # Higher frequency, lower amplitude
                value = base_noise + detail_noise
            case "Random":
                value = random.random()
            case _:
                value = pnoise2(row / param1, col / param1)
            
        value += .20
        value *= 10
        if value < 0:
            value = -(value**2)
        else:   
            value **= 2
                    
        return math.floor(value)
    
    @staticmethod
    def adjust_dimensions(height, width, tile_size):
        """
        Adjusts the given height and width to be divisible by the tile size.

        Parameters:
        - height (int): The original height value.
        - width (int): The original width value.
        - tile_size (int): The size of each tile.

        Returns:
        - adjusted_height (int): The adjusted height value that is divisible by the tile size.
        - adjusted_width (int): The adjusted width value that is divisible by the tile size.
        """
        adjusted_height = (height // tile_size) * tile_size
        adjusted_width = (width // tile_size) * tile_size
        return adjusted_height, adjusted_width