import sys

import pygame
import pygame_menu
from gui.button import Button
from world.world import World
import settings.screen
import settings.simulation
import settings.colors
import settings.gui
import settings.font
import settings.database
from simulation import Simulation

# def generate_world():
#     world_rect: pygame.Rect = SCREEN.get_rect().scale_by(.8, .8)
#     tile_size: int = world_rect.width // 120

#     world: World = None
#     drawing = False

#     brush_size = 20
#     brush_outline = 2
#     brush_rect: pygame.Rect = pygame.Rect(0 , 0, brush_size, brush_size)

#     while True:
#         MOUSE_POSITION: tuple[int, int] = pygame.mouse.get_pos()
#         brush_rect.center = (MOUSE_POSITION[0], MOUSE_POSITION[1])

#         if world:
#             world.draw(SCREEN)

#             if world_rect.contains(brush_rect):
#                 # Draw cursor highlight
#                 pygame.draw.rect(
#                     SCREEN,
#                     pygame.Color("white"),
#                     brush_rect,
#                     width=brush_outline
#                 )
#             if drawing:
#                 intersecting_tiles = world.get_tiles(brush_rect)
#                 if intersecting_tiles:
#                     for tile in intersecting_tiles:
#                         change_in_height = 0.01
#                         if tile.height >= change_in_height:
#                             tile.height -= change_in_height
#                     world.refresh_tiles()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 drawing = True
#             if event.type == pygame.MOUSEBUTTONUP:
#                 drawing = False
#             if event.type == pygame.VIDEORESIZE:
#                 generate_world()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     pygame_menu.pygame_menu.Menu._open(world_generation_menu)
#             if world:
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_a:
#                         world.spawn_animals(chance_to_spawn=.01)
#                     elif event.key == pygame.K_p:
#                         world.spawn_plants(chance_to_spawn= .1)

#         pygame.display.update()

def simulate(world: World):
    SCREEN.fill(settings.colors.SIMULATION_BACKGROUND_COLOR)
    running: bool = True
    selected_org = None

    while True:
        SCREEN.fill(settings.colors.BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    simulation_options(world)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                tile = world.get_tile((pos[0], pos[1]))
                if tile:
                    if tile.has_animal():
                        selected_org = tile.animal.sprite
                    elif tile.has_plant():
                        selected_org = tile.plant.sprite
                    else:
                        selected_org = None
                        if not tile.has_water:
                            world.spawn_animal(tile)
                else:
                    selected_org = None
            if event.type == pygame.VIDEORESIZE:
                world.resize(SCREEN.get_rect().scale_by(.8, .8))
            if running:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = True

        if running:
            world.update()

        world.draw(SCREEN)

        if selected_org:
            selected_org.show_stats(SCREEN, world.rect.topleft)

        fps_screen = settings.gui.title_font.render(f"{int(CLOCK.get_fps())}", True, pygame.Color("black"))
        fps_screen.set_alpha(100)
        SCREEN.blit(
            fps_screen,
            fps_screen.get_rect(topleft = (0,0))
        )

        CLOCK.tick()
        pygame.display.update()

def simulation_options(world: World):
    SCREEN.fill(settings.colors.BACKGROUND_COLOR)

    TITLE_TEXT: pygame.Surface = settings.gui.title_font.render(
        settings.gui.options_title_text,
        True,
        settings.colors.TEXT_COLOR
    )
    TITLE_RECT: pygame.Rect = TITLE_TEXT.get_rect(
        top = SCREEN.get_rect().top + SCREEN.get_rect().centery//10,
        centerx = (SCREEN.get_rect().centerx)
    )

    BACK_BUTTON: Button = Button(
        (SCREEN.get_rect().centerx, SCREEN.get_rect().centery + SCREEN.get_rect().height//3),
        "BACK",
        settings.gui.button_font,
        settings.colors.BUTTON_TEXT_BASE_COLOR,
        settings.colors.BUTTON_TEXT_HOVER_COLOR
    )

    MENU_BUTTON: Button = Button(
        SCREEN.get_rect().center,
        "MENU",
        settings.gui.button_font,
        settings.colors.BUTTON_TEXT_BASE_COLOR,
        settings.colors.BUTTON_TEXT_HOVER_COLOR
    )
    MENU_BUTTON.rect.bottom = SCREEN.get_rect().bottom
    MENU_BUTTON.text_rect.bottom = SCREEN.get_rect().bottom

    OPTIONS_PLACEHOLDER_RECT: pygame.Rect = pygame.Rect(
        SCREEN.get_rect().centerx // 2,
        SCREEN.get_rect().centery // 2,
        SCREEN.get_rect().centerx,
        SCREEN.get_rect().centery
    )
    OPTIONS_PLACEHOLDER: pygame.Surface = pygame.Surface(OPTIONS_PLACEHOLDER_RECT.size)
    OPTIONS_PLACEHOLDER.fill(pygame.Color(40, 40, 40))

    while True:
        SCREEN.blit(TITLE_TEXT, TITLE_RECT)
        SCREEN.blit(OPTIONS_PLACEHOLDER, OPTIONS_PLACEHOLDER_RECT)
        MOUSE_POSITION: tuple[int, int] = pygame.mouse.get_pos()

        for button in [BACK_BUTTON, MENU_BUTTON]:
            button.change_color(MOUSE_POSITION)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.check_for_input(MOUSE_POSITION):
                    simulate(world)
                if MENU_BUTTON.check_for_input(MOUSE_POSITION):
                    starting_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    simulate(world)

        pygame.display.update()

def exit():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    Simulation().mainlopp()