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

    def function(self, x: float, y: float) -> tuple[float, float]:
        _x = x * self.factor_x._value
        _y = y * self.factor_y._value

        try:
            _x = math.pow(_x, self.pow_x._value)
        except ValueError:
            print("math domain error!")
        try:
            _y = math.pow(_y, self.pow_y._value)
        except ValueError:
            print("math domain error!")

        _x += self.offset_x._value
        _y += self.offset_y._value

        return _x, _y


    def noise(self, x:float, y:float) -> float:
        _x, _y = self.function(x, y)
        _noise = noise.snoise2(_x, _y)
        _noise = NoiseFunction._normalise(_noise)
        _noise *= self.fudge._value
        try:
            value = math.pow(_noise, self.pow._value)
        except ValueError:
            print("math domain error!")
            value = _noise

        value = pygame.math.clamp(value, 0, 1)
        if not(0 <= value <= 1):
            raise ValueError(f"noise value not in range [0, 1] {value}")
        return value
    
    def add_function_controller_to_menu(self, menu: pygame_menu.Menu, randomiser = False) -> None:
        self.label = menu.add.label("Function")
        if randomiser:
            randomiser_buttom = menu.add.button("Randomise", self.randomise)
            height = max(self.label.get_height(), randomiser_buttom.get_height()) + 10 # TODO fix the usage of +10 (throws error)
            frame = menu.add.frame_h(menu.get_width(inner=True), height)
            frame.pack(self.label, align=pygame_menu.pygame_menu.locals.ALIGN_LEFT)
            frame.pack(randomiser_buttom, align=pygame_menu.pygame_menu.locals.ALIGN_RIGHT)
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
        