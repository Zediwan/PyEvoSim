from datetime import datetime
from pygame import sprite
from pygame.math import clamp, lerp
from math import pow, floor
from random import random, randint
from noise import snoise2
import logging

from settings.database_settings import database_csv_filename
from settings.noise_settings import *
from settings.config import *
from entities.plant import Plant
from world.tile import Tile
from entities.animal import Animal
from helper.direction import Direction
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class World(sprite.Sprite):
    def __init__(self, height : int, width : int, tile_size : int):
        sprite.Sprite.__init__(self)
        self.tile_size = tile_size
        self.height, self.width = World.adjust_dimensions(height, width, self.tile_size)
        self.shape = pygame.Rect(0, 0, self.width, self.height)
        self.rows = floor(self.height / self.tile_size)
        self.cols = floor(self.width / self.tile_size)
        
        self.generate_frequency()
        
        self.tiles: list[Tile] = []
        for row in range(self.rows):
            for col in range(self.cols):
                self.tiles.append(self.create_tile(row, col))
        self.add_neighbors()
        #self.create_river()
        
        database_csv_filename = f'databases/organism_database_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'
        
    def update(self):
        for tile in self.tiles:
            tile.update()
            #self.handle_border_update(tile)
            self.handle_coast_update(tile)
            
            chance_to_spawn_plant_anywhere = .00005
            if not tile.has_plant() and random() <= tile.moisture * chance_to_spawn_plant_anywhere:
                self.spawn_plant(tile)

    def handle_coast_update(self, tile):
        if tile.is_coast and not tile.has_animal():
            chance_to_spawn_plant_at_coast = .001
            if random() <= chance_to_spawn_plant_at_coast and not tile.has_plant():
                self.spawn_plant(tile)

    def handle_border_update(self, tile: Tile):
        if tile.is_border and not tile.has_water and not tile.has_animal():
            chance_to_spawn_animal_at_border = .00001
            chance_to_spawn_plant_at_border = .0001
            if random() <= chance_to_spawn_animal_at_border and not tile.has_animal():
                self.spawn_animal(tile)
            if random() <= chance_to_spawn_plant_at_border and not tile.has_plant():
                self.spawn_plant(tile)
                    
    def draw(self):
        for tile in self.tiles:
            tile.draw() 
    
    def is_border_tile(self, row: int, col: int) -> bool:
        return (row == 0 or col == 0 or row == self.rows - 1 or col == self.cols - 1)
    
    # def create_river(self, tile_to_start: Tile | None = None):
    #     if not tile_to_start:
    #         tile = self.highest_tile
    #     else:
    #         tile = tile_to_start
    #     while tile != None and tile.steepest_decline_direction != None and tile.water <= 0:
    #         tile.water = lerp(10, 1, tile.height/self.highest_tile.height)
    #         tile: Tile | None = tile.get_neighbor(tile.steepest_decline_direction)
    #         river_branch_chance = 0.2 * random()
    #         if random() < river_branch_chance and tile != None and tile.steepest_decline_direction != None:
    #             branch_of = tile.get_neighbor(choice(Direction.get_neighboring_directions(tile.steepest_decline_direction)))
    #             self.create_river(branch_of)
    
    def create_tile(self, row: int, col: int) -> Tile:
        rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
        height, moisture = self.generate_noise_values(row, col)
        
        tile : Tile = Tile(rect, self.tile_size, height=height, moisture = moisture, is_border = self.is_border_tile(row = row, col = col))
        
        if not tile.has_water:
            self.spawn_animal(tile, chance_to_spawn = STARTING_ANIMAL_SPAWNING_CHANCE)
            self.spawn_plant(tile, chance_to_spawn = STARTING_PLANT_SPAWNING_CHANCE)
            
        return tile
    
    def spawn_animals(self, chance_to_spawn: float = 1):
        for tile in self.tiles:
            self.spawn_animal(tile, chance_to_spawn = chance_to_spawn)
    
    def spawn_animal(self, tile: Tile, chance_to_spawn: float = 1):
        if random() <= chance_to_spawn and not tile.has_water and not tile.has_animal():
            Animal(tile)
                
    def spawn_plant(self, tile: Tile, chance_to_spawn: float = 1):
        if random() <= chance_to_spawn and not tile.has_water and not tile.has_plant():
            Plant(tile)

    def add_neighbors(self):
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
    
    def generate_frequency(self):
        #TODO add a slider for this in world gen mode
        frequency_max = 7 #TODO make this a setting
        self.frequency_x = random() * frequency_max
        self.frequency_y = random() * frequency_max
        self.wavelentgh_x = 1/self.frequency_x
        self.wavelentgh_y = 1/self.frequency_y
        
        RANDOM_VALUE_RANGE = (-150, 150)
        MIN_PARAM_VALUE_THRESHOLD = 40
        
        self.world_gen_param1 = randint(*RANDOM_VALUE_RANGE) 
        while True:
            if abs(self.world_gen_param1) >= MIN_PARAM_VALUE_THRESHOLD:
                break
            self.world_gen_param1 = randint(*RANDOM_VALUE_RANGE) 
            
        self.world_gen_param2  = 100 - abs(self.world_gen_param1)  # Inversely proportional example
        while True:
            if abs(self.world_gen_param2) >= MIN_PARAM_VALUE_THRESHOLD:
                break
            self.world_gen_param2  = randint(*RANDOM_VALUE_RANGE) 
        
        logging.info(f"Perlin noise parameters: [{self.world_gen_param1}, {self.world_gen_param2}]")
        logging.info(f"Frequency parameters: [{self.frequency_x}, {self.frequency_y}]")
    
    def generate_noise_values(self, row: int, col: int) -> tuple[float, float]:
        x = row / self.world_gen_param1
        y = col / self.world_gen_param2
                
        height = (
            snoise2((x * freq_x1) + offset_x1, (y * freq_y1) + offset_y1) * scale_1 + 
            snoise2((x * freq_x2) + offset_x2, (y * freq_y2) + offset_y2) * scale_2 +
            snoise2((x * freq_x3) + offset_x3, (y * freq_y3) + offset_y3) * scale_3
            )
        height /= (scale_1 + scale_2 + scale_3) # Normalize back in range -1 to 1
        
        height += 1
        height /= 2
        
        island_mode = False
        if island_mode:
            nx =  2 * col * self.tile_size / self.width - 1
            ny = 2 * row * self.tile_size / self.height - 1
            d = 1 - (1 - pow(nx, 2)) * (1 - pow(ny, 2))
            mix = .7
            height = lerp(height, 1 - d, mix)
          
        terraces = False
        if terraces:
            n = 5
            height = round(height * n) / n
        else:
            power = 2 #TODO make this a slider in the settings
            is_neg = height < 0
            fudge_factor = 1.2 # Should be a number near 1
            height = clamp(pow(abs(height * fudge_factor), power), 0, 1)
            if is_neg:
                height *= -1 
        
        moisture = (snoise2(x * self.wavelentgh_x, y * self.wavelentgh_y)+1)/2
        
        assert 0 <= height <= 1
        assert 0 <= moisture <= 1
        
        return height, moisture
    
    def get_tile(self, x: int, y: int) -> Tile:
        """
        Retrieves the tile at the specified x and y coordinates.

        Args:
        - x (int): The x-coordinate of the point.
        - y (int): The y-coordinate of the point.

        Returns:
        - Tile: The tile at the given coordinates.
        """
        col = x // self.tile_size
        row = y // self.tile_size
        if row < self.rows and col < self.cols:
            return self.tiles[(row * self.cols) + col]
        else:
            raise ValueError("Coordinates are out of the world bounds.")
    
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