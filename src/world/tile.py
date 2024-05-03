from __future__ import annotations

from random import choice, shuffle
from typing import List

import pygame
from pygame import Color, Rect, Surface

import helper.direction
import settings.colors
import settings.font
import settings.simulation_settings


class Tile:
    def __init__(
        self,
        rect: Rect,
        height: float = 0,
        moisture: float = 0,
        is_border: bool = False,
    ):
        # Tile
        self.rect: Rect = rect
        self.neighbors: dict[helper.direction.Direction, Tile] = {}

        # Height
        self._height: float = height
        self._moisture: float = moisture
        self.set_height_moisture_dependent_attributes()

        # Organisms
        from entities.animal import Animal

        self.animal: Animal | None = None

        from entities.plant import Plant

        self.plant: Plant | None = None

        self.is_border: bool = is_border
        self.is_coast: bool = False
        self.steepest_decline_direction: helper.direction.Direction | None = None

        # Stats
        self.times_visted: int = 0

    ########################## Initialisation #################################
    def set_height_moisture_dependent_attributes(self):
        """
        Set the color and plant growth potential attributes of a Tile object based on its height and moisture levels.
        """
        self.plant_growth_potential: float
        self.color: Color
        self.has_water: bool = False
    
        if self.height <= settings.simulation_settings.WATER_HEIGHT_LEVEL:
            # Waterlogged, no growth
            self.plant_growth_potential = settings.simulation_settings.WATER_PLANT_GROWTH
            self.color = settings.colors.WATER_COLOR
            self.has_water = True
        elif self.height <= settings.simulation_settings.BEACH_HEIGHT_LEVEL:
            # Sandy areas have limited growth
            self.plant_growth_potential = settings.simulation_settings.BEACH_PLANT_GROWTH
            self.color = settings.colors.SAND_COLOR
        elif self.height <= settings.simulation_settings.TROPICAL_HEIGHT_LEVEL:
            if self.moisture < 0.16:
                # Subtropical desert, low growth
                self.plant_growth_potential = settings.simulation_settings.SUBTROPICAL_DESERT_PLANT_GROWTH
                self.color = settings.colors.SUBTROPICAL_DESERT_COLOR
            elif self.moisture < 0.33:
                # Grassland, favorable
                self.plant_growth_potential = settings.simulation_settings.GRASSLAND_PLANT_GROWTH
                self.color = settings.colors.GRASSLAND_COLOR
            elif self.moisture < 0.66:
                # Tropical seasonal forest, favorable
                self.plant_growth_potential = settings.simulation_settings.TROPICAL_SEASON_FOREST_PLANT_GROWTH
                self.color = settings.colors.TROPICAL_SEASONAL_FOREST_COLOR
            else:
                # Tropical rain forest, very favorable
                self.plant_growth_potential = settings.simulation_settings.TROPICAL_RAIN_FOREST_PLANT_GROWTH
                self.color = settings.colors.TROPICAL_RAIN_FOREST_COLOR
        elif self.height <= settings.simulation_settings.TEMPERATE_HEIGHT_LEVEL:
            if self.moisture < 0.16:
                # Temperate desert, low growth
                self.plant_growth_potential = settings.simulation_settings.TEMPERATE_DESERT_PLANT_GROWTH
                self.color = settings.colors.TEMPERATE_DESERT_COLOR
            elif self.moisture < 0.50:
                # Grassland, favorable
                self.plant_growth_potential = settings.simulation_settings.GRASSLAND_PLANT_GROWTH
                self.color = settings.colors.GRASSLAND_COLOR
            elif self.moisture < 0.83:
                # Temperate deciduous forest, very favorable
                self.plant_growth_potential = settings.simulation_settings.TEMPERATER_DECIDOUS_FOREST_PLANT_GROWTH
                self.color = settings.colors.TEMPERATE_DECIDUOUS_FOREST_COLOR
            else:
                # Temperate rain forest, optimal
                self.plant_growth_potential = settings.simulation_settings.TEMPERATE_RAIN_FOREST_PLANT_GROWTH
                self.color = settings.colors.TEMPERATE_RAIN_FOREST_COLOR
        elif self.height <= settings.simulation_settings.TRANSITION_HEIGHT_LEVEL:
            if self.moisture < 0.33:
                # Temperate desert, low growth
                self.plant_growth_potential = settings.simulation_settings.TEMPERATE_DESERT_PLANT_GROWTH
                self.color = settings.colors.TEMPERATE_DESERT_COLOR
            elif self.moisture < 0.66:
                # Shrubland, moderate growth
                self.plant_growth_potential = settings.simulation_settings.SHRUBLAND_PLANT_GROWTH
                self.color = settings.colors.SHRUBLAND_COLOR
            else:
                # Taiga, favorable
                self.plant_growth_potential = settings.simulation_settings.TAIGA_PLANT_GROWTH
                self.color = settings.colors.TAIGA_COLOR
        elif self.height <= settings.simulation_settings.MOUNTAIN_HEIGHT_LEVEL:
            if self.moisture < 0.1:
                # Scorched, minimal growth
                self.plant_growth_potential = settings.simulation_settings.SCORCHED_PLANT_GROWTH
                self.color = settings.colors.SCORCHED_COLOR
            elif self.moisture < 0.2:
                # Bare, low growth
                self.plant_growth_potential = settings.simulation_settings.BARE_PLANT_GROWTH
                self.color = settings.colors.BARE_COLOR
            elif self.moisture < 0.5:
                # Tundra, moderate growth
                self.plant_growth_potential = settings.simulation_settings.TUNDRA_PLANT_GROWTH
                self.color = settings.colors.TUNDRA_COLOR
            else:
                # Snow, slightly favorable
                self.plant_growth_potential = settings.simulation_settings.SNOW_PLANT_GROWTH
                self.color = settings.colors.SNOW_COLOR
            
        assert self.color is not None, f"Color has not been set. moisture={self.moisture} height={self.height}"
        assert self.plant_growth_potential is not None, f"Plant growth has not been set. moisture={self.moisture} height={self.height}"

    ########################## Properties #################################
    @property
    def moisture(self) -> float:
        return self._moisture
    
    @moisture.setter
    def moisture(self, value: float):
        if value < 0:
            raise ValueError("Moisture value is smaller than 0")
        elif value > 1:
            raise ValueError("Moisture value is bigger than 1")
        else:
            self._moisture = value
        self.set_height_moisture_dependent_attributes()
        
    @property
    def height(self) -> float:
        return self._height
    
    @height.setter
    def height(self, value: float):
        if value < 0:
            raise ValueError("Height value is smaller than 0")
        elif value > 1:
            raise ValueError("Height value is bigger than 1")
        else:
            self._height = value
        self.set_height_moisture_dependent_attributes()
            
    ########################## Main methods #################################
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

    ########################## Drawing #################################
    def draw_stat(self, stat: float):
        # Analyzing background color brightness
        if self.has_animal():
            col = self.animal.color
        else:
            col = self.color

        text = settings.font.font.render(str(round(stat)), True, col.__invert__())
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
        assert self.animal is None, "Tile already occupied by an animal."

        self.animal = animal
        self.times_visted += 1

        assert animal.tile == self, "Animal-Tile assignment not equal."

    def add_plant(self, plant):
        assert self.plant is None, "Tile is already occupied by a plant."

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

    def add_neighbor(self, direction: helper.direction.Direction, tile: Tile):
        self.neighbors[direction] = tile
        self.is_coast = tile.has_water and self.has_water

    def get_directions(self) -> List[helper.direction.Direction]:
        dirs = list(self.neighbors.keys())
        shuffle(dirs)
        return dirs

    def get_neighbors(self) -> List[Tile]:
        ns = list(self.neighbors.values())
        shuffle(ns)
        return ns

    def get_neighbor(self, direction: helper.direction.Direction) -> Tile | None:
        return self.neighbors.get(direction, None)

    def get_random_neigbor(
        self, no_plant=False, no_animal=False, no_water=False
    ) -> Tile | None:
        options = []
        has_options = False
        for tile in self.neighbors.values():
            if no_plant and tile.has_plant():
                continue
            if no_animal and tile.has_animal():
                continue
            if no_water and tile.has_water:
                continue
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
