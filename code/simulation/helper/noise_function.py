from __future__ import annotations

import math
import noise


class NoiseFunction():
    def __init__(self, factor_x = 1, factor_y = 1, offset_x = 0, offset_y = 0, pow_x = 1, pow_y = 1) -> None:
        self.factor_x = factor_x
        self.factor_y = factor_y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.pow_x = pow_x
        self.pow_y = pow_y
        
    def x(self, x: float) -> float:
        return math.pow(x * self.factor_x, self.pow_x) + self.offset_x
    
    def y(self, y: float) -> float:
        return math.pow(y * self.factor_y, self.pow_y) + self.offset_y
    
    def noise(self, x:float, y:float) -> float:
        value = NoiseFunction._normalise(noise.snoise2(self.x(x), self.y(y)))
        if not(0 <= value <= 1):
            raise ValueError(f"noise value not in range [0, 1] {value}")
        return value
    
    @classmethod
    def _normalise(cls, value) -> float:
        value += 1
        value /= 2
        if not(0 <= value <= 1):
            raise ValueError(f"noise value not in range [0, 1] {value}")
        return value
    
    @classmethod
    def weigh(cls, x:float, y:float, functions: list[NoiseFunction], weights: list[float] = None) -> float:
        if weights is None:
            weights = [1 for function in functions]
        else:
            while len(weights) < len(functions):
                weights.append(1)

        sum = 0
        weight_sum = 0
        for i, function in enumerate(functions):
            sum += function.noise(x, y) * weights[i]
            weight_sum += weights[i]
        value = sum / weight_sum
        value = NoiseFunction._normalise(value)
        
        if not(0 <= value <= 1):
            raise ValueError(f"noise value not in range [0, 1] {value}")
        