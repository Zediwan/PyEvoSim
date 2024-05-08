import sys

import pygame
from gui.button import Button
from world.world import World
import settings.screen
import settings.simulation
import settings.colors
import settings.gui

def generate_world():
    pygame.display.set_caption("Generate World")
    SCREEN.fill(settings.colors.BACKGROUND_COLOR)

    TITLE_TEXT: pygame.Surface = settings.gui.title_font.render(
        "WORLD GENERATION",
        True,
        settings.colors.TEXT_COLOR,
        settings.colors.BACKGROUND_COLOR
    )
    TITLE_RECT: pygame.Rect = TITLE_TEXT.get_rect(
        bottom = SCREEN.get_rect().top + SCREEN.get_rect().centery*.25,
        centerx = (SCREEN.get_rect().centerx)
    )

    generate_world_button_x: int = 0
    generate_world_button_y: int = 0
    GENERATE_WORLD_BUTTON: Button = Button(
        (generate_world_button_x, generate_world_button_y),
        "GENERATE WORLD",
        settings.gui.button_font,
        settings.colors.BUTTON_TEXT_BASE_COLOR,
        settings.colors.BUTTON_TEXT_HOVER_COLOR,
        settings.colors.BACKGROUND_COLOR
    )
    GENERATE_WORLD_BUTTON.rect.bottomleft = SCREEN.get_rect().bottomleft
    GENERATE_WORLD_BUTTON.text_rect.bottomleft = SCREEN.get_rect().bottomleft

    start_button_x: int = 0
    start_button_y: int = 0
    START_BUTTON: Button = Button(
        (start_button_x, start_button_y),
        "START",
        settings.gui.button_font,
        settings.colors.BUTTON_TEXT_BASE_COLOR,
        settings.colors.BUTTON_TEXT_HOVER_COLOR,
        settings.colors.BACKGROUND_COLOR
    )
    START_BUTTON.rect.bottomright = SCREEN.get_rect().bottomright
    START_BUTTON.text_rect.bottomright = SCREEN.get_rect().bottomright

    world_rect: pygame.Rect = SCREEN.get_rect()
    world: World = World(world_rect, settings.screen.TILE_SIZE)

    while True:
        MOUSE_POSITION: tuple[int, int] = pygame.mouse.get_pos()

        if world:
            world.draw(SCREEN)

        SCREEN.blit(TITLE_TEXT, TITLE_RECT)

        for button in [GENERATE_WORLD_BUTTON, START_BUTTON]:
            button.change_color(MOUSE_POSITION)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if GENERATE_WORLD_BUTTON.check_for_input(MOUSE_POSITION):
                    world = World(world_rect, settings.screen.TILE_SIZE)
                elif START_BUTTON.check_for_input(MOUSE_POSITION):
                    simulate(world)
                else:
                    drawing = True
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            if event.type == pygame.MOUSEMOTION and drawing:
                MOUSE_POSITION: tuple[int, int] = pygame.mouse.get_pos()
                tile = world.get_tile(MOUSE_POSITION[0], MOUSE_POSITION[1])
                tile.height = 0
                tile.set_height_moisture_dependent_attributes()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    world.spawn_animals(chance_to_spawn=settings.simulation.chance_to_spawn_animals_with_enter_key)
                elif event.key == pygame.K_p:
                    world.spawn_plants(chance_to_spawn= .2)

        pygame.display.update()

def simulate(world: World):
    pygame.display.set_caption("Simulation")
    SCREEN.fill(settings.colors.SIMULATION_BACKGROUND_COLOR)
    running: bool = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if running:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    menu(world)

        if running:
            world.update()
            world.draw(SCREEN)

        pygame.display.update()

