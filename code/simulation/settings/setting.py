import pygame_menu
import random
from abc import ABC, abstractmethod

class Setting(ABC):
    """
    An abstract base class representing a setting.

    Attributes:
        _value (float): The value of the setting.
        _name (str): The name of the setting.
        widget_controller: Controller for the widget.
        controller_frame: Frame for the controller.
        _onreturn (bool): Flag indicating if the setting updates on return.
        _onchange (bool): Flag indicating if the setting updates on change.
        post_update_methods (list): List of methods to call after updating the setting.

    Methods:
        post_update(self) -> None: Calls all post update methods.
        set_value(self, new_value: float) -> None: Abstract method to set the value of the setting.
        randomise_value(self, type: str = "uniform") -> None: Abstract method to randomize the value of the setting.
        add_controller_to_menu(self, menu: pygame_menu.Menu, randomiser: bool = False) -> None: Abstract method to add the setting controller to a menu.
    """
    # TODO think of making value an optional argument and if _mid existst then setting value equal to it else it being 0
    def __init__(self, *args, value: float = 0, name: str = "None", type: str = "onreturn") -> None:
        self._value = value
        self._name = name
        
        self.widget_controller = None
        self.controller_frame = None

        # Set update type
        self._onreturn = False
        self._onchange = False
        if type == "onreturn":
            self._onreturn = True
        elif type == "onchange":
            self._onchange= True
        else:
            raise ValueError(f"{type} is not a valid type.")
        
        # Add post update methods
        self.post_update_methods: list = []
        for arg in args:
            if not callable(arg):
                raise ValueError("args must be callable.")
            self.post_update_methods.append(arg)

    def post_update(self) -> None:
        """
        Calls all post update methods.

        Parameters:
            None

        Returns:
            None
        """
        if self.post_update_methods:
            for method in self.post_update_methods:
                method()

    @abstractmethod
    def set_value(self, new_value: float) -> None:
        """
        Set the value of the setting to the specified new value.

        Parameters:
            new_value (float): The new value to set for the setting.

        Returns:
            None
        """
        pass

    @abstractmethod
    def randomise_value(self, type = "uniform") -> None:
        """
        Randomize the value of the setting based on the specified type.

        Parameters:
            type (str): The type of randomization to apply. Default is "uniform".

        Returns:
            None
        """
        pass

    @abstractmethod
    def add_controller_to_menu(self, menu: pygame_menu.Menu, randomiser = False) -> pygame_menu.pygame_menu.widgets.Widget:
        """
        Add the setting controller to a menu.

        Parameters:
            menu (pygame_menu.Menu): The menu to add the setting controller to.
            randomiser (bool): Flag indicating whether to include a randomizer button. Default is False.

        Returns:
            pygame_menu.pygame_menu.widgets.Widget: The widget representing the setting controller.
        """
        pass

class BoundedSetting(Setting):
    def __init__(self, *args, value: float = None, name: str = "None", min: float = None, max: float = None, type: str = "onreturn", increment = None) -> None:
        self._min = min
        self._max = max
        self._mid = (self._max-self._min) / 2

        if value is None:
            value = self._mid

        super().__init__(*args, value=value, name=name, type=type)
        self.label_widget: pygame_menu.pygame_menu.widgets.Label = None

        if increment is not None:
            self.increment = increment
        else:
            self.increment = (self._max-self._min)/100

    def set_value(self, new_value: float) -> None:
        if new_value >= self._max:
            new_value = self._max
        elif new_value <= self._min:
            new_value = self._min

        self._value = new_value
        self.post_update()

    def randomise_value(self, type = "uniform"):
        if type == "uniform":
            self.set_value(random.uniform(self._min, self._max))
        elif type == "gauss":
            self.set_value(random.gauss(self._mid, self._mid/2))
        else:
            raise ValueError("Type not defined")
        self.widget.set_value(self._value)

    def add_controller_to_menu(self, menu: pygame_menu.Menu, randomiser = False):
        self.widget = menu.add.range_slider(self._name, default=self._value, range_values=(self._min, self._max), increment=self.increment)

        if self._onreturn:
            self.widget.set_onreturn(self.set_value)
        elif self._onchange:
            self.widget.set_onchange(self.set_value)

        if randomiser:
            randomiser_buttom = menu.add.button("Randomise", self.randomise_value)
            height = max(self.widget.get_height(), randomiser_buttom.get_height()) + 10 # TODO fix the usage of +10 (throws error)
            frame = menu.add.frame_h(menu.get_width(inner=True) * 0.8, height)
            frame.pack(self.widget, align=pygame_menu.pygame_menu.locals.ALIGN_LEFT)
            frame.pack(randomiser_buttom, align=pygame_menu.pygame_menu.locals.ALIGN_RIGHT)

class UnboundedSetting(Setting):
    def __init__(self, *args, value: float = 0, name: str = "None", type: str = "onreturn") -> None:
        super().__init__(*args, value=value, name=name, type=type)

    def set_value(self, new_value: float) -> None:
        self._value = new_value
        self.post_update()

    def randomise_value(self, type="uniform"):
        # TODO think of the best way to randomise an unbounded value
        pass

    def add_controller_to_menu(self, menu: pygame_menu.Menu, randomiser = False):
        self.widget: pygame_menu.pygame_menu.widgets.TextInput = menu.add.text_input(self._name, default=self._value, input_type=pygame_menu.pygame_menu.locals.INPUT_INT) # TODO does input int make most sense here? why not use float?

        if self._onreturn:
            self.widget.set_onreturn(self.set_value)
        elif self._onchange:
            self.widget.set_onchange(self.set_value)

        if randomiser:
            randomiser_buttom = menu.add.button("Randomise", self.randomise_value)
            height = max(self.widget.get_height(), randomiser_buttom.get_height()) + 10 # TODO fix the usage of +10 (throws error)
            frame = menu.add.frame_h(menu.get_width(inner=True) * 0.8, height)
            frame.pack(self.widget, align=pygame_menu.pygame_menu.locals.ALIGN_LEFT)
            frame.pack(randomiser_buttom, align=pygame_menu.pygame_menu.locals.ALIGN_RIGHT)