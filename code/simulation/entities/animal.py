from __future__ import annotations

import random

import pygame

import settings.database
import settings.simulation
from dna.dna import DNA
from .organism import Organism
from world.tile import Tile


class Animal(Organism):
    #region class settings
    _BASE_ENERGY_MAINTENANCE: float = 10
    _MAX_HEALTH: float = 100
    _MAX_ENERGY: float = 100
    _NUTRITION_FACTOR: float = 1
    _MAX_ALPHA: float = 255
    _MIN_ALPHA: float = 150
    _MOVEMENT_ENERGY_COST: float = 2
    #endregion
    #region starting values
    _STARTING_HEALTH: float = _MAX_HEALTH
    _STARTING_ENERGY: float = _MAX_ENERGY
    _STARTING_ATTACK_POWER_RANGE: tuple[float, float] = (8, 16)
    _STARTING_MOISTURE_PREFERENCE_RANGE: tuple[float, float] = (0, 1)
    _STARTING_HEIGHT_PREFERENCE_RANGE: tuple[float, float] = (0, 1)
    _STARTING_MUTATION_CHANCE_RANGE: tuple[float, float] = (0, 1)
    _STARTING_MIN_REPRODUCTION_HEALTH_RANGE: tuple[float, float] = (0, 1)
    _STARTING_MIN_REPRODUCTION_ENERGY_RANGE: tuple[float, float] = (0, 1)
    _STARTING_REPRODUCTION_CHANCE_RANGE: tuple[float, float] = (0, 1)
    _STARTING_ENERGY_TO_OFFSPRING_RATIO_RANGE: tuple[float, float] = (0, 1)
    #endregion
    #region class setting setters
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
    def set_movement_energy_cost(cls, value: float):
        cls._MOVEMENT_ENERGY_COST = value

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
    #endregion
    #region class properties
    @property
    def MAX_HEALTH(self) -> float:
        return Animal._MAX_HEALTH

    @property
    def MAX_ENERGY(self) -> float:
        return Animal._MAX_ENERGY

    @property
    def NUTRITION_FACTOR(self) -> float:
        return Animal._NUTRITION_FACTOR
    
    @property
    def MAX_ALPHA(self) -> float:
        return Animal._MAX_ALPHA
    
    @property
    def MIN_ALPHA(self) -> float:
        return Animal._MIN_ALPHA

    @staticmethod
    def BASE_ANIMAL_COLOR() -> pygame.Color:
        return pygame.Color(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )
    #endregion
    #region stats
    animals_birthed: int = 0
    animals_died: int = 0
    #endregion

    def __init__(
        self,
        tile: Tile,
        rect: pygame.Rect = None,
        parent: Animal = None,
        dna: DNA = None,
    ):
        #region defaults
        if not rect:
            rect = tile.rect.copy()

        if not dna:
            dna = DNA(
                Animal.BASE_ANIMAL_COLOR(),
                random.uniform(Animal._STARTING_ATTACK_POWER_RANGE[0], Animal._STARTING_ATTACK_POWER_RANGE[1]),
                random.uniform(Animal._STARTING_MOISTURE_PREFERENCE_RANGE[0], Animal._STARTING_MOISTURE_PREFERENCE_RANGE[1]),
                random.uniform(Animal._STARTING_HEIGHT_PREFERENCE_RANGE[0], Animal._STARTING_HEIGHT_PREFERENCE_RANGE[1]),
                random.uniform(Animal._STARTING_MUTATION_CHANCE_RANGE[0], Animal._STARTING_MUTATION_CHANCE_RANGE[1]),
                random.uniform(Animal._STARTING_MIN_REPRODUCTION_HEALTH_RANGE[0], Animal._STARTING_MIN_REPRODUCTION_HEALTH_RANGE[1]),
                random.uniform(Animal._STARTING_MIN_REPRODUCTION_ENERGY_RANGE[0], Animal._STARTING_MIN_REPRODUCTION_ENERGY_RANGE[1]),
                random.uniform(Animal._STARTING_REPRODUCTION_CHANCE_RANGE[0], Animal._STARTING_REPRODUCTION_CHANCE_RANGE[1]),
                random.uniform(Animal._STARTING_ENERGY_TO_OFFSPRING_RATIO_RANGE[0], Animal._STARTING_ENERGY_TO_OFFSPRING_RATIO_RANGE[1]),
            )
        #endregion

        super().__init__(
            tile,
            rect,
            Animal._STARTING_HEALTH,
            Animal._STARTING_ENERGY,
            dna,
        )

        self.parent: Animal | None = parent

    #region main methods
    def think(self):
        super().think()
        """
        Handles the decision-making process of the animal.

        If the animal's current tile has a plant, the animal will determine the best neighboring tile with the highest plant growth and set it as the desired tile movement. If there is no plant on the current tile, the animal will randomly select a neighboring tile without any animals and set it as the desired tile movement.

        The animal evaluates the neighboring tiles by checking if they have a plant and comparing the health of the plants on those tiles. The animal will choose the tile with the highest plant health as the destination.

        The desired tile movement is stored in the `desired_tile_movement` attribute of the animal.

        """
        if self.tile.has_plant():
            best_growth = self.tile.plant.sprite.health
            destination = None
        else:
            best_growth = 0
            destination = self.tile.get_random_neigbor(needs_no_animal=True)

        ns = self.tile.get_neighboring_tiles()
        for n in ns:
            if n.has_animal():
                continue
            if not n.has_plant():
                continue
            if n.plant.sprite.health > best_growth:
                best_growth = n.plant.sprite.health
                destination = n

        self.desired_tile_movement = destination

    def handle_attack(self):
        """
        Handles the attack behavior of the animal.

        If the animal's current tile has a plant and the animal wants to eat (determined by the `wants_to_eat()` method), the animal will attack the plant by calling the `attack()` method.

        """
        super().handle_attack()
        if self.tile.has_plant() and self.wants_to_eat():
            self.attack(self.tile.plant.sprite)

    def handle_movement(self):
        """
        Handles the movement of the animal.

        If the animal has a desired tile movement (stored in the `desired_tile_movement` attribute), the animal will enter that tile by calling the `enter_tile()` method.

        """
        super().handle_movement()
        if self.desired_tile_movement:
            self.enter_tile(self.desired_tile_movement)
            self.energy -= Animal._MOVEMENT_ENERGY_COST
    #endregion

    #region tiles
    def enter_tile(self, tile: Tile):
        super().enter_tile(tile)
        if tile.has_animal():
            raise ValueError("Animal trying to enter a tile that is already occupied.")
        else:
            if self.tile:
                self.tile.animal.remove(self)

            self.tile = tile
            tile.add_animal(self)

            self.check_tile_assignment()

    def check_tile_assignment(self):
        if not self.tile:
            raise ValueError("Animal does not have a tile!")
        if not self.tile.animal.has(self):
            raise ValueError("Animal-Tile assignment not equal.")
    #endregion

    #region energy and health
    def die(self):
        super().die()
        Animal.animals_died += 1

        if settings.database.save_csv and settings.database.save_animals_csv:
            self.save_to_csv()

        self.kill()

    def get_energy_maintenance(self) -> float:
        # TODO update this so it is different for different animals
        return Animal._BASE_ENERGY_MAINTENANCE
    #endregion

    #region attacking
    def get_attacked(self, attacking_organism: Organism):
        super().get_attacked(attacking_organism)
        if not self.is_alive():
            attacking_organism.animals_killed += 1

    def wants_to_eat(self) -> bool:
        # TODO add genes that define eating habits of animals
        return self.energy_ratio() < 1 or self.health_ratio() < 1
    #endregion

    #region reproduction
    def reproduce(self):
        options = self.tile.get_random_neigbor(needs_no_animal=True, needs_no_water=True)
        if options:
            # TODO add a gene that defines how long an animal is pregnant
            ENERGY_TO_CHILD = self.MAX_ENERGY * self.energy_to_offspring_ratio
            self.energy -= ENERGY_TO_CHILD
            offspring = self.copy(options)
            # TODO add a gene that defines the energy distribution
            offspring_energy_distribution = .4
            offspring.energy = ENERGY_TO_CHILD * offspring_energy_distribution
            offspring.health = ENERGY_TO_CHILD * (1-offspring_energy_distribution)
            settings.simulation.organisms.add(offspring)
            settings.simulation.animals.add(offspring)

    def copy(self, tile: Tile) -> Animal:
        super().copy(tile)
        Animal.animals_birthed += 1

        copied_dna = self.dna.copy()
        copied_dna.mutate()

        return Animal(tile, parent=self, dna=copied_dna)
    #endregion
