from __future__ import annotations

import random

import pygame

import helper.direction
import settings.colors
import settings.font
import settings.simulation


class Tile(pygame.sprite.Sprite):
    """
    Class representing a tile in the simulation.

    Attributes:
        rect (pygame.Rect): The rectangle representing the tile.
        height (float): The height level of the tile, ranging from 0 to 1.
        moisture (float): The moisture level of the tile, ranging from 0 to 1.
        is_border (bool): Flag indicating if the tile is a border tile.

    Properties:
        moisture (float): Get or set the moisture level of the tile.
        height (float): Get or set the height level of the tile.

    Methods:
        draw(screen: pygame.Surface) -> None:
            Draw the tile on the screen.

        add_animal(animal) -> None:
            Add an animal to the tile.

        add_plant(plant) -> None:
            Add a plant to the tile.

        has_animal() -> bool:
            Check if the tile has an animal.

        has_plant() -> bool:
            Check if the tile has a plant.

        add_neighbor(direction: helper.direction.Direction, tile: Tile) -> None:
            Add a neighboring tile in a specific direction.

        get_possible_directions() -> list[helper.direction.Direction]:
            Get a shuffled list of directions to neighboring tiles.

        get_neighboring_tiles() -> list[Tile]:
            Get a shuffled list of neighboring tiles.

        get_neighbor_tile(direction: helper.direction.Direction) -> Tile | None:
            Get the neighboring tile in a specified direction.

        get_random_neigbor(needs_plant=False, needs_no_plant=False, needs_animal=False, needs_no_animal=False, needs_water=False, needs_no_water=False) -> Tile | None:
            Get a random neighboring tile based on specified criteria.

        is_neighboring_tile(tile: Tile) -> bool:
            Check if a given tile is a neighbor of the current tile.
    """
    def __init__(
        self,
        rect: pygame.Rect,
        height: float = 0,
        moisture: float = 0,
        is_border: bool = False,
    ) -> None:
        """
        Initialize a Tile object.

        Parameters:
        - rect (pygame.Rect): The rectangle representing the tile.
        - height (float): The height level of the tile, ranging from 0 to 1. Default is 0.
        - moisture (float): The moisture level of the tile, ranging from 0 to 1. Default is 0.
        - is_border (bool): Flag indicating if the tile is a border tile. Default is False.

        Returns:
        - None
        """
        pygame.sprite.Sprite.__init__(self)

        self.rect: pygame.Rect = rect
        self.image: pygame.Surface = pygame.Surface(self.rect.size)
        self.neighbors: dict[helper.direction.Direction, Tile] = {}
        self._height: float = height
        self._moisture: float = moisture

        self.plant_growth_potential: float
        self.color: pygame.Color
        self.has_water: bool
        self._set_height_moisture_dependent_attributes()

        self.animal: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
        self.plant: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()

        self.is_border: bool = is_border
        self.is_coast: bool = False

        #region stats
        self.times_visted: int = 0
        #endregion

    #region properties
    @property
    def moisture(self) -> float:
        return self._moisture

    @moisture.setter
    def moisture(self, value: float) -> None:
        """
        Set the moisture level of the Tile object.

        Parameters:
        - value (float): The moisture level to be set. Should be between 0 and 1.

        Raises:
        - ValueError: If the provided moisture value is smaller than 0 or bigger than 1.

        Returns:
        - None
        """
        if value < 0:
            raise ValueError("Moisture value is smaller than 0")
        elif value > 1:
            raise ValueError("Moisture value is bigger than 1")
        else:
            self._moisture = value
        self._set_height_moisture_dependent_attributes()

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        """
        Set the height value of the Tile object.

        Parameters:
        - value (float): The height value to be set. Should be between 0 and 1.

        Raises:
        - ValueError: If the provided height value is smaller than 0 or bigger than 1.

        Returns:
        - None
        """
        if value < 0:
            raise ValueError("Height value is smaller than 0")
        elif value > 1:
            raise ValueError("Height value is bigger than 1")
        else:
            self._height = value
        self._set_height_moisture_dependent_attributes()
    #endregion

    #region setup
    def _set_height_moisture_dependent_attributes(self) -> None:
        """
        Set the color and plant growth potential attributes of a Tile object based on its height and moisture levels.
        """
        # TODO add all these as settings
        self.has_water = False

        if self.height <= settings.simulation.WATER_HEIGHT_LEVEL:
            # Waterlogged, no growth
            self.plant_growth_potential = settings.simulation.WATER_PLANT_GROWTH
            self.color = settings.colors.WATER_COLOR
            self.has_water = True
        elif self.height <= settings.simulation.BEACH_HEIGHT_LEVEL: # TODO update this so not every tile close to water is sand but it depends on moisture
            # Sandy areas have limited growth
            self.plant_growth_potential = settings.simulation.BEACH_PLANT_GROWTH
            self.color = settings.colors.SAND_COLOR
        elif self.height <= settings.simulation.TROPICAL_HEIGHT_LEVEL:
            if self.moisture < 0.16:
                # Subtropical desert, low growth
                self.plant_growth_potential = (
                    settings.simulation.SUBTROPICAL_DESERT_PLANT_GROWTH
                )
                self.color = settings.colors.SUBTROPICAL_DESERT_COLOR
            elif self.moisture < 0.33:
                # Grassland, favorable
                self.plant_growth_potential = settings.simulation.GRASSLAND_PLANT_GROWTH
                self.color = settings.colors.GRASSLAND_COLOR
            elif self.moisture < 0.66:
                # Tropical seasonal forest, favorable
                self.plant_growth_potential = (
                    settings.simulation.TROPICAL_SEASON_FOREST_PLANT_GROWTH
                )
                self.color = settings.colors.TROPICAL_SEASONAL_FOREST_COLOR
            else:
                # Tropical rain forest, very favorable
                self.plant_growth_potential = (
                    settings.simulation.TROPICAL_RAIN_FOREST_PLANT_GROWTH
                )
                self.color = settings.colors.TROPICAL_RAIN_FOREST_COLOR
        elif self.height <= settings.simulation.TEMPERATE_HEIGHT_LEVEL:
            if self.moisture < 0.16:
                # Temperate desert, low growth
                self.plant_growth_potential = (
                    settings.simulation.TEMPERATE_DESERT_PLANT_GROWTH
                )
                self.color = settings.colors.TEMPERATE_DESERT_COLOR
            elif self.moisture < 0.50:
                # Grassland, favorable
                self.plant_growth_potential = settings.simulation.GRASSLAND_PLANT_GROWTH
                self.color = settings.colors.GRASSLAND_COLOR
            elif self.moisture < 0.83:
                # Temperate deciduous forest, very favorable
                self.plant_growth_potential = (
                    settings.simulation.TEMPERATER_DECIDOUS_FOREST_PLANT_GROWTH
                )
                self.color = settings.colors.TEMPERATE_DECIDUOUS_FOREST_COLOR
            else:
                # Temperate rain forest, optimal
                self.plant_growth_potential = (
                    settings.simulation.TEMPERATE_RAIN_FOREST_PLANT_GROWTH
                )
                self.color = settings.colors.TEMPERATE_RAIN_FOREST_COLOR
        elif self.height <= settings.simulation.TRANSITION_HEIGHT_LEVEL:
            if self.moisture < 0.33:
                # Temperate desert, low growth
                self.plant_growth_potential = (
                    settings.simulation.TEMPERATE_DESERT_PLANT_GROWTH
                )
                self.color = settings.colors.TEMPERATE_DESERT_COLOR
            elif self.moisture < 0.66:
                # Shrubland, moderate growth
                self.plant_growth_potential = settings.simulation.SHRUBLAND_PLANT_GROWTH
                self.color = settings.colors.SHRUBLAND_COLOR
            else:
                # Taiga, favorable
                self.plant_growth_potential = settings.simulation.TAIGA_PLANT_GROWTH
                self.color = settings.colors.TAIGA_COLOR
        elif self.height <= settings.simulation.MOUNTAIN_HEIGHT_LEVEL:
            if self.moisture < 0.1:
                # Scorched, minimal growth
                self.plant_growth_potential = settings.simulation.SCORCHED_PLANT_GROWTH
                self.color = settings.colors.SCORCHED_COLOR
            elif self.moisture < 0.2:
                # Bare, low growth
                self.plant_growth_potential = settings.simulation.BARE_PLANT_GROWTH
                self.color = settings.colors.BARE_COLOR
            elif self.moisture < 0.5:
                # Tundra, moderate growth
                self.plant_growth_potential = settings.simulation.TUNDRA_PLANT_GROWTH
                self.color = settings.colors.TUNDRA_COLOR
            else:
                # Snow, slightly favorable
                self.plant_growth_potential = settings.simulation.SNOW_PLANT_GROWTH
                self.color = settings.colors.SNOW_COLOR

        if self.color is None:
            raise ValueError(
                f"Color has not been set. moisture={self.moisture} height={self.height}"
            )
        if self.plant_growth_potential is None:
            raise ValueError(
                f"Plant growth has not been set. moisture={self.moisture} height={self.height}"
            )
        self.image.fill(self.color)
    #endregion

    #region main methods
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)
    #endregion

    #region organisms
    def add_animal(self, animal) -> None:
        """
        Add an animal to the Tile object.

        Parameters:
        - animal: The animal object to be added to the tile.

        Raises:
        - ValueError: If the tile already holds an animal.
        - ValueError: If the animal's tile reference does not match with the tile's animal reference.

        Returns:
        - None
        """
        # TODO declaer animal:Animal once circular import issue is solved
        if self.has_animal():
            raise ValueError("Trying to add an animal despite tile already holding one")

        self.animal.add(animal)
        self.times_visted += 1

        if animal.tile != self:
            raise ValueError(
                "Animal's tile reference not matching with tile's animal reference"
            )

    def add_plant(self, plant) -> None:
        """
        Add a plant to the Tile object.

        Parameters:
        - plant: The plant object to be added to the tile.

        Raises:
        - ValueError: If the tile already holds a plant.
        - ValueError: If the plant's tile reference does not match with the tile's plant reference.

        Returns:
        - None
        """
        # TODO declaer animal:Animal once circular import issue is solved
        if self.has_plant():
            raise ValueError("Trying to add an plant despite tile already holding one")

        self.plant.add(plant)

        if plant.tile != self:
            raise ValueError(
                "Plant's tile reference not matching with tile's plant reference"
            )

    def has_animal(self) -> bool:
        return self.animal

    def has_plant(self) -> bool:
        return self.plant
    #endregion

    #region tiles
    def add_neighbor(self, direction: helper.direction.Direction, tile: Tile) -> None:
        """
        Add a neighboring Tile to the current Tile object in a specific direction.

        Parameters:
        - direction (helper.direction.Direction): The direction in which the neighboring Tile is located.
        - tile (Tile): The neighboring Tile object to be added.

        Returns:
        - None
        """
        self.neighbors[direction] = tile
        self.is_coast = self.is_coast or (tile.has_water and self.has_water) # TODO improve this so it is in relation to distance to water

    def get_possible_directions(self) -> list[helper.direction.Direction]:
        """
        Return a shuffled list of directions representing neighboring Tiles relative to the current Tile object.

        Returns:
            list[helper.direction.Direction]: A shuffled list of directions representing neighboring Tiles.
        """
        # TODO write a test that cheks that the self keys are not shuffled
        dirs = list(self.neighbors.keys())
        random.shuffle(dirs)
        return dirs

    def get_neighboring_tiles(self) -> list[Tile]:
        """
        Return a shuffled list of neighboring Tile objects relative to the current Tile object.

        Returns:
            list[Tile]: A shuffled list of neighboring Tile objects.
        """
        # TODO write a test that cheks that the self values are not shuffled
        ns = list(self.neighbors.values())
        random.shuffle(ns)
        return ns

    def get_neighbor_tile(self, direction: helper.direction.Direction) -> Tile | None:
        """
        Return the neighboring Tile object in the specified direction.

        Parameters:
        - direction (helper.direction.Direction): The direction in which the neighboring Tile is located.

        Returns:
        - Tile | None: The neighboring Tile object if it exists in the specified direction, None otherwise.
        """
        return self.neighbors.get(direction, None)

    def get_random_neigbor(
        self, needs_plant=False, needs_no_plant=False, needs_animal=False, needs_no_animal=False, needs_water=False, needs_no_water=False
    ) -> Tile | None:
        """
        Return a random neighboring Tile object based on specified criteria.

        Parameters:
        - needs_plant (bool, optional): If True, the neighboring Tile must have a plant. Defaults to False.
        - needs_no_plant (bool, optional): If True, the neighboring Tile must not have a plant. Defaults to False.
        - needs_animal (bool, optional): If True, the neighboring Tile must have an animal. Defaults to False.
        - needs_no_animal (bool, optional): If True, the neighboring Tile must not have an animal. Defaults to False.
        - needs_water (bool, optional): If True, the neighboring Tile must have water. Defaults to False.
        - needs_no_water (bool, optional): If True, the neighboring Tile must not have water. Defaults to False.

        Returns:
        - Tile | None: A random neighboring Tile object that meets the specified criteria, or None if no such Tile is found.

        Raises:
        - ValueError: If conflicting needs are provided (e.g., needs_plant=True and needs_no_plant=True).

        """
        if needs_plant and needs_no_plant:
            raise ValueError(f"Conflicting needs needs_plant={needs_plant} and needs_no_plant={needs_no_plant}")
        if needs_animal and needs_no_animal:
            raise ValueError(f"Conflicting needs needs_animal={needs_animal} and needs_no_animal={needs_no_animal}")
        if needs_water and needs_no_water:
            raise ValueError(f"Conflicting needs needs_water={needs_water} and needs_no_water={needs_no_water}")

        options = []
        for tile in self.neighbors.values():
            if needs_plant and not tile.has_plant():
                continue
            if needs_no_plant and tile.has_plant():
                continue
            if needs_animal and not tile.has_animal():
                continue
            if needs_no_animal and tile.has_animal():
                continue
            if needs_water and tile.has_water:
                continue
            if needs_no_water and tile.has_water:
                continue
            options.append(tile)

        try:
            return random.choice(options)
        except IndexError: # If no choices
            return None

    def is_neighboring_tile(self, tile: Tile) -> bool:
        """
        Check if a given Tile object is a neighbor of the current Tile object.

        Parameters:
        - tile (Tile): The Tile object to check for neighbor relationship.

        Returns:
        - bool: True if the provided Tile object is a neighbor of the current Tile object, False otherwise.
        """
        return tile in self.neighbors.values()
    #endregion
