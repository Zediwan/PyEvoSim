import pygame
from config import *
import random
from tiles.tile import Tile


class DrawWorld:

    def __init__(self, world):
        self.font0 = pygame.font.Font(pygame.font.get_default_font(), 14)
        self.font1 = pygame.font.Font(pygame.font.get_default_font(), 11)
        self.font2 = pygame.font.Font(pygame.font.get_default_font(), 8)
        self.world = world
        self.worldSurface = pygame.Surface((self.world.cols * self.world.tile_size, self.world.rows * self.world.tile_size))

    def update(self):
        lowest_entropy = self.world.getLowestEntropy()
        for row in range(self.world.rows):
            for col in range(self.world.cols):
                tile_entropy = self.world.getEntropy(col, row)
                tile_type = self.world.getType(col, row)
                if tile_entropy > 0:
                    tile_image = pygame.Surface((self.world.tile_size, self.world.tile_size))
                    if tile_entropy == 27:
                        textSurface = self.font2.render(str(tile_entropy), True, "darkgrey")
                        tile_image.blit(textSurface, (3, 3))
                    elif tile_entropy >= 10:
                        textSurface = self.font1.render(str(tile_entropy), True, "grey")
                        tile_image.blit(textSurface, (2, 3))
                    elif tile_entropy < 10:
                        if tile_entropy == lowest_entropy:
                            textSurface = self.font0.render(str(tile_entropy), True, "green")
                        else:
                            textSurface = self.font0.render(str(tile_entropy), True, "white")
                        tile_image.blit(textSurface, (4, 1))
                else:
                    match tile_type:
                        case _:
                            tile_image = pygame.Rect(col * self.world.tile_size, row * self.world.tile_size, self.world.tile_size, self.world.tile_size)
                            #self.world.ground.tiles[row][col] = Tile(tile_immage, self.world.tile_size, value = random.randint(1, 10)) 
                            #self.worldSurface.blit(tile_image, (col * self.world.tile_size, row * self.world.tile_size))

    def draw(self, displaySurface):
        displaySurface.blit(self.worldSurface, (0, 0))