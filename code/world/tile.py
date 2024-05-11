from __future__ import annotations

from random import choice, shuffle
from typing import List

import pygame

import helper.direction
import settings.colors
import settings.font
import settings.gui
import settings.simulation
import settings.test


class Tile(pygame.sprite.Sprite):
    size = 16

    def __init__(
        self,
        x: int,
        y: int,
        global_offset_x: int,
        global_offset_y: int,
        height: float = 0,
        moisture: float = 0,
        is_border: bool = False,
    ):
        pygame.sprite.Sprite.__init__(self)
        # Tile
        self.rect: pygame.Rect = pygame.Rect(x, y, Tile.size, Tile.size)
        self.global_rect = self.rect.move(global_offset_x, global_offset_y)

        self.image: pygame.Surface = pygame.Surface(self.rect.size)
        self.neighbors: dict[helper.direction.Direction, Tile] = {}

        # Height
        self._height: float = height
        self._moisture: float = moisture

        self.plant_growth_potential: float
        self.color: pygame.Color
        self.has_water: bool
        self.set_height_moisture_dependent_attributes()

        # Organisms
        self.animal: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
        self.plant: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()

        self.is_border: bool = is_border
        self.is_coast: bool = False
        self.steepest_decline_direction: helper.direction.Direction | None = None

        # Stats
        self.times_visted: int = 0

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

    @property
    def visible_rect(self):
        return self.global_rect.move(settings.test.offset_x, settings.test.offset_y)

    ########################## Initialisation #################################
    def set_height_moisture_dependent_attributes(self):
        """
        Set the color and plant growth potential attributes of a Tile object based on its height and moisture levels.
        """
        self.has_water = False

        if self.height <= settings.simulation.WATER_HEIGHT_LEVEL:
            # Waterlogged, no growth
            self.plant_growth_potential = settings.simulation.WATER_PLANT_GROWTH
            self.color = settings.colors.WATER_COLOR
            self.has_water = True
        elif self.height <= settings.simulation.BEACH_HEIGHT_LEVEL:
            # Sandy areas have limited growth
            self.plant_growth_potential = settings.simulation.BEACH_PLANT_GROWTH
            self.color = settings.colors.SAND_COLOR
        elif self.height <= settings.simulation.TROPICAL_HEIGHT_LEVEL:
            if self.moisture < 0.16:
                # Subtropical desert, low growth
                self.plant_growth_potential = (
                    settings.simulation.SUBTROPICAL_DESERT_PLANT_GROWTH
                )
                self.color = settings.colors.SUBTROPICAL_DESERT_COLOR
            elif self.moisture < 0.33:
                # Grassland, favorable
                self.plant_growth_potential = settings.simulation.GRASSLAND_PLANT_GROWTH
                self.color = settings.colors.GRASSLAND_COLOR
            elif self.moisture < 0.66:
                # Tropical seasonal forest, favorable
                self.plant_growth_potential = (
                    settings.simulation.TROPICAL_SEASON_FOREST_PLANT_GROWTH
                )
                self.color = settings.colors.TROPICAL_SEASONAL_FOREST_COLOR
            else:
                # Tropical rain forest, very favorable
                self.plant_growth_potential = (
                    settings.simulation.TROPICAL_RAIN_FOREST_PLANT_GROWTH
                )
                self.color = settings.colors.TROPICAL_RAIN_FOREST_COLOR
        elif self.height <= settings.simulation.TEMPERATE_HEIGHT_LEVEL:
            if self.moisture < 0.16:
                # Temperate desert, low growth
                self.plant_growth_potential = (
                    settings.simulation.TEMPERATE_DESERT_PLANT_GROWTH
                )
                self.color = settings.colors.TEMPERATE_DESERT_COLOR
            elif self.moisture < 0.50:
                # Grassland, favorable
                self.plant_growth_potential = settings.simulation.GRASSLAND_PLANT_GROWTH
                self.color = settings.colors.GRASSLAND_COLOR
            elif self.moisture < 0.83:
                # Temperate deciduous forest, very favorable
                self.plant_growth_potential = (
                    settings.simulation.TEMPERATER_DECIDOUS_FOREST_PLANT_GROWTH
                )
                self.color = settings.colors.TEMPERATE_DECIDUOUS_FOREST_COLOR
            else:
                # Temperate rain forest, optimal
                self.plant_growth_potential = (
                    settings.simulation.TEMPERATE_RAIN_FOREST_PLANT_GROWTH
                )
                self.color = settings.colors.TEMPERATE_RAIN_FOREST_COLOR
        elif self.height <= settings.simulation.TRANSITION_HEIGHT_LEVEL:
            if self.moisture < 0.33:
                # Temperate desert, low growth
                self.plant_growth_potential = (
                    settings.simulation.TEMPERATE_DESERT_PLANT_GROWTH
                )
                self.color = settings.colors.TEMPERATE_DESERT_COLOR
            elif self.moisture < 0.66:
                # Shrubland, moderate growth
                self.plant_growth_potential = settings.simulation.SHRUBLAND_PLANT_GROWTH
                self.color = settings.colors.SHRUBLAND_COLOR
            else:
                # Taiga, favorable
                self.plant_growth_potential = settings.simulation.TAIGA_PLANT_GROWTH
                self.color = settings.colors.TAIGA_COLOR
        elif self.height <= settings.simulation.MOUNTAIN_HEIGHT_LEVEL:
            if self.moisture < 0.1:
                # Scorched, minimal growth
                self.plant_growth_potential = settings.simulation.SCORCHED_PLANT_GROWTH
                self.color = settings.colors.SCORCHED_COLOR
            elif self.moisture < 0.2:
                # Bare, low growth
                self.plant_growth_potential = settings.simulation.BARE_PLANT_GROWTH
                self.color = settings.colors.BARE_COLOR
            elif self.moisture < 0.5:
                # Tundra, moderate growth
                self.plant_growth_potential = settings.simulation.TUNDRA_PLANT_GROWTH
                self.color = settings.colors.TUNDRA_COLOR
            else:
                # Snow, slightly favorable
                self.plant_growth_potential = settings.simulation.SNOW_PLANT_GROWTH
                self.color = settings.colors.SNOW_COLOR

        if self.color is None:
            raise ValueError(
                f"Color has not been set. moisture={self.moisture} height={self.height}"
            )
        if self.plant_growth_potential is None:
            raise ValueError(
                f"Plant growth has not been set. moisture={self.moisture} height={self.height}"
            )
        self.image.fill(self.color)
        # pygame.draw.rect(
        #     self.image,
        #     pygame.Color("gray40"),
        #     self.image.get_rect(topleft = (0,0)),
        #     width=1
        # )

    ########################## Main methods #################################
    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

        if settings.gui.draw_height_level:
            self.draw_stat(self.height * 9, screen)

    ########################## Drawing #################################
    def draw_stat(self, stat: float, screen: pygame.Surface):
        if self.has_animal():
            col = self.animal.sprite.color
        else:
            col = self.color

        text = settings.font.tile_font.render(
            str(int(stat)),
            True,
            settings.colors.choose_visible_text_color(col)
        )
        text_rect: pygame.Rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

    ########################## Tile Property Handling #################################
    def add_animal(self, animal):
        if self.has_animal():
            raise ValueError("Trying to add an animal despite tile already holding one")

        self.animal.add(animal)
        self.times_visted += 1

        if animal.tile != self:
            raise ValueError(
                "Animal's tile reference not matching with tile's animal reference"
            )

    def add_plant(self, plant):
        if self.has_plant():
            raise ValueError("Trying to add an plant despite tile already holding one")

        self.plant.add(plant)

        if plant.tile != self:
            raise ValueError(
                "Plant's tile reference not matching with tile's plant reference"
            )

    def has_animal(self) -> bool:
        return self.animal

    def has_plant(self) -> bool:
        return self.plant

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
