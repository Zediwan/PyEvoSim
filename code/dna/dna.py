from __future__ import annotations

import math

import pygame

import settings.dna
from dna.gene import Gene


class DNA:
    def __init__(
        self,
        color: pygame.Color,
        attack_power: float,
        prefered_moisture: float,
        prefered_height: float,
    ) -> None:
        self.color_r_gene: Gene = Gene(
            settings.dna.color_max,
            settings.dna.color_min,
            value=color.r,
            mutation_range=settings.dna.color_mutation_range,
        )
        self.color_g_gene: Gene = Gene(
            settings.dna.color_max,
            settings.dna.color_min,
            value=color.g,
            mutation_range=settings.dna.color_mutation_range,
        )
        self.color_b_gene: Gene = Gene(
            settings.dna.color_max,
            settings.dna.color_min,
            value=color.b,
            mutation_range=settings.dna.color_mutation_range,
        )
        self.attack_power_gene: Gene = Gene(
            settings.dna.attack_power_max,
            settings.dna.attack_power_min,
            value=attack_power,
            mutation_range=settings.dna.attack_power_mutation_range,
        )
        self.prefered_moisture_gene: Gene = Gene(
            settings.dna.prefered_moisture_max,
            settings.dna.prefered_moisture_min,
            prefered_moisture,
            settings.dna.prefered_moisture_muation_range,
        )
        self.prefered_height_gene: Gene = Gene(
            settings.dna.prefered_height_max,
            settings.dna.prefered_height_min,
            prefered_height,
            settings.dna.prefered_height_muation_range,
        )

    @property
    def color(self):
        return pygame.Color(
            math.floor(self.color_r_gene.value),
            math.floor(self.color_g_gene.value),
            math.floor(self.color_b_gene.value),
        )

    def copy(self) -> DNA:
        return DNA(
            self.color,
            self.attack_power_gene.value,
            self.prefered_moisture_gene.value,
            self.prefered_height_gene.value,
        )

    def mutate(self) -> None:
        for gene in [
            self.color_r_gene,
            self.color_g_gene,
            self.color_b_gene,
            self.attack_power_gene,
            self.prefered_moisture_gene,
            self.prefered_height_gene,
        ]:
            gene.mutate()
