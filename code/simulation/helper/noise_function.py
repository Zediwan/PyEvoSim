from __future__ import annotations

import math
import noise
from settings.setting import Setting
import pygame_menu
import pygame


class NoiseFunction():
    # TODO add the option to display the function as it is written
    FACTOR_MIN = 0
    FACTOR_MAX = 10
    OFFSET_MIN = -20
    OFFSET_MAX = abs(OFFSET_MIN)
    POW_MIN = 0
    POW_MAX = 2
    FUDGE_MIN = 0.5
    FUDGE_MAX = 1.5


    def __init__(self, *args, factor_x = 1, factor_y = 1, offset_x = 0, offset_y = 0, pow_x = 1, pow_y = 1, pow = 1, fudge = 1.2) -> None:
        self.factor_x = Setting(factor_x, *args, name="Factor x", min = self.FACTOR_MIN, max=self.FACTOR_MAX, type="onchange")
        self.factor_y = Setting(factor_y, *args, name="Factor y", min = self.FACTOR_MIN, max=self.FACTOR_MAX, type="onchange")
        self.offset_x = Setting(offset_x, *args, name="Offset x", min = self.OFFSET_MIN, max=self.OFFSET_MAX, type="onchange")
        self.offset_y = Setting(offset_y, *args, name="Offset y", min = self.OFFSET_MIN, max=self.OFFSET_MAX, type="onchange")
        self.pow_x = Setting(pow_x, *args, name="Pow x", min = self.POW_MIN, max=self.POW_MAX, type="onchange", increment = 1)
        self.pow_y = Setting(pow_y, *args, name="Pow y", min = self.POW_MIN, max=self.POW_MAX, type="onchange", increment = 1)
        self.pow = Setting(pow, *args, name="Pow", min = self.POW_MIN, max=self.POW_MAX, type="onchange", increment = 1)
        self.fudge = Setting(fudge, *args, name="Fudge", min = self.FUDGE_MIN, max=self.FUDGE_MAX, type="onchange")
        
        self.settings: list[Setting] = []
        self.settings.append(self.factor_x)
        self.settings.append(self.factor_y)
        self.settings.append(self.offset_x)
        self.settings.append(self.offset_y)
        self.settings.append(self.pow_x)
        self.settings.append(self.pow_y)
        self.settings.append(self.pow)
        self.settings.append(self.fudge)

    def x(self, x: float) -> float:
        try:
            value = math.pow(x * self.factor_x._value, self.pow_x._value) + self.offset_x._value
        except ValueError:
            print("math domain error!")
            value = x * self.factor_x._value + + self.offset_x._value
        return value
    
    def y(self, y: float) -> float:
        try:
            value = math.pow(y * self.factor_y._value, self.pow_y._value) + self.offset_y._value
        except ValueError:
            print("math domain error!")
            value = y * self.factor_y._value + + self.offset_y._value
        return value

    def noise(self, x:float, y:float) -> float:
        try:
            value = math.pow(NoiseFunction._normalise(noise.snoise2(self.x(x), self.y(y))) * self.fudge._value, self.pow._value)
        except ValueError:
            print("math domain error!")
            value = NoiseFunction._normalise(noise.snoise2(self.x(x), self.y(y)) * self.fudge._value, self.pow._value)

        value = pygame.math.clamp(value, 0, 1)
        if not(0 <= value <= 1):
            raise ValueError(f"noise value not in range [0, 1] {value}")
        return value
    
    def add_function_controller_to_menu(self, menu: pygame_menu.Menu) -> None:
        menu.add.label("Function")
        for setting in self.settings:
            setting.add_controller_to_menu(menu)

    def randomise(self) -> None:
        for setting in self.settings:
            setting.randomise_value(type="gauss")

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
        
        if not(0 <= value <= 1):
            raise ValueError(f"noise value not in range [0, 1] {value}")

        return value
        