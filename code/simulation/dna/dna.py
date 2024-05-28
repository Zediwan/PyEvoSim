from __future__ import annotations

import pygame

import random
from .gene import Gene, ColorComponentGene, PercentageGene


class DNA:
    """
    Represents a DNA configuration for an organism with various genetic traits.

    Attributes:
        attack_power_min (float): The minimum value for attack power gene.
        attack_power_max (float): The maximum value for attack power gene.
        attack_power_mutation_range (float): The mutation range for attack power gene.

        color_mutation_range (float): The mutation range for color gene.

        prefered_moisture_min (float): The minimum value for preferred moisture gene.
        prefered_moisture_max (float): The maximum value for preferred moisture gene.
        prefered_moisture_mutation_range (float): The mutation range for preferred moisture gene.

        prefered_height_min (float): The minimum value for preferred height gene.
        prefered_height_max (float): The maximum value for preferred height gene.
        prefered_height_mutation_range (float): The mutation range for preferred height gene.

        min_reproduction_health_min (float): The minimum value for minimum reproduction health gene.
        min_reproduction_health_max (float): The maximum value for minimum reproduction health gene.
        min_reproduction_health_mutation_range (float): The mutation range for minimum reproduction health gene.

        min_reproduction_energy_min (float): The minimum value for minimum reproduction energy gene.
        min_reproduction_energy_max (float): The maximum value for minimum reproduction energy gene.
        min_reproduction_energy_mutation_range (float): The mutation range for minimum reproduction energy gene.

        reproduction_chance_min (float): The minimum value for reproduction chance gene.
        reproduction_chance_max (float): The maximum value for reproduction chance gene.
        reproduction_chance_mutation_range (float): The mutation range for reproduction chance gene.

        mutation_chance_min (float): The minimum value for mutation chance gene.
        mutation_chance_max (float): The maximum value for mutation chance gene.
        mutation_chance_mutation_range (float): The mutation range for mutation chance gene.

        energy_to_offspring_min (float): The minimum value for energy to offspring gene.
        energy_to_offspring_max (float): The maximum value for energy to offspring gene.
        energy_to_offspring_mutation_range (float): The mutation range for energy to offspring gene.

    Methods:
        set_attack_power_mutation_range(value): Set the mutation range for attack power gene.
        set_color_mutation_range(value): Set the mutation range for color gene.
        set_prefered_moisture_mutation_range(value): Set the mutation range for preferred moisture gene.
        set_prefered_height_mutation_range(value): Set the mutation range for preferred height gene.
        set_min_reproduction_health_mutation_range(value): Set the mutation range for minimum reproduction health gene.
        set_min_reproduction_energy_mutation_range(value): Set the mutation range for minimum reproduction energy gene.
        set_reproduction_chance_mutation_range(value): Set the mutation range for reproduction chance gene.
        set_mutation_chance_mutation_range(value): Set the mutation range for mutation chance gene.
        set_energy_to_offspring_mutation_range(value): Set the mutation range for energy to offspring gene.

        __init__(color: pygame.Color, attack_power: float, prefered_moisture: float, prefered_height: float, mutation_chance: float, min_reproduction_health: float, min_reproduction_energy: float, reproduction_chance: float, energy_to_offspring_ratio: float): Initializes a new DNA instance with the provided parameters.

        color(): Return the color represented by the RGB values stored in the genes of the DNA instance.

        copy(): Return a new DNA instance that is a copy of the current DNA instance.

        mutate(): Mutates each gene in the DNA instance based on the mutation chance.

    Returns:
        None
    """
    #region Gene settings
    attack_power_min: float = 0
    attack_power_max: float = 50
    attack_power_mutation_range: float = 2

    color_mutation_range: float = 12

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

    energy_to_offspring_min: float = 0
    energy_to_offspring_max: float = 1
    energy_to_offspring_mutation_range: float = 0.01
    #endregion
    #region class methods
    @classmethod
    def set_attack_power_mutation_range(cls, value):
        """
        Set the mutation range for attack power.

        Parameters:
            value: The new value for the mutation range for attack power.

        Returns:
            None
        """
        cls.attack_power_mutation_range = value

    @classmethod
    def set_color_mutation_range(cls, value):
        """
        Set the mutation range for color.

        Parameters:
            value: The new value for the mutation range for color.

        Returns:
            None
        """
        cls.color_mutation_range = value

    @classmethod
    def set_prefered_moisture_mutation_range(cls, value):
        """
        Set the mutation range for preferred moisture level.

        Parameters:
            value: The new value for the mutation range for preferred moisture level.

        Returns:
            None
        """
        cls.prefered_moisture_muation_range = value

    @classmethod
    def set_prefered_height_mutation_range(cls, value):
        """
        Set the mutation range for preferred height.

        Parameters:
            value: The new value for the mutation range for preferred height.

        Returns:
            None
        """
        cls.prefered_height_muation_range = value

    @classmethod
    def set_min_reproduction_health_mutation_range(cls, value):
        """
        Set the mutation range for minimum reproduction health.

        Parameters:
            value: The new value for the mutation range for minimum reproduction health.

        Returns:
            None
        """
        cls.min_reproduction_health_mutation_range = value

    @classmethod
    def set_min_reproduction_energy_mutation_range(cls, value):
        """
        Set the mutation range for minimum reproduction energy.

        Parameters:
            value: The new value for the mutation range for minimum reproduction energy.

        Returns:
            None
        """
        cls.min_reproduction_energy_mutation_range = value

    @classmethod
    def set_reproduction_chance_mutation_range(cls, value):
        """
        Set the mutation range for reproduction chance.

        Parameters:
            value: The new value for the mutation range for reproduction chance.

        Returns:
            None
        """
        cls.reproduction_chance_mutation_range = value
    
    @classmethod
    def set_mutation_chance_mutation_range(cls, value):
        """
        Set the mutation range for mutation chance.

        Parameters:
            value: The new value for the mutation range for mutation chance.

        Returns:
            None
        """
        cls.mutation_chance_mutation_range = value

    @classmethod
    def set_energy_to_offspring_mutation_range(cls, value):
        """
        Set the mutation range for energy to offspring.

        Parameters:
            value: The new value for the mutation range for energy to offspring.

        Returns:
            None
        """
        cls.energy_to_offspring_mutation_range = value
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
        reproduction_chance: float,
        energy_to_offspring_ratio: float
    ) -> None:
        """
        Initialize a new DNA instance with the provided genetic traits.

        Parameters:
            color (pygame.Color): The color of the organism.
            attack_power (float): The attack power of the organism.
            prefered_moisture (float): The preferred moisture level of the organism.
            prefered_height (float): The preferred height of the organism.
            mutation_chance (float): The chance of mutation for the organism.
            min_reproduction_health (float): The minimum reproduction health of the organism.
            min_reproduction_energy (float): The minimum reproduction energy of the organism.
            reproduction_chance (float): The chance of reproduction for the organism.
            energy_to_offspring_ratio (float): The energy passed to offspring by the organism.

        Returns:
            None
        """
        self.genes: list[Gene] = []

        self.color_r_gene: ColorComponentGene = ColorComponentGene(
            value=color.r, 
            mutation_range=DNA.color_mutation_range
            )
        self.genes.append(self.color_r_gene)
        self.color_g_gene: ColorComponentGene = ColorComponentGene(
            value=color.g,
            mutation_range=DNA.color_mutation_range,
        )
        self.genes.append(self.color_g_gene)
        self.color_b_gene: ColorComponentGene = ColorComponentGene(
            value=color.b,
            mutation_range=DNA.color_mutation_range,
        )
        self.genes.append(self.color_b_gene)
        self.attack_power_gene: Gene = Gene(
            max_value=DNA.attack_power_max,
            min_value=DNA.attack_power_min,
            value=attack_power,
            mutation_range=DNA.attack_power_mutation_range,
        )
        self.genes.append(self.attack_power_gene)
        self.prefered_moisture_gene: PercentageGene = PercentageGene(
            max_value=DNA.prefered_moisture_max,
            min_value=DNA.prefered_moisture_min,
            value=prefered_moisture,
            mutation_range=DNA.prefered_moisture_muation_range,
        )
        self.genes.append(self.prefered_moisture_gene)
        self.prefered_height_gene: PercentageGene = PercentageGene(
            max_value=DNA.prefered_height_max,
            min_value=DNA.prefered_height_min,
            value=prefered_height,
            mutation_range=DNA.prefered_height_muation_range,
        )
        self.genes.append(self.prefered_height_gene)
        self.mutation_chance_gene: PercentageGene = PercentageGene(
            max_value=DNA.mutation_chance_max,
            min_value=DNA.mutation_chance_min,
            value=muation_chance,
            mutation_range=DNA.mutation_chance_mutation_range
        )
        self.genes.append(self.mutation_chance_gene)
        self.min_reproduction_health_gene: PercentageGene = PercentageGene(
            max_value=DNA.min_reproduction_health_max,
            min_value=DNA.min_reproduction_health_min,
            value=min_reproduction_health,
            mutation_range=DNA.min_reproduction_health_mutation_range
        )
        self.genes.append(self.min_reproduction_health_gene)
        self.min_reproduction_energy_gene: PercentageGene = PercentageGene(
            max_value=DNA.min_reproduction_energy_max,
            min_value=DNA.min_reproduction_energy_min,
            value=min_reproduction_energy,
            mutation_range=DNA.min_reproduction_energy_mutation_range
        )
        self.genes.append(self.min_reproduction_energy_gene)
        self.reproduction_chance_gene: PercentageGene = PercentageGene(
            max_value=DNA.reproduction_chance_max,
            min_value=DNA.reproduction_chance_min,
            value=reproduction_chance,
            mutation_range=DNA.reproduction_chance_mutation_range
        )
        self.genes.append(self.reproduction_chance_gene)
        self.energy_to_offspring_ratio_gene: PercentageGene = PercentageGene(
            max_value=DNA.energy_to_offspring_max,
            min_value=DNA.energy_to_offspring_min,
            value=energy_to_offspring_ratio,
            mutation_range=DNA.energy_to_offspring_mutation_range
        )
        self.genes.append(self.energy_to_offspring_ratio_gene)

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
            self.reproduction_chance_gene.value,
            self.energy_to_offspring_ratio_gene.value
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
