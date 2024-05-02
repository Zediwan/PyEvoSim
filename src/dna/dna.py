from __future__ import annotations

from pygame import Color

from gene import Gene
import dna_settings

class DNA():
    def __init__(self, color: Color | tuple[float, float, float] | tuple[Gene | Gene | Gene], attack_power: float | Gene) -> None:
        self._init_color(color)
        self._init_attack_power(attack_power)

    def _init_color(self, color: Color | tuple[float, float, float] | tuple[Gene | Gene | Gene]) -> None:
        if isinstance(color, Color):
            self._init_color_from_color(color)
        else:
            self._init_color_from_tuple(color)

    def _init_color_from_color(self, color: Color) -> None:
        self.color_r: Gene = self._create_gene(color.r)
        self.color_g: Gene = self._create_gene(color.g)
        self.color_b: Gene = self._create_gene(color.b)

    def _init_color_from_tuple(self, color: tuple[float, float, float] | tuple[Gene, Gene, Gene]) -> None:
        if isinstance(color[0], float):
            self.color_r: Gene = self._create_gene(color[0])
            self.color_g: Gene = self._create_gene(color[1])
            self.color_b: Gene = self._create_gene(color[2])
        else:
            self.color_r: Gene = color[0].copy()
            self.color_g: Gene = color[1].copy()
            self.color_b: Gene = color[2].copy()

    def _init_attack_power(self, attack_power: float | Gene) -> None:
        if isinstance(attack_power, Gene):
            self.attack_power: Gene = attack_power.copy()
        else:
            self.attack_power: Gene = self._create_gene(attack_power)

    def _create_gene(self, value: float) -> Gene:
        return Gene(value, dna_settings.color_max, dna_settings.color_min, dna_settings.color_mutation_range)
    
    def copy(self) -> DNA:
        return DNA((self.color_r.copy(), self.color_g.copy(), self.color_b.copy()), self.attack_power.copy())

    def mutate(self) -> None:
        for gene in [self.color_r, self.color_g, self.color_b, self.attack_power]:
            gene.mutate()