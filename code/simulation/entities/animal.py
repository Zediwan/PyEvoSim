from __future__ import annotations

import random

import pygame

import settings.database
import settings.simulation
from dna.dna import DNA
from entities.organism import Organism
from world.tile import Tile


class Animal(Organism):
    _BASE_ENERGY_MAINTENANCE: float = 10
    _MAX_HEALTH: float = 100
    _MAX_ENERGY: float = 100
    _NUTRITION_FACTOR: float = 1
    _REPRODUCTION_CHANCE: float = 0.01
    _MIN_REPRODUCTION_HEALTH: float = 0.25
    _MIN_REPRODUCTION_ENERGY: float = 0.6
    _MAX_ALPHA: float = 255
    _MIN_ALPHA: float = 150
    _MOVEMENT_ENERGY_COST: float = 2

    # Starting values
    _STARTING_HEALTH: float = _MAX_HEALTH
    _STARTING_ENERGY: float = _MAX_ENERGY
    _STARTING_ATTACK_POWER_RANGE: tuple[float, float] = (8, 16)
    _STARTING_MOISTURE_PREFERENCE_RANGE: tuple[float, float] = (0, 1)
    _STARTING_HEIGHT_PREFERENCE: tuple[float, float] = (0, 1)
    _STARTING_MUTATION_CHANCE_RANGE: tuple[float, float] = (0, 1)

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
    def REPRODUCTION_CHANCE(self) -> float:
        return Animal._REPRODUCTION_CHANCE

    @property
    def MIN_REPRODUCTION_HEALTH(self) -> float:
        return Animal._MIN_REPRODUCTION_HEALTH

    @property
    def MIN_REPRODUCTION_ENERGY(self) -> float:
        return Animal._MIN_REPRODUCTION_ENERGY
    
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

    animals_birthed: int = 0
    animals_died: int = 0

    def __init__(
        self,
        tile: Tile,
        rect: pygame.Rect = None,
        parent: Animal = None,
        dna: DNA = None,
    ):
        if not rect:
            rect = tile.rect.copy()

        if not dna:
            dna = DNA(
                Animal.BASE_ANIMAL_COLOR(),
                random.uniform(Animal._STARTING_ATTACK_POWER_RANGE[0], Animal._STARTING_ATTACK_POWER_RANGE[1]),
                random.uniform(Animal._STARTING_MOISTURE_PREFERENCE_RANGE[0], Animal._STARTING_MOISTURE_PREFERENCE_RANGE[1]),
                random.uniform(Animal._STARTING_HEIGHT_PREFERENCE[0], Animal._STARTING_HEIGHT_PREFERENCE[1]),
                random.uniform(Animal._STARTING_MUTATION_CHANCE_RANGE[0], Animal._STARTING_MUTATION_CHANCE_RANGE[1]),
            )

        super().__init__(
            tile,
            rect,
            Animal._STARTING_HEALTH,
            Animal._STARTING_ENERGY,
            dna,
        )

        self.parent: Animal | None = parent

    ########################## Update #################################
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
            destination = self.tile.get_random_neigbor(no_animal=True)

        ns = self.tile.get_neighbors()
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

    ########################## Tile #################################
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

    ########################## Energy and Health #################################
    def die(self):
        super().die()
        Animal.animals_died += 1

        if settings.database.save_csv and settings.database.save_animals_csv:
            self.save_to_csv()

        self.kill()

    def get_attacked(self, attacking_organism: Organism):
        super().get_attacked(attacking_organism)
        if not self.is_alive():
            attacking_organism.animals_killed += 1

    def wants_to_eat(self) -> bool:
        # TODO add genes that define eating habits of animals
        return self.energy_ratio() < 1 or self.health_ratio() < 1

    def get_energy_maintenance(self) -> float:
        # TODO update this so it is different for different animals
        return Animal._BASE_ENERGY_MAINTENANCE

    ########################## Reproduction #################################
    def reproduce(self):
        unoccupied_neighbor = self.tile.get_random_neigbor(
            no_animal=True, no_water=True
        )
        if unoccupied_neighbor:
            # TODO create a gene that defines the amount of energy given to the child
            # TODO add a gene that defines how long an animal is pregnant
            ENERGY_TO_CHILD = self.MAX_ENERGY / 2
            self.energy -= ENERGY_TO_CHILD
            offspring = self.copy(unoccupied_neighbor)
            # TODO add a gene that defines the energy distribution
            offspring_energy_distribution = .4
            offspring.energy = ENERGY_TO_CHILD * offspring_energy_distribution
            offspring.health = (ENERGY_TO_CHILD * (1-offspring_energy_distribution)) * settings.entities.ENERGY_TO_HEALTH_RATIO
            offspring.mutate()
            settings.simulation.organisms.add(offspring)

    def copy(self, tile: Tile) -> Animal:
        super().copy(tile)
        Animal.animals_birthed += 1

        return Animal(tile, parent=self, dna=self.dna.copy())