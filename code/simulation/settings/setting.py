import pygame_menu

class Setting():
    def __init__(self, value: float, name: str = "None", min: float = None, max: float = None, type: str = "onreturn", post_update_method = None) -> None:
        self._value = value
        self._name = name
        self._min = min
        self._max = max
        if self._max is not None and self._min is not None:
            self.increment = (self._max-self._min)/100
        
        self._onreturn = False
        self._onchange = False
        if type == "onreturn":
            self._onreturn = True
        elif type == "onchange":
            self._onchange= True
        else:
            raise ValueError(f"{type} is not a valid type.")
        
        self.post_update_method = post_update_method
        
    def set_value(self, new_value: float):
        if self._max:
            if new_value >= self._max:
                new_value = self._max
        if self._min:
            if new_value <= self._min:
                new_value = self._min
        self._value = new_value
        if self.post_update_method is not None:
            self.post_update_method()
            
    def add_controller_to_menu(self, menu: pygame_menu.Menu):
        widget = None
        if self._min is not None and self._max is not None:
            widget = menu.add.range_slider(self._name, default=self._value, range_values=(self._min, self._max), increment=self.increment)
        else:
            widget = menu.add.text_input(self._name + ": ", input_type=pygame_menu.pygame_menu.locals.INPUT_INT)

        if self._onreturn:
            widget.set_onreturn(self.set_value)
        elif self._onchange:
            widget.set_onchange(self.set_value)