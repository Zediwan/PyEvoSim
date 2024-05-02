from __future__ import annotations

import random

import pygame
from pygame import Rect

import settings.colors
import settings.entity_settings
import settings.screen_settings
from dna.dna import DNA
from entities.organism import Organism
from world.tile import Tile


class Plant(Organism):
    @property
    def MAX_HEALTH(self) -> float:
        return settings.entity_settings.PLANT_MAX_HEALTH

    @property
    def MAX_ENERGY(self) -> float:
        return settings.entity_settings.PLANT_MAX_ENERGY

    @property
    def NUTRITION_FACTOR(self) -> float:
        return settings.entity_settings.PLANT_NUTRITION_FACTOR

    @property
    def REPRODUCTION_CHANCE(self) -> float:
        return (
            settings.entity_settings.PLANT_REPRODUCTION_CHANCE_FACTOR
            * self.health_ratio()
        )

    @property
    def MIN_REPRODUCTION_HEALTH(self) -> float:
        return settings.entity_settings.PLANT_MIN_REPRODUCTION_HEALTH

    @property
    def MIN_REPRODUCTION_ENERGY(self) -> float:
        return settings.entity_settings.PLANT_MIN_REPRODUCTION_ENERGY

    plants_birthed: int = 0
    plants_died: int = 0

    def __init__(
        self,
        tile: Tile,
        shape: Rect | None = None,
        parent: Plant = None,
        dna: DNA = None,
    ):
        if not shape:
            shape = tile.rect.copy()

        if not dna:
            dna = DNA(
                settings.colors.BASE_PLANT_COLOR,
                settings.entity_settings.PLANT_BASE_ATTACK_POWER,
                settings.entity_settings.PLANT_BASE_MOISTURE_PREFERENCE(),
                settings.entity_settings.PLANT_BASE_HEIGHT_PREFERENCE(),
            )

        super().__init__(
            tile,
            shape,
            settings.entity_settings.PLANT_STARTING_HEALTH(),
            settings.entity_settings.PLANT_STARTING_ENERGY(),
            dna,
        )

        self.parent: Plant | None = parent

    ########################## Main methods #################################
    def update(self):
        super().update()
        self.energy += self.get_photosynthesis_energy()

        if self.tile.is_coast:
            self.energy += self.get_coast_energy()

        if self.can_reproduce() and random.random() <= self.REPRODUCTION_CHANCE:
            self.reproduce()

        if not self.is_alive():
            self.die()

    def get_photosynthesis_energy(self):
        # Base photosynthesis energy calculation
        base_energy = (
            random.random()
            * self.tile.plant_growth_potential
            * settings.entity_settings.PLANT_PHOTOSYNTHESIS_ENERGY_MULTIPLIER
        )

        # Calculate the preference match
        height_preference_match = 0.5 + 0.5 * (
            1 - abs(self.tile.height - self.height_preference)
        )
        moisture_preference_match = 0.5 + 0.5 * (
            1 - abs(self.tile.moisture - self.moisture_preference)
        )

        # Combine the matches to adjust the base energy gain
        adjusted_energy_gain = (
            base_energy * (height_preference_match + moisture_preference_match) / 2
        )

        return adjusted_energy_gain

    def get_coast_energy(self):
        return random.random() * settings.entity_settings.PLANT_COAST_ENERGY_MULTIPLIER

    # TODO rethink plant drawing with biomes
    def draw(self):
        super().draw()

        pygame.draw.rect(
            pygame.display.get_surface(),
            self.tile.color.lerp(
                self.color, settings.colors.PLANT_TILE_COLOR_VISIBILITY
            ),
            self.shape.scale_by(self.health_ratio()),
        )

    ########################## Tile #################################
    def enter_tile(self, tile: Tile):
        super().enter_tile(tile)

        if self.tile:
            self.tile.remove_plant()

        self.tile = tile
        tile.add_plant(self)

        self.check_tile_assignment()

    def check_tile_assignment(self):
        if not self.tile:
            raise ValueError("Plant does not have a tile!")
        if self != self.tile.plant:
            raise ValueError("Plant-Tile assignment not equal.")

    ########################## Energy and Health #################################
    def die(self):
        super().die()
        Plant.plants_died += 1
        self.tile.remove_plant()

    def get_attacked(self, attacking_organism: Organism):
        super().get_attacked(attacking_organism)
        if not self.is_alive():
            attacking_organism.plants_killed += 1

    ########################## Reproduction #################################
    def reproduce(self):
        super().reproduce()
        option = self.tile.get_random_neigbor(no_plant=True, no_water=True)
        if option:
            self.energy -= (
                settings.entity_settings.PLANT_REPRODUCTION_ENERGY_COST_FACTOR
                * self.MAX_ENERGY
            )
            offspring = self.copy(option)
            offspring.health = (
                settings.entity_settings.PLANT_OFFSPRING_HEALTH_FACTOR * self.MAX_HEALTH
            )
            offspring.mutate()
            # print("Plant offspring birthed!")

    def copy(self, tile: Tile):
        super().copy(tile)
        Plant.plants_birthed += 1

        return Plant(tile, parent=self, dna=self.dna.copy())

    def mutate(self):
        super().mutate()
