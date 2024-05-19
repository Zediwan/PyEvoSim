from __future__ import annotations

import pygame

import random
from dna.gene import Gene


class DNA:
    attack_power_min: float = 0
    attack_power_max: float = 50
    attack_power_mutation_range: float = 2

    color_min: float = 1
    color_max: float = 255
    color_mutation_range: float = 10

    prefered_moisture_min: float = 0
    prefered_moisture_max: float = 1
    prefered_moisture_muation_range: float = 0.2

    prefered_height_min: float = 0
    prefered_height_max: float = 1
    prefered_height_muation_range: float = 0.2

    min_reproduction_health_min: float = 0
    min_reproduction_health_max: float = 1
    min_reproduction_health_mutation_range: float = 0.01

    min_reproduction_energy_min: float = 0
    min_reproduction_energy_max: float = 1
    min_reproduction_energy_mutation_range: float = 0.01

    #region class methods
    @classmethod
    def set_attack_power_mutation_range(cls, value):
        cls.attack_power_mutation_range = value

    @classmethod
    def set_color_mutation_range(cls, value):
        cls.color_mutation_range = value

    @classmethod
    def set_prefered_moisture_mutation_range(cls, value):
        cls.prefered_moisture_muation_range = value

    @classmethod
    def set_prefered_height_mutation_range(cls, value):
        cls.prefered_height_muation_range = value

    @classmethod
    def set_min_reproduction_health_mutation_range(cls, value):
        cls.min_reproduction_health_mutation_range = value

    @classmethod
    def set_min_reproduction_energy_mutation_range(cls, value):
        cls.min_reproduction_energy_mutation_range = value
    #endregion

    def __init__(
        self,
        color: pygame.Color,
        attack_power: float,
        prefered_moisture: float,
        prefered_height: float,
        muation_chance: float,
        min_reproduction_health: float,
        min_reproduction_energy: float
    ) -> None:
        self.color_r_gene: Gene = Gene(
            DNA.color_max,
            DNA.color_min,
            color.r,
            DNA.color_mutation_range,
        )
        self.color_g_gene: Gene = Gene(
            DNA.color_max,
            DNA.color_min,
            color.g,
            DNA.color_mutation_range,
        )
        self.color_b_gene: Gene = Gene(
            DNA.color_max,
            DNA.color_min,
            color.b,
            DNA.color_mutation_range,
        )
        self.attack_power_gene: Gene = Gene(
            DNA.attack_power_max,
            DNA.attack_power_min,
            attack_power,
            DNA.attack_power_mutation_range,
        )
        self.prefered_moisture_gene: Gene = Gene(
            DNA.prefered_moisture_max,
            DNA.prefered_moisture_min,
            prefered_moisture,
            DNA.prefered_moisture_muation_range,
        )
        self.prefered_height_gene: Gene = Gene(
            DNA.prefered_height_max,
            DNA.prefered_height_min,
            prefered_height,
            DNA.prefered_height_muation_range,
        )
        self.mutation_chance_gene: Gene = Gene(
            1, 0, muation_chance, .1
        )
        self.min_reproduction_health_gene: Gene = Gene(
            DNA.min_reproduction_health_max,
            DNA.min_reproduction_health_min,
            min_reproduction_health,
            DNA.min_reproduction_health_mutation_range
        )
        self.min_reproduction_energy_gene: Gene = Gene(
            DNA.min_reproduction_energy_max,
            DNA.min_reproduction_energy_min,
            min_reproduction_energy,
            DNA.min_reproduction_energy_mutation_range
        )

    @property
    def color(self):
        return pygame.Color(
            int(self.color_r_gene.value),
            int(self.color_g_gene.value),
            int(self.color_b_gene.value),
        )

    def copy(self) -> DNA:
        return DNA(
            self.color,
            self.attack_power_gene.value,
            self.prefered_moisture_gene.value,
            self.prefered_height_gene.value,
            self.mutation_chance_gene.value,
            self.min_reproduction_health_gene.value,
            self.min_reproduction_energy_gene.value
        )

    def mutate(self) -> None:
        for gene in [
            self.color_r_gene,
            self.color_g_gene,
            self.color_b_gene,
            self.attack_power_gene,
            self.prefered_moisture_gene,
            self.prefered_height_gene,
            self.mutation_chance_gene
        ]:
            if self.mutation_chance_gene.value <= random.random():
                gene.mutate()
