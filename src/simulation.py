import sys

import pygame

import helper.formatter
import settings.colors
import settings.gui
import settings.screen
from entities.animal import Animal
from entities.organism import Organism
from entities.plant import Plant
from world.tile import Tile
from world.world import World


class Simulation:
    STARTING_FPS_LIMIT: int = 60

    def __init__(self, height: int = settings.screen.SCREEN_HEIGHT, width: int = settings.screen.SCREEN_WIDTH, tile_size: int = settings.screen.TILE_SIZE):
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.world: World = World(height, width, tile_size)

        # Game speed
        self.fps_max_limit: int = self.STARTING_FPS_LIMIT
        self.increase_game_speed: bool = False
        self.decrease_game_speed: bool = False

        self.selected_organism: Organism | None = None

        self.is_paused: bool = False
        self.simulating: bool = True
        self.in_menu: bool = False

        # Menu
        self.setup_menu()

        # Stats
        self.setup_stat_dict()

        # Stat Panels
        self.setup_stat_panels()
        self.setup_stat_surfaces_and_boxes()

    def setup_menu(self):
        self.menu_background: pygame.Surface = pygame.Surface(pygame.display.get_surface().get_size())
        self.menu_background.set_alpha(settings.colors.MENU_BACKGROUND_ALPHA)
        self.menu_background.fill(settings.colors.MENU_BACKGROUND_COLOR)
        self.menu_background_rect: pygame.Rect = pygame.display.get_surface().get_rect()
        self.menu_text: pygame.Surface = settings.gui.menu_font.render(
            settings.gui.menu_title_text,
            True,
            settings.colors.MENU_FONT_COLOR,
        )
        self.menu_text_rect: pygame.Rect = self.menu_text.get_rect(center=(pygame.display.get_surface().get_width() / 2, pygame.display.get_surface().get_height() / 2))

    def setup_stat_dict(self):
        self.stats = {
            "World runtime seconds": (self.world.age_seconds, "top"),
            "Ticks in World": (self.world.age_ticks, "top"),
            "FPS": (int(self.clock.get_fps()), "top"),
            "FPS Max Setting": (int(self.fps_max_limit), "top"),
            "Organisms birthed": (Organism.organisms_birthed, "bottom"),
            "Organisms died": (Organism.organisms_died, "bottom"),
            "Animals birthed": (Animal.animals_birthed, "bottom"),
            "Animals died": (Animal.animals_died, "bottom"),
            "Plants birthed": (Plant.plants_birthed, "bottom"),
            "Plants died": (Plant.plants_died, "bottom"),
        }

    def setup_stat_panels(self):
        self.panel_height: int = int(settings.gui.stat_panel_height_percentage * pygame.display.get_surface().get_height())
        self.panel_font_size: int = int(settings.gui.stat_panel_font_percentage * self.panel_height)
        self.panel_font: pygame.font.Font = pygame.font.SysFont(None, self.panel_font_size)

        self.panel_top_rect: pygame.Rect = pygame.Rect(0, 0, pygame.display.get_surface().get_width(), self.panel_height)
        self.panel_top: pygame.Surface = pygame.Surface(self.panel_top_rect.size)
        self.panel_top.fill(settings.colors.STAT_BAR_BACKGROUND_COLOR)

        self.panel_top_border_rect: pygame.Rect = self.panel_top_rect.move(0, settings.gui.stat_panel_line_width)
        self.panel_top_border: pygame.Surface = pygame.Surface(self.panel_top_border_rect.size)
        self.panel_top_border.fill(settings.colors.STAT_BAR_BORDER_COLOR)

        self.panel_bottom_rect: pygame.Rect = pygame.Rect(0, pygame.display.get_surface().get_height() - self.panel_height, pygame.display.get_surface().get_width(), self.panel_height)
        self.panel_bottom: pygame.Surface = pygame.Surface(self.panel_bottom_rect.size)
        self.panel_bottom.fill(settings.colors.STAT_BAR_BACKGROUND_COLOR)

        self.panel_bottom_border_rect: pygame.Rect = self.panel_bottom_rect.move(0, -settings.gui.stat_panel_line_width)
        self.panel_bottom_border: pygame.Surface = pygame.Surface(self.panel_bottom_border_rect.size)
        self.panel_bottom_border.fill(settings.colors.STAT_BAR_BORDER_COLOR)

    def setup_stat_surfaces_and_boxes(self):
        self.stat_surfaces = {}
        self.stat_rects = {}
        self.top_stats = {key: value for key, value in self.stats.items() if value[1] == 'top'}
        self.bottom_stats = {key: value for key, value in self.stats.items() if value[1] == 'bottom'}

        # Setup for top panel
        top_spacing = pygame.display.get_surface().get_width() / (len(self.top_stats) + 1)
        top_panel_y = self.panel_height / 2
        for index, (key, (value, _)) in enumerate(self.top_stats.items(), start=1):
            text_surface = self.panel_font.render(f"{key}: {value}", True, settings.colors.STAT_BAR_FONT_COLOR)
            text_rect = text_surface.get_rect(center=(top_spacing * index, top_panel_y))
            self.stat_surfaces[key] = text_surface
            self.stat_rects[key] = text_rect

        # Setup for bottom panel
        bottom_spacing = pygame.display.get_surface().get_width() / (len(self.bottom_stats) + 1)
        bottom_panel_y = pygame.display.get_surface().get_height() - self.panel_height / 2
        for index, (key, (value, _)) in enumerate(self.bottom_stats.items(), start=1):
            text_surface = self.panel_font.render(f"{key}: {value}", True, settings.colors.STAT_BAR_FONT_COLOR)
            text_rect = text_surface.get_rect(center=(bottom_spacing * index, bottom_panel_y))
            self.stat_surfaces[key] = text_surface
            self.stat_rects[key] = text_rect

    # TODO enable spawning of animals and plants via mouse
    # TODO enable stat displaying of animals and plants by klicking on them via mouse
    # TODO implement settings panel
    # TODO implement menu panel
    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.simulating:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.is_paused = not self.is_paused
                        elif event.key == pygame.K_RETURN:
                            self.world.spawn_animals(chance_to_spawn=settings.simulation.chance_to_spawn_animals_with_enter_key)
                        elif event.key == pygame.K_1 and pygame.key.get_mods() and pygame.KMOD_ALT:
                            settings.gui.draw_height_level = not settings.gui.draw_height_level
                            self.world.draw(pygame.display.get_surface())
                        elif event.key == pygame.K_2 and pygame.key.get_mods() and pygame.KMOD_ALT:
                            settings.gui.draw_animal_health = not settings.gui.draw_animal_health
                            self.world.draw(pygame.display.get_surface())
                        elif event.key == pygame.K_3 and pygame.key.get_mods() and pygame.KMOD_ALT:
                            settings.gui.draw_animal_energy = not settings.gui.draw_animal_energy
                            self.world.draw(pygame.display.get_surface())
                        elif (event.key == pygame.K_r and pygame.key.get_mods() and pygame.KMOD_SHIFT):
                            self.world = World(self.world.height, self.world.width, self.world.tile_size)
                            self.selected_organism = None
                            self.world.draw(pygame.display.get_surface())
                        elif (event.key == pygame.K_UP and pygame.key.get_mods() and pygame.KMOD_SHIFT):
                            self.increase_game_speed = True
                            self.decrease_game_speed = False
                        elif (event.key == pygame.K_DOWN and pygame.key.get_mods() and pygame.KMOD_SHIFT):
                            self.increase_game_speed = False
                            self.decrease_game_speed = True
                        if event.key == pygame.K_ESCAPE:
                            self.in_menu = True
                            self.was_paused = self.is_paused
                            self.is_paused = True
                            self.simulating = False
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP and pygame.key.get_mods() and pygame.KMOD_SHIFT:
                            self.increase_game_speed = False
                        elif (
                            event.key == pygame.K_DOWN
                            and pygame.key.get_mods()
                            and pygame.KMOD_SHIFT
                        ):
                            self.decrease_game_speed = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        tile: Tile = self.world.get_tile(mouse_x, mouse_y)

                        self.world.draw(pygame.display.get_surface())
                        self.handle_stat_panels()

                        if tile.has_animal():
                            self.selected_organism = tile.animal.sprite
                            self.selected_organism.show_stats(pygame.display.get_surface())
                        elif tile.has_plant():
                            self.selected_organism = tile.plant.sprite
                            self.selected_organism.show_stats(pygame.display.get_surface())
                        else:
                            if self.selected_organism:
                                self.selected_organism.stat_panel = None
                                self.selected_organism = None
                elif self.in_menu:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.is_paused = self.was_paused
                            self.simulating = True
                            self.in_menu = False
                else:
                    pass

            if self.simulating:
                pygame.display.get_surface().fill(settings.colors.SIMULATION_BACKGROUND_COLOR)
                if not self.is_paused:
                    self.world.update()
                    self.display_selected_organisms_stats()
                self.world.draw(pygame.display.get_surface())
                self.handle_stat_panels()
                self.handle_game_speed()
            elif self.in_menu:
                pygame.display.get_surface().fill(settings.colors.SIMULATION_BACKGROUND_COLOR)
                self.world.draw(pygame.display.get_surface())
                self.handle_stat_panels()
                self.draw_menu()
            else:
                pygame.display.get_surface().fill(pygame.Color("red"))

            pygame.display.update()
            self.clock.tick(self.fps_max_limit)

    def draw_menu(self):
            pygame.display.get_surface().blit(self.menu_background, self.menu_background_rect)
            pygame.display.get_surface().blit(self.menu_text, self.menu_text_rect)

    def display_selected_organisms_stats(self):
        if self.selected_organism:
            if (
                self.selected_organism.is_alive()
                or settings.gui.show_dead_organisms_stats
            ):
                self.selected_organism.show_stats(pygame.display.get_surface())
            else:
                self.selected_organism.stat_panel = None
                self.selected_organism = None

    def handle_game_speed(self):
        if (
            self.increase_game_speed
            and self.fps_max_limit + settings.simulation.GAME_SPEED_CHANGE
            <= settings.simulation.MAX_FPS_LIMIT
        ):
            self.fps_max_limit += settings.simulation.GAME_SPEED_CHANGE
        elif (
            self.decrease_game_speed
            and self.fps_max_limit > settings.simulation.GAME_SPEED_CHANGE
        ):
            self.fps_max_limit -= settings.simulation.GAME_SPEED_CHANGE

    def handle_stat_panels(self):
        self.update_stats()
        self.upper_stat_panel()
        self.lower_stat_panel()
        self.draw_stats()

    def update_stats(self):
        self.stats["World runtime seconds"] = (self.world.age_seconds, "top")
        self.stats["Ticks in World"] = (self.world.age_ticks, "top")
        self.stats["FPS"] = (int(self.clock.get_fps()), "top")
        self.stats["FPS Max Setting"] = (int(self.fps_max_limit), "top")
        self.stats["Organisms birthed"] = (Organism.organisms_birthed, "bottom")
        self.stats["Organisms died"] = (Organism.organisms_died, "bottom")
        self.stats["Animals birthed"] =  (Animal.animals_birthed, "bottom")
        self.stats["Animals died"] = (Animal.animals_died, "bottom")
        self.stats["Plants birthed"] =  (Plant.plants_birthed, "bottom")
        self.stats["Plants died"] = (Plant.plants_died, "bottom")

        # Update the text surfaces
        for key, (value, _) in self.stats.items():
            updated_text = f"{key}: {helper.formatter.format_number(value)}"
            self.stat_surfaces[key] = self.panel_font.render(updated_text, True, settings.colors.STAT_BAR_FONT_COLOR)

    def upper_stat_panel(self):
        # Drawing base panel for upper stats
        pygame.display.get_surface().blit(self.panel_top_border, self.panel_top_border_rect)
        pygame.display.get_surface().blit(self.panel_top, self.panel_top_rect)

    def lower_stat_panel(self):
        # Drawing base panel for lower stats
        pygame.display.get_surface().blit(self.panel_bottom_border, self.panel_bottom_border_rect)
        pygame.display.get_surface().blit(self.panel_bottom, self.panel_bottom_rect)

    def draw_stats(self):
        for key in self.stats:
            pygame.display.get_surface().blit(self.stat_surfaces[key], self.stat_rects[key])
