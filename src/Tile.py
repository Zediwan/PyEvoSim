from __future__ import annotations
from typing import List, Optional
from pygame import Rect, Surface, SRCALPHA, draw, Color
from bounded_variable import BoundedVariable
import random
from config import *
import math

import entities.organism as organism

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
    WATER_FLOW_BETWEEN_TILES = 1
    WATER_DROWNING_HEIGHT = 3   # Water value at which animals can drown
    
    MIN_WATER_VALUE, MAX_WATER_VALUE= 0, 10
    BASE_WATER_LEVEL = 0
    WATER_BOUND = BoundedVariable(BASE_WATER_LEVEL, MIN_WATER_VALUE, MAX_WATER_VALUE)
    
    MIN_WATER_COLOR = Color(204, 229, 233, ground_alpha)
    MAX_WATER_COLOR = Color(26, 136, 157, ground_alpha)
    
    # Water spawning
    WATER_FLOW_AT_BORDER = 1

    # Water Evaporation
    EVAPORATION_BASE_CHANCE = .001
    EVAPORATION_INCREASING_THRESHOLD = 2        # If the water value is less than this then the chance of evaporation is increased
    EVAPORTAION_INCREASED_CHANCE_MULTIPLIER = 2 # Multiplier applied to chance of evaporation if water value is below Threshold
    EVAPORATION = 1                             # How much water evaporates at once
    EVAPORATION_GROWTH_INCREASE = 1             # How much evaporation increases growth on its tile
    
    ### Land
    MIN_GROWTH_VALUE, MAX_GROWTH_VALUE = 0, 10
    BASE_GROWTH_VALUE = MIN_GROWTH_VALUE
    GROWTH_BOUND = BoundedVariable(BASE_GROWTH_VALUE, MIN_GROWTH_VALUE, MAX_GROWTH_VALUE)
    
    # TODO: improve names
    LAND_DAMAGE = 30
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
    MOUNTAIN_TOP_COLOR = Color("white")
    MOUNTAIN_FLOOR_COLOR = Color("azure4")
    
    def __init__(self, rect: Rect, tile_size: int, height: int = 0,
                 organisms: Optional[List[organism.Organism]] = None,
                 starting_water_level: Optional[int] = None,
                 water: BoundedVariable = WATER_BOUND,
                 starting_growth_level: Optional[int] = None,
                 growth: BoundedVariable = GROWTH_BOUND,
                 is_coast: bool = False
                 ):
        # Organisms
        if organisms:
            self.organisms: list[organism.Organism] = organisms
        else:
            self.organisms: list[organism.Organism] = []
                    
        # Water
        self.water: BoundedVariable = water.copy()
        if starting_water_level:
            self.water.value = starting_water_level
        elif height < 0:
            self.water.value = random.randint(self.MIN_WATER_VALUE, self.MAX_WATER_VALUE)
            
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
        
        #if height == 0:
        #    height += 1
        self.height:int = height
        self.height_contours = []
        
        if self.height > 10:
            self.height_growth_penalty = (self.height / 10)
            self.height_growth_penalty = pygame.math.clamp(self.height_growth_penalty, self.MIN_GROWTH_VALUE, self.MAX_GROWTH_VALUE)
            self.height_growth_penalty = math.floor(self.height_growth_penalty)
            self.height_growth_penalty = - self.height_growth_penalty
            self.growth.add_value(self.height_growth_penalty)
        
        # Drawing
        self.color: Color = Color(0,0,0,0)
        self.temp_surface: Surface = Surface((self.rect.width, self.rect.height), SRCALPHA)
        

    def update(self):
        if self.organisms:
            for org in self.organisms:
                org.update()
                
        # Water Update
        self.update_water()
                    
        # Growth Update # TODO: refactor into separate method
        growth_chance = self.GROWTH_BASE_CHANCE
        growth_rate = self.GROWTH_BASE_RATE
        
        # Check if neighbour has water
        for neighbor in self.neighbors.values():
            ratio = neighbor.water.ratio()
            if ratio > 0 and self.water.value < 3:
                growth_rate += (int)(self.WATER_GROWTH_RATE_INCREASE * ratio)
                growth_chance += (int)(self.WATER_GROWTH_CHANCE_INCREASE * ratio)
        
        if self.height > 10:
            growth_chance /= (self.height /10)
        
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

    def update_water(self):
        if self.DOES_WATER_FLOW:
            self.spawn_new_water()

            if self.water.value > 0:
                self.handle_evaporation()

                possible_tiles, found_tiles = self.find_suitable_tiles_for_water_distribution()
                if found_tiles:
                    possible_tiles.sort(key=lambda tile: (tile.water.value, random.random()))
                    self.dynamic_water_distribution(possible_tiles)
                
    def spawn_new_water(self):
        is_water_source = self.is_border_tile and self.height < 0
        if is_water_source:
            self.water.add_value(self.WATER_FLOW_AT_BORDER)
            
    def handle_evaporation(self):
        evaporate_chance = self.EVAPORATION_BASE_CHANCE
        if self.water.value <= self.EVAPORATION_INCREASING_THRESHOLD:
            evaporate_chance *= self.EVAPORTAION_INCREASED_CHANCE_MULTIPLIER   
                               
        if random.random() <= evaporate_chance:
            # TODO: rethink if this does even make sense?
            # TODO: retink if this should be turned into a formula that is in relation to evaporated water value
            self.growth.add_value(1) 
            self.water.add_value(-self.EVAPORATION)
            
    def find_suitable_tiles_for_water_distribution(self):
        all_same_and_lower_height_neighbors_at_max_water = self.water.value == self.MAX_WATER_VALUE and all(neighbor.water.value == self.MAX_WATER_VALUE for neighbor in self.neighbors.values() if neighbor.height <= self.height)
        found_tiles = False
        possible_tiles = []
        lowest_height = 10000

        for neighbor in self.neighbors.values():
            # Allow for upward flow if all tiles are at max water value
            if all_same_and_lower_height_neighbors_at_max_water:
                if neighbor.height > self.height and neighbor.height <= lowest_height:
                    if neighbor.height < lowest_height:
                        possible_tiles = [neighbor]
                    else:
                        possible_tiles.append(neighbor)
                    found_tiles = True
            else: 
                if neighbor.water.value >= self.MAX_WATER_VALUE or neighbor.height > self.height:
                    continue
                        
                if neighbor.height <= lowest_height:
                    if neighbor.height < lowest_height:  
                        possible_tiles = [neighbor]
                        lowest_height = neighbor.height
                    else:
                        possible_tiles.append(neighbor)
                    found_tiles = True
                
        return possible_tiles, found_tiles
    
    def dynamic_water_distribution(self, possible_tiles):
        while self.water.value > 0 and possible_tiles:
            lowest_value = possible_tiles[0].water.value
            if self.water.value <= lowest_value:
                break  # Ensure no distribution if there's no excess water

            next_lowest_index = next((i for i, tile in enumerate(possible_tiles) if tile.water.value > lowest_value), len(possible_tiles))
            if next_lowest_index < len(possible_tiles):
                next_lowest_value = possible_tiles[next_lowest_index].water.value
            else:
                next_lowest_value = self.MAX_WATER_VALUE + 1  # Ensure we only fill up to the max water value

            total_water_needed = (next_lowest_value - lowest_value) * next_lowest_index
            water_to_distribute = min(self.water.value - lowest_value, total_water_needed)  # Ensure we only distribute actual excess water

            if water_to_distribute > 0:
                distributed_water = 0
                for tile in possible_tiles[:next_lowest_index]:
                    excess = min(next_lowest_value - tile.water.value, water_to_distribute)
                    tile.water.add_value(excess)
                    distributed_water += excess
                    water_to_distribute -= excess
                    if water_to_distribute <= 0:
                        break
                self.water.add_value(-distributed_water)
            else:
                break  # No excess water to distribute

            possible_tiles = possible_tiles[next_lowest_index:]
    
    def draw(self, screen: Surface):
        """
        Renders the tile on the screen with its color, border, and any organisms present.
        Displays the water level, growth level, and height level of the tile if the corresponding configuration options are enabled.

        Args:
            screen (Surface): The surface on which the tile will be drawn.
        """
        # Draw organisms if present
        if self.organisms:
            for org in self.organisms:
                if org.is_alive():
                    org.draw(screen)
        else:
            growth_ratio = self.growth.ratio()
            water_ratio = self.water.ratio()
            height_ratio = pygame.math.clamp(self.height / 50, 0, 1)
        
            growth_color = self.DIRT_COLOR.lerp(self.MIN_GRASS_COLOR, growth_ratio).lerp(self.MAX_GRASS_COLOR, growth_ratio)
            water_color = self.MIN_WATER_COLOR.lerp(self.MAX_WATER_COLOR, water_ratio)
            height_color = self.MOUNTAIN_FLOOR_COLOR.lerp(self.MOUNTAIN_TOP_COLOR, height_ratio)

            self.color = growth_color.lerp(water_color, pygame.math.clamp(water_ratio, 0, .75)).lerp(height_color, pygame.math.clamp(height_ratio, 0, .5))

            self.temp_surface.fill(self.color)
        
        screen.blit(self.temp_surface, (self.rect.left, self.rect.top))

        # Render water level if enabled
        from config import draw_water_level
        if draw_water_level:
            text = font.render(str(self.water.value), True, (0, 0, 0))
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
            text = font.render(str(self.height), True, (0, 0, 0))
            text.set_alpha(ground_font_alpha)
            self._render_text_centered(screen, text)

        # Draw height lines if enabled
        from config import draw_height_lines
        if draw_height_lines:
            self.draw_height_contours(screen)

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
        
    def transfer_water(self, amount : int, tile: Tile):
        if amount < 0:
            raise ValueError("Amount to transfer is negative.")
        if self.water.value < tile.water.value:
            raise ValueError("Water flow is wrong.")
        if not self.is_neighbor(tile):
            raise ValueError("Tile to transfer to is not a neighbour.")
    
        max_transfer = min(amount, self.water.value - self.MIN_WATER_VALUE, self.MAX_WATER_VALUE - tile.water.value)
        if max_transfer > 0:
            self.water.add_value(-max_transfer)
            tile.water.add_value(max_transfer)
        
    def leave(self, organism: organism.Organism):
        if self.organisms:
            self.organisms.remove(organism)
        
    def enter(self, organism: organism.Organism):
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
    
    def calculate_height_contours(self):
        """
        Calculates the contour lines based on the current height and neighbors
        and stores them in self.height_contours.
        """
        self.height_contours.clear()
    
        for direction, neighbor in self.neighbors.items():
            if neighbor.height != self.height:
                color = Color(0, 0, 0)  # Adjust as needed
                thickness = abs(neighbor.height - self.height)  # Example logic
            
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