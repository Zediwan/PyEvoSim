from typing import List
from pygame import Rect, sprite, Surface

from pygame.math import clamp, lerp
from math import pow, floor
from random import random, shuffle, choice, randint

from config import *
from custom_group import Custom_Group
from plant import Plant
from tile import Tile
from animal import Animal
from direction import Direction
from noise import snoise2

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class World(sprite.Sprite):
    highest_height: float = 0
    lowest_height: float = 0
    
    def __init__(self, height : int, width : int, tile_size : int):
        sprite.Sprite.__init__(self)
        
        height, width = World.adjust_dimensions(height, width, tile_size)
        self.tile_size = tile_size
        self.rows = floor(height / tile_size)
        self.cols = floor(width / tile_size)
        self.rect = Rect(0, 0, width, height)
        self.surface = Surface(self.rect.size, pygame.SRCALPHA)
        
        self.generate_frequency()
        
        self.tiles = Custom_Group()
        self.tile_generation()
        self.world_post_processing()
   
    def update(self):
        self.tiles.update()
                    
    def draw(self, screen : Surface):
        self.tiles.draw(self.surface)
        screen.blit(self.surface, self.rect)  
    
    # TILES
    def world_post_processing(self):
        self.add_neighbors() 
        self.create_river()
    
    def tile_generation(self):
        for row in range(self.rows):
            for col in range(self.cols):
                t = self.create_tile(row = row, col = col)
                self.tiles.add(t)
    
    def create_tile(self, row: int, col: int) -> Tile:     
        height, moisture = self.generate_noise_values(row, col)
        
        tile : Tile = Tile(
            pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size), 
            height = height, 
            moisture = moisture, 
            is_border = self.is_border_tile(row = row, col = col)
            )
            
        self.spawn_animal(tile,
                          chance_to_spawn = STARTING_ANIMAL_PERCENTAGE, 
                          chance_of_land_animals = STARTING_LAND_ANIMAL_PERCENTAGE, 
                          chance_of_water_animals = STARTING_WATER_ANIMAL_PERCENTAGE
                          )
        self.spawn_plant(tile)
            
        return tile
    
    def add_neighbors(self):
        for tile in self.tiles:
            neighbors = pygame.sprite.spritecollide(tile, self.tiles, False)
            for n in neighbors:
                tile.add_neighbor(n)
    
    # TODO rethink this in the sense of infinite sized worlds
    def is_border_tile(self, row: int, col: int) -> bool:
        return (row == 0 or col == 0 or row == self.rows - 1 or col == self.cols - 1)
    
    # ORGANSIM SPAWNING
    def spawn_animals(self, chance_to_spawn: float = 1, chance_of_land_animals: float = 1, chance_of_water_animals: float = 1):
        for tile in self.tiles:
            if not tile.has_animal():
                self.spawn_animal(tile, 
                                chance_to_spawn = chance_to_spawn,
                                chance_of_land_animals = chance_of_land_animals,
                                chance_of_water_animals = chance_of_water_animals
                                )
    
    def spawn_animal(self, tile: Tile, chance_to_spawn: float = 1, chance_of_land_animals: float = 1, chance_of_water_animals: float = 1):
        if random() <= chance_to_spawn:
            if tile.water > 0:
                self.spawn_water_animal(tile, chance_of_water_animals)
            else:
                self.spawn_land_animal(tile, chance_of_land_animals)
                
    def spawn_plant(self, tile: Tile, chance_to_spawn: float = 1):
        if random() <= chance_to_spawn:
            Plant(tile)
            
    def spawn_water_animal(self, tile: Tile, chance_to_spawn: float = 1):
        wA = Animal.MAX_ANIMAL_WATER_AFFINITY - 2
        lA = Animal.MIN_ANIMAL_LAND_AFFINITY + 5
        if random() <= chance_to_spawn:
            Animal(tile, starting_land_affinity=lA, starting_water_affinity=wA)
            
    def spawn_land_animal(self, tile: Tile, chance_to_spawn: float = 1):
        wA = Animal.MIN_ANIMAL_WATER_AFFINITY + 2
        lA = Animal.MAX_ANIMAL_LAND_AFFINITY - 2
        if random() <= chance_to_spawn:
            Animal(tile, starting_land_affinity=lA, starting_water_affinity=wA)
      
       
    # WORLD GENERATION
    def generate_frequency(self):
        #TODO add a slider for this in world gen mode
        frequency_max = 7 #TODO make this a setting
        self.frequency_x = random() * frequency_max
        self.frequency_y = random() * frequency_max
        #TODO make use of the wavelength
        self.wavelentgh_x = 1/self.frequency_x
        self.wavelentgh_y = 1/self.frequency_y
        
        logging.info(f"Frequency parameters: [{self.frequency_x}, {self.frequency_y}]")
    
    def generate_noise_values(self, row: int, col: int) -> tuple[float, float]:
        x = row / self.frequency_x  # TODO rethink this to use different freq than moisture
        y = col / self.frequency_y  # TODO rethink this to use different freq than moisture
        freq_x1 = 1
        freq_y1 = 1
        freq_x2 = 2
        freq_y2 = 2
        freq_x3 = 4
        freq_y3 = 4
        scale_1 = 1
        scale_2 = .5
        scale_3 = .25
        offset_x1 = 0
        offset_y1 = 0
        offset_x2 = 4.7
        offset_y2 = 2.3
        offset_x3 = 19.1
        offset_y3 = 16.6
                
        height = (
            snoise2(x * freq_x1 + offset_x1, y * freq_y1 + offset_y1) * scale_1 + 
            snoise2(x * freq_x2 + offset_x2, y * freq_y2 + offset_y2) * scale_2 +
            snoise2(x * freq_x3 + offset_x3, y * freq_y3 + offset_y3) * scale_3
            )
        height /= (scale_1 + scale_2 + scale_3) # Normalize back in range -1 to 1
        
        # Rescale the height to values between 0 and 1
        height += 1
        height /= 2
        
        island_mode = False
        if island_mode:
            nx =  2 * col * self.tile_size / self.rect.width - 1
            ny = 2 * row * self.tile_size / self.rect.height - 1
            d = 1 - (1 - pow(nx, 2)) * (1 - pow(ny, 2))
            mix = .5
            height = lerp(height, 1 - d, mix)
          
        terraces = False
        if terraces:
            n = 5
            height = round(height * n) / n
        else:
            power = 2 #TODO make this a slider in the settings
            fudge_factor = 1.2 # Should be a number near 1
            height = clamp(pow(height * fudge_factor, power), 0, 1)
                
        moisture = (snoise2(x * self.frequency_x, y * self.frequency_y)+1)/2
        
        assert 0 <= moisture <= 1
        assert 0 <= height <= 1
        
        return height, moisture
    
    def create_river(self, tile_to_start: Tile | None = None):
        if not tile_to_start:
            for tl in sorted(self.tiles.sprites(), key = lambda tile: tile.height, reverse = True):
                if random() <= .1:
                    tile = tl
        else:
            tile = tile_to_start
        
        while tile != None and tile.steepest_decline_neighbor != None and tile.water == 0:
            tile.water = lerp(10, 1, tile.height)
            tile: Tile = tile.steepest_decline_neighbor
            river_branch_chance = 0.2
            if random() <= river_branch_chance and tile != None and tile.steepest_decline_neighbor != None:
                branch_tile = tile.get_random_neighbor()              
                self.create_river(branch_tile)
    
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