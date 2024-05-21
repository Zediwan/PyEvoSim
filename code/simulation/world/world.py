from __future__ import annotations

import datetime
import random

import pygame

import settings.database
import settings.simulation
from entities.animal import Animal
from entities.plant import Plant
from helper.direction import Direction
from world.tile import Tile
import noise
import math


class World(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, tile_size: int):
        pygame.sprite.Sprite.__init__(self)

        self.rect: pygame.Rect = rect
        self.image: pygame.Surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.organism_surface: pygame.Surface = self.image.copy()
        self.ground_surface: pygame.Surface = self.image.copy()

        self.tile_size = tile_size
        self.cols = self.rect.width // tile_size
        self.rows = self.rect.height // tile_size

        self._setup_noise_settings()

        #region time
        self.starting_time_msec: int = pygame.time.get_ticks()
        self.age_ticks: int = 0
        #endregion
        #region tiles
        self.tiles = pygame.sprite.Group()
        tiles_grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.create_tile(row, col)
                tiles_grid[row][col] = tile
                self.tiles.add(tile)
        self.add_neighbors(tiles_grid)
        self.tiles.draw(self.ground_surface)
        #endregion

        settings.database.database_csv_filename = f'databases/organism_database_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.csv'

    #region properties
    @property
    def age_msec(self):
        # TODO this should not count the time the world was paused
        return pygame.time.get_ticks() - self.starting_time_msec
    #endregion

    #region main methods
    def update(self):
        self.age_ticks += 1
        settings.simulation.organisms.update()

    def reload(self):
        for tile in self.tiles.sprites():
            tile.height = self.generate_height_values(tile.rect.x * self.height_freq_x, tile.rect.y * self.height_freq_y)
            tile.moisture = self.generate_moisture_values(tile.rect.x * self.moisture_freq_x, tile.rect.y * self.moisture_freq_y)
            tile.draw(self.ground_surface)

    def draw(self, screen: pygame.Surface):
        self.image.blit(self.ground_surface, self.rect)

        # Clear previous drawings on the organism surface
        self.organism_surface.fill((0, 0, 0, 0))
        settings.simulation.organisms.draw(self.organism_surface)
        self.image.blit(self.organism_surface, self.rect)

        screen.blit(self.image, self.rect)
    #endregion

    #region spawning
    def spawn_animals(self, amount: float = 1):
        for tile in random.choices(self.tiles.sprites(), k = amount):
            self.spawn_animal(tile)

    def spawn_plants(self, amount: float = 1):
        for tile in random.choices(self.tiles.sprites(), k = amount):
            self.spawn_plant(tile)

    def spawn_animal(self, tile: Tile):
        if not(tile.has_water or tile.has_animal()):
            settings.simulation.organisms.add(Animal(tile))

    def spawn_plant(self, tile: Tile):
        if not(tile.has_water or tile.has_plant()):
            settings.simulation.organisms.add(Plant(tile))
    #endregion

    #region tiles
    def create_tile(self, row: int, col: int) -> Tile:
        x = col * self.tile_size
        y = row * self.tile_size

        return Tile(
            pygame.Rect(x ,y ,self.tile_size, self.tile_size),
            height = self.generate_height_values(x * self.height_freq_x, y * self.height_freq_y),
            moisture = self.generate_moisture_values(x * self.moisture_freq_x, y * self.moisture_freq_y),
            is_border = self.is_border_tile(row=row, col=col),
        )

    def add_neighbors(self, tiles):
        for row in range(self.rows):
            for col in range(self.cols):
                tile: Tile = tiles[row][col]
                if row > 0:
                    tile.add_neighbor(Direction.NORTH, tiles[row-1][col])
                if col < self.cols - 1:
                    tile.add_neighbor(Direction.EAST, tiles[row][col+1])
                if row < self.rows - 1:
                    tile.add_neighbor(Direction.SOUTH, tiles[row+1][col])
                if col > 0:
                    tile.add_neighbor(Direction.WEST, tiles[row][col-1])

    def is_border_tile(self, row: int, col: int) -> bool:
        return row == 0 or col == 0 or row == self.rows - 1 or col == self.cols - 1

    def get_tiles(self, rect: pygame.Rect) -> list[Tile]:
        # Transform rect global coordinates into world coordinates
        rect.x -= self.rect.left
        rect.y -= self.rect.top

        s = pygame.sprite.Sprite()
        s.rect = rect
        return pygame.sprite.spritecollide(s, self.tiles, False)

    def get_tile(self, pos: tuple[int, int]) -> Tile:
        # Transform global coordinates into world coordinates
        x = pos[0] - self.rect.left
        y = pos[1] - self.rect.top
        
        s = pygame.sprite.Sprite()
        s.rect = pygame.Rect(x, y, 1, 1)
        return pygame.sprite.spritecollideany(s, self.tiles)
    #endregion

    #region noise
    def _setup_noise_settings(self):
        self.freq_x1: float = 1
        self.freq_y1: float = 1
        self.freq_x2: float = 2
        self.freq_y2: float = 2
        self.freq_x3: float = 4
        self.freq_y3: float = 4
        self.scale_1: float = random.uniform(.66, 1)
        self.scale_2: float = random.uniform(.33, .66)
        self.scale_3: float = random.uniform(0, .33)
        self.offset_x1: float = 0
        self.offset_y1: float = 0
        self.offset_x2: float = 4.7
        self.offset_y2: float = 2.3
        self.offset_x3: float = 19.1
        self.offset_y3: float = 16.6
        self.height_power: float = 2  # TODO make this a slider in the settings
        self.height_fudge_factor: float = 1.2  # Should be a number near 1
        self.height_freq_x: float = random.uniform(-0.01, 0.01)
        self.height_freq_y: float = random.uniform(-0.01, 0.01)
        self.moisture_freq_x: float = random.uniform(-0.01, 0.01)
        self.moisture_freq_y: float = random.uniform(-0.01, 0.01)
        self.moisture: float = 0.5
        self.height: float = 0.5

    #region noise generators
    def generate_height_values(self, x: int, y: int) -> float:
        noise1 = noise.snoise2((x * self.freq_x1) + self.offset_x1, (y * self.freq_y1) + self.offset_y1)
        noise1 *= self.scale_1
        noise2 = noise.snoise2((x * self.freq_x2) + self.offset_x2, (y * self.freq_y2) + self.offset_y2)
        noise2 *= self.scale_2
        noise3 = noise.snoise2((x * self.freq_x3) + self.offset_x3, (y * self.freq_y3) + self.offset_y3)
        noise3 *= self.scale_3
        height = noise1 + noise2 + noise3

        # Normalize back in range -1 to 1
        height /= self.scale_1 + self.scale_2 + self.scale_3

        # Normalise to range 0 to 1
        height += 1
        height /= 2

        if not(0 <= height <= 1):
            raise ValueError(f"Height value not in range [0, 1] {height}")

        height = math.pow(height * self.height_fudge_factor, self.height_power)
        height = pygame.math.clamp(height, 0, 1)
        height += (self.height*2)
        height -= 1
        height = pygame.math.clamp(height, 0, 1)

        return height

    def generate_moisture_values(self, x: int, y: int) -> float:
        moisture = noise.snoise2(x, y)

        # Normalise to range 0 to 1
        moisture += 1
        moisture /= 2

        moisture += (self.moisture*2)
        moisture -= 1
        moisture = pygame.math.clamp(moisture, 0, 1)

        if not(0 <= moisture <= 1):
            raise ValueError(f"Moisture value not in range [0, 1] {moisture}")
        return moisture
    #endregion

    #region noise setters
    def set_freq_x1(self, value):
        self.freq_x1 = value
        self.reload()

    def set_freq_y1(self, value):
        self.freq_y1 = value
        self.reload()

    def set_freq_x2(self, value):
        self.freq_x2 = value
        self.reload()

    def set_freq_y2(self, value):
        self.freq_y2 = value
        self.reload()

    def set_freq_x3(self, value):
        self.freq_x3 = value
        self.reload()

    def set_freq_y3(self, value):
        self.freq_y3 = value
        self.reload()

    def set_scale_1(self, value):
        self.scale_1 = value
        self.reload()

    def set_scale_2(self, value):
        self.scale_2 = value
        self.reload()

    def set_scale_3(self, value):
        self.scale_3 = value
        self.reload()

    def set_offset_x1(self, value):
        self.offset_x1 = value
        self.reload()

    def set_offset_y1(self, value):
        self.offset_y1 = value
        self.reload()

    def set_offset_x2(self, value):
        self.offset_x2 = value
        self.reload()

    def set_offset_y2(self, value):
        self.offset_y2 = value
        self.reload()

    def set_offset_x3(self, value):
        self.offset_x3 = value
        self.reload()

    def set_offset_y3(self, value):
        self.offset_y3 = value
        self.reload()

    def set_height_power(self, value):
        self.height_power = value
        self.reload()

    def set_fudge_factor(self, value):
        self.height_fudge_factor = value
        self.reload()

    def set_height_freq_x(self, value):
        self.height_freq_x = value
        self.reload()

    def set_height_freq_y(self, value):
        self.height_freq_y = value
        self.reload()

    def set_moisture_freq_x(self, value):
        self.moisture_freq_x = value
        self.reload()

    def set_moisture_freq_y(self, value):
        self.moisture_freq_y = value
        self.reload()

    def set_moisture(self, value):
        self.moisture = value
        self.reload()

    def set_height(self, value):
        self.height = value
        self.reload()
    #endregion

    def randomise_freqs(self):
        self.height_freq_x = random.uniform(-0.01, 0.01)
        self.height_freq_y = random.uniform(-0.01, 0.01)
        self.moisture_freq_x = random.uniform(-0.01, 0.01)
        self.moisture_freq_y = random.uniform(-0.01, 0.01)
        self.reload()
    #endregion

    def copy(self) -> World:
        """
        Create a copy of the World instance.

        Note:
            This does not create an exact copy right now as the noise values have random values that are defined in the initialisation.

            This should only be used to create a copy world of the same dimension and tile size

        Returns:
            World: A new World instance with the same dimensions and tile size as the original.
        """
        # TODO not working properly yet as _setup_noise_settings initiates with random variables so not exact copy
        return World(self.rect.copy(), self.tile_size)

    #region static methods
    @staticmethod
    def adjust_dimensions(rect: pygame.Rect, tile_size: int) -> pygame.Rect:
        """
        Adjust the dimensions of a rectangle to be multiples of a given tile size.

        Parameters:
            rect (pygame.Rect): The rectangle whose dimensions need to be adjusted.
            tile_size (int): The size of the tiles to which the dimensions should be adjusted.

        Returns:
            pygame.Rect: A new rectangle with adjusted dimensions that are multiples of the tile size.
        """
        rect.width = (rect.width // tile_size) * tile_size
        rect.height = (rect.height // tile_size) * tile_size

        return rect
    #endregion
