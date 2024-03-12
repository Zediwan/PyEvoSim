import math
from pygame import sprite, Surface
from sun import Sun
from tile import Tile
from animal import Animal
from config import *
import random
from noise import pnoise2

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
    
    highest_tile = float("inf")
    lowest_tile = float("-inf")
    
    def __init__(self, height : int, width : int, tile_size : int):
        sprite.Sprite.__init__(self)
        self.tile_size = tile_size
        self.height, self.width = World.adjust_dimensions(height, width, self.tile_size)
        self.rows = math.floor(self.height / self.tile_size)
        self.cols = math.floor(self.width / self.tile_size)
        
        if WORLD_GENERATION_PARAM1 is not None and WORLD_GENERATION_PARAM2 is not None:
            self.world_gen_param1: int = WORLD_GENERATION_PARAM1
            self.world_gen_param2: int = WORLD_GENERATION_PARAM2
        else:
            self.world_gen_param1 = random.randint(-150, 150) 
            self.world_gen_param2  = 100 - abs(self.world_gen_param1)  # Inversely proportional example
            while abs(self.world_gen_param1) < 40: 
                self.world_gen_param1 = random.randint(-150, 150) 
            while abs(self.world_gen_param2) < 40:
                self.world_gen_param2  = random.randint(-150, 150) 
            print(f"Perlin noise parameters: [{self.world_gen_param1}, {self.world_gen_param2}]")
        
        self.tiles = [self.create_tile(col, row) for row in range(self.rows) for col in range(self.cols)]
        self.sun = Sun()
        self.add_cell_neighbours()
        self.create_potential_lake_areas()
        
    def update(self):
        self.sun.update()
        random.shuffle(self.tiles)
        for tile in self.tiles:
            tile.update()
        
    def draw(self, screen : Surface):
        temp_surface = Surface((self.cols * self.tile_size, self.rows * self.tile_size), pygame.SRCALPHA)
        for tile in self.tiles:
            tile.draw(temp_surface)
            
        self.sun.draw(temp_surface)
        screen.blit(temp_surface, (0, 0))
        
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
    
    def is_border_tile(self, row: int, col: int) -> bool:
        return (row == 0 or col == 0 or row == self.rows - 1 or col == self.cols - 1)
    
    def create_tile(self, col: int, row: int) -> Tile:
        rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
                
        height = self.generate_noise_value(row, col, self.world_gen_param1, self.world_gen_param2)
        height += .20
        height *= 10
        if height < 0:
            height = -(height**2)
        else:   
            height **= 2
        height = math.floor(height)
        is_border = self.is_border_tile(row, col)
        
        self.highest_tile = max(self.highest_tile, height)
        self.lowest_tile = min(self.lowest_tile, height)
    
        if height < WATER_PERCENTAGE:
            tile : Tile = Tile(rect, self.tile_size, height=height, starting_growth_level= random.randint(Tile.MAX_GROWTH_VALUE-2, Tile.MAX_GROWTH_VALUE))
            # wA = Animal.MAX_ANIMAL_WATER_AFFINITY - 2
            # lA = Animal.MIN_ANIMAL_LAND_AFFINITY + 5
            # if random.random() <= STARTING_WATER_ANIMAL_PERCENTAGE:
            #     Animal(tile, starting_land_affinity=lA, starting_water_affinity=wA)
        else:
            tile : Tile = Tile(rect, self.tile_size, height=height, starting_growth_level=random.randint(Tile.MAX_GROWTH_VALUE-2, Tile.MAX_GROWTH_VALUE))
            # wA = Animal.MIN_ANIMAL_WATER_AFFINITY + 2
            # lA = Animal.MAX_ANIMAL_LAND_AFFINITY - 2
            # if random.random() <= STARTING_LAND_ANIMAL_PERCENTAGE:
            #     Animal(tile, starting_land_affinity=lA, starting_water_affinity=wA)
        
        tile.is_border_tile = is_border 
        return tile
    
    def create_potential_lake_areas(self):
        potential_lake_centers = []
        # Step 1: Identify potential lake center tiles
        for tile in self.tiles:
            if self.is_potential_lake_location(tile):
                potential_lake_centers.append(tile)
        
        # Step 2: Select a subset of these tiles to become lakes
        MAX_LAKES = 10
        selected_centers = random.sample(potential_lake_centers, k=min(len(potential_lake_centers), MAX_LAKES))
        
        # Step 3 & 4: Determine lake size and shape, and lower the height of the lake tiles
        for center_tile in selected_centers:
            lake_tiles = [center_tile]
            expansion_chance = 0.5  # 50% chance to expand in any direction
            lake_size = random.randint(10, 15)  # Randomize the target size of the lake

            while len(lake_tiles) < lake_size:
                new_lake_tiles = []
                for tile in lake_tiles:
                    for neighbor in tile.get_neighbors():  # Assuming a method to get neighboring tiles
                        if neighbor not in lake_tiles and neighbor not in new_lake_tiles:
                            if random.random() < expansion_chance:
                                new_lake_tiles.append(neighbor)
                lake_tiles.extend(new_lake_tiles)
                if not new_lake_tiles:  # Stop if no new tiles were added
                    break

            # Apply lake properties to the selected tiles
            for tile in lake_tiles:
                tile.is_lake = True
                LAKE_DEPTH_ADJUSTMENT = 2
                tile.height -= LAKE_DEPTH_ADJUSTMENT
                max_possible_starting_water = 10 * LAKE_DEPTH_ADJUSTMENT
                tile.water = pygame.math.clamp(random.random(), .8, .9) * max_possible_starting_water
                tile.tile_hardness = 3
    
    def is_potential_lake_location(self, tile):
        # Implement logic to determine if a tile is a good candidate for a lake
        # This could involve checking the surrounding tiles' heights, terrain types, etc.
        return tile.height > Tile.MOUNTAIN_LAKE_MIN_HEIGHT or not Tile.START_WITH_WATER_TILES
    
    def generate_noise_value(self, row: int, col: int, param1: int, param2: int) -> float:
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
                return pnoise2(row / param1, col / param1)
            case "Perlin Summation":
                base_noise = pnoise2(row / param1, col / param2)
                detail_noise = pnoise2(row / (param1 * 0.5), col / (param2 * 0.5)) * 0.5  # Higher frequency, lower amplitude
                return base_noise + detail_noise
            case "Random":
                return random.random()
            case _:
                return pnoise2(row / param1, col / param1)
        self.sun.draw(screen)

    
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