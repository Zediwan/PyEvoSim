from __future__ import annotations

import random

import pygame

from ..settings import database, simulation
from ..terrain.tile import Tile
from .organism import Organism
from .properties.dna import DNA


class Plant(Organism):
    # region class settings
    _BASE_ENERGY_MAINTENANCE: float = 0
    _MAX_HEALTH: float = 50
    _MAX_ENERGY: float = 50
    _NUTRITION_FACTOR: float = 0.8
    _REPRODUCTION_ENERGY_COST_FACTOR: float = 0.5
    _OFFSPRING_HEALTH_FACTOR: float = 0
    _OFFSPRING_ENERGY_FACTOR: float = 0.5
    _PHOTOSYNTHESIS_ENERGY_MULTIPLIER: float = 4
    _COAST_ENERGY_MULTIPLIER: float = 3
    _BASE_COLOR: pygame.Color = pygame.Color(76, 141, 29)
    _MAX_ALPHA: float = 100
    _MIN_ALPHA: float = 0
    # endregion
    # region starting values
    _STARTING_HEALTH: float = _MAX_HEALTH
    _STARTING_ENERGY: float = _MAX_ENERGY
    _STARTING_ATTACK_POWER_RANGE: tuple[float, float] = (0, 1)
    _STARTING_DEFENSE_RANGE: tuple[float, float] = _STARTING_ATTACK_POWER_RANGE
    _STARTING_MOISTURE_PREFERENCE_RANGE: tuple[float, float] = (0, 1)
    _STARTING_HEIGHT_PREFERENCE_RANGE: tuple[float, float] = (0, 1)
    _STARTING_MUTATION_CHANCE_RANGE: tuple[float, float] = (0, 1)
    _STARTING_MIN_REPRODUCTION_HEALTH_RANGE: tuple[float, float] = (0.1, 1)
    _STARTING_MIN_REPRODUCTION_ENERGY_RANGE: tuple[float, float] = (0.1, 1)
    _STARTING_REPRODUCTION_CHANCE_RANGE: tuple[float, float] = (0, 1)
    _STARTING_ENERGY_TO_OFFSPRING_RATIO_RANGE: tuple[float, float] = (0, 1)

    # endregion
    # region class setting setters
    @classmethod
    def set_base_energy_maintenance(cls, value: float):
        cls._BASE_ENERGY_MAINTENANCE = value

    @classmethod
    def set_max_health(cls, value: float):
        cls._MAX_HEALTH = value

    @classmethod
    def set_max_energy(cls, value: float):
        cls._MAX_ENERGY = value

    @classmethod
    def set_nutrition_factor(cls, value: float):
        cls._NUTRITION_FACTOR = value

    @classmethod
    def set_starting_health(cls, value: float):
        cls._STARTING_HEALTH = value

    @classmethod
    def set_starting_energy(cls, value: float):
        cls._STARTING_ENERGY = value

    @classmethod
    def set_starting_min_reproduction_health_range(cls, value: tuple[float, float]):
        cls._STARTING_MIN_REPRODUCTION_HEALTH_RANGE = value

    @classmethod
    def set_starting_min_reproduction_energy_range(cls, value: tuple[float, float]):
        cls._STARTING_MIN_REPRODUCTION_ENERGY_RANGE = value

    @classmethod
    def set_starting_attack_power_range(cls, value: tuple[float, float]):
        cls._STARTING_ATTACK_POWER_RANGE = value

    @classmethod
    def set_starting_defense_range(cls, value: tuple[float, float]):
        cls._STARTING_DEFENSE_RANGE = value

    @classmethod
    def set_starting_moisture_preference_range(cls, value: tuple[float, float]):
        cls._STARTING_MOISTURE_PREFERENCE_RANGE = value

    @classmethod
    def set_starting_height_preference(cls, value: tuple[float, float]):
        cls._STARTING_HEIGHT_PREFERENCE_RANGE = value

    @classmethod
    def set_starting_mutation_chance_range(cls, value: tuple[float, float]):
        cls._STARTING_MUTATION_CHANCE_RANGE = value

    @classmethod
    def set_starting_reproduction_chance_range(cls, value: tuple[float, float]):
        cls._STARTING_REPRODUCTION_CHANCE_RANGE = value

    @classmethod
    def set_starting_energy_to_offspring_ratio_range(cls, value: tuple[float, float]):
        cls._STARTING_ENERGY_TO_OFFSPRING_RATIO_RANGE = value

    # endregion
    # region class properties
    @property
    def MAX_HEALTH(self) -> float:
        return Plant._MAX_HEALTH

    @property
    def MAX_ENERGY(self) -> float:
        return Plant._MAX_ENERGY

    @property
    def NUTRITION_FACTOR(self) -> float:
        return Plant._NUTRITION_FACTOR

    @property
    def MAX_ALPHA(self) -> float:
        return Plant._MAX_ALPHA

    @property
    def MIN_ALPHA(self) -> float:
        return Plant._MIN_ALPHA

    # endregion
    # region stats
    plants_birthed: int = 0
    plants_died: int = 0
    # endregion

    def __init__(
        self,
        tile: Tile,
        rect: pygame.Rect | None = None,
        parent: Plant = None,
        dna: DNA = None,
        health: float = None,
        energy: float = None,
    ):
        # region defaults
        if not rect:
            rect = tile.rect.copy()
        if not dna:
            dna = DNA(
                Plant._BASE_COLOR,
                random.uniform(
                    Plant._STARTING_ATTACK_POWER_RANGE[0],
                    Plant._STARTING_ATTACK_POWER_RANGE[1],
                ),
                random.uniform(
                    Plant._STARTING_MOISTURE_PREFERENCE_RANGE[0],
                    Plant._STARTING_MOISTURE_PREFERENCE_RANGE[1],
                ),
                random.uniform(
                    Plant._STARTING_HEIGHT_PREFERENCE_RANGE[0],
                    Plant._STARTING_HEIGHT_PREFERENCE_RANGE[1],
                ),
                random.uniform(
                    Plant._STARTING_MUTATION_CHANCE_RANGE[0],
                    Plant._STARTING_MUTATION_CHANCE_RANGE[1],
                ),
                random.uniform(
                    Plant._STARTING_MIN_REPRODUCTION_HEALTH_RANGE[0],
                    Plant._STARTING_MIN_REPRODUCTION_HEALTH_RANGE[1],
                ),
                random.uniform(
                    Plant._STARTING_MIN_REPRODUCTION_ENERGY_RANGE[0],
                    Plant._STARTING_MIN_REPRODUCTION_ENERGY_RANGE[1],
                ),
                random.uniform(
                    Plant._STARTING_REPRODUCTION_CHANCE_RANGE[0],
                    Plant._STARTING_REPRODUCTION_CHANCE_RANGE[1],
                ),
                random.uniform(
                    Plant._STARTING_ENERGY_TO_OFFSPRING_RATIO_RANGE[0],
                    Plant._STARTING_ENERGY_TO_OFFSPRING_RATIO_RANGE[1],
                ),
                random.uniform(
                    Plant._STARTING_DEFENSE_RANGE[0], Plant._STARTING_DEFENSE_RANGE[1]
                ),
            )
        if health is None:
            health = Plant._STARTING_HEALTH
        if energy is None:
            energy = Plant._STARTING_ENERGY
        # endregion

        super().__init__(
            tile,
            rect,
            health,
            energy,
            dna,
        )
        self.image.set_alpha(100)
        self.parent: Plant | None = parent

    # region main methods
    def update(self):
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
            * Plant._PHOTOSYNTHESIS_ENERGY_MULTIPLIER
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

    # endregion

    # region tile
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

    # endregion

    # region health and energy
    def die(self):
        super().die()
        Plant.plants_died += 1

        if database.save_csv:
            if database.save_plants_csv:
                self.save_to_csv()

        self.kill()

    def get_energy_maintenance(self) -> float:
        # TODO update this so it is different for different plants
        return Plant._BASE_ENERGY_MAINTENANCE

    # endregion

    # region attacking
    def get_attacked(self, attacking_organism: Organism):
        super().get_attacked(attacking_organism)
        if not self.is_alive():
            attacking_organism.plants_killed += 1

    # endregion

    # region reproduction
    def reproduce(self):
        option = self.tile.get_random_neigbor(needs_no_plant=True, needs_no_water=True)
        if option:
            ENERGY_TO_CHILD = self.MAX_ENERGY * self.energy_to_offspring_ratio
            offspring_energy_distribution = (
                0.4  # TODO add a gene that defines the energy distribution
            )
            self.energy -= ENERGY_TO_CHILD
            offspring = self.copy(
                option,
                health=ENERGY_TO_CHILD * offspring_energy_distribution,
                energy=ENERGY_TO_CHILD * (1 - offspring_energy_distribution),
            )
            simulation.organisms.add(offspring)
            simulation.plants.add(offspring)

    def copy(self, tile: Tile, health: float = None, energy: float = None):
        super().copy(tile)
        Plant.plants_birthed += 1

        copied_dna = self.dna.copy()
        copied_dna.mutate()

        return Plant(tile, parent=self, dna=copied_dna, health=health, energy=energy)

    # endregion
