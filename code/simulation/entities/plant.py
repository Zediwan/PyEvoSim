from __future__ import annotations

import random
import pygame

import settings.colors
import settings.database
import settings.entities
import settings.screen
import settings.simulation
from dna.dna import DNA
from entities.organism import Organism
from world.tile import Tile


class Plant(Organism):
    _BASE_ENERGY_MAINTENANCE: float = 1

    @property
    def MAX_HEALTH(self) -> float:
        return settings.entities.PLANT_MAX_HEALTH

    @property
    def MAX_ENERGY(self) -> float:
        return settings.entities.PLANT_MAX_ENERGY

    @property
    def NUTRITION_FACTOR(self) -> float:
        return settings.entities.PLANT_NUTRITION_FACTOR

    @property
    def REPRODUCTION_CHANCE(self) -> float:
        return settings.entities.PLANT_REPRODUCTION_CHANCE_FACTOR * self.health_ratio()

    @property
    def MIN_REPRODUCTION_HEALTH(self) -> float:
        return settings.entities.PLANT_MIN_REPRODUCTION_HEALTH

    @property
    def MIN_REPRODUCTION_ENERGY(self) -> float:
        return settings.entities.PLANT_MIN_REPRODUCTION_ENERGY
    
    @property
    def MAX_ALPHA(self) -> float:
        return settings.colors.PLANT_MAX_ALPHA
    
    @property
    def MIN_ALPHA(self) -> float:
        return settings.colors.PLANT_MIN_ALPHA

    plants_birthed: int = 0
    plants_died: int = 0

    def __init__(
        self,
        tile: Tile,
        rect: pygame.Rect | None = None,
        parent: Plant = None,
        dna: DNA = None,
    ):
        if not rect:
            rect = tile.rect.copy()

        if not dna:
            dna = DNA(
                settings.colors.BASE_PLANT_COLOR,
                settings.entities.PLANT_BASE_ATTACK_POWER,
                settings.entities.PLANT_BASE_MOISTURE_PREFERENCE(),
                settings.entities.PLANT_BASE_HEIGHT_PREFERENCE(),
                settings.entities.PLANT_STARTING_MUTATION_CHANCE()
            )

        super().__init__(
            tile,
            rect,
            settings.entities.PLANT_STARTING_HEALTH(),
            settings.entities.PLANT_STARTING_ENERGY(),
            dna,
        )

        self.parent: Plant | None = parent

    ########################## Update #################################
    def update(self):
        """
        Update the plant's state and perform photosynthesis.

        This method updates the plant's state by calling the parent class's update method and then performs photosynthesis.
        The steps performed in this method are as follows:

        1. Call the parent class's update method:
        - This updates the plant's health and energy based on its current state.

        2. Perform photosynthesis:
        - Calculate the base energy gained through photosynthesis by multiplying a random number between 0 and 1 with the plant's growth potential and the energy multiplier for photosynthesis.
        - Calculate the preference match for height and moisture by subtracting the differences between the tile's height and moisture and the plant's height and moisture preferences from 1.
        - Adjust the base energy gain by multiplying it with the average of the height preference match and moisture preference match.
        - Add the adjusted energy gain to the plant's energy.

        This method is called during the plant's update process to update its state and simulate photosynthesis.
        """
        super().update()
        self.photosynthesise()

    def photosynthesise(self):
        """
        Calculate the energy gained through photosynthesis.

        This method calculates the energy gained by the plant through photosynthesis. It performs the following steps:

        1. Base photosynthesis energy calculation:
        - Generate a random number between 0 and 1.
        - Multiply it by the plant's growth potential and the energy multiplier for photosynthesis.

        2. Calculate the preference match:
        - Calculate the difference between the tile's height and the plant's height preference.
        - Calculate the difference between the tile's moisture and the plant's moisture preference.
        - Subtract these differences from 1 to get the match values.

        3. Adjust the base energy gain:
        - Multiply the base energy by the average of the height preference match and moisture preference match.

        4. Add the adjusted energy gain to the plant's energy.

        This method is called during the plant's update process to simulate photosynthesis and increase its energy level.
        """
        # Base photosynthesis energy calculation
        base_energy = (
            random.random()
            * self.tile.plant_growth_potential
            * settings.entities.PLANT_PHOTOSYNTHESIS_ENERGY_MULTIPLIER
        )

        # Calculate the preference match
        height_preference_match = 1 - abs(self.tile.height - self.height_preference)
        moisture_preference_match = 1 - abs(
            self.tile.moisture - self.moisture_preference
        )

        # Combine the matches to adjust the base energy gain
        adjusted_energy_gain = (
            base_energy * (height_preference_match + moisture_preference_match) / 2
        )

        self.energy += adjusted_energy_gain

    ########################## Tile #################################
    def enter_tile(self, tile: Tile):
        super().enter_tile(tile)

        if self.tile:
            self.tile.plant.remove(self)

        self.tile = tile
        tile.add_plant(self)

        self.check_tile_assignment()

    def check_tile_assignment(self):
        if not self.tile:
            raise ValueError("Plant does not have a tile!")
        if not self.tile.plant.has(self):
            raise ValueError("Plant-Tile assignment not equal.")

    ########################## Energy and Health #################################
    def die(self):
        super().die()
        Plant.plants_died += 1

        if settings.database.save_csv:
            if settings.database.save_plants_csv:
                self.save_to_csv()

        self.kill()

    def get_attacked(self, attacking_organism: Organism):
        super().get_attacked(attacking_organism)
        if not self.is_alive():
            attacking_organism.plants_killed += 1

    def get_energy_maintenance(self) -> float:
        # TODO update this so it is different for different plants
        return Plant._BASE_ENERGY_MAINTENANCE

    ########################## Reproduction #################################
    def reproduce(self):
        super().reproduce()
        option = self.tile.get_random_neigbor(no_plant=True, no_water=True)
        if option:
            ENERGY_TO_CHILD = max(
                settings.entities.PLANT_REPRODUCTION_ENERGY_COST_FACTOR * self.MAX_ENERGY,
                self.energy * .8
                )
            self.energy -= ENERGY_TO_CHILD
            offspring = self.copy(option)
            offspring_energy_distribution = .5
            offspring.energy = ENERGY_TO_CHILD * offspring_energy_distribution
            offspring.health = (ENERGY_TO_CHILD * (1-offspring_energy_distribution)) * settings.entities.ENERGY_TO_HEALTH_RATIO
            offspring.mutate()
            settings.simulation.organisms.add(offspring)
            # print("Plant offspring birthed!")

    def copy(self, tile: Tile):
        super().copy(tile)
        Plant.plants_birthed += 1

        return Plant(tile, parent=self, dna=self.dna.copy())

    def mutate(self):
        super().mutate()
