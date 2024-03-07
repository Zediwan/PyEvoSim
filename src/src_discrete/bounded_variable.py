import copy
import random

class BoundedVariable:
    def __init__(self, value: int, min_val: int, max_val: int):
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
        if new_value < self._min_val:
            self._value = self._min_val
        elif new_value > self._max_val:
            self._value = self._max_val
        else:
            self._value = new_value
    
    def add_value(self, add_val: int):
        self.value += add_val
        return max(self._value - self._max_val, 0)
            
    def ratio(self) -> float:
        total_range = self._max_val - self._min_val
        current_difference = self._value - self._min_val
        return current_difference / total_range
            
    def mutate(self):
        self.add_value(random.choice([-1, 1]))
            
    def copy(self):
        return copy.copy(self)