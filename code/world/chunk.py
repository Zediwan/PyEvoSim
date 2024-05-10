import pygame

from world.tile import Tile
import settings.test
import helper.noise

class Chunk(pygame.sprite.Sprite):
    tiles_per_axis: int = 32
    size: int  = tiles_per_axis * Tile.size
    
    def __init__(self, x: int, y: int, rect: pygame.Rect) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.rect: pygame.Rect = pygame.Rect(x * Chunk.size + rect.left, y * Chunk.size + rect.top, Chunk.size, Chunk.size)
        self.image: pygame.Surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill(pygame.Color(0,0,0,0))
        
        self.tile_image = self.image.copy()
        self.organism_image = self.image.copy()
        
        self.tiles = pygame.sprite.Group()
        self.organisms = pygame.sprite.Group()
        
        for y in range(Chunk.tiles_per_axis):
            for x in range(Chunk.tiles_per_axis):
                global_x = (x * Tile.size) + self.rect.left
                global_y = (y * Tile.size) + self.rect.top
                self.add_tile(global_x, global_y)
                
        self.reload()
        
    def add_tile(self, x_global: int, y_global: int):
        # TODO think if there is a better way to check if a tile is in the chunk in world coordinates
        rect = pygame.Rect(x_global, y_global, Tile.size, Tile.size)
        if not self.rect.contains(rect):
            raise ValueError("Tile trying to be added that doesn't belong in this chunk.")
        else:
            x_local = x_global - self.rect.left
            y_local = y_global - self.rect.top
            self.tiles.add(
                Tile(x_local, 
                     y_local,
                     height = helper.noise.generate_height_values(x_global / 1000, y_global/ 1000),
                     moisture = helper.noise.generate_moisture_values(x_global/ 1000, y_global/ 1000)
                     )
                )
        
    def update(self):
        self.organisms.update()
    
    def draw(self, screen: pygame.Surface):
        # Ground
        # self.image.blit(self.tile_image, (0, 0))
        
        # Organism
        # self.organism_image.fill(pygame.Color(0,0,0,0))
        # self.organisms.draw(self.organism_image)
        # self.image.blit(self.organism_image, (0, 0))

        # Chunk borders
        pygame.draw.rect(
            self.image,
            pygame.Color("gray20"),
            self.image.get_rect(topleft = (0,0)),
            width=1
        )
        
        # Draw onto screen
        screen.blit(self.image, self.rect.move(settings.test.offset_x, settings.test.offset_y))
        
    def reload(self):
        self.tiles.update()
        self.tiles.draw(self.tile_image)
        self.image.blit(self.tile_image, (0, 0))  
        
    # # Interaction
    # def get_tile_at(self, x: int, y: int):
    #     pass
    
    # # Coordinates
    # def transform_global_to_local_coordinates(self, x_global: int, y_global: int) -> tuple[int, int]:
    #     x_local = x_global - self.rect.left
    #     y_local = y_global - self.rect.top
    #     return (x_local, y_local)
    
    # def transform_local_to_global_coordinates(self, x_local: int, y_local: int) -> tuple[int, int]:
    #     x_global = x_local + self.rect.left
    #     y_global = y_local + self.rect.top
    #     return (x_global, y_global)      
