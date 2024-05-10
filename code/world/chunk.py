import pygame

from world.tile import Tile
import settings.test
import helper.noise

class Chunk(pygame.sprite.Sprite):
    tiles_per_axis: int = 16
    size: int  = tiles_per_axis * Tile.size
    
    def __init__(self, x: int, y: int, rect: pygame.Rect) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.rect: pygame.Rect = pygame.Rect(x * Chunk.size, y * Chunk.size, Chunk.size, Chunk.size)
        self.global_rect = self.rect.move(rect.left, rect.top) # This is used for debug mode
        self.image: pygame.Surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill(pygame.Color(0,0,0,0))
        
        self.tile_image = self.image.copy()
        self.organism_image = self.image.copy()
        
        self.tiles = pygame.sprite.Group()
        self.organisms = pygame.sprite.Group()
        
        # Setup tiles
        for y in range(Chunk.tiles_per_axis):
            for x in range(Chunk.tiles_per_axis):
                local_x = (x * Tile.size)
                local_y = (y * Tile.size)
                self.add_tile(local_x, local_y)
                
        self.reload()
        
    def add_tile(self, local_x: int, local_y: int):
        # TODO think if there is a better way to check if a tile is in the chunk in world coordinates
        global_x, global_y = self.transform_local_to_global_coordinates(local_x, local_y)
        if not self.rect.collidepoint(global_x, global_y):
            raise ValueError("Tile trying to be added that doesn't belong in this chunk.")
        else:
            self.tiles.add(
                Tile(local_x,
                     local_y,
                     height = helper.noise.generate_height_values(global_x / 1000, global_y/ 1000),
                     moisture = helper.noise.generate_moisture_values(global_x/ 1000, global_y/ 1000)
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
        
        if settings.test.debug_mode:
            rect = self.global_rect
        else:
            rect = self.rect

        # Set the current visible rectangle
        # TODO find if this can be done in a better way
        self.visible_rect = rect.move(settings.test.offset_x, settings.test.offset_y)
        # Draw onto screen
        screen.blit(self.image, self.visible_rect)
        
    def reload(self):
        self.tiles.update()
        self.tiles.draw(self.tile_image)
        self.image.blit(self.tile_image, (0, 0))  
        
    # Interaction
    def get_tile_at(self, x: int, y: int):
        pass
    
    # Coordinates
    def transform_global_to_local_coordinates(self, x_global: int, y_global: int) -> tuple[int, int]:
        x_local = x_global - self.rect.left
        y_local = y_global - self.rect.top
        return (x_local, y_local)
    
    def transform_local_to_global_coordinates(self, x_local: int, y_local: int) -> tuple[int, int]:
        x_global = x_local + self.rect.left
        y_global = y_local + self.rect.top
        return (x_global, y_global)
