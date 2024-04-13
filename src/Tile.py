from __future__ import annotations
from typing import List, Optional
import random
from math import floor

from pygame import Rect, Surface, SRCALPHA, draw, Color, math
from sklearn import neighbors

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
    AMOUNT_OF_WATER_FOR_ONE_HEIGHT_LEVEL: float = 10
    SEA_LEVEL: float = 0
    MIN_WATER_HEIGHT_FOR_DROWING: float = 3
    MIN_WATER_VALUE: float = 0
    MAX_WATER_VALUE: float = float("inf")
    
    MIN_WATER_COLOR = Color(204, 229, 233, ground_alpha)
    MAX_WATER_COLOR = Color(26, 136, 157, ground_alpha)
    #MAX_WATER_COLOR =  Color("dodgerblue4")
    
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
    MOUNTAIN_TOP_COLOR: Color = Color("white")
    MOUNTAIN_FLOOR_COLOR: Color = Color("azure4")
    
    #### TODO: improve names
    LAND_DAMAGE: float = 10
    ####
    
    def __init__(self, rect: Rect, tile_size: int, height: float = 0,
                 animal = None,
                 plant = None,
                 is_border = False
                 ):
        # Tile
        self.rect: Rect = rect
        self.tile_size: int = tile_size
        self.neighbors: dict[Direction, Tile] = {}
        
        # Height
        self.height: float = height
        self.height_contours = []  
              
        # Organisms
        from animal import Animal
        self.animal: Animal | None = animal
            
        from plant import Plant
        self.plant: Plant | None = plant
        
        # Water      
        self.water: float = 0
        if self.height <= self.SEA_LEVEL:
            self.water = self.AMOUNT_OF_WATER_FOR_ONE_HEIGHT_LEVEL * (abs(height) + 1)
        
        # Drawing
        self.color: Color = self.DIRT_COLOR
        hr = math.clamp(self.height / 10, 0, 1)
        self.color: Color = self.DIRT_COLOR.lerp(
            self.MOUNTAIN_TOP_COLOR, hr
        )
        # self.color.r += random.randint(0,5)
        # self.color.g += random.randint(0,5)
        # self.color.b += random.randint(0,5)
        self.temp_surface: Surface = Surface(self.rect.size, SRCALPHA)
        self.is_border = is_border
        self.steepest_decline_direction: Direction | None = None

    def update(self):        
        if self.animal:
            self.animal.update()
        
        if self.plant:
            self.plant.update()          

    def calculate_growth_height_penalty(self, growth_chance: float) -> float:
        height_threshold_for_growth_penalty = 20
        if self.height > height_threshold_for_growth_penalty:
            return -(growth_chance * (self.height / 100))
        else:
            return 0

    def draw(self, screen: Surface):
        self.temp_surface.fill(self.color)

        if self.animal:
            self.animal.draw(self.temp_surface)
        elif self.plant:
            self.plant.draw(self.temp_surface)
            
        screen.blit(self.temp_surface, self.rect.topleft)
        
        if self.water > 0:
            water_surface: Surface = Surface(self.rect.size, SRCALPHA)
            water_ratio = pygame.math.clamp(self.water / 100, 0, 1)  #TODO rethink this as water is always bigger than 10 and currently not moving
            alpha = floor(pygame.math.lerp(0, 255, pygame.math.clamp(water_ratio + .7, 0, 1)))
            water_surface.set_alpha(alpha)
            water_color = self.MIN_WATER_COLOR.lerp(self.MAX_WATER_COLOR, pygame.math.clamp((water_ratio * 10)+.2, 0, 1))
            water_surface.fill(water_color)
            screen.blit(water_surface, self.rect.topleft)
        
        from config import draw_water_level
        if draw_water_level:
            self.draw_stat(self.water, screen)

        from config import draw_height_level
        if draw_height_level:
            self.draw_stat(self.height, screen)

        from config import draw_height_lines
        if draw_height_lines:
            self.draw_height_contours(screen)

    def draw_stat(self, stat: float, screen: Surface):
        stat_alpha = 255
        # if abs(stat) < 10:
        #     stat = round(stat, 0)
        # else:
        #     stat = round(stat, 0)
        
        text = font.render(str(round(stat)), True, (0, 0, 0))
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
        steepest_decline = 1
        steepest_decline_direction = None
        
        
        for direction in self.get_directions():
            neighbor = self.get_neighbor(direction)
            if neighbor == None: continue
            
            difference_in_height = neighbor.height - self.height
            if difference_in_height < steepest_decline or (difference_in_height == steepest_decline and random.random() < .5):
                steepest_decline = difference_in_height
                steepest_decline_direction = direction
            
            self.steepest_decline_direction = steepest_decline_direction
            
            floored_dif_height = abs(floor(round(self.height, 0) - round(neighbor.height, 0)))
            if floored_dif_height >= 1:
                color = Color(0, 0, 0)  # Adjust as needed
                thickness = pygame.math.clamp(floored_dif_height, 0, 8)  # Example logic
            
                if direction in [Direction.NORTH, Direction.SOUTH]:
                    start_pos = self.rect.topleft if direction == Direction.NORTH else self.rect.bottomleft
                    end_pos = self.rect.topright if direction == Direction.NORTH else self.rect.bottomright
                else:
                    start_pos = self.rect.topright if direction == Direction.EAST else self.rect.topleft
                    end_pos = self.rect.bottomright if direction == Direction.EAST else self.rect.bottomleft
            
                self.height_contours.append((start_pos, end_pos, color, thickness))
        #print("Calculated height contours")

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
        
    def leave(self):
        self.animal = None
        
    def enter(self, animal):
        assert self.animal == None, "Tile already occupied by an animal"
        
        self.animal = animal
        
        assert animal.tile == self, "Tiles Organism and Organisms tile are not equal."
        
    def add_plant(self, plant):
        assert self.plant == None, "Tile is already occupied by a plant"
        
        self.plant = plant
        assert plant.tile == self, "Tiles Plant and plants tile are not equal."    
    
    def has_animal(self) -> bool:
        return self.animal is not None
    
    def has_plant(self) -> bool:
        return self.plant is not None

    def add_neighbor(self, direction: Direction, tile: Tile):
        self.neighbors[direction] = tile

    def get_directions(self) -> List[Direction]:
        dirs = list(self.neighbors.keys())
        random.shuffle(dirs)
        return dirs
    
    def get_neighbors(self) -> List[Tile]:
        ns = list(self.neighbors.values())
        random.shuffle(ns)
        return ns

    def get_neighbor(self, direction: Direction) -> Tile|None:
        return self.neighbors.get(direction, None)

    def get_random_neigbor(self, no_plant = False, no_animal = False) -> Tile | None:
        options = []
        has_options = False
        for tile in self.neighbors.values():
            if no_plant and tile.has_plant(): continue 
            if no_animal and tile.has_animal(): continue
            options.append(tile)
            has_options = True
            
        if has_options:
            return random.choice(options)
        else:
            return None
    
    def is_neighbor(self, tile: Tile) -> bool:  
        if not self.neighbors.values():
            return False
        return tile in self.neighbors.values()