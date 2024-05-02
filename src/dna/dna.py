from __future__ import annotations

from random import random

from pygame import Color
from pygame.math import lerp

from dna.gene import Gene
from dna import dna_settings

class DNA():
    def __init__(self, color: Color | tuple[float, float, float] | tuple[Gene | Gene | Gene], attack_power: float | Gene = None) -> None:
        self._init_color(color)
        self._init_attack_power(attack_power)
        
    @property
    def color(self):
        return Color(round(self.color_r_gene.value), round(self.color_g_gene.value), round(self.color_b_gene.value))

    def _init_color(self, color: Color | tuple[float, float, float] | tuple[Gene | Gene | Gene]) -> None:
        if isinstance(color, Color):
            self._init_color_from_color(color)
        else:
            self._init_color_from_tuple(color)

    def _init_color_from_color(self, color: Color) -> None:
        self.color_r_gene: Gene = self._create_color_gene(color.r)
        self.color_g_gene: Gene = self._create_color_gene(color.g)
        self.color_b_gene: Gene = self._create_color_gene(color.b)

    def _init_color_from_tuple(self, color: tuple[float, float, float] | tuple[Gene, Gene, Gene]) -> None:
        if isinstance(color[0], float):
            self.color_r_gene: Gene = self._create_color_gene(color[0])
            self.color_g_gene: Gene = self._create_color_gene(color[1])
            self.color_b_gene: Gene = self._create_color_gene(color[2])
        else:
            self.color_r_gene: Gene = color[0].copy()
            self.color_g_gene: Gene = color[1].copy()
            self.color_b_gene: Gene = color[2].copy()

    def _init_attack_power(self, attack_power: float | Gene) -> None:
        if not attack_power:
            ap = lerp(dna_settings.attack_power_starting_range[0], dna_settings.attack_power_starting_range[1], random())
            self.attack_power_gene: Gene = Gene(dna_settings.attack_power_max, dna_settings.attack_power_min, value = ap, mutation_range=dna_settings.attack_power_mutation_range)
        elif isinstance(attack_power, Gene):
            self.attack_power_gene: Gene = attack_power.copy()
        else:
            self.attack_power_gene: Gene = Gene(dna_settings.attack_power_max, dna_settings.attack_power_min, attack_power, dna_settings.attack_power_mutation_range)

    def _create_color_gene(self, value: float) -> Gene:
        return Gene(dna_settings.color_max, dna_settings.color_min, value, dna_settings.color_mutation_range)
    
    def copy(self) -> DNA:
        return DNA((self.color_r_gene.copy(), self.color_g_gene.copy(), self.color_b_gene.copy()), self.attack_power_gene.copy())

    def mutate(self) -> None:
        for gene in [self.color_r_gene, self.color_g_gene, self.color_b_gene, self.attack_power_gene]:
            gene.mutate()