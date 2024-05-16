import pygame
import pygame_menu

import settings.database
import settings.screen
import settings.gui

from world.world import World

class Simulation():
    base_theme = pygame_menu.pygame_menu.themes.THEME_GREEN.copy()

    def __init__(self) -> None:
        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.VIDEORESIZE])

        self._width = settings.screen.SCREEN_WIDTH
        self._height = settings.screen.SCREEN_HEIGHT
        self._surface: pygame.Surface = pygame.display.set_mode(
                (self._width, self._height),
                pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SRCALPHA
            )
        pygame.display.set_caption("Evolution Simulation")

        self._clock = pygame.time.Clock()
        self._fps = 320

        rect = self._surface.get_rect()
        rect.width *= .75
        world_rect: pygame.Rect = rect
        tile_size: int = world_rect.width // 120
        self.world: World = World(world_rect, tile_size)

        self._setup_menus()

    def _setup_menus(self) -> None:
        self.starting_menu = pygame_menu.Menu("Starting Menu", self._surface.get_width(), self._surface.get_height(), theme=self.base_theme)
        self.options_menu = pygame_menu.Menu("Options", self._surface.get_width(), self._surface.get_height(), theme= self.base_theme)
        self.database_options = pygame_menu.Menu("Database Options", self._surface.get_width(), self._surface.get_height(), theme= self.base_theme)

        self._setup_starting_menu()
        self._setup_options_menu()
        self._setup_database_options_menu()
        self._setup_generation_settings_menu()

    def _setup_starting_menu(self) -> None:
        self.starting_menu.add.button("Create a World", self.world_generation_loop)
        self.starting_menu.add.button("Options", self.options_menu)
        self.starting_menu.add.button("Quit", quit)

    def _setup_options_menu(self) -> None:
        self.options_menu.add.button("Database", self.database_options)
        self.options_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_database_options_menu(self) -> None:
        self.database_options.add.toggle_switch("Create database", settings.database.save_csv, onchange=settings.database.update_save_csv)
        self.database_options.add.toggle_switch("Save Animals to database", settings.database.save_animals_csv, onchange=settings.database.update_save_animals_csv)
        self.database_options.add.toggle_switch("Save Plants to database", settings.database.save_plants_csv, onchange=settings.database.update_save_plants_csv)
        self.database_options.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_generation_settings_menu(self) -> None:
        theme = pygame_menu.Theme(
            background_color = pygame_menu.pygame_menu.themes.TRANSPARENT_COLOR,
            title = False,
            widget_margin = (0, 15),
        )
        self._generation_settings_menu = pygame_menu.Menu(
            width=self._surface.get_width()-self.world.rect.right,
            height=self._height,
            position=(self.world.rect.right, 0, False),
            theme=theme,
            title="",
        )
        #self._generation_settings_menu.add.range_slider()
        self._generation_settings_menu.add.button("Generate World", self.generate_new_world)
        self.animal_spawning_chance = 0
        #self._generation_settings_menu.add.text_input("ASC: ", self.animal_spawning_chance, input_type=pygame_menu.pygame_menu.locals.INPUT_INT, onchange=self.update_animal_spawning_chance,)
        self._generation_settings_menu.add.range_slider("ASC", self.animal_spawning_chance, (0,1), increment=.01, onchange=self.update_animal_spawning_chance,)
        self.plant_spawning_chance = 0
        self._generation_settings_menu.add.range_slider("PSC", self.plant_spawning_chance, (0,1), increment=.01, onchange=self.update_plant_spawning_chance,)
        self._generation_settings_menu.add.button("Spawn animals", self.spawn_animals)
        self._generation_settings_menu.add.button("Spawn plants", self.spawn_plants)
        self._generation_settings_menu.add.button("Start simulation", self.run)
        self._generation_settings_menu.add.button("Back", self.starting_menu.mainloop, self._surface)

    def spawn_animals(self):
        self.world.spawn_animals(self.animal_spawning_chance)

    def spawn_plants(self):
        self.world.spawn_plants(self.plant_spawning_chance)

    def update_animal_spawning_chance(self, value):
        self.animal_spawning_chance = value

    def update_plant_spawning_chance(self, value):
        self.plant_spawning_chance = value

    def _update_gui(self, draw_menu=True, draw_grid=True, draw_fps = True) -> None:
        self._surface.fill(pygame_menu.pygame_menu.themes.THEME_GREEN.background_color)
        if draw_grid:
            # TODO implement grid drawing
            pass

        self.world.draw(self._surface)

        if draw_menu:
            self._generation_settings_menu.draw(self._surface)

        if draw_fps:
            fps_screen: pygame.Surface = settings.gui.title_font.render(f"{int(self._clock.get_fps())}", True, pygame.Color("black"))
            fps_screen.set_alpha(100)
            self._surface.blit(
                fps_screen,
                fps_screen.get_rect(topright = self._surface.get_rect().topright)
            )

    def world_generation_loop(self) -> None:
        while True:
            events = pygame.event.get()

            self._generation_settings_menu.update(events)

            for event in events:
                if event.type == pygame.QUIT:
                    self._quit()

            self._update_gui()
            pygame.display.flip()
            self._clock.tick(self._fps)

    def generate_new_world(self) -> None:
        # TODO add loading bar
        self.world = World(self.world.rect.copy(), self.world.tile_size)

    def run(self) -> None:
        paused = False
        while True:
            events = pygame.event.get()

            self._generation_settings_menu.update(events) # TODO change to runtime settings menu

            for event in events:
                if event.type == pygame.QUIT:
                    self._quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused

            if not paused:
                self.world.update()

            self.world.draw(self._surface)
            self._update_gui()
            pygame.display.flip()

            self._clock.tick(self._fps)

    def _quit(self) -> None:
        pygame.quit()
        exit()

    def mainlopp(self) -> None:
        self.starting_menu.mainloop(self._surface)
