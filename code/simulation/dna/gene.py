from __future__ import annotations

import random


class Gene:
    """
    Represents a gene with a value that can mutate within a specified range.

    Attributes:
        _max_value (float): The maximum value that the gene can have.
        _min_value (float): The minimum value that the gene can have.
        value (float): The current value of the gene.
        _mutation_range (float): The range within which the gene's value can mutate.

    Methods:
        __init__(max_value: float, min_value: float, value: float | int, mutation_range: float = 1) -> None:
            Initializes a new Gene instance with the provided parameters.

        copy() -> Gene:
            Creates a copy of the current Gene instance.

        mutate() -> None:
            Mutates the gene's value by adding a random float value within the mutation range to the current value.
    """
    def __init__(
        self,
        max_value: float,
        min_value: float,
        value: float | int,
        mutation_range: float = 1,
    ) -> None:
        """
        Initializes a new Gene instance with the provided parameters.

        Parameters:
            max_value (float): The maximum value that the gene can have.
            min_value (float): The minimum value that the gene can have.
            value (float | int): The initial value of the gene.
            mutation_range (float, optional): The range within which the gene's value can mutate. Defaults to 1.

        Returns:
            None
        """
        self._max_value: float = max_value
        self._min_value: float = min_value
        self.value: float = value
        self._mutation_range: float = mutation_range

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        if value >= self._max_value:
            self._value = self._max_value
        elif value <= self._min_value:
            self._value = self._min_value
        else:
            self._value = value

    def copy(self) -> Gene:
        """
        Creates a copy of the current Gene instance.

        Parameters:
            None

        Returns:
            Gene: A new Gene instance with the same maximum value, minimum value, current value, and mutation range as the original Gene instance.
        """
        return Gene(
            self._max_value,
            self._min_value,
            value=self.value,
            mutation_range=self._mutation_range,
        )

    def mutate(self) -> None:
        """
        Mutates the gene's value by adding a random float value within the mutation range to the current value.

        Parameters:
            None

        Returns:
            None
        """
        self.value += random.uniform(-self._mutation_range, self._mutation_range)


class PercentageGene(Gene):
    """
    Represents a gene that stores a percentage value within the range of 0 to 1.

    Attributes:
        Inherited from Gene class:
            _max_value (float): The maximum value that the gene can have (1 for PercentageGene).
            _min_value (float): The minimum value that the gene can have (0 for PercentageGene).
            value (float): The current value of the gene.
            _mutation_range (float): The range within which the gene's value can mutate.

    Methods:
        Inherited from Gene class:
            __init__(value: float | int, mutation_range: float = .01) -> None:
                Initializes a new PercentageGene instance with the provided parameters.

            copy() -> PercentageGene:
                Creates a copy of the current PercentageGene instance.

            mutate() -> None:
                Mutates the gene's value by adding a random float value within the mutation range to the current value.
    """
    def __init__(self, value: float | int, mutation_range: float = .01) -> None:
        super().__init__(1, 0, value, mutation_range)
