from __future__ import annotations
from pygame import Rect, Surface, SRCALPHA, draw
import random
from config import *
from abc import ABC, abstractmethod

import entities.organism as organism

"""
The Tile class represents a tile in a game. It is an abstract base class (ABC) that provides common functionality for different types of tiles.

Attributes:
    rect (pygame.Rect): The rectangle representing the tile's position and size.
    cell_size (int): The size of the tile in pixels.
    neighbours (dict): A dictionary of the tile's neighboring tiles, with directions as keys and Tile objects as values.

Methods:
    update(): Abstract method that should be implemented by subclasses to update the tile's state.
    draw(screen: pygame.Surface): Draws the tile on the screen.
    add_neighbor(direction: Direction, tile: Tile): Adds a neighbor tile in the specified direction.
    get_neighbor(direction: Direction) -> Tile: Returns the neighbor tile in the specified direction.
    get_directions() -> list[Direction]: Returns a list of directions to the tile's neighbors.
    get_random_neigbor() -> Tile: Returns a random neighbor tile.
"""
class Tile(ABC):
    def __init__(self, rect: Rect, tile_size: int, organism: organism.Organism|None = None):
        self.tile_size = max(tile_size, MIN_TILE_SIZE)
        self.rect = rect
        self.neighbours = {}
        self.temp_surface = Surface((self.rect.width, self.rect.height), SRCALPHA)
        self.is_border_tile = False
        
        if organism:
            self.organism = organism
        else:
            self.organism = None

    @abstractmethod
    def update(self):
        """
        Abstract method that should be implemented by subclasses to update the tile's state.
        """
        if self.organism:
            self.organism.update()

    # TODO: this method does not currently work / display the borders, find a way to fix it
    def draw(self, screen: Surface):
        """
        Draws the tile on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the tile on.
        """
        draw.rect(self.temp_surface, tile_border_color, self.rect, tile_outline_thickness)
        screen.blit(self.temp_surface, (self.rect.left, self.rect.top))
        
    def leave(self):
        self.organism = None
        
    def enter(self, organism: organism.Organism):
        self.organism = organism
        
        assert self.organism.tile == self, "Tiles Organism and Organisms tile are not equal."
        
    def is_occupied(self):
        return self.organism is not None

    def add_neighbor(self, direction: Direction, tile: Tile):
        """
        Adds a neighbor tile in the specified direction.

        Args:
            direction (int): The direction of the neighbor tile.
            @see config for declaration of directions as variables
            tile: The neighbor tile to add.
        """
        if tile is None:
            raise ValueError("Tile is None")

        # TODO find out why this is not working properly and alway raising the error
        #if not Direction.is_valid_direction(direction):
        #    raise ValueError("Invalid direction", direction)
        
        self.neighbours[direction] = tile

    def get_directions(self) -> list[Direction]:
        """
        Returns a list of directions to the tile's neighbors.

        Returns:
            A list of directions to the tile's neighbors.
        """
        return list(self.neighbours.keys())

    def get_neighbor(self, direction: Direction) -> Tile:
        """
        Returns the neighbor tile in the specified direction.

        Args:
            direction (Direction): The direction of the neighbor tile.

        Returns:
            The neighbor tile in the specified direction.
        """
        if direction not in self.neighbours:
            raise ValueError("Invalid direction")
        
        return self.neighbours[direction]

    def get_neighbors(self) -> list[Tile]|None:
        """
        Returns a list of all neighboring tiles.

        Returns:
            list[Tile]|None: A list of Tile objects that are neighbors to this tile, or None if there are no neighbors.
        """
        if not self.neighbours:
            return None
        return list(self.neighbours.values())

    def get_random_neigbor(self) -> Tile|None:
        return self.neighbours[random.choice(self.get_directions())]
    
    def get_random_unoccupied_neighbor(self) -> Tile|None:
        unoccupied_neighbors = [tile for direction, tile in self.neighbours.items() if not tile.is_occupied()]
        
        if not unoccupied_neighbors:
            return None
        
        return random.choice(unoccupied_neighbors)
    
    def is_neighbour(self, tile):        
        for direction in self.get_directions():
            neigbour = self.neighbours[direction]
            if neigbour == tile:
                return True
            
        return False
    