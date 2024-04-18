from __future__ import annotations
from typing import List

from pygame import Rect, Surface, SRCALPHA, draw, Color

from pygame.math import clamp, lerp
from math import floor
from random import random, choice, shuffle

from config import *
from custom_group import Custom_Group
class Tile(pygame.sprite.Sprite):
    ### Water
    AMOUNT_OF_WATER_FOR_ONE_HEIGHT_LEVEL: float = 10
    SEA_LEVEL: float = 0
    MIN_WATER_HEIGHT_FOR_DROWING: float = 3
    MIN_WATER_VALUE: float = 0
    MAX_WATER_VALUE: float = float("inf")
    
    WATER_COLOR = Color(26, 136, 157, ground_alpha)
    SAND_COLOR = Color(228,232,202)
    SCORCHED_COLOR = Color(153, 153, 153)
    BARE_COLOR = Color(187, 187, 187)
    TUNDRA_COLOR = Color(221,221,187)
    SNOW_COLOR = Color(248,248,248)
    TEMPERATE_DESERT_COLOR = Color(228,232,202)
    SHRUBLAND_COLOR = Color(195,204,187) 
    TAIGA_COLOR = Color(203,212,187)
    GRASSLAND_COLOR = Color(196,212,170)
    TEMPERATE_DECIDUOUS_FOREST_COLOR = Color(180,200,169)
    TEMPERATE_RAIN_FOREST_COLOR = Color(163,196,168)
    SUBTROPICAL_DESERT_COLOR = Color(233,220,198)
    GRASSLAND_COLOR = Color(196,212,170)
    TROPICAL_SEASONAL_FOREST_COLOR = Color(169,204,163)
    TROPICAL_RAIN_FOREST_COLOR = Color(156,187,169)
    
    #### TODO: improve names
    LAND_DAMAGE: float = 10
    ####
    
    chance_to_spawn_animal_at_border = .000001
    chance_to_spawn_plant_at_border = .00001
    
    def __init__(self, rect: Rect, 
                 height: float = 0, 
                 moisture: float = 0,
                 is_border = False
                 ):
        pygame.sprite.Sprite.__init__(self)
        # Tile
        self.rect: Rect = rect
        
        # Groups
        self.neighbors: Custom_Group = Custom_Group()
        self.animals: Custom_Group = Custom_Group()
        self.plants: Custom_Group = Custom_Group()
        
        # Properties
        self.height: float = height
        self.moisture: float = moisture      
        self.water: float = 0
        self.is_border: bool = is_border
        self.is_coast: bool = False
        self.steepest_decline_neighbor: Tile | None = None
        
        # Color & Drawing
        self.color: Color = self.get_biome_color()
        self.image: Surface = Surface(self.rect.size, SRCALPHA)
        self.height_contours = []

    def update(self):
        self.animals.update()
        self.plants.update()
    
    def draw(self, screen: Surface):
        self.image.fill(self.color)

        self.animals.draw(self.image)
        self.plants.draw(self.image)
            
        screen.blit(self.image, self.rect.topleft)
        
        from config import draw_water_level
        if draw_water_level:
            self.draw_stat(self.water, screen)

        from config import draw_height_level
        if draw_height_level:
            self.draw_stat(self.height * 99, screen)
    
    # Animal handling
    def add_animal(self, animal):
        self.animals.add(animal)
        assert animal.tile == self, "Tiles Animal and Animals tile are not equal."
        
    def remove_animal(self, animal):
        self.animals.remove(animal)
        assert animal.tile != self, "Tiles Animal not being removed despite animal being removed."
    
    def add_plant(self, plant):
        self.plants.add(plant)
        assert plant.tile == self, "Tiles Plant and plants tile are not equal."  
        
    def remove_plant(self, plant):
        self.plants.remove(plant)
        assert plant.tile != self, "Tiles Plant not being removed despite plant being removed." 
    
    def has_animal(self) -> bool:
        return self.animals.__bool__()
    
    def has_plant(self) -> bool:
        return self.plants.__bool__()

    # Tile neighbor handling
    def add_neighbor(self, tile: Tile):
        self.neighbors.add(tile)
        self.is_coast = tile.water > 0 and self.water == 0
        
        self.update_steepest_descent(tile)

    def update_steepest_descent(self, tile: Tile):
        if not self.steepest_decline_neighbor:
            self.steepest_decline_neighbor = tile
        elif tile.get_height_dif(self) < self.steepest_decline_neighbor.get_height_dif(self):
            self.steepest_decline_neighbor = tile
    
    def get_neighbors(self) -> List[Tile]:
        ns = self.neighbors.sprites()
        shuffle(ns)
        return ns

    def get_random_neighbor(self, no_plant = False, no_animal = False) -> Tile | None:
        options = []
        has_options = False
        for tile in self.get_neighbors():
            if no_plant and tile.has_plant(): continue 
            if no_animal and tile.has_animal(): continue
            options.append(tile)
            has_options = True
            
        if has_options:
            return choice(options)
        else:
            return None
    
    def is_neighbor(self, tile: Tile) -> bool:  
        return self.rect.colliderect(tile.rect)
    
    def get_height_dif(self, tile: Tile) -> float:
        return tile.height - self.height
    
    # Drawing                  
    def get_biome_color(self) -> Color:
        if (self.height < 0.1):
            self.water = self.AMOUNT_OF_WATER_FOR_ONE_HEIGHT_LEVEL * (abs(self.height) + 1)
            return self.WATER_COLOR
        if (self.height < 0.12): 
            return self.SAND_COLOR
        
        if (self.height > 0.8):
            if (self.moisture < 0.1): 
                return self.SCORCHED_COLOR
            if (self.moisture < 0.2): 
                return self.BARE_COLOR
            if (self.moisture < 0.5): 
                return self.TUNDRA_COLOR
            return self.SNOW_COLOR

        if (self.height > 0.6):
            if (self.moisture < 0.33): 
                return self.TEMPERATE_DESERT_COLOR
            if (self.moisture < 0.66): 
                return self.SHRUBLAND_COLOR
            return self.TAIGA_COLOR

        if (self.height > 0.3):
            if (self.moisture < 0.16): 
                return self.TEMPERATE_DESERT_COLOR
            if (self.moisture < 0.50): 
                return self.GRASSLAND_COLOR
            if (self.moisture < 0.83): 
                return self.TEMPERATE_DECIDUOUS_FOREST_COLOR
            return self.TEMPERATE_RAIN_FOREST_COLOR

        if (self.moisture < 0.16): 
            return self.SUBTROPICAL_DESERT_COLOR
        if (self.moisture < 0.33): 
            return self.GRASSLAND_COLOR
        if (self.moisture < 0.66): 
            return self.TROPICAL_SEASONAL_FOREST_COLOR
        return self.TROPICAL_RAIN_FOREST_COLOR

    def draw_stat(self, stat: float, screen: Surface):
        stat_alpha = 255
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