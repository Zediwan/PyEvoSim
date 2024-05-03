from __future__ import annotations

import csv
import os
import random
from abc import ABC, abstractmethod

import pygame

import settings.colors
import settings.database
import settings.entities
import settings.screen
import stats.stat_panel
from dna.dna import DNA
from world.tile import Tile


class Organism(ABC, pygame.sprite.Sprite):
    @property
    @abstractmethod
    def MAX_HEALTH(self) -> float:
        pass

    @property
    @abstractmethod
    def MAX_ENERGY(self) -> float:
        pass

    @property
    def MIN_HEALTH(self) -> float:
        return 0

    @property
    def MIN_ENERGY(self) -> float:
        return 0

    @property
    @abstractmethod
    def NUTRITION_FACTOR(self) -> float:
        pass

    @property
    @abstractmethod
    def REPRODUCTION_CHANCE(self) -> float:
        pass

    @property
    @abstractmethod
    def MIN_REPRODUCTION_HEALTH(self) -> float:
        pass

    @property
    @abstractmethod
    def MIN_REPRODUCTION_ENERGY(self) -> float:
        pass

    # Stats
    organisms_birthed: int = 0
    organisms_died: int = 0
    next_organism_id: int = 0

    def __init__(
        self,
        tile: Tile,
        shape: pygame.Rect,
        health: float,
        energy: float,
        dna: DNA = None,
    ):
        pygame.sprite.Sprite.__init__(self)

        self.id = Organism.next_organism_id
        Organism.next_organism_id += 1

        if not dna:
            dna = DNA(
                settings.colors.BASE_ORGANISM_COLOR,
                settings.entities.ORGANISM_BASE_ATTACK_POWER,
                settings.entities.ORGANISM_BASE_MOISTURE_PREFERENCE,
                settings.entities.ORGANISM_BASE_HEIGHT_PREFERENCE,
            )
        self.dna: DNA = dna

        self._set_attributes_from_dna()

        self.health = health
        self.energy = energy

        self.shape: pygame.Rect = shape
        self.parent: Organism

        # Stats
        self.animals_killed: int = 0
        self.plants_killed: int = 0
        self.organisms_attacked: int = 0
        self.total_energy_gained: float = 0
        self.tiles_visited: int = 0
        self.num_offspring: int = 0
        self.tick_age: int = 0
        self.birth_time: int = pygame.time.get_ticks()
        self.death_time: int | None = None

        self.stat_panel: stats.stat_panel.StatPanel | None = None

        self.tile: Tile = None
        self.enter_tile(tile)

    def _set_attributes_from_dna(self):
        if not self.dna:
            raise ValueError("Trying to set attributes from DNA despite DNA being None")

        self.color: pygame.Color = self.dna.color
        self.attack_power: float = self.dna.attack_power_gene.value
        self.moisture_preference: float = self.dna.prefered_moisture_gene.value
        self.height_preference: float = self.dna.prefered_height_gene.value

    ########################## Properties #################################
    @property
    def health(self) -> float:
        return self._health

    @health.setter
    def health(self, value: float):
        if value > self.MAX_HEALTH:
            self._health = self.MAX_HEALTH
        else:
            self._health = value

    @property
    def energy(self) -> float:
        return self._energy

    @energy.setter
    def energy(self, value: float):
        if value < self.MIN_ENERGY:
            self._energy = self.MIN_ENERGY
            self.health += value
        elif value > self.MAX_ENERGY:
            self._energy = self.MAX_ENERGY
            self.health += value - self.MAX_ENERGY
        else:
            self._energy = value

    ########################## Update #################################
    def update(self):
        """
        Updates the organism by performing various actions and behaviors.

        This method is called during each update cycle to update the state of the organism. It performs the following actions in order:

        1. Use Maintenance Energy: Decreases the energy of the organism by the maintenance energy cost.
        2. Handle Aging: Increments the age of the organism by one tick.
        3. Handle Reproduction: Checks if the organism is able to reproduce based on its health and energy levels. If the criteria for reproduction are met and a random chance is satisfied, the organism reproduces.
        4. Handle Drowning: Handles the drowning process of the organism.
        5. Think: Performs any thinking or decision-making processes for the organism.
        6. Handle Attack: Handles the attack process of the organism.
        7. Handle Movement: Handles the movement process of the organism.
        8. Post Update: Performs any post-update actions, such as checking if the organism is still alive and triggering its death if necessary.

        Parameters:
            None

        Returns:
            None
        """
        self.use_maintanance_energy()
        self.handle_aging()
        self.handle_reproduction()
        self.handle_drowning()
        self.think()
        self.handle_attack()
        self.handle_movement()
        self._post_update()

    def use_maintanance_energy(self):
        self.energy -= settings.entities.ORGANISM_BASE_ENERGY_MAINTANCE

    def handle_aging(self):
        """
        Handles the aging process of an organism.

        This method is called during each update cycle to increment the age of the organism by one tick. The 'tick_age' attribute keeps track of the number of ticks the organism has lived.

        Parameters:
            None

        Returns:
            None
        """
        self.tick_age += 1

    def handle_reproduction(self):
        """
        Handles the reproduction process of an organism.

        This method checks if the organism is able to reproduce based on its health and energy levels. If the organism meets the criteria for reproduction and a random chance is satisfied, the organism will reproduce by calling the 'reproduce' method.

        Parameters:
            None

        Returns:
            None
        """
        if self.can_reproduce() and random.random() <= self.REPRODUCTION_CHANCE:
            self.reproduce()

    def handle_drowning(self):
        pass

    def think(self):
        pass

    def handle_attack(self):
        pass

    def handle_movement(self):
        pass

    def _post_update(self):
        """
        Performs any post-update actions for the organism.

        This method is called at the end of each update cycle to perform any necessary post-update actions for the organism. It checks if the organism is still alive by calling the 'is_alive' method. If the organism is not alive, it triggers the 'die' method to handle the organism's death.

        Parameters:
            None

        Returns:
            None
        """
        if not self.is_alive():
            self.die()

    ########################## Drawing #################################

    @abstractmethod
    def draw(self):
        if not self.is_alive():
            raise ValueError(
                "Organism is being drawn despite being dead. ", self.health
            )

    ########################## Tile #################################
    @abstractmethod
    def enter_tile(self, tile: Tile):
        self.shape.topleft = tile.rect.topleft
        self.tiles_visited += 1

    @abstractmethod
    def check_tile_assignment(self):
        pass

    ########################## Energy and Health #################################
    def health_ratio(self) -> float:
        ratio = self.health / self.MAX_HEALTH

        if ratio > 1:
            raise ValueError(f"Health ratio {ratio} is bigger than 1")
        return ratio

    def energy_ratio(self) -> float:
        ratio = self.energy / self.MAX_ENERGY

        if ratio > 1:
            raise ValueError(f"Energy ratio {ratio} is bigger than 1")
        return ratio

    def is_alive(self) -> bool:
        return self.health > 0

    @abstractmethod
    def die(self):
        if self.is_alive():
            raise ValueError("Organism tries to die despite not being dead.")
        Organism.organisms_died += 1
        self.death_time = pygame.time.get_ticks()

    def attack(self, organism_to_attack: Organism):
        if not (
            self.tile.is_neighbor(organism_to_attack.tile)
            or self.tile == organism_to_attack.tile
        ):
            raise ValueError(
                "Organism to attack is not on a neighbor tile or same tile."
            )
        self.organisms_attacked += 1
        organism_to_attack.get_attacked(self)

    @abstractmethod
    def get_attacked(self, attacking_organism: Organism):
        if not (
            self.tile.is_neighbor(attacking_organism.tile)
            or self.tile == attacking_organism.tile
        ):
            raise ValueError(
                "Organism attacking is not on a neighbor tile or same tile."
            )

        damage = attacking_organism.attack_power

        if damage > 0:
            self.health -= damage
            attacking_organism.energy += damage * self.NUTRITION_FACTOR

    ########################## Reproduction #################################
    @abstractmethod
    def reproduce(self):
        pass

    def can_reproduce(self) -> bool:
        return (
            self.health_ratio() >= self.MIN_REPRODUCTION_HEALTH
            and self.energy_ratio() >= self.MIN_REPRODUCTION_ENERGY
        )

    @abstractmethod
    def copy(self, tile: Tile) -> Organism:
        self.num_offspring += 1
        Organism.organisms_birthed += 1
        pass

    def mutate(self):
        self.dna.mutate()
        self._set_attributes_from_dna()

    ########################## Stats #################################
    def show_stats(self):
        stats_data = self.get_stats()

        if not self.stat_panel:
            self.stat_panel = stats.stat_panel.StatPanel(self.get_headers(), stats_data)

        self.stat_panel.update(self.shape, stats_data)
        self.stat_panel.draw()

    def get_stats(self) -> list:
        return [
            self.__class__.__name__,
            self.id,
            self.birth_time,
            self.death_time,
            (
                self.death_time - self.birth_time
                if self.death_time
                else pygame.time.get_ticks() - self.birth_time
            ),
            self.tick_age,
            round(self.health, 2),
            round(self.MAX_HEALTH, 2),
            round(self.health_ratio(), 2),
            round(self.energy, 2),
            round(self.MAX_ENERGY, 2),
            round(self.energy_ratio(), 2),
            round(self.total_energy_gained, 2),
            self.tiles_visited,
            round(self.attack_power, 2),
            self.organisms_attacked,
            self.animals_killed,
            self.plants_killed,
            self.parent.id if self.parent else None,
            self.num_offspring,
            self.color.r,
            self.color.g,
            self.color.b,
            self.moisture_preference,
            self.height_preference,
        ]

    def get_headers(self) -> list[str]:
        return [
            "Type",
            "ID",
            "Birth time (milsec)",
            "Death time (milsec)",
            "Time lived (milsec)",
            "Updates / Frames lived",
            "Health",
            "Max health",
            "Health ratio",
            "Energy",
            "Max energy",
            "Energy ratio",
            "Total Energy gained",
            "Tiles traveled",
            "Attack power",
            "Organisms attacked",
            "Animals killed",
            "Plants killed",
            "Parent Id",
            "Number of Offsprings",
            "Color red value",
            "Color green value",
            "Color blue value",
            "Moisture preference",
            "Height preference",
        ]

    def save_to_csv(self):
        file_exists = os.path.isfile(settings.database.database_csv_filename)

        try:
            with open(
                settings.database.database_csv_filename, mode="a", newline=""
            ) as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(self.get_headers())
                writer.writerow(self.get_stats())
        except IOError as e:
            print(f"Error writing to CSV: {e}")
