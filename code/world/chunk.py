import pygame

from world.tile import Tile
import settings.test
import helper.noise

class Chunk(pygame.sprite.Sprite):
    tiles_per_axis: int = 4
    size: int  = tiles_per_axis * Tile.size
    
    def __init__(self, x: int, y: int, world_rect: pygame.Rect) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.starting_rect: pygame.Rect = pygame.Rect(x * Chunk.size, y * Chunk.size, Chunk.size, Chunk.size)
        self.global_rect = self.starting_rect.move(world_rect.left, world_rect.top) # This is used for debug mode

        self.image: pygame.Surface = pygame.Surface(self.starting_rect.size, pygame.SRCALPHA)
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
        
    @property
    def rect(self) -> pygame.Rect:
        if settings.test.debug_mode:
            return self.global_rect
        else:
            return self.starting_rect

    @property
    def visible_rect(self) -> pygame.Rect:
        return self.global_rect.move(settings.test.offset_x, settings.test.offset_y)

    def add_tile(self, local_x: int, local_y: int):
        # TODO think if there is a better way to check if a tile is in the chunk in world coordinates
        global_x, global_y = self.transform_local_to_global_coordinates(local_x, local_y)
        if self.starting_rect.collidepoint(global_x, global_y):
            self.tiles.add(
                Tile(local_x,
                     local_y,
                     self.global_rect,
                     height = helper.noise.generate_height_values(global_x / 1000, global_y/ 1000),
                     moisture = helper.noise.generate_moisture_values(global_x/ 1000, global_y/ 1000)
                     )
                )
        else:
            raise ValueError("Tile trying to be added that doesn't belong in this chunk.")
        
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
        if settings.test.debug_mode:
            screen.blit(self.image, self.visible_rect)
        else:
            screen.blit(self.image, self.rect.move(settings.test.offset_x, settings.test.offset_y))
        
    def reload(self):
        self.tiles.draw(self.tile_image)
        self.image.blit(self.tile_image, (0, 0))  
        
    # Interaction
    def get_tile_at(self, x_global: int, y_global: int) -> Tile:
        mouse_rect = pygame.Rect(x_global, y_global, Tile.size, Tile.size)
        s = pygame.sprite.Sprite()
        s.rect = mouse_rect.move(-self.visible_rect.left, -self.visible_rect.top)

        return pygame.sprite.spritecollideany(s, self.tiles)
    
    # Coordinates
    def transform_global_to_local_coordinates(self, x_global: int, y_global: int) -> tuple[int, int]:
        x_local = x_global - self.starting_rect.left
        y_local = y_global - self.starting_rect.top
        return (x_local, y_local)
    
    def transform_local_to_global_coordinates(self, x_local: int, y_local: int) -> tuple[int, int]:
        x_global = x_local + self.starting_rect.left
        y_global = y_local + self.starting_rect.top
        return (x_global, y_global)
