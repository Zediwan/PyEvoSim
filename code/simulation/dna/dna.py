from __future__ import annotations

import pygame

import random
from .gene import Gene


class DNA:
    """
    Class representing a DNA instance with genes for color, attack power, preferred moisture level, preferred height, mutation chance, minimum reproduction health, minimum reproduction energy, and reproduction chance.

    Attributes:
        attack_power_min (float): The minimum attack power value.
        attack_power_max (float): The maximum attack power value.
        attack_power_mutation_range (float): The mutation range for attack power.
        color_min (float): The minimum color value.
        color_max (float): The maximum color value.
        color_mutation_range (float): The mutation range for color.
        prefered_moisture_min (float): The minimum preferred moisture level.
        prefered_moisture_max (float): The maximum preferred moisture level.
        prefered_moisture_mutation_range (float): The mutation range for preferred moisture level.
        prefered_height_min (float): The minimum preferred height.
        prefered_height_max (float): The maximum preferred height.
        prefered_height_mutation_range (float): The mutation range for preferred height.
        min_reproduction_health_min (float): The minimum reproduction health value.
        min_reproduction_health_max (float): The maximum reproduction health value.
        min_reproduction_health_mutation_range (float): The mutation range for minimum reproduction health.
        min_reproduction_energy_min (float): The minimum reproduction energy value.
        min_reproduction_energy_max (float): The maximum reproduction energy value.
        min_reproduction_energy_mutation_range (float): The mutation range for minimum reproduction energy.
        reproduction_chance_min (float): The minimum reproduction chance value.
        reproduction_chance_max (float): The maximum reproduction chance value.
        reproduction_chance_mutation_range (float): The mutation range for reproduction chance.
        mutation_chance_min (float): The minimum mutation chance value.
        mutation_chance_max (float): The maximum mutation chance value.
        mutation_chance_mutation_range (float): The mutation range for mutation chance.

    Methods:
        set_attack_power_mutation_range(cls, value): Set the mutation range for attack power.
        set_color_mutation_range(cls, value): Set the mutation range for color.
        set_prefered_moisture_mutation_range(cls, value): Set the mutation range for preferred moisture level.
        set_prefered_height_mutation_range(cls, value): Set the mutation range for preferred height.
        set_min_reproduction_health_mutation_range(cls, value): Set the mutation range for minimum reproduction health.
        set_min_reproduction_energy_mutation_range(cls, value): Set the mutation range for minimum reproduction energy.
        set_reproduction_chance_mutation_range(cls, value): Set the mutation range for reproduction chance.
        set_mutation_chance_mutation_range(cls, value): Set the mutation range for mutation chance.
        __init__(color, attack_power, prefered_moisture, prefered_height, muation_chance, min_reproduction_health, min_reproduction_energy, reproduction_chance): Initialize a new DNA instance with the given parameters.
        color: Return the color represented by the RGB values stored in the genes of the DNA instance.
        copy: Return a new DNA instance that is a copy of the current DNA instance.
        mutate: Mutate each gene in the DNA instance based on the mutation chance.
    """
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
        """
        Initialize a new DNA instance with the given parameters.

        Parameters:
            color (pygame.Color): The color of the DNA.
            attack_power (float): The attack power of the DNA.
            prefered_moisture (float): The preferred moisture level of the DNA.
            prefered_height (float): The preferred height of the DNA.
            muation_chance (float): The mutation chance of the DNA.
            min_reproduction_health (float): The minimum reproduction health of the DNA.
            min_reproduction_energy (float): The minimum reproduction energy of the DNA.
            reproduction_chance (float): The reproduction chance of the DNA.

        Returns:
            None
        """
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
    def color(self) -> pygame.Color:
        """
        Return the color represented by the RGB values stored in the genes of the DNA instance.

        Returns:
            pygame.Color: The color represented by the RGB values stored in the genes.
        """
        return pygame.Color(
            int(self.color_r_gene.value),
            int(self.color_g_gene.value),
            int(self.color_b_gene.value),
        )

    def copy(self) -> DNA:
        """
        Return a new DNA instance that is a copy of the current DNA instance.

        Returns:
            DNA: A new DNA instance that is an exact copy of the current DNA instance, with the same gene values.
        """
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
        """
        Mutates each gene in the DNA instance based on the mutation chance.

        For each gene in the list of genes:
            - If the mutation chance is greater than a random value between 0 and 1, the gene will mutate.

        Returns:
            None
        """
        for gene in self.genes:
            if self.mutation_chance_gene.value <= random.random():
                gene.mutate()
