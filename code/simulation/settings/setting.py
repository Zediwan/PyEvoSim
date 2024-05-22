import pygame_menu
import random
import pygame

class Setting():
    def __init__(self, value: float, *args, name: str = "None", min: float = None, max: float = None, type: str = "onreturn", **kwargs,) -> None:
        self._value = value
        self._name = name
        self._min = min
        self._max = max
        if self._max is not None and self._min is not None:
            if "increment" in kwargs:
                self.increment = kwargs["increment"]
            else:
                self.increment = (self._max-self._min)/100
        
        self._onreturn = False
        self._onchange = False
        if type == "onreturn":
            self._onreturn = True
        elif type == "onchange":
            self._onchange= True
        else:
            raise ValueError(f"{type} is not a valid type.")
        
        self.post_update_methods: list = []
        for arg in args:
            if not callable(arg):
                raise ValueError("args must be callable.")
            self.post_update_methods.append(arg)
        
    def set_value(self, new_value: float):
        if self._max is not None:
            if new_value >= self._max:
                new_value = self._max
        if self._min is not None:
            if new_value <= self._min:
                new_value = self._min
        self._value = new_value
        if self.post_update_methods:
            for method in self.post_update_methods:
                method()

    def randomise_value(self, type = "uniform"):
        if type == "uniform":
            self.set_value(random.uniform(self._min, self._max))
        elif type == "gauss":
            self.set_value(random.gauss((self._max+self._min)/2, (self._max+self._min)/4))
        else:
            raise ValueError("Type not defined")
        self.widget.set_value(self._value)
            
    def add_controller_to_menu(self, menu: pygame_menu.Menu):
        self.widget = None
        if self._min is not None and self._max is not None:
            self.widget = menu.add.range_slider(self._name, default=self._value, range_values=(self._min, self._max), increment=self.increment)
        else:
            self.widget = menu.add.text_input(self._name + ": ", input_type=pygame_menu.pygame_menu.locals.INPUT_INT)

        if self._onreturn:
            self.widget.set_onreturn(self.set_value)
        elif self._onchange:
            self.widget.set_onchange(self.set_value)