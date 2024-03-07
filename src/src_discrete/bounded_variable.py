import random

class BoundedVariable:
    def __init__(self, value: int, min_val: int, max_val: int):
        if min_val >= max_val:
            raise ValueError("Minimum value must be less than maximum value.")
        if value < min_val:
            value = min_val
        elif value > max_val:
            value = max_val
        
        self._value = value
        self._min_val = min_val
        self._max_val = max_val

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
        new_value = self._value + add_val
        if new_value < self._min_val:
            self._value = self._min_val
        elif new_value > self._max_val:
            self._value = self._max_val
        else:
            self._value = new_value
            
    def mutate(self):
        if self._value == self._min_val:
            self._value += 1
        elif self._value == self._max_val:
            self._value -= 1
        else:
            self._value += random.choice([-1, 1])
            
    def copy(self):
        return BoundedVariable(self._value, self._min_val, self._max_val)