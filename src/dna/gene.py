from __future__ import annotations

class Gene():
    def __init__(self, value: float, max_value: float, min_value: float, mutation_range: float) -> None:
        self._value: float = value
        
        self._max_value: float = max_value
        self._min_value: float = min_value
        
        self._mutation_range: float = mutation_range
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: float):
        if value > self._max_value:
            self._value = self._max_value
            return
        if value < self._min_value:
            self._value = self._min_value
            return
        self._value = value
        
    def copy(self) -> Gene:
        return Gene(self.value, self._max_value, self._min_value)
    
    def mutate(self) -> None:
        self.value += (self._mutation_range * 2) - self._mutation_range