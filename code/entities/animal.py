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


class Animal(Organism):
    @property
    def MAX_HEALTH(self) -> float:
        return 100

    @property
    def MAX_ENERGY(self) -> float:
        return 200

    @property
    def NUTRITION_FACTOR(self) -> float:
        return 1

    @property
    def REPRODUCTION_CHANCE(self) -> float:
        return .01

    @property
    def MIN_REPRODUCTION_HEALTH(self) -> float:
        return 0.25

    @property
    def MIN_REPRODUCTION_ENERGY(self) -> float:
        return 0.6
    
    @property
    def MAX_ALPHA(self) -> float:
        return settings.colors.ANIMAL_MAX_ALPHA
    
    @property
    def MIN_ALPHA(self) -> float:
        return settings.colors.ANIMAL_MIN_ALPHA

    animals_birthed: int = 0
    animals_died: int = 0

    def __init__(
        self,
        tile: Tile,
        rect: pygame.Rect | None = None,
        parent: Animal = None,
        dna: DNA = None,
    ):
        if not rect:
            rect = tile.rect.copy()

        if not dna:
            dna = DNA(
                settings.colors.BASE_ANIMAL_COLOR(),
                settings.entities.ANIMAL_BASE_ATTACK_POWER,
                settings.entities.ANIMAL_BASE_MOISTURE_PREFERENCE(),
                settings.entities.PLANT_BASE_HEIGHT_PREFERENCE(),
            )

        super().__init__(
            tile,
            rect,
            settings.entities.ANIMAL_STARTING_HEALTH(),
            settings.entities.ANIMAL_STARTING_ENERGY(),
            dna,
        )

        self.parent: Animal | None = parent

    ########################## Update #################################
    def use_maintanance_energy(self):
        super().use_maintanance_energy()
        self.energy -= random.random() * settings.entities.ANIMAL_BASE_ENERGY_MAINTANCE

    def handle_drowning(self):
        """
        Handles the drowning behavior of the animal.

        If the animal's current tile has water (determined by the `has_water` attribute of the tile), the animal's health will be decreased by the value specified in the `DROWNING_DAMAGE` constant in the `settings.entities` module.

        """
        super().handle_drowning()
        if self.tile.has_water:
            self.health -= settings.entities.DROWNING_DAMAGE

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

    ########################## Tile #################################
    def enter_tile(self, tile: Tile):
        super().enter_tile(tile)
        if tile.has_animal():
            raise ValueError("Animal trying to enter a tile that is already occupied.")

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

        if settings.database.save_csv:
            if settings.database.save_animals_csv:
                self.save_to_csv()

        self.kill()

    def attack(self, organism_to_attack: Organism):
        assert (
            self.tile.is_neighbor(organism_to_attack.tile)
            or self.tile == organism_to_attack.tile
        ), "Organism to attack is not a neighbor or on own tile."
        organism_to_attack.get_attacked(self)

    def get_attacked(self, attacking_organism: Organism):
        super().get_attacked(attacking_organism)
        if not self.is_alive():
            attacking_organism.animals_killed += 1

    def wants_to_eat(self) -> bool:
        return self.energy_ratio() < 1 or self.health_ratio() < 1

    ########################## Reproduction #################################
    def reproduce(self):
        super().reproduce()
        unoccupied_neighbor = self.tile.get_random_neigbor(
            no_animal=True, no_water=True
        )
        if unoccupied_neighbor:
            ENERGY_TO_CHILD = self.MAX_ENERGY / 2
            self.energy -= ENERGY_TO_CHILD
            offspring = self.copy(unoccupied_neighbor)
            offspring_energy_distribution = .4
            offspring.energy = ENERGY_TO_CHILD * offspring_energy_distribution
            offspring.health = (ENERGY_TO_CHILD * (1-offspring_energy_distribution)) * settings.entities.ENERGY_TO_HEALTH_RATIO
            offspring.mutate()
            settings.simulation.organisms.add(offspring)

    def copy(self, tile: Tile) -> Animal:
        super().copy(tile)
        Animal.animals_birthed += 1

        return Animal(tile, parent=self, dna=self.dna.copy())
