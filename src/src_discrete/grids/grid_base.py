import random
from pygame import sprite, Surface
from abc import ABC, abstractmethod
from entities.organism import Organism
from tiles.tile_base import Tile
from config import *

class Grid(ABC, sprite.Sprite):
    """
    The Grid class represents a grid of tiles in a game. It is an abstract base class (ABC) that provides common functionality for grids.

    Attributes:
        rows (int): The number of rows in the grid.
        cols (int): The number of columns in the grid.
        tile_size (int): The size of each tile in the grid.
        tiles (list[Tile]): The list of tiles in the grid.

    Methods:
        __init__(rows: int, cols: int, tile_size: int): Initializes a new Grid object with the specified number of rows, columns, and tile size.
        update(): Updates the state of all tiles in the grid.
        draw(screen: pygame.Surface): Draws all tiles in the grid on the specified screen surface.
        create_tile(col: int, row: int) -> Tile: Abstract method that should be implemented by subclasses to create a new tile at the specified column and row.
        add_cell_neighbours(): Adds the neighboring tiles for each tile in the grid.
        is_border_tile(row: int, col: int) -> bool: Checks if the tile at the specified row and column is a border tile.

    Note:
        This class is an abstract base class (ABC) and should not be instantiated directly. Subclasses should implement the create_tile method to create specific types of tiles for the grid.
    """
    def __init__(self, rows : int, cols : int, tile_size : int):
        sprite.Sprite.__init__(self)
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.tiles = [self.create_tile(col, row) for row in range(self.rows) for col in range(self.cols)]
        self.add_cell_neighbours()
    
    def update(self):
        """
        Updates the state of all tiles in the grid.

        This method shuffles the list of tiles randomly and then calls the update method on each tile. The update method is responsible for updating the state of the tile based on the game logic.

        Parameters:
            None

        Returns:
            None

        Example:
            grid = Grid(10, 10, 20)
            grid.update()
        """
        random.shuffle(self.tiles)
        for tile in self.tiles:
            tile.update()
            
    def draw(self, screen : Surface):
        """
        Draws all tiles in the grid on the specified screen surface.

        This method creates a temporary surface with the size of the grid (number of columns multiplied by tile size, number of rows multiplied by tile size). It then iterates over each tile in the grid and calls the draw method on each tile, passing the temporary surface as the argument. The draw method of each tile is responsible for drawing the tile on the temporary surface. Finally, the temporary surface is blitted onto the specified screen surface at the position (0, 0).

        Parameters:
            screen (pygame.Surface): The screen surface on which to draw the tiles.

        Returns:
            None

        Example:
            grid = Grid(10, 10, 20)
            screen = pygame.display.set_mode((800, 600))
            grid.draw(screen)
        """
        temp_surface = Surface((self.cols * self.tile_size, self.rows * self.tile_size), pygame.SRCALPHA)
        for tile in self.tiles:
            tile.draw(temp_surface)
        screen.blit(temp_surface, (0, 0))
                
    @abstractmethod
    def create_tile(self, col, row) -> Tile:
        pass
    
    def add_cell_neighbours(self):
        """
        Adds the neighboring tiles for each tile in the grid.

        This method iterates over each tile in the grid and adds the neighboring tiles to the 'neighbours' dictionary of each tile. The neighboring tiles are determined based on the current row and column of the tile. The 'neighbours' dictionary is then assigned to the 'neighbours' attribute of the tile.

        Parameters:
            None

        Returns:
            None

        Example:
            grid = Grid(10, 10, 20)
            grid.add_cell_neighbours()
        """
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.tiles[row * self.cols + col]
                neighbours = {}
                if row > 0:
                    neighbours[Direction.NORTH] = self.tiles[(row - 1) * self.cols + col]
                if col < self.cols - 1:
                    neighbours[Direction.EAST] = self.tiles[row * self.cols + col + 1]
                if row < self.rows - 1:
                    neighbours[Direction.SOUTH] = self.tiles[(row + 1) * self.cols + col]
                if col > 0:
                    neighbours[Direction.WEST] = self.tiles[row * self.cols + col - 1]
                tile.neighbours = neighbours
    
    def is_border_tile(self, row: int, col: int) -> bool:
        """
        Checks if the tile at the specified row and column is a border tile.

        Parameters:
            row (int): The row index of the tile.
            col (int): The column index of the tile.

        Returns:
            bool: True if the tile is a border tile, False otherwise.

        Example:
            grid = Grid(10, 10, 20)
            is_border = grid.is_border_tile(0, 0)
            print(is_border)  # Output: True
        """
        return (row == 0 or col == 0 or row == self.rows - 1 or col == self.cols - 1)