def menu(world: World = None):
    pygame.display.set_caption("Menu")
    SCREEN.fill(settings.colors.BACKGROUND_COLOR)

    TITLE_TEXT: pygame.Surface = settings.gui.title_font.render(
        settings.gui.menu_title_text,
        True,
        settings.colors.TEXT_COLOR
    )
    TITLE_RECT: pygame.Rect = TITLE_TEXT.get_rect(
        top = SCREEN.get_rect().top + SCREEN.get_rect().centery//10,
        centerx = (SCREEN.get_rect().centerx)
    )

    play_button_x: int = SCREEN.get_rect().centerx
    play_button_y: int = SCREEN.get_rect().centery - SCREEN.get_rect().height//20
    text = "PLAY"
    if world:
        text = "BACK"
    PLAY_BUTTON: Button = Button(
        (play_button_x, play_button_y),
        text,
        settings.gui.button_font,
        settings.colors.BUTTON_TEXT_BASE_COLOR,
        settings.colors.BUTTON_TEXT_HOVER_COLOR,
    )


    options_button_x: int = SCREEN.get_rect().centerx
    options_button_y: int = SCREEN.get_rect().centery + SCREEN.get_rect().height//20
    OPTIONS_BUTTON: Button = Button(
        (options_button_x, options_button_y),
        "OPTIONS",
        settings.gui.button_font,
        settings.colors.BUTTON_TEXT_BASE_COLOR,
        settings.colors.BUTTON_TEXT_HOVER_COLOR
    )

    quit_button_x: int = SCREEN.get_rect().centerx
    quit_button_y: int = SCREEN.get_rect().centery + SCREEN.get_rect().height//3
    QUIT_BUTTON: Button = Button(
        (quit_button_x, quit_button_y),
        "QUIT",
        settings.gui.button_font,
        settings.colors.BUTTON_TEXT_BASE_COLOR,
        settings.colors.BUTTON_TEXT_HOVER_COLOR
    )

    while True:
        SCREEN.blit(TITLE_TEXT, TITLE_RECT)
        MOUSE_POSITION: tuple[int, int] = pygame.mouse.get_pos()

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.change_color(MOUSE_POSITION)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_for_input(MOUSE_POSITION):
                    if world:
                        simulate(world)
                    else:
                        generate_world()
                if OPTIONS_BUTTON.check_for_input(MOUSE_POSITION):
                    options()
                if QUIT_BUTTON.check_for_input(MOUSE_POSITION):
                    exit()

        pygame.display.update()

def options():
    pygame.display.set_caption("Options")
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

    menu_button_x: int = SCREEN.get_rect().centerx
    menu_button_y: int = SCREEN.get_rect().centery + SCREEN.get_rect().height//3
    MENU_BUTTON: Button = Button(
        (menu_button_x, menu_button_y),
        "BACK",
        settings.gui.button_font,
        settings.colors.BUTTON_TEXT_BASE_COLOR,
        settings.colors.BUTTON_TEXT_HOVER_COLOR
    )


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

        for button in [MENU_BUTTON]:
            button.change_color(MOUSE_POSITION)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BUTTON.check_for_input(MOUSE_POSITION):
                    menu()

        pygame.display.update()

def exit():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.init()
    SCREEN: pygame.Surface = pygame.display.set_mode(
            (settings.screen.SCREEN_WIDTH, settings.screen.SCREEN_HEIGHT),
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )
    CLOCK: pygame.time.Clock = pygame.time.Clock()
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN])

    menu()

def placeholder_state():
    pygame.display.set_caption("Name")
    SCREEN.fill(settings.colors.BACKGROUND_COLOR)

    TITLE_TEXT: pygame.Surface = settings.gui.title_font.render(
        "Title text",
        True,
        settings.colors.TEXT_COLOR
    )
    TITLE_RECT: pygame.Rect = TITLE_TEXT.get_rect(
        top = SCREEN.get_rect().top + SCREEN.get_rect().centery//10,
        centerx = (SCREEN.get_rect().centerx)
    )

    while True:
        SCREEN.blit(TITLE_TEXT, TITLE_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        pygame.display.update()