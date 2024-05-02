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
        tile_size: int,
        height: float = 0,
        moisture: float = 0,
        is_border=False,
    ):
        # Tile
        self.rect: Rect = rect
        self.tile_size: int = tile_size
        self.neighbors: dict[helper.direction.Direction, Tile] = {}

        # Height
        self.height: float = height
        self.moisture: float = moisture
        self.color: Color = self.get_biome_color()

        # Organisms
        from entities.animal import Animal

        self.animal: Animal | None = None

        from entities.plant import Plant

        self.plant: Plant | None = None

        self.has_water = self.height < settings.simulation_settings.WATER_LEVEL
        self.is_border: bool = is_border
        self.is_coast: bool = False
        self.steepest_decline_direction: helper.direction.Direction | None = None
        self.plant_growth_potential: float = self.calculate_plant_growth()

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
    def calculate_plant_growth(self) -> float:
        if self.height < settings.simulation_settings.WATER_LEVEL:
            return 0  # Waterlogged, no growth

        if self.height < 0.12:
            return 0.32  # Sandy areas have limited growth

        if self.height > 0.8:
            if self.moisture < 0.1:
                return 0.35  # Scorched, minimal growth
            if self.moisture < 0.2:
                return 0.6  # Bare, low growth
            if self.moisture < 0.5:
                return 0.65  # Tundra, moderate growth
            return 0.7  # Snow, slightly favorable

        if self.height > 0.6:
            if self.moisture < 0.33:
                return 0.6  # Temperate desert, low growth
            if self.moisture < 0.66:
                return 0.7  # Shrubland, moderate growth
            return 0.8  # Taiga, favorable

        if self.height > 0.3:
            if self.moisture < 0.16:
                return 0.6  # Temperate desert, low growth
            if self.moisture < 0.50:
                return 0.9  # Grassland, favorable
            if self.moisture < 0.83:
                return 0.95  # Temperate deciduous forest, very favorable
            return 1  # Temperate rain forest, optimal

        if self.moisture < 0.16:
            return 0.3  # Subtropical desert, low growth
        if self.moisture < 0.33:
            return 0.7  # Grassland, favorable
        if self.moisture < 0.66:
            return 0.75  # Tropical seasonal forest, favorable
        return 0.9  # Tropical rain forest, very favorable

    ########################## Drawing #################################
    def get_biome_color(self) -> Color:
        if self.height < settings.simulation_settings.WATER_LEVEL:
            return settings.colors.WATER_COLOR
        if self.height < 0.12:
            return settings.colors.SAND_COLOR

        if self.height > 0.8:
            if self.moisture < 0.1:
                return settings.colors.SCORCHED_COLOR
            if self.moisture < 0.2:
                return settings.colors.BARE_COLOR
            if self.moisture < 0.5:
                return settings.colors.TUNDRA_COLOR
            return settings.colors.SNOW_COLOR

        if self.height > 0.6:
            if self.moisture < 0.33:
                return settings.colors.TEMPERATE_DESERT_COLOR
            if self.moisture < 0.66:
                return settings.colors.SHRUBLAND_COLOR
            return settings.colors.TAIGA_COLOR

        if self.height > 0.3:
            if self.moisture < 0.16:
                return settings.colors.TEMPERATE_DESERT_COLOR
            if self.moisture < 0.50:
                return settings.colors.GRASSLAND_COLOR
            if self.moisture < 0.83:
                return settings.colors.TEMPERATE_DECIDUOUS_FOREST_COLOR
            return settings.colors.TEMPERATE_RAIN_FOREST_COLOR

        if self.moisture < 0.16:
            return settings.colors.SUBTROPICAL_DESERT_COLOR
        if self.moisture < 0.33:
            return settings.colors.GRASSLAND_COLOR
        if self.moisture < 0.66:
            return settings.colors.TROPICAL_SEASONAL_FOREST_COLOR
        return settings.colors.TROPICAL_RAIN_FOREST_COLOR

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
