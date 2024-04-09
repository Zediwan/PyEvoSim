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
    DOES_WATER_FLOW: bool = True
    DO_TILES_START_WITH_WATER: bool = True
    AMOUNT_OF_WATER_FOR_ONE_HEIGHT_LEVEL = 10
    SEA_LEVEL = 0
    MIN_WATER_HEIGHT_FOR_DROWING: float = 3
    MIN_WATER_VALUE: float = 0
    MAX_WATER_VALUE: float = float("inf")
    
    # Water spawning
    DOES_WATER_ARTIFICALY_SPAWN: bool = False
    AMOUNT_OF_WATER_SPAWNING_AT_MOUNTAIN_SOURCE: float = 1

    # Water Evaporation
    BASE_EVAPORATION_CHANCE: float = .01
    MIN_WATER_TO_INCREASE_EVAPORATION: float = 2        # If the water value is less than this then the chance of evaporation is increased
    LOW_WATER_EVAPORATION_CHANCE_MULTIPLIER: float = 2 
    MIN_STARTING_EVAPORATION: float = 0
    MAX_STARTING_EVAPORATION: float = 3 
    MIN_EVAPORATION: float = 0.1
    MAX_EVAPORATION: float = 2                    
    GROWTH_INCREASE_BY_EVAPORATION: float = 1
    
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
    
    # Erosion
    TERRAIN_HARDNESS: float = 0.5
    
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
                 starting_water_level: Optional[float] = None,
                 starting_growth_level: Optional[float] = None,
                 is_coast: bool = False
                 ):
        # Tile
        self.is_border_tile: bool = False
        self.rect: Rect = rect
        self.tile_size: int = tile_size
        self.neighbors: dict[Direction, Tile] = {}
        
        # Height
        self.height: float = height
        self.height_contours = []
        
        # Organisms
        if organisms:
            self.organisms = organisms
        else:
            self.organisms = []
            
        # Plants
        # self.plants = []
        # self.cloud = None
        # self.water = None
        # self.organisms = []
                    
        # Growth
        self.growth: float = 0
        if starting_growth_level:
            self.growth = starting_growth_level
        else:
            self.growth = random.random() * self.MAX_GROWTH_VALUE
        
        # Water      
        self.water: float = 0
        if starting_water_level:
            self.water = starting_water_level
        elif self.DO_TILES_START_WITH_WATER and height < self.SEA_LEVEL:
            max_possible_starting_water = (self.AMOUNT_OF_WATER_FOR_ONE_HEIGHT_LEVEL * abs(height))
            self.water = pygame.math.clamp(random.random(), .8, 1) * max_possible_starting_water
        self.evaporated_water = random.random() * self.MAX_STARTING_EVAPORATION
        
        self.is_lake = False
        self.is_coast = is_coast
        self.is_raining = False
        
        # Clouds
        self.last_cloud_direction = None
        
        # Erosion
        self.tile_hardness: float = self.TERRAIN_HARDNESS
        self.erosion_accumulator: float = 0.0
        
        # Temparature
        self.surface_temperature: float = 0
        
        # Drawing
        self.color: Color = Color(0,0,0,0)
        self.temp_surface: Surface = Surface(self.rect.size, SRCALPHA)
        
        # Growth penalties
        if self.height >= 0:
            self.growth -= pygame.math.clamp((self.height / 20), self.MIN_GROWTH_VALUE, self.MAX_GROWTH_VALUE)

    def update(self):
        if self.organisms:
            for org in self.organisms:
                org.update()
                        
        # Water Update
        self.update_water()
                    
        # Growth Update # TODO: refactor into separate method
        growth_chance = self.BASE_GROWTH_CHANCE
        growth_rate = self.BASE_GROWTH_RATE
        
        # # Check if neighbour has water
        # for neighbor in self.neighbors.values():
        #     water_height = neighbor.calculate_effective_height() - self.calculate_effective_height()
        #     ratio = neighbor.water.ratio()
        #     if ratio > 0 and self.water.value < 3:
        #         growth_rate += (int)(self.WATER_GROWTH_RATE_INCREASE * ratio)
        #         growth_chance += (int)(self.WATER_GROWTH_CHANCE_INCREASE * ratio)
        
        if self.height > self.SEA_LEVEL:
            growth_chance /= (self.height / 100)
        
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

    def update_water(self):
        if self.DOES_WATER_ARTIFICALY_SPAWN and self.is_lake:
            self.spawn_new_water()
        
        if self.water > 0:    
            # Step 1 & 2: Distribute water to lower tiles
            lower_tiles = sorted([neighbor for neighbor in self.neighbors.values() if neighbor.calculate_effective_height() < self.calculate_effective_height()], key=lambda x: x.calculate_effective_height())
            if lower_tiles:                
                # Distribute water based on height difference
                for lower_tile in lower_tiles:
                    height_diff = self.calculate_effective_height() - lower_tile.calculate_effective_height()
                    water_to_transfer = (height_diff / 2)*10
                                        
                    # Transfer water
                    self.transfer_water(water_to_transfer, lower_tile)
                
    def spawn_new_water(self):
        # Calculate gradient
        height_differences = [self.height - neighbor.height for neighbor in self.neighbors.values()]
        gradient = sum(height_differences) / len(self.neighbors)
            
        # Adjust spawn chance based on gradient
        spawn_chance = self.MOUNTAIN_WATER_SPAWN_CHANCE * (1 + gradient / 10)
        if random.random() < spawn_chance:
            # if not self.START_WITH_WATER_TILES:
            #     self.WATER_SPAWNING_AT_MOUNTAIN_SOURCE += 5
            self.water += self.AMOUNT_OF_WATER_SPAWNING_AT_MOUNTAIN_SOURCE
    
    def transfer_water(self, amount : float, tile: Tile):
        if not self.is_neighbor(tile):
            raise ValueError("Tile to transfer to is not a neighbour.")
        
        max_transfer = pygame.math.clamp(amount, 0, self.water)
        self.water = pygame.math.clamp(self.water - max_transfer, 0, self.water)
        tile.water = pygame.math.clamp(tile.water + max_transfer, tile.water, float("inf"))
        self.update_erosion(max_transfer)
        
    def calculate_effective_height(self) -> float:
        """
        Calculates the effective height of the tile considering both its physical height and water level.
        Every 10 units of water is considered equivalent to an increase of 1 in height.

        Returns:
            float: The effective height of the tile.
        """
        water_height_effect = self.water / 10
        return self.height + water_height_effect

    def update_erosion(self, waterflow):
        """
        Updates the erosion based on water flow and terrain hardness.
        """
        # Example erosion calculation
        # Adjust these values based on your game's scale and desired erosion rate
        EROSION_RATE = 0.01  # Base erosion rate
        WATER_FLOW_FACTOR = 0.1 # How much water flow affects erosion

        # Calculate erosion based on water level and flow
        # This is a simplified example; you might want to factor in flow rate and direction
        erosion_effect = EROSION_RATE * waterflow * WATER_FLOW_FACTOR * (1 - self.tile_hardness)

        # Accumulate erosion effect over time
        self.erosion_accumulator += erosion_effect

        # If enough erosion has accumulated, lower the terrain height
        if self.erosion_accumulator >= 1.0:
            self.height -= 0.1  # Lower the height by 1 unit
            self.erosion_accumulator = 0.0  # Reset the accumulator

            # Ensure height does not go below a certain threshold
            self.height = max(self.height, -100)

        # Optionally, adjust terrain hardness based on erosion
        # For example, terrain might become softer as it erodes
        self.tile_hardness = max(self.tile_hardness - 0.01, 0.0)
    
    def draw(self, screen: Surface):
        """
        Renders the tile on the screen with its color, border, and any organisms present.
        Displays the water level, growth level, and height level of the tile if the corresponding configuration options are enabled.

        Args:
            screen (Surface): The surface on which the tile will be drawn.
        """
        self.calculate_height_contours()
        # Draw organisms if present
        if self.organisms:
            for org in self.organisms:
                if org.is_alive():
                    org.draw(screen)
        else:
            growth_ratio = self.growth_ratio()
            water_ratio = pygame.math.clamp(self.water / 10, 0, 1)
            height_ratio = pygame.math.clamp(self.height / 50, 0, 1)
        
            growth_color = self.DIRT_COLOR.lerp(self.MIN_GRASS_COLOR, growth_ratio).lerp(self.MAX_GRASS_COLOR, growth_ratio)
            water_color = self.MIN_WATER_COLOR.lerp(self.MAX_WATER_COLOR, water_ratio)
            height_color = self.MOUNTAIN_FLOOR_COLOR.lerp(self.MOUNTAIN_TOP_COLOR, height_ratio)

            self.color = growth_color.lerp(water_color, pygame.math.clamp(water_ratio, 0, .75)).lerp(height_color, pygame.math.clamp(height_ratio, 0, .5))

            self.temp_surface.fill(self.color)
        
        from config import draw_water_sources
        if draw_water_sources:
            if self.is_lake:
                self.temp_surface.fill(Color("fuchsia"))
                
        MIN_EVAP_WATER_TO_CLOUD = 4
        if self.evaporated_water > MIN_EVAP_WATER_TO_CLOUD:
            heaviness = pygame.math.clamp(self.evaporated_water / (MIN_EVAP_WATER_TO_CLOUD*2), 0, 1)
            alpha = math.floor(pygame.math.lerp(0, 200, heaviness))
            
            cloud_surface = self.temp_surface.copy()
            cloud_surface.set_alpha(alpha)

            light_cloud_color: Color = Color("grey100")
            heavy_cloud_color: Color = Color("grey0")
            #cloud_color = light_cloud_color.lerp(heavy_cloud_color, heaviness)
            cloud_color: Color = light_cloud_color
            
            if self.is_raining:
                rain_color = heavy_cloud_color
                cloud_color = rain_color
                
            cloud_surface.fill(cloud_color)
            self.temp_surface.blit(cloud_surface, (0, 0))
        
        screen.blit(self.temp_surface, (self.rect.left, self.rect.top))

        # Render water level if enabled
        from config import draw_water_level
        if draw_water_level:
            text = font.render(str(math.floor(self.water)), True, (0, 0, 0))
            text.set_alpha(ground_font_alpha)
            self._render_text_centered(screen, text)

        # Render growth level if enabled
        from config import draw_growth_level
        if draw_growth_level:
            text = font.render(str(math.floor(self.growth)), True, (0, 0, 0))
            text.set_alpha(ground_font_alpha)
            self._render_text_centered(screen, text)

        # Render height level if enabled
        from config import draw_height_level
        if draw_height_level:
            text = font.render(str(math.floor(self.height)), True, (0, 0, 0))
            text.set_alpha(ground_font_alpha)
            self._render_text_centered(screen, text)
            
        # Render temperature if enabled
        from config import draw_temperature_level
        if draw_temperature_level:
            text = font.render(str(math.floor(self.surface_temperature)), True, (0, 0, 0))
            text.set_alpha(ground_font_alpha)
            self._render_text_centered(screen, text)

        # Draw height lines if enabled
        from config import draw_height_lines
        if draw_height_lines:
            self.calculate_height_contours()
            self.draw_height_contours(screen)
            
        draw_cloud_level = False
        if draw_cloud_level:
            text = font.render(str(math.floor(self.evaporated_water)), True, (0, 0, 0))
            text.set_alpha(ground_font_alpha)
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
        self.height_contours.clear()
    
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
        if self.organisms:
            self.organisms.remove(organism)
        
    def enter(self, organism):
        if not self.organisms:
            self.organisms.append(organism)
        
        assert organism.tile == self, "Tiles Organism and Organisms tile are not equal."
        
    def is_occupied(self) -> bool:
        return bool(self.organisms)

    def add_neighbor(self, direction: Direction, tile: Tile):
        # TODO find out why this is not working properly and alway raising the error
        self.is_coast = self.is_coast or tile.height != self.height
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