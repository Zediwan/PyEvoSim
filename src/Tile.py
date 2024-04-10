from __future__ import annotations
from typing import List, Optional
import random
import math

from pygame import Rect, Surface, SRCALPHA, draw, Color

from config import *
from direction import Direction

"""
The Tile class represents a tile in a game. It is an abstract base class (ABC) that provides common functionality for different types of tiles.

Attributes:
    rect (pygame.Rect): The rectangle representing the tile's position and size.
    cell_size (int): The size of the tile in pixels.
    neighbours (dict): A dictionary of the tile's neighboring tiles, with directions as keys and Tile objects as values.

Methods:
    update(): Abstract method that should be implemented by subclasses to update the tile's state.
    draw(screen: pygame.Surface): Draws the tile on the screen.
    add_neighbor(direction: Direction, tile: Tile): Adds a neighbor tile in the specified direction.
    get_neighbor(direction: Direction) -> Tile: Returns the neighbor tile in the specified direction.
    get_directions() -> list[Direction]: Returns a list of directions to the tile's neighbors.
    get_random_neigbor() -> Tile: Returns a random neighbor tile.
"""
class Tile():
    ### Water
    AMOUNT_OF_WATER_FOR_ONE_HEIGHT_LEVEL = 10
    SEA_LEVEL = 0
    MIN_WATER_HEIGHT_FOR_DROWING: float = 3
    MIN_WATER_VALUE: float = 0
    MAX_WATER_VALUE: float = float("inf")
    
    MIN_WATER_COLOR = Color(204, 229, 233, ground_alpha)
    #MAX_WATER_COLOR = Color(26, 136, 157, ground_alpha)
    MAX_WATER_COLOR =  Color("dodgerblue4")
    
    #################################################################################################################################
    
    ### Land
    MIN_GROWTH_VALUE: float = 0
    MAX_GROWTH_VALUE: float = 10
        
    BASE_GROWTH_RATE: float = 1
    BASE_GROWTH_CHANCE: float = .01
    GROWTH_RATE_INCREASE_BY_WATER: float = 5
    GROWTH_CHANCE_INCREASE_BY_WATER: float = .05
    GROW_FOR_YOURSELF_UNTIL_THRESHOLD: float = .5
    NATURAL_GROWTH_LOSS_PERCENTAGE_THRESHOLD: float = .9
    NATURAL_GROWTH_LOSS_CHANCE: float = .02
    NATURAL_GROWTH_LOSS_AMOUNT: float = 1
    
    MIN_GRASS_COLOR: Color = Color(235, 242, 230, ground_alpha)
    MAX_GRASS_COLOR: Color = Color(76, 141, 29, ground_alpha)
    
    # Soil
    DIRT_COLOR: Color = Color(155, 118, 83, ground_alpha)
    SAND_COLOR: Color = Color("lightgoldenrod")
    
    # Mountains
    MIN_HEIGHT_FOR_MOUNTAIN_LAKE:float = 20
    MOUNTAIN_WATER_SPAWN_CHANCE: float = 1
    MOUNTAIN_TOP_COLOR: Color = Color("white")
    MOUNTAIN_FLOOR_COLOR: Color = Color("azure4")
    
    #### TODO: improve names
    LAND_DAMAGE: int = 50
    ####
    
    def __init__(self, rect: Rect, tile_size: int, height: int = 0,
                 organisms = None,
                 starting_growth_level: Optional[float] = None
                 ):
        # Tile
        self.rect: Rect = rect
        self.tile_size: int = tile_size
        self.neighbors: dict[Direction, Tile] = {}
        
        # Height
        self.height: float = height
        self.height_contours = []  
              
        # Organisms
        from organism import Organism
        if organisms:
            self.organisms: List[Organism] = organisms
        else:
            self.organisms: List[Organism] = []
                    
        # Growth
        if starting_growth_level:
            self.growth: float = starting_growth_level
        else:
            self.growth: float = random.random() * self.MAX_GROWTH_VALUE
        
        # Water      
        self.water: float = 0
        if height <= self.SEA_LEVEL:
            self.water = self.AMOUNT_OF_WATER_FOR_ONE_HEIGHT_LEVEL * (abs(height) + 1)
        
        # Drawing
        self.color: Color = Color(0,0,0,0)
        self.temp_surface: Surface = Surface(self.rect.size, SRCALPHA)

    def update(self):        
        if self.organisms:
            for org in self.organisms:
                org.update()
                    
        self.update_growth()

    def update_growth(self):
        # Growth Update # TODO: refactor into separate method
        growth_chance = self.BASE_GROWTH_CHANCE
        growth_rate = self.BASE_GROWTH_RATE
    
        growth_chance -= self.calculate_growth_height_penalty(growth_chance)
        
        if random.random() < growth_chance:
            if self.growth_ratio() < self.GROW_FOR_YOURSELF_UNTIL_THRESHOLD:
                tile_to_grow = self
            else:
                options = self.get_neighbors()
                options.append(self)
                tile_to_grow = random.choice(options)
                
            tile_to_grow.growth += growth_rate
            tile_to_grow.growth = pygame.math.clamp(tile_to_grow.growth, tile_to_grow.MIN_GROWTH_VALUE, tile_to_grow.MAX_GROWTH_VALUE)
        
        if self.growth_ratio() > self.NATURAL_GROWTH_LOSS_PERCENTAGE_THRESHOLD:
            if random.random() < self.NATURAL_GROWTH_LOSS_CHANCE:
                self.growth -= self.NATURAL_GROWTH_LOSS_AMOUNT
                self.growth = pygame.math.clamp(self.growth, self.MIN_GROWTH_VALUE, self.MAX_GROWTH_VALUE)

    def calculate_growth_height_penalty(self, growth_chance: float) -> float:
        height_threshold_for_growth_penalty = 20
        if self.height > height_threshold_for_growth_penalty:
            return -(growth_chance * (self.height / 100))
        else:
            return 0

    def draw(self, screen: Surface):
        if self.organisms:
            for org in self.organisms:
                org.draw(screen)
        else:
            self.set_color()
            self.temp_surface.fill(self.color)
        
        screen.blit(self.temp_surface, (self.rect.left, self.rect.top))

        from config import draw_water_level
        if draw_water_level:
            self.draw_stat(self.water, screen)

        from config import draw_growth_level
        if draw_growth_level:
            self.draw_stat(self.growth, screen)

        from config import draw_height_level
        if draw_height_level:
            self.draw_stat(self.height, screen)

        from config import draw_height_lines
        if draw_height_lines:
            self.draw_height_contours(screen)

    def set_color(self):
        growth_ratio = self.growth_ratio()
        water_ratio = pygame.math.clamp(self.water / 10, 0, 1)
        height_ratio = pygame.math.clamp(self.height / 50, 0, 1)
        
        growth_color = self.DIRT_COLOR.lerp(self.MIN_GRASS_COLOR, growth_ratio).lerp(self.MAX_GRASS_COLOR, growth_ratio)
        water_color = self.MIN_WATER_COLOR.lerp(self.MAX_WATER_COLOR, water_ratio)
        height_color = self.MOUNTAIN_FLOOR_COLOR.lerp(self.MOUNTAIN_TOP_COLOR, height_ratio)

        self.color = growth_color.lerp(water_color, pygame.math.clamp(water_ratio, 0, .75)).lerp(height_color, pygame.math.clamp(height_ratio, 0, .5))

    def draw_stat(self, stat: float, screen: Surface):
        stat_alpha = 255
        text = font.render(str(math.floor(stat)), True, (0, 0, 0))
        screen.set_alpha(stat_alpha)
        self._render_text_centered(screen, text)

    def _render_text_centered(self, screen: Surface, text: Surface):
        """
        Renders the given text surface centered on the tile.

        Args:
            screen (Surface): The surface on which the text will be rendered.
            text (Surface): The text surface to be rendered.
        """
        center_x = self.rect.x + self.rect.width // 2
        center_y = self.rect.y + self.rect.height // 2
        text_x = center_x - text.get_width() // 2
        text_y = center_y - text.get_height() // 2
        screen.blit(text, (text_x, text_y))
     
    def calculate_height_contours(self):
        """
        Calculates the contour lines based on the current height and neighbors
        and stores them in self.height_contours.
        """    
        for direction, neighbor in self.neighbors.items():
            if neighbor.height != self.height:
                color = Color(0, 0, 0)  # Adjust as needed
                thickness = pygame.math.clamp(abs(math.floor(neighbor.height - self.height)), 0, 8)  # Example logic
            
                if direction in [Direction.NORTH, Direction.SOUTH]:
                    start_pos = self.rect.topleft if direction == Direction.NORTH else self.rect.bottomleft
                    end_pos = self.rect.topright if direction == Direction.NORTH else self.rect.bottomright
                else:
                    start_pos = self.rect.topright if direction == Direction.EAST else self.rect.topleft
                    end_pos = self.rect.bottomright if direction == Direction.EAST else self.rect.bottomleft
            
                self.height_contours.append((start_pos, end_pos, color, thickness))
        print("Calculated height contours")

    def draw_height_contours(self, screen: Surface):
        """
        Draw height contours on the screen.

        Args:
            screen (Surface): A Surface object representing the screen.

        Returns:
            None
        """
        for start_pos, end_pos, color, thickness in self.height_contours:
            draw.line(screen, color, start_pos, end_pos, thickness)
        
    def leave(self, organism):
        self.organisms.remove(organism)
        
    def enter(self, organism):
        self.organisms.append(organism)
        
        assert organism.tile == self, "Tiles Organism and Organisms tile are not equal."
        
    def is_occupied(self) -> bool:
        return bool(self.organisms)

    def add_neighbor(self, direction: Direction, tile: Tile):
        self.neighbors[direction] = tile

    def get_directions(self) -> List[Direction]:
        return list(self.neighbors.keys())
    
    def get_neighbors(self) -> List[Tile]:
        return list(self.neighbors.values())

    def get_neighbor(self, direction: Direction) -> Tile|None:
        return self.neighbors.get(direction, None)

    def get_random_neigbor(self) -> Tile:
        return self.neighbors[random.choice(self.get_directions())]
    
    def get_random_unoccupied_neighbor(self) -> Tile|None:
        unoccupied_neighbors = [tile for tile in self.neighbors.values() if not tile.is_occupied()]

        if not unoccupied_neighbors:
            return None
        return random.choice(unoccupied_neighbors)
    
    def is_neighbor(self, tile: Tile) -> bool:  
        if not self.neighbors.values():
            return False
        return tile in self.neighbors.values()
    
    def growth_ratio(self) -> float:
        return pygame.math.clamp(self.growth / self.MAX_GROWTH_VALUE, 0, 1)