import copy
import random

class BoundedVariable:
    """
    A class representing a bounded variable.

    Attributes:
        _min_val (int): The minimum value that the variable can have.
        _max_val (int): The maximum value that the variable can have.
        _value (int): The current value of the variable.

    Methods:
        __init__(self, value: int, min_val: int, max_val: int): Initializes a new instance of the BoundedVariable class.
        value(self) -> int: Gets the current value of the variable.
        value(self, new_value: int): Sets the value of the variable.
        add_value(self, add_val: int): Adds a value to the variable and returns the excess value.
        ratio(self) -> float: Calculates the ratio of the current value to the total range of the variable.
        mutate(self): Mutates the variable by adding a random value of -1 or 1.
        copy(self) -> BoundedVariable: Creates a copy of the variable.

    """
    def __init__(self, value: int, min_val: int, max_val: int):
        """
        Initializes a new instance of the BoundedVariable class.

        Parameters:
            value (int): The initial value of the variable.
            min_val (int): The minimum value that the variable can have.
            max_val (int): The maximum value that the variable can have.

        Raises:
            ValueError: If the minimum value is greater than or equal to the maximum value.

        """
        if min_val >= max_val:
            raise ValueError("Minimum value must be less than maximum value.")
        self._min_val = min_val
        self._max_val = max_val
        self.value = value

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, new_value: int):
        """
        Sets the value of the variable.

        Parameters:
            new_value (int): The new value to set for the variable.

        Raises:
            None

        Returns:
            None

        """
        if new_value < self._min_val:
            self._value = self._min_val
        elif new_value > self._max_val:
            self._value = self._max_val
        else:
            self._value = new_value
    
    def add_value(self, add_val: int) -> int:
        """
        Adds a value to the variable and returns the excess value.

        Parameters:
            add_val (int): The value to be added to the variable.

        Raises:
            None

        Returns:
            int: The excess value, which is the difference between the current value and the maximum value, or 0 if there is no excess.

        """
        self.value += add_val
        return max(self._value - self._max_val, 0)
            
    def ratio(self) -> float:
        """
        Calculates the ratio of the current value to the total range of the variable.

        Returns:
            float: The ratio of the current value to the total range of the variable.

        """
        total_range = self._max_val - self._min_val
        current_difference = self._value - self._min_val
        return current_difference / total_range
            
    def mutate(self):
        self.add_value(random.choice([-1, 1]))
            
    def copy(self):
        return copy.copy(self)