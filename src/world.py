import math
from typing import List
from pygame import sprite, Surface
from plant import Plant
from tile import Tile
from config import *
from animal import Animal
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
    
    highest_tile: Tile = Tile(pygame.rect.Rect(0, 0, 0, 0), 0, height= 0)
    lowest_tile: Tile
    
    def __init__(self, height : int, width : int, tile_size : int):
        sprite.Sprite.__init__(self)
        self.tile_size = tile_size
        self.height, self.width = World.adjust_dimensions(height, width, self.tile_size)
        self.rows = math.floor(self.height / self.tile_size)
        self.cols = math.floor(self.width / self.tile_size)
        
        self.generate_world_parameters()
        
        self.tiles = [self.create_tile(col, row) for row in range(self.rows) for col in range(self.cols)]
        self.define_neighbor_attributes()
        self.create_river()
   
    def update(self):
        random.shuffle(self.tiles)
        for tile in self.tiles:
            tile.update()
            if tile.is_border or tile.water > 0 or tile.height <= 1:
                chance_to_spawn_animal_at_border = .000001
                chance_to_spawn_plant_at_border = .00001
                if random.random() <= chance_to_spawn_animal_at_border and not tile.has_animal():
                    self.spawn_animal(tile)
                if random.random() <= chance_to_spawn_plant_at_border and not tile.has_plant():
                    self.spawn_plant(tile)
                    
    def draw(self, screen : Surface):
        temp_surface = Surface((self.cols * self.tile_size, self.rows * self.tile_size), pygame.SRCALPHA)
        for tile in self.tiles:
            tile.draw(temp_surface)
            
        screen.blit(temp_surface, (0, 0))  
    
    def is_border_tile(self, row: int, col: int) -> bool:
        return (row == 0 or col == 0 or row == self.rows - 1 or col == self.cols - 1)
    
    def create_river(self, tile_to_start: Tile | None = None):
        if not tile_to_start:
            tile = self.highest_tile
        else:
            tile = tile_to_start
        while tile != None and tile.steepest_decline_direction != None and tile.water <= 0:
            tile.water = pygame.math.lerp(10, 1, tile.height/self.highest_tile.height)
            tile: Tile | None = tile.get_neighbor(tile.steepest_decline_direction)
            river_branch_chance = 0.2 * random.random()
            if random.random() < river_branch_chance and tile != None and tile.steepest_decline_direction != None:
                branch_of = tile.get_neighbor(random.choice(Direction.get_neighboring_directions(tile.steepest_decline_direction)))
                self.create_river(branch_of)
    
    def create_tile(self, col: int, row: int) -> Tile:
        rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
                
        height = self.generate_noise_value(row, col, self.world_gen_param1, self.world_gen_param2)
        
        tile : Tile = Tile(rect, self.tile_size, height=height, is_border = self.is_border_tile(row = row, col = col))
        
        if self.highest_tile:
            if height > self.highest_tile.height and random.random() < .75:
                self.highest_tile = tile
        else:
            self.highest_tile = tile
            
        self.spawn_animal(tile,
                          chance_to_spawn = STARTING_ANIMAL_PERCENTAGE, 
                          chance_of_land_animals = STARTING_LAND_ANIMAL_PERCENTAGE, 
                          chance_of_water_animals = STARTING_WATER_ANIMAL_PERCENTAGE
                          )
        
        self.spawn_plant(tile)
            
        return tile
    
    def spawn_animals(self, chance_to_spawn: float = 1, chance_of_land_animals: float = 1, chance_of_water_animals: float = 1):
        for tile in self.tiles:
            if not tile.has_animal():
                self.spawn_animal(tile, 
                                chance_to_spawn = chance_to_spawn,
                                chance_of_land_animals = chance_of_land_animals,
                                chance_of_water_animals = chance_of_water_animals)
    
    def spawn_animal(self, tile: Tile, chance_to_spawn: float = 1, chance_of_land_animals: float = 1, chance_of_water_animals: float = 1):
        if random.random() <= chance_to_spawn:
            if tile.water > 0:
                self.spawn_water_animal(tile, chance_of_water_animals)
            else:
                self.spawn_land_animal(tile, chance_of_land_animals)
                
    def spawn_plant(self, tile: Tile, chance_to_spawn: float = 1):
        if random.random() <= chance_to_spawn:
            Plant(tile)
            
    def spawn_water_animal(self, tile: Tile, chance_to_spawn: float = 1):
        wA = Animal.MAX_ANIMAL_WATER_AFFINITY - 2
        lA = Animal.MIN_ANIMAL_LAND_AFFINITY + 5
        if random.random() <= chance_to_spawn:
            Animal(tile, starting_land_affinity=lA, starting_water_affinity=wA)
            
    def spawn_land_animal(self, tile: Tile, chance_to_spawn: float = 1):
        wA = Animal.MIN_ANIMAL_WATER_AFFINITY + 2
        lA = Animal.MAX_ANIMAL_LAND_AFFINITY - 2
        if random.random() <= chance_to_spawn:
            Animal(tile, starting_land_affinity=lA, starting_water_affinity=wA)
        
    def define_neighbor_attributes(self):
        for row in range(self.rows):
            for col in range(self.cols):
                tile: Tile = self.tiles[row * self.cols + col]
                self.add_neighbors(row, col, tile) 
                tile.calculate_height_contours() 

    def add_neighbors(self, row, col, tile: Tile):
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

        self.generate_frequency()

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
    
    def generate_frequency(self):
        frequency_max = 7
        self.frequency_x = random.random() * frequency_max
        self.frequency_y = random.random() * frequency_max
        
        logging.info(f"Frequency parameters: [{self.frequency_x}, {self.frequency_y}]")
    
    def generate_noise_value(self, row: int, col: int, param1: int, param2: int) -> float:
        x = row / param1
        y = col / param2
        match(WORLD_GENERATION_MODE):
            case "Perlin":
                value = pnoise2(x, y)
            case "Perlin Summation":
                base_noise = pnoise2(x, y)
                detail_noise = pnoise2(x * self.frequency_x, y * self.frequency_y)
                value = base_noise + detail_noise
            case "Random":
                value = random.random()
            case _:
                value = pnoise2(row / param1, col / param1)
        
        value += .4
        value *= 10
        # if value <= 0:
        #     value **= 3
        # else:   
        #     value **= 2
                    
        return value
    
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