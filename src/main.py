import sys

import pygame
from simulation import Simulation
from gui.button import Button
import settings.screen
import settings.colors
import settings.gui

def starting_screen():
    pygame.display.set_caption("Starting Screen")
    pass

def simulate():
    pygame.display.set_caption("Evolution Simulation")
    simulation.run()

def menu():
    pygame.display.set_caption("Menu")
    SCREEN.fill(settings.colors.BACKGROUND_COLOR)

    MENU_TEXT: pygame.Surface = settings.gui.title_font.render(
        settings.gui.menu_title_text,
        True,
        settings.colors.TEXT_COLOR
    )
    MENU_TEXT_RECT: pygame.Rect = MENU_TEXT.get_rect(
        top = SCREEN.get_rect().top + SCREEN.get_rect().centery//10,
        centerx = (SCREEN.get_rect().centerx)
    )

    play_button_x: int = SCREEN.get_rect().centerx
    play_button_y: int = SCREEN.get_rect().centery - SCREEN.get_rect().height//20
    PLAY_BUTTON: Button = Button(
        (play_button_x, play_button_y),
        "PLAY",
        settings.gui.button_font,
        settings.colors.BUTTON_TEXT_BASE_COLOR,
        settings.colors.BUTTON_TEXT_HOVER_COLOR
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
        SCREEN.blit(MENU_TEXT, MENU_TEXT_RECT)
        MOUSE_POSITION: tuple[int, int] = pygame.mouse.get_pos()

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.change_color(MOUSE_POSITION)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_for_input(MOUSE_POSITION):
                    simulate()
                if OPTIONS_BUTTON.check_for_input(MOUSE_POSITION):
                    options()
                if QUIT_BUTTON.check_for_input(MOUSE_POSITION):
                    exit()

        pygame.display.update()

def options():
    pygame.display.set_caption("Options")
    SCREEN.fill(settings.colors.BACKGROUND_COLOR)

    OPTIONS_TEXT: pygame.Surface = settings.gui.title_font.render(
        settings.gui.options_title_text,
        True,
        settings.colors.TEXT_COLOR
    )
    OPTIONS_TEXT_RECT: pygame.Rect = OPTIONS_TEXT.get_rect(
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
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_TEXT_RECT)
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
    pygame.display.init()
    pygame.font.init()
    SCREEN: pygame.Surface = pygame.display.set_mode(
            (settings.screen.SCREEN_WIDTH, settings.screen.SCREEN_HEIGHT),
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )
    CLOCK: pygame.time.Clock = pygame.time.Clock()
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN])

    simulation = Simulation()
    menu()

    # while True:
    #     events = pygame.event.get()
    #     for event in events:
    #         if event.type == pygame.QUIT:
    #             exit()

    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             pass

    #     pygame.display.update()
    #     CLOCK.tick()
