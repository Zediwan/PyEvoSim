class BoundedVariable:
    def __init__(self, value: int, min_val: int, max_val: int):
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