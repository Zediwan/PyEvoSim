from __future__ import annotations
from typing import List, Optional
from pygame import Rect, Surface, SRCALPHA, draw, Color
from bounded_variable import BoundedVariable
import random
from config import *
import math

from sun import Sun

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
    DOES_WATER_FLOW = True
    START_WITH_WATER_TILES = True
    WATER_DROWNING_HEIGHT: float = 3   # Water value at which animals can drown
    
    MIN_WATER_VALUE: float = 0
    BASE_WATER_LEVEL: float = 0
    
    MIN_WATER_COLOR = Color(204, 229, 233, ground_alpha)
    #MAX_WATER_COLOR = Color(26, 136, 157, ground_alpha)
    MAX_WATER_COLOR =  Color("dodgerblue4")
    
    # Water spawning
    WATER_SPAWNING_AT_MOUNTAIN_SOURCE: float = 0.1

    # Water Evaporation
    EVAPORATION_BASE_CHANCE: float = .01
    EVAPORATION_INCREASING_THRESHOLD: float = 2        # If the water value is less than this then the chance of evaporation is increased
    EVAPORTAION_INCREASED_CHANCE_MULTIPLIER: float = 2 # Multiplier applied to chance of evaporation if water value is below Threshold
    MAX_EVAPORATION: float = 2                             # How much water evaporates at once
    EVAPORATION_GROWTH_INCREASE: float = 1             # How much evaporation increases growth on its tile
    
    ### Land
    MIN_GROWTH_VALUE, MAX_GROWTH_VALUE = 0, 10
    BASE_GROWTH_VALUE = MIN_GROWTH_VALUE
    GROWTH_BOUND = BoundedVariable(BASE_GROWTH_VALUE, MIN_GROWTH_VALUE, MAX_GROWTH_VALUE)
    TERRAIN_HARDNESS: float = 0.5
    
    # TODO: improve names
    LAND_DAMAGE = 50
    GROWTH_BASE_RATE = 1
    GROWTH_BASE_CHANCE = .01
    WATER_GROWTH_RATE_INCREASE = 5
    WATER_GROWTH_CHANCE_INCREASE = .05
    COMMON_GROWTH_THRESHOLD_PERCENTAGE = .5
    POSSIBLE_GROWTH_LOSS_THRESHOLD_PERCENTAGE = .9
    GROWTH_LOSS_CHANCE = .02
    GROWTH_LOSS = 1
    
    DIRT_COLOR = Color(155, 118, 83, ground_alpha)
    MIN_GRASS_COLOR = Color(235, 242, 230, ground_alpha)
    MAX_GRASS_COLOR = Color(76, 141, 29, ground_alpha)
    
    # Mountains
    MOUNTAIN_LAKE_MIN_HEIGHT:float = 20
    MAX_WATER_AT_MOUNTAIN_SOURCE_TO_SPAWN_WATER: float = 1
    CHANCE_OF_MOUNTAIN_WATER_SPAWN: float = 1
    MOUNTAIN_TOP_COLOR = Color("white")
    MOUNTAIN_FLOOR_COLOR = Color("azure4")
    
    def __init__(self, rect: Rect, tile_size: int, height: int = 0,
                 organisms = None,
                 starting_water_level: Optional[float] = None,
                 starting_growth_level: Optional[int] = None,
                 growth: BoundedVariable = GROWTH_BOUND,
                 is_coast: bool = False
                 ):
        # Organisms
        if organisms:
            self.organisms = organisms
        else:
            self.organisms = []
                
        self.water: float = 0
        # Water
        if starting_water_level:
            self.water = starting_water_level
        elif self.START_WITH_WATER_TILES and height < 0:
            max_possible_starting_water = 10 * -height
            self.water = pygame.math.clamp(random.random(), .8, 1) * max_possible_starting_water
        self.is_lake = False
        self.evaporated_water = random.randint(0,3)
            
        # Growth
        self.growth: BoundedVariable = growth.copy()
        if starting_growth_level:
            self.growth.value = starting_growth_level
        else:
            self.growth.value = random.randint(self.MIN_GROWTH_VALUE, self.MAX_GROWTH_VALUE)
        
        # Tile
        self.tile_size: int = max(tile_size, MIN_TILE_SIZE)
        self.rect: Rect = rect
        self.is_border_tile: bool = False
        self.neighbors: dict[Direction, Tile] = {}
        self.is_coast = is_coast
        self.erosion_accumulator: float = 0.0
        self.tile_hardness: float = self.TERRAIN_HARDNESS
        self.height: float = height
        self.height_contours = []
        self.surface_temperature: float = 0
        self.is_raining = False
        
        if self.height > 10:
            self.height_growth_penalty = (self.height / 10)
            self.height_growth_penalty = pygame.math.clamp(self.height_growth_penalty, self.MIN_GROWTH_VALUE, self.MAX_GROWTH_VALUE)
            self.height_growth_penalty = math.floor(self.height_growth_penalty)
            self.height_growth_penalty = - self.height_growth_penalty
            self.growth.add_value(self.height_growth_penalty)
        
        # Drawing
        self.color: Color = Color(0,0,0,0)
        self.temp_surface: Surface = Surface((self.rect.width, self.rect.height), SRCALPHA)

    def update(self, sun: Sun):
        if self.organisms:
            for org in self.organisms:
                org.update()
                
        self.adjust_temperature(sun)
        
        # Water Update
        self.update_water(sun)
        
        self.update_clouds()
                    
        # Growth Update # TODO: refactor into separate method
        growth_chance = self.GROWTH_BASE_CHANCE
        growth_rate = self.GROWTH_BASE_RATE
        
        # # Check if neighbour has water
        # for neighbor in self.neighbors.values():
        #     water_height = neighbor.calculate_effective_height() - self.calculate_effective_height()
        #     ratio = neighbor.water.ratio()
        #     if ratio > 0 and self.water.value < 3:
        #         growth_rate += (int)(self.WATER_GROWTH_RATE_INCREASE * ratio)
        #         growth_chance += (int)(self.WATER_GROWTH_CHANCE_INCREASE * ratio)
        
        if self.height > 0:
            growth_chance /= (self.height / 100)
        
        if random.random() < growth_chance:
            growth_rate = math.floor(growth_rate)
            if self.growth.ratio() < self.COMMON_GROWTH_THRESHOLD_PERCENTAGE:
                self.growth.add_value(growth_rate)
            else:
                neighbor = self.get_random_neigbor()
                if neighbor:
                    tile = random.choice((self, neighbor))
                else:
                    tile = self
                tile.growth.add_value(growth_rate)
        
        if self.growth.ratio() > self.POSSIBLE_GROWTH_LOSS_THRESHOLD_PERCENTAGE:
            if random.random() < self.GROWTH_LOSS_CHANCE:
                self.growth.add_value(-self.GROWTH_LOSS)

    def adjust_temperature(self, sun: Sun):
        environmental_temperature = sun.get_temperature()
        water_cooling_effect = max(0, (100 - min(self.water,100)) / 100)
        
        # Apply a stronger cooling effect at night for higher altitudes
        if sun.is_night():
            altitude_factor = max(0, 1 - (self.height * 0.05))
        else:
            altitude_factor = max(0, 1 - (self.height * 0.01))
        
        # Modify temperature adjustment rate based on water level
        water_adjustment_factor = 1 - (min(self.water,100) / 100)  # Assuming 100 is the max water level
        temperature_adjustment = ((environmental_temperature - self.surface_temperature) * water_cooling_effect * altitude_factor * 0.1) * water_adjustment_factor   
             
        self.surface_temperature += temperature_adjustment

    def update_water(self, sun: Sun):
        self.spawn_new_water()
        
        if self.water > 0:
            self.handle_evaporation(sun)
            
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
        if self.is_lake:
            # Calculate gradient
            height_differences = [self.height - neighbor.height for neighbor in self.neighbors.values()]
            gradient = sum(height_differences) / len(self.neighbors)
            
            # Adjust spawn chance based on gradient
            spawn_chance = self.CHANCE_OF_MOUNTAIN_WATER_SPAWN * (1 + gradient / 10)
            if random.random() < spawn_chance:
                # if not self.START_WITH_WATER_TILES:
                #     self.WATER_SPAWNING_AT_MOUNTAIN_SOURCE += 5
                self.water += self.WATER_SPAWNING_AT_MOUNTAIN_SOURCE
            
    def handle_evaporation(self, sun: Sun):
        # Adjust the base evaporation chance based on sunlight intensity
        sunlight_intensity = sun.get_light_intensity()
        adjusted_evaporation_chance = self.EVAPORATION_BASE_CHANCE * sunlight_intensity
        
        # Increase chance if water is below the threshold
        if self.water <= self.EVAPORATION_INCREASING_THRESHOLD:
            adjusted_evaporation_chance *= self.EVAPORTAION_INCREASED_CHANCE_MULTIPLIER
        
        temperature_factor = self.surface_temperature / sun.max_temperature
        adjusted_evaporation_amount = self.MAX_EVAPORATION * temperature_factor
        amount_evaporated = pygame.math.clamp(adjusted_evaporation_amount, 0, self.water)
        
        EVAPORATION_TEMPERATURE_THRESHOLD = sun.max_temperature * .5
        if self.surface_temperature > EVAPORATION_TEMPERATURE_THRESHOLD and random.random() <= adjusted_evaporation_chance:
            #self.growth.add_value(1)  # Adjust growth based on evaporation if needed
            self.water -= pygame.math.clamp(amount_evaporated, 0, self.water)
            self.evaporated_water += amount_evaporated
            
        # condition_met, sufficient_neighbors, evaporated_water = self.has_sufficient_evaporation_and_neighbors()
        # if condition_met:
        #     # Create a new cloud
        #     new_cloud = Cloud(sufficient_neighbors, evaporated_water)
        #     pass
    
    # def adjust_growth_due_to_evaporation(self):
    #     # Example condition: Increase growth if water level is within an optimal range
    #     if self.MIN_OPTIMAL_WATER_LEVEL <= self.water <= self.MAX_OPTIMAL_WATER_LEVEL:
    #         # Adjust growth based on a function of water level and evaporation rate
    #         growth_increase = calculate_growth_increase(self.water, self.EVAPORATION)
    #         self.growth.add_value(growth_increase)
    #     # Optionally, handle conditions of drought or waterlogging
    #     elif self.water < self.MIN_OPTIMAL_WATER_LEVEL:
    #         # Drought condition might slow down or reduce growth
    #         self.growth.add_value(-self.DROUGHT_GROWTH_PENALTY)
    #     elif self.water > self.MAX_OPTIMAL_WATER_LEVEL:
    #         # Waterlogging condition might also negatively affect growth
    #         self.growth.add_value(-self.WATERLOGGING_GROWTH_PENALTY)
    
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
    
    def update_clouds(self):
        if self.evaporated_water > 1:
            self.move_clouds()
            can_rain =  self.evaporated_water > 5
            chance_to_rain = .2 * (self.evaporated_water / 5)
            if can_rain and random.random() <= chance_to_rain:
                self.rain()
                return
        self.is_raining = False
        
    def move_clouds(self):
        if self.evaporated_water > 1:
            self.evaporated_water -= 1
            self.get_random_neigbor().evaporated_water += 1
        self.is_raining = False
        
    def rain(self):
        if self.evaporated_water > 1:
            rain_frequency = .3
            if random.random() <= rain_frequency:
                self.is_raining = True
                self.water += 1
                self.evaporated_water -= 1
                return
        self.is_raining = False
            
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
            growth_ratio = self.growth.ratio()
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
                
        MIN_EVAP_WATER_TO_CLOUD = 5
        if self.evaporated_water > MIN_EVAP_WATER_TO_CLOUD:
            light_cloud_color = Color("grey70")
            heavy_cloud_color = Color("grey30")
            heaviness = pygame.math.clamp(self.evaporated_water / 40, 0, 1)
            cloud_color = light_cloud_color.lerp(heavy_cloud_color, heaviness)
            self.temp_surface.fill(cloud_color)
            
        if self.is_raining:
            rain_color = Color("navy")
            pygame.draw.circle(self.temp_surface, rain_color, self.temp_surface.get_rect().center, radius = self.rect.width / 2, draw_bottom_left=True, draw_bottom_right=True)
        
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
            text = font.render(str(self.growth.value), True, (0, 0, 0))
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