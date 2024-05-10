import sys
import pygame
import settings.screen
import settings.test
import settings.gui
from world.world import World

if __name__ == "__main__":
    pygame.init()
    SCREEN: pygame.Surface = pygame.display.set_mode(
            (settings.screen.SCREEN_WIDTH, settings.screen.SCREEN_HEIGHT),
            pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SRCALPHA | pygame.RESIZABLE
        )
    CLOCK: pygame.time.Clock = pygame.time.Clock()
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.VIDEORESIZE])
    pygame.display.set_caption("Evolution Simulation")

    SCREEN.fill(pygame.Color("white"))
    
    # Make the world half the screen
    world_rect = SCREEN.get_rect().scale_by(.5, .5)
    world = World(world_rect)
    
    moving_right: bool = False
    moving_left: bool = False
    moving_up: bool = False
    moving_down: bool = False
    settings.test.offset_x = 0
    settings.test.offset_y = 0
    
    while True:
        SCREEN.fill(pygame.Color(0,0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    moving_right = True
                if event.key == pygame.K_LEFT:
                    moving_left = True
                if event.key == pygame.K_UP:
                    moving_up = True
                if event.key == pygame.K_DOWN:
                    moving_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    moving_right = False
                if event.key == pygame.K_LEFT:
                    moving_left = False
                if event.key == pygame.K_UP:
                    moving_up = False
                if event.key == pygame.K_DOWN:
                    moving_down = False
        
        if moving_right:
            settings.test.offset_x += 1
        if moving_left:
            settings.test.offset_x -= 1
        if moving_up:
            settings.test.offset_y -= 1
        if moving_down:
            settings.test.offset_y += 1
        if moving_right or moving_left or moving_down or moving_up:
            world.load_active_chunks()
                    
        world.draw(SCREEN)
        
        fps_screen = settings.gui.title_font.render(f"{int(CLOCK.get_fps())}", True, pygame.Color("white"))
        fps_screen.set_alpha(100)
        SCREEN.blit(
            fps_screen,
            fps_screen.get_rect(topleft = (0,0))
        )
        
        CLOCK.tick()
        pygame.display.update()