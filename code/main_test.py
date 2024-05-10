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
    
    chunk_clicked = None

    moving_right: bool = False
    moving_left: bool = False
    moving_up: bool = False
    moving_down: bool = False
    settings.test.offset_x = 0
    settings.test.offset_y = 0
    
    world.draw(SCREEN)

    while True:
        SCREEN.fill(pygame.Color(0,0,0))
        world.draw(SCREEN)
        if chunk_clicked:
            pygame.draw.rect(
                SCREEN,
                pygame.Color("red"),
                chunk_clicked.global_rect,
                width=5
            )
        
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                chunk_clicked = world.get_chunk_at(pos[0], pos[1])

        if moving_right:
            settings.test.shift_x = 1
            settings.test.offset_x += settings.test.shift_x
        elif moving_left:
            settings.test.shift_x = -1
            settings.test.offset_x += settings.test.shift_x
        else:
            settings.test.shift_x = 0
        if moving_up:
            settings.test.shift_y = -1
            settings.test.offset_y += settings.test.shift_y
        elif moving_down:
            settings.test.shift_y = 1
            settings.test.offset_y += settings.test.shift_y
        else:
            settings.test.shift_y = 0
        if moving_right or moving_left or moving_down or moving_up:
            world.load_active_chunks()
        
        fps_screen = settings.gui.title_font.render(f"{int(CLOCK.get_fps())}", True, pygame.Color("white"))
        fps_screen.set_alpha(100)
        SCREEN.blit(
            fps_screen,
            fps_screen.get_rect(topleft = (0,0))
        )
        
        CLOCK.tick()
        pygame.display.update()