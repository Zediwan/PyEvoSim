from __future__ import annotations

import pygame

import random
from .gene import Gene


class DNA:
    #region Gene settings
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

    reproduction_chance_min: float = 0
    reproduction_chance_max: float = 1
    reproduction_chance_mutation_range: float = 0.01

    mutation_chance_min: float = 0
    mutation_chance_max: float = 1
    mutation_chance_mutation_range: float = 0.01
    #endregion
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

    @classmethod
    def set_reproduction_chance_mutation_range(cls, value):
        cls.reproduction_chance_mutation_range = value
    
    @classmethod
    def set_mutation_chance_mutation_range(cls, value):
        cls.mutation_chance_mutation_range = value
    #endregion

    def __init__(
        self,
        color: pygame.Color,
        attack_power: float,
        prefered_moisture: float,
        prefered_height: float,
        muation_chance: float,
        min_reproduction_health: float,
        min_reproduction_energy: float,
        reproduction_chance: float
    ) -> None:
        self.genes: list[Gene] = []

        self.color_r_gene: Gene = Gene(
            DNA.color_max,
            DNA.color_min,
            color.r,
            DNA.color_mutation_range,
        )
        self.genes.append(self.color_r_gene)
        self.color_g_gene: Gene = Gene(
            DNA.color_max,
            DNA.color_min,
            color.g,
            DNA.color_mutation_range,
        )
        self.genes.append(self.color_g_gene)
        self.color_b_gene: Gene = Gene(
            DNA.color_max,
            DNA.color_min,
            color.b,
            DNA.color_mutation_range,
        )
        self.genes.append(self.color_b_gene)
        self.attack_power_gene: Gene = Gene(
            DNA.attack_power_max,
            DNA.attack_power_min,
            attack_power,
            DNA.attack_power_mutation_range,
        )
        self.genes.append(self.attack_power_gene)
        self.prefered_moisture_gene: Gene = Gene(
            DNA.prefered_moisture_max,
            DNA.prefered_moisture_min,
            prefered_moisture,
            DNA.prefered_moisture_muation_range,
        )
        self.genes.append(self.prefered_moisture_gene)
        self.prefered_height_gene: Gene = Gene(
            DNA.prefered_height_max,
            DNA.prefered_height_min,
            prefered_height,
            DNA.prefered_height_muation_range,
        )
        self.genes.append(self.prefered_height_gene)
        self.mutation_chance_gene: Gene = Gene(
            DNA.mutation_chance_max,
            DNA.mutation_chance_min,
            muation_chance,
            DNA.mutation_chance_mutation_range
        )
        self.genes.append(self.mutation_chance_gene)
        self.min_reproduction_health_gene: Gene = Gene(
            DNA.min_reproduction_health_max,
            DNA.min_reproduction_health_min,
            min_reproduction_health,
            DNA.min_reproduction_health_mutation_range
        )
        self.genes.append(self.min_reproduction_health_gene)
        self.min_reproduction_energy_gene: Gene = Gene(
            DNA.min_reproduction_energy_max,
            DNA.min_reproduction_energy_min,
            min_reproduction_energy,
            DNA.min_reproduction_energy_mutation_range
        )
        self.genes.append(self.min_reproduction_energy_gene)
        self.reproduction_chance_gene: Gene = Gene(
            DNA.reproduction_chance_max,
            DNA.reproduction_chance_min,
            reproduction_chance,
            DNA.reproduction_chance_mutation_range
        )
        self.genes.append(self.reproduction_chance_gene)

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
            self.min_reproduction_energy_gene.value,
            self.reproduction_chance_gene.value
        )

    def mutate(self) -> None:
        for gene in self.genes:
            if self.mutation_chance_gene.value <= random.random():
                gene.mutate()
