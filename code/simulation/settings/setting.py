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
        """
        Initialize a Setting object with the given parameters.

        Parameters:
            *args: Variable length argument list.
            value (float): The initial value of the setting. Default is 0.
            name (str): The name of the setting. Default is "None".
            type (str): The type of setting update ('onreturn' or 'onchange'). Default is "onreturn".

        Returns:
            None
        """
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
    def add_controller_to_menu(self, menu: pygame_menu.Menu, randomiser = False) -> None:
        """
        Add the setting controller to a menu.

        Parameters:
            menu (pygame_menu.Menu): The menu to add the setting controller to.
            randomiser (bool): Flag indicating whether to include a randomizer button. Default is False.

        Returns:
            None
        """
        pass

class BoundedSetting(Setting):
    """
    An extension of the Setting class representing a bounded setting.

    Attributes:
        _min (float): The minimum value of the setting.
        _max (float): The maximum value of the setting.
        _mid (float): The middle value between the minimum and maximum values.
        label_widget: The label widget associated with the setting.
        increment (float): The increment value for the setting.

    Methods:
        set_value(self, new_value: float) -> None: Set the value of the setting within the bounds.
        randomise_value(self, type: str = "uniform") -> None: Randomize the value of the setting based on the specified type.
        add_controller_to_menu(self, menu: pygame_menu.Menu, randomiser: bool = False) -> None: Add the setting controller to a menu.

    Inherits from:
        Setting
    """
    def __init__(self, *args, value: float = None, name: str = "None", min: float = None, max: float = None, type: str = "onreturn", increment = None) -> None:
        """
        Initialize a BoundedSetting object with the given parameters.

        Parameters:
            *args: Variable length argument list.
            value (float): The initial value of the setting. If None, it will be set to the middle value between min and max.
            name (str): The name of the setting.
            min (float): The minimum value of the setting.
            max (float): The maximum value of the setting.
            type (str): The type of setting update ('onreturn' or 'onchange').
            increment: The increment value for the setting. If None, it will be set to (max - min) / 100.

        Returns:
            None
        """
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
        """
        Set the value of the setting to the specified new value.

        Parameters:
            new_value (float): The new value to set for the setting.

        Returns:
            None
        """
        if new_value >= self._max:
            new_value = self._max
        elif new_value <= self._min:
            new_value = self._min

        self._value = new_value
        self.post_update()

    def randomise_value(self, type = "uniform") -> None:
        """
        Randomize the value of the setting based on the specified type.

        Parameters:
            type (str): The type of randomization to apply. Default is "uniform".
            Valid options for now are "uniform" and "gauss" if type is not valid then an ValueError is thrown

        Returns:
            None
        """
        if type == "uniform":
            self.set_value(random.uniform(self._min, self._max))
        elif type == "gauss":
            self.set_value(random.gauss(self._mid, self._mid/2))
        else:
            raise ValueError("Type not defined")
        self.widget.set_value(self._value)

    def add_controller_to_menu(self, menu: pygame_menu.Menu, randomiser = False) -> None:
        """
        Add the setting controller to a menu.

        Parameters:
            menu (pygame_menu.Menu): The menu to add the setting controller to.
            randomiser (bool): Flag indicating whether to include a randomizer button. Default is False.

        Returns:
            None.
        """
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
    """
    An extension of the Setting class representing an unbounded setting.

    Attributes:
        Inherits all attributes from the Setting class.

    Methods:
        set_value(self, new_value: float) -> None: Sets the value of the unbounded setting to the specified new value.
        randomise_value(self, type: str = "uniform") -> None: Abstract method to randomize the value of the unbounded setting.
        add_controller_to_menu(self, menu: pygame_menu.Menu, randomiser: bool = False) -> None: Adds the unbounded setting controller to a menu.

    Raises:
        NotImplementedError: If the randomise_value method is not implemented in the subclass.
    """
    def __init__(self, *args, value: float = 0, name: str = "None", type: str = "onreturn") -> None:
        super().__init__(*args, value=value, name=name, type=type)

    def set_value(self, new_value: float) -> None:
        """
        Set the value of the unbounded setting to the specified new value.

        Parameters:
            new_value (float): The new value to set for the unbounded setting.

        Returns:
            None
        """
        self._value = new_value
        self.post_update()

    def randomise_value(self, type="uniform") -> None:
        """
        Randomize the value of the unbounded setting based on the specified type.

        Uniform randomisation:
            min = 0

            max = (value + 1) * 2

        Gauss randomisation:
            mu = value

            sigma = 1

        Parameters:
            type (str): The type of randomization to apply. Default is "uniform".
            Valid options for now are "uniform" and "gauss" if type is not valid then an ValueError is thrown

        Returns:
            None

        Raises:
            ValueError: If the specified type is not valid.
        """
        # TODO think of the best way to randomise an unbounded value
        if type == "uniform":
            self.set_value(random.uniform(0, (self._value + 1) * 2))
        elif type == "gauss":
            self.set_value(random.gauss(self._value))
        else:
            raise ValueError("Type not defined")
        self.widget.set_value(self._value)

    def add_controller_to_menu(self, menu: pygame_menu.Menu, randomiser = False) -> None:
        """
        Add the unbounded setting controller to a menu.

        Parameters:
            menu (pygame_menu.Menu): The menu to add the unbounded setting controller to.
            randomiser (bool): Flag indicating whether to include a randomizer button. Default is False.

        Returns:
            None
        """
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