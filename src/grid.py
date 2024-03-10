import math
import random
from noise import pnoise2
from pygame import sprite, Surface
from entities.animal import Animal
from entities.organism import Organism
from Tile import Tile
from config import *

class Grid(sprite.Sprite):
    """
    The Grid class represents a grid of tiles in a game. It is an abstract base class (ABC) that provides common functionality for grids.

    Attributes:
        rows (int): The number of rows in the grid.
        cols (int): The number of columns in the grid.
        tile_size (int): The size of each tile in the grid.
        tiles (list[Tile]): The list of tiles in the grid.

    Methods:
        __init__(rows: int, cols: int, tile_size: int): Initializes a new Grid object with the specified number of rows, columns, and tile size.
        update(): Updates the state of all tiles in the grid.
        draw(screen: pygame.Surface): Draws all tiles in the grid on the specified screen surface.
        create_tile(col: int, row: int) -> Tile: Abstract method that should be implemented by subclasses to create a new tile at the specified column and row.
        add_cell_neighbours(): Adds the neighboring tiles for each tile in the grid.
        is_border_tile(row: int, col: int) -> bool: Checks if the tile at the specified row and column is a border tile.

    Note:
        This class is an abstract base class (ABC) and should not be instantiated directly. Subclasses should implement the create_tile method to create specific types of tiles for the grid.
    """
    highest_tile = float("inf")
    lowest_tile = float("-inf")
    
    def __init__(self, rows : int, cols : int, tile_size : int):
        sprite.Sprite.__init__(self)
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        
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
        self.add_cell_neighbours()
        self.create_potential_lake_areas()
        self.calculate_height_lines()
    
    def update(self):
        """
        Updates the state of all tiles in the grid.

        This method shuffles the list of tiles randomly and then calls the update method on each tile. The update method is responsible for updating the state of the tile based on the game logic.

        Parameters:
            None

        Returns:
            None

        Example:
            grid = Grid(10, 10, 20)
            grid.update()
        """
        random.shuffle(self.tiles)
        for tile in self.tiles:
            tile.update()
            
    def draw(self, screen : Surface):
        """
        Draws all tiles in the grid on the specified screen surface.

        This method creates a temporary surface with the size of the grid (number of columns multiplied by tile size, number of rows multiplied by tile size). It then iterates over each tile in the grid and calls the draw method on each tile, passing the temporary surface as the argument. The draw method of each tile is responsible for drawing the tile on the temporary surface. Finally, the temporary surface is blitted onto the specified screen surface at the position (0, 0).

        Parameters:
            screen (pygame.Surface): The screen surface on which to draw the tiles.

        Returns:
            None

        Example:
            grid = Grid(10, 10, 20)
            screen = pygame.display.set_mode((800, 600))
            grid.draw(screen)
        """
        temp_surface = Surface((self.cols * self.tile_size, self.rows * self.tile_size), pygame.SRCALPHA)
        for tile in self.tiles:
            tile.draw(temp_surface)
        screen.blit(temp_surface, (0, 0))
    
    def add_cell_neighbours(self):
        """
        Adds the neighboring tiles for each tile in the grid.

        This method iterates over each tile in the grid and adds the neighboring tiles to the 'neighbours' dictionary of each tile. The neighboring tiles are determined based on the current row and column of the tile. The 'neighbours' dictionary is then assigned to the 'neighbours' attribute of the tile.

        Parameters:
            None

        Returns:
            None

        Example:
            grid = Grid(10, 10, 20)
            grid.add_cell_neighbours()
        """
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.tiles[row * self.cols + col]
                neighbours = {}
                if row > 0:
                    tile.add_neighbor(Direction.NORTH, self.tiles[(row - 1) * self.cols + col])
                if col < self.cols - 1:
                    tile.add_neighbor(Direction.EAST, self.tiles[row * self.cols + col + 1])
                if row < self.rows - 1:
                    tile.add_neighbor(Direction.SOUTH, self.tiles[(row + 1) * self.cols + col])
                if col > 0:
                    tile.add_neighbor(Direction.WEST, self.tiles[row * self.cols + col - 1])
    
    def calculate_height_lines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.tiles[row * self.cols + col]
                tile.calculate_height_contours()
    
    def is_border_tile(self, row: int, col: int) -> bool:
        """
        Checks if the tile at the specified row and column is a border tile.

        Parameters:
            row (int): The row index of the tile.
            col (int): The column index of the tile.

        Returns:
            bool: True if the tile is a border tile, False otherwise.

        Example:
            grid = Grid(10, 10, 20)
            is_border = grid.is_border_tile(0, 0)
            print(is_border)  # Output: True
        """
        return (row == 0 or col == 0 or row == self.rows - 1 or col == self.cols - 1)
    
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
            wA = Animal.MAX_ANIMAL_WATER_AFFINITY - 2
            lA = Animal.MIN_ANIMAL_LAND_AFFINITY + 5
            if random.random() <= STARTING_WATER_ANIMAL_PERCENTAGE:
                Animal(tile, starting_land_affinity=lA, starting_water_affinity=wA)
        else:
            tile : Tile = Tile(rect, self.tile_size, height=height, starting_growth_level=random.randint(Tile.MAX_GROWTH_VALUE-2, Tile.MAX_GROWTH_VALUE))
            wA = Animal.MIN_ANIMAL_WATER_AFFINITY + 2
            lA = Animal.MAX_ANIMAL_LAND_AFFINITY - 2
            if random.random() <= STARTING_LAND_ANIMAL_PERCENTAGE:
                Animal(tile, starting_land_affinity=lA, starting_water_affinity=wA)
        
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