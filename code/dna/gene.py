from __future__ import annotations

import random


class Gene:
    def __init__(
        self,
        max_value: float,
        min_value: float,
        value: float | int,
        mutation_range: float = 1,
    ) -> None:
        self._max_value: float = max_value
        self._min_value: float = min_value

        self.value: float = value

        self._mutation_range: float = mutation_range

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
        if value >= self._max_value:
            self._value = self._max_value
        elif value <= self._min_value:
            self._value = self._min_value
        else:
            self._value = value

    def copy(self) -> Gene:
        return Gene(
            self._max_value,
            self._min_value,
            value=self.value,
            mutation_range=self._mutation_range,
        )

    def mutate(self) -> None:
        self.value += (
            self._mutation_range * 2 * random.random()
        ) - self._mutation_range
