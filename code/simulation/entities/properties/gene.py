from __future__ import annotations

import random
import pygame_menu

class Gene:
    """
    Represents a generic gene with a value that can mutate within a specified range.

    Attributes:
        MUTATION_TYPE (str): The type of mutation applied to the gene, either "gauss" for Gaussian distribution mutation or "uniform" for uniform distribution mutation.

    Methods:
        set_mutation_type(type: str) -> None:
            Set the mutation type for the Gene class.

        __init__(max_value: float, min_value: float, value: float | int, mutation_range: float) -> None:
            Initialize a new Gene instance with the provided parameters.

        value() -> float:
            Get the current value of the gene.

        value(value: float) -> None:
            Set the current value of the gene.

        copy() -> Gene:
            Create a copy of the current Gene instance.

        mutate() -> None:
            Mutate the gene's value based on the specified mutation type.

    Raises:
        ValueError: If max_value is less than min_value, if mutation_range is negative, or if the mutation type is not recognized.

    Returns:
        None
    """
    MUTATION_TYPE: str = "gauss"
    
    @classmethod
    def set_mutation_type(cls, selected_item: str, type: str) -> None:
        """
        Set the mutation type for the Gene class.

        Parameters:
            - selected_item (str): The selected item for setting the mutation type. This parameter is not used within the method but is required for the match statement.
            - type (str): The type of mutation to be set for the Gene class. Should be either "gauss" for Gaussian distribution mutation or "uniform" for uniform distribution mutation.

        Raises:
            - ValueError: If the provided mutation type is not recognized (neither "gauss" nor "uniform").

        Returns:
            - None
        """
        match type:
            case "gauss":
                cls.MUTATION_TYPE = type
            case "uniform":
                cls.MUTATION_TYPE = type
            case _:
                raise ValueError(f"{type} is invalid!")
    
    def __init__(self, max_value: float, min_value: float, value: float | int, mutation_range: float) -> None:
        """
        Initialize a new Gene instance with the provided parameters.

        Parameters:
        - max_value (float): The maximum value that the gene can have.
        - min_value (float): The minimum value that the gene can have.
        - value (float | int): The current value of the gene.
        - mutation_range (float): The range within which the gene's value can mutate.

        Raises:
        - ValueError: If max_value is less than min_value or if mutation_range is negative.

        Returns:
        - None
        """
        if max_value < min_value:
            raise ValueError(f"Max Value {max_value} needs to be bigger or equal than min value {min_value}.")
        if mutation_range < 0:
            raise ValueError(f"Mutation Range {mutation_range} cannot be negative!")

        self._max_value: float = max_value
        self._min_value: float = min_value
        self.value = value
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
        Mutates the gene's value based on the specified mutation type.

        If the mutation type is "gauss", a random float value within one-third of the mutation range is added to the current value using a Gaussian distribution.
        If the mutation type is "uniform", a random float value within the mutation range is added to the current value uniformly.
        Raises a ValueError if the mutation type is not recognized.

        Parameters:
            None

        Returns:
            None
        """
        mutation = None
        match self.MUTATION_TYPE:
            case "gauss":
                mutation = random.gauss(0, self._mutation_range/3) # TODO figure if it makes sense so that most values are in the mutation range
            case "uniform":
                mutation = random.uniform(-self._mutation_range, self._mutation_range)
            case _:
                raise ValueError(f"{self.MUTATION_TYPE} is invalid!")

        self.value += mutation

    def subscribe_controller(self, menu: pygame_menu.Menu, name: str) -> None:
        #TODO implement class to add a gene controller
        pass

class PercentageGene(Gene):
    """
    Represents a gene that stores a percentage value within the range of 0 to 1 and can mutate within a specified range.

    Attributes:
        MAX (float): The maximum value allowed for the gene (1).
        MIN (float): The minimum value allowed for the gene (0).
        BASE_MUTATION_RANGE (float): The default range within which the gene can mutate (0.01).

    Methods:
        __init__(value: float | int, max_value: float = MAX, min_value: float = MIN, mutation_range: float = BASE_MUTATION_RANGE) -> None:
            Initializes a new PercentageGene instance with the provided parameters.

        Raises:
            ValueError: If max_value exceeds the class constant MAX or if min_value is smaller than the class constant MIN.

        Returns:
            None
    """
    MAX = 1
    MIN = 0
    BASE_MUTATION_RANGE = 0.01
    def __init__(self, value: float | int, max_value: float = MAX, min_value: float = MIN, mutation_range: float = BASE_MUTATION_RANGE) -> None:
        """
        Initialize a PercentageGene object.

        Parameters:
        - value (float | int): The initial value for the gene.
        - max_value (float): The maximum value allowed for the gene (default is 1).
        - min_value (float): The minimum value allowed for the gene (default is 0).
        - mutation_range (float): The range within which the gene can mutate (default is 0.01).

        Raises:
        - ValueError: If max_value exceeds the class constant MAX or if min_value is smaller than the class constant MIN.

        Returns:
        - None
        """
        if max_value > PercentageGene.MAX:
            raise ValueError(f"Percentage gene max {max_value} cannot exceed {PercentageGene.MAX}.")
        if min_value < PercentageGene.MIN:
            raise ValueError(f"Percentage gene min {min_value} cannot be smaller than {PercentageGene.MIN}.")
        super().__init__(max_value=max_value, min_value=min_value, value=value, mutation_range=mutation_range)
        
class ColorComponentGene(Gene):
    """
    Represents a gene for color component values with a value that can mutate within a specified range.

    Attributes:
        MAX (int): The maximum value that the color component gene can have (default is 255).
        MIN (int): The minimum value that the color component gene can have (default is 1).
        BASE_MUTATION_RANGE (int): The base range within which the color component gene's value can mutate (default is 1).

    Methods:
        __init__(value: float | int, max_value: float = MAX, min_value: float = MIN, mutation_range: float = BASE_MUTATION_RANGE) -> None:
            Initializes a new ColorComponentGene instance with the provided parameters.

    Raises:
        ValueError: If max_value exceeds ColorComponentGene.MAX or if min_value is smaller than ColorComponentGene.MIN.

    Returns:
        None
    """
    MAX = 255
    MIN = 1
    BASE_MUTATION_RANGE = 1
    def __init__(self, value: float | int, max_value: float = MAX, min_value: float = MIN, mutation_range: float = BASE_MUTATION_RANGE) -> None:
        """
        Initialize a ColorComponentGene object.

        Parameters:
        - value (float | int): The initial value for the gene.
        - max_value (float): The maximum value allowed for the gene (default is ColorComponentGene.MAX).
        - min_value (float): The minimum value allowed for the gene (default is ColorComponentGene.MIN).
        - mutation_range (float): The range within which the gene can mutate (default is ColorComponentGene.BASE_MUTATION_RANGE).

        Raises:
        - ValueError: If max_value exceeds ColorComponentGene.MAX or if min_value is smaller than ColorComponentGene.MIN.

        Returns:
        - None
        """
        if max_value > ColorComponentGene.MAX:
            raise ValueError(f"Color gene max {max_value} cannot exceed {ColorComponentGene.MAX}.")
        if min_value < ColorComponentGene.MIN:
            raise ValueError(f"Color gene min {min_value} cannot be smaller than {ColorComponentGene.MIN}.")

        super().__init__(max_value=max_value, min_value=min_value, value=value, mutation_range=mutation_range)
