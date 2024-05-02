from __future__ import annotations

from random import random

from pygame import Color
from pygame.math import lerp
from math import floor

from dna.gene import Gene
from settings import dna_settings

class DNA():
    def __init__(self, color: Color, attack_power: float = None) -> None:
        self.color_r_gene: Gene = Gene(dna_settings.color_max, dna_settings.color_min, value=color.r, mutation_range=dna_settings.color_mutation_range)
        self.color_g_gene: Gene = Gene(dna_settings.color_max, dna_settings.color_min, value=color.g, mutation_range=dna_settings.color_mutation_range)
        self.color_b_gene: Gene = Gene(dna_settings.color_max, dna_settings.color_min, value=color.b, mutation_range=dna_settings.color_mutation_range)
        
        if not attack_power:
            ap = lerp(dna_settings.attack_power_starting_range[0], dna_settings.attack_power_starting_range[1], random())
            self.attack_power_gene: Gene = Gene(dna_settings.attack_power_max, dna_settings.attack_power_min, value=ap, mutation_range=dna_settings.attack_power_mutation_range)
        else:
            self.attack_power_gene: Gene = Gene(dna_settings.attack_power_max, dna_settings.attack_power_min, value=attack_power, mutation_range=dna_settings.attack_power_mutation_range)

        
    @property
    def color(self):
        return Color(floor(self.color_r_gene.value), floor(self.color_g_gene.value), floor(self.color_b_gene.value))
    
    def copy(self) -> DNA:
        return DNA(self.color, self.attack_power_gene.value)

    def mutate(self) -> None:
        for gene in [self.color_r_gene, self.color_g_gene, self.color_b_gene, self.attack_power_gene]:
            gene.mutate()