from __future__ import annotations
from typing import List
from pygame import Rect, Surface, Color
import pygame
from random import choice, shuffle

from settings.config import *
from settings.colors import *
from settings.font import font
from helper.direction import Direction

class Tile():
    WATER_LEVEL = .1
    
    def __init__(self, rect: Rect, tile_size: int, height: float = 0, moisture: float = 0, is_border = False):
        # Tile
        self.rect: Rect = rect
        self.tile_size: int = tile_size
        self.neighbors: dict[Direction, Tile] = {}
        
        # Height
        self.height: float = height        
        self.moisture: float = moisture      
        self.color: Color = self.get_biome_color()
              
        # Organisms
        from entities.animal import Animal
        self.animal: Animal | None = None
            
        from entities.plant import Plant
        self.plant: Plant | None = None
                
        self.has_water = self.height < self.WATER_LEVEL
        self.is_border: bool = is_border
        self.is_coast: bool = False
        self.steepest_decline_direction: Direction | None = None
        
        # Stats
        self.times_visted: int = 0

    def update(self):        
        if self.animal:
            self.animal.update()
        
        if self.plant:
            self.plant.update()          

    def draw(self):
        pygame.display.get_surface().fill(self.color, self.rect)
        
        if self.has_animal():
            self.animal.draw()
            
            from settings.gui_settings import draw_animal_health
            if draw_animal_health:
                self.draw_stat(self.animal.health)
                
            from settings.gui_settings import draw_animal_energy
            if draw_animal_energy:
                self.draw_stat(self.animal.energy)
                
        elif self.has_plant():
            self.plant.draw()
        
        from settings.gui_settings import draw_height_level
        if draw_height_level:
            self.draw_stat(self.height * 9)

    ########################## Tile Organism influence #################################
    def calculate_growth_height_penalty(self, growth_chance: float) -> float:
        return -(growth_chance * self.height)

    ########################## Drawing #################################
    def get_biome_color(self) -> Color:
        if (self.height < self.WATER_LEVEL):
            return WATER_COLOR
        if (self.height < 0.12): 
            return SAND_COLOR
        
        if (self.height > 0.8):
            if (self.moisture < 0.1): 
                return SCORCHED_COLOR
            if (self.moisture < 0.2): 
                return BARE_COLOR
            if (self.moisture < 0.5): 
                return TUNDRA_COLOR
            return SNOW_COLOR

        if (self.height > 0.6):
            if (self.moisture < 0.33): 
                return TEMPERATE_DESERT_COLOR
            if (self.moisture < 0.66): 
                return SHRUBLAND_COLOR
            return TAIGA_COLOR

        if (self.height > 0.3):
            if (self.moisture < 0.16): 
                return TEMPERATE_DESERT_COLOR
            if (self.moisture < 0.50): 
                return GRASSLAND_COLOR
            if (self.moisture < 0.83): 
                return TEMPERATE_DECIDUOUS_FOREST_COLOR
            return TEMPERATE_RAIN_FOREST_COLOR

        if (self.moisture < 0.16): 
            return SUBTROPICAL_DESERT_COLOR
        if (self.moisture < 0.33): 
            return GRASSLAND_COLOR
        if (self.moisture < 0.66): 
            return TROPICAL_SEASONAL_FOREST_COLOR
        return TROPICAL_RAIN_FOREST_COLOR
    
    def draw_stat(self, stat: float):
        # Analyzing background color brightness
        if self.has_animal():
            col = self.animal.color
        else:
            col = self.color
            
        text = font.render(str(round(stat)), True, col.__invert__())
        self._render_text_centered(text)

    def _render_text_centered(self, text: Surface):
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
        pygame.display.get_surface().blit(text, (text_x, text_y))
    
    ########################## Tile Property Handling #################################
    def add_animal(self, animal):
        assert self.animal == None, "Tile already occupied by an animal."
        
        self.animal = animal
        self.times_visted += 1
        
        assert animal.tile == self, "Animal-Tile assignment not equal."
        
    def add_plant(self, plant):
        assert self.plant == None, "Tile is already occupied by a plant."
        
        self.plant = plant
        
        assert plant.tile == self, "Plant-Tile assignment not equal."  
        
    def remove_animal(self):        
        self.animal = None
        
    def remove_plant(self):        
        self.plant = None  
    
    def has_animal(self) -> bool:
        return self.animal is not None
    
    def has_plant(self) -> bool:
        return self.plant is not None

    def add_neighbor(self, direction: Direction, tile: Tile):
        self.neighbors[direction] = tile
        self.is_coast = tile.has_water and self.has_water

    def get_directions(self) -> List[Direction]:
        dirs = list(self.neighbors.keys())
        shuffle(dirs)
        return dirs
    
    def get_neighbors(self) -> List[Tile]:
        ns = list(self.neighbors.values())
        shuffle(ns)
        return ns

    def get_neighbor(self, direction: Direction) -> Tile|None:
        return self.neighbors.get(direction, None)

    def get_random_neigbor(self, no_plant = False, no_animal = False, no_water = False) -> Tile | None:
        options = []
        has_options = False
        for tile in self.neighbors.values():
            if no_plant and tile.has_plant(): continue 
            if no_animal and tile.has_animal(): continue
            if no_water and tile.has_water: continue
            options.append(tile)
            has_options = True
            
        if has_options:
            return choice(options)
        else:
            return None
    
    def is_neighbor(self, tile: Tile) -> bool:  
        if not self.neighbors.values():
            return False
        return tile in self.neighbors.values()
