from __future__ import annotations

import math
import noise
from settings.setting import Setting


class NoiseFunction():
    # TODO add the option to display the function as it is written
    FACTOR_MIN = 0
    FACTOR_MAX = 10
    OFFSET_MIN = -20
    OFFSET_MAX = abs(OFFSET_MIN)
    POW_MIN = 0
    POW_MAX = 4

    def __init__(self, factor_x = 1, factor_y = 1, offset_x = 0, offset_y = 0, pow_x = 1, pow_y = 1, post_update_method = None) -> None:
        self.factor_x = Setting(factor_x, "Factor x", min = self.FACTOR_MIN, max=self.FACTOR_MAX, post_update_method=post_update_method)
        self.factor_y = Setting(factor_y, "Factor y", min = self.FACTOR_MIN, max=self.FACTOR_MAX, post_update_method=post_update_method)
        self.offset_x = Setting(offset_x, "Offset x", min = self.OFFSET_MIN, max=self.OFFSET_MAX, post_update_method=post_update_method)
        self.offset_y = Setting(offset_y, "Offset y", min = self.OFFSET_MIN, max=self.OFFSET_MAX, post_update_method=post_update_method)
        self.pow_x = Setting(pow_x, "Pow x", min = self.POW_MIN, max=self.POW_MAX, post_update_method=post_update_method)
        self.pow_y = Setting(pow_y, "Pow y", min = self.POW_MIN, max=self.POW_MAX, post_update_method=post_update_method)
        
    def x(self, x: float) -> float:
        return math.pow(x * self.factor_x._value, self.pow_x._value) + self.offset_x._value
    
    def y(self, y: float) -> float:
        return math.pow(y * self.factor_y._value, self.pow_y._value) + self.offset_y._value
    
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
        