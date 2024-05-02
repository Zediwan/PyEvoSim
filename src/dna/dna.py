from __future__ import annotations

import math
import random

import pygame

import settings.dna_settings
from dna.gene import Gene


class DNA:
    def __init__(self, color: pygame.Color, attack_power: float = None) -> None:
        self.color_r_gene: Gene = Gene(
            settings.dna_settings.color_max,
            settings.dna_settings.color_min,
            value=color.r,
            mutation_range=settings.dna_settings.color_mutation_range,
        )
        self.color_g_gene: Gene = Gene(
            settings.dna_settings.color_max,
            settings.dna_settings.color_min,
            value=color.g,
            mutation_range=settings.dna_settings.color_mutation_range,
        )
        self.color_b_gene: Gene = Gene(
            settings.dna_settings.color_max,
            settings.dna_settings.color_min,
            value=color.b,
            mutation_range=settings.dna_settings.color_mutation_range,
        )

        if not attack_power:
            ap = pygame.math.lerp(
                settings.dna_settings.attack_power_starting_range[0],
                settings.dna_settings.attack_power_starting_range[1],
                random.random(),
            )
            self.attack_power_gene: Gene = Gene(
                settings.dna_settings.attack_power_max,
                settings.dna_settings.attack_power_min,
                value=ap,
                mutation_range=settings.dna_settings.attack_power_mutation_range,
            )
        else:
            self.attack_power_gene: Gene = Gene(
                settings.dna_settings.attack_power_max,
                settings.dna_settings.attack_power_min,
                value=attack_power,
                mutation_range=settings.dna_settings.attack_power_mutation_range,
            )

    @property
    def color(self):
        return pygame.Color(
            math.floor(self.color_r_gene.value),
            math.floor(self.color_g_gene.value),
            math.floor(self.color_b_gene.value),
        )

    def copy(self) -> DNA:
        return DNA(self.color, self.attack_power_gene.value)

    def mutate(self) -> None:
        for gene in [
            self.color_r_gene,
            self.color_g_gene,
            self.color_b_gene,
            self.attack_power_gene,
        ]:
            gene.mutate()
