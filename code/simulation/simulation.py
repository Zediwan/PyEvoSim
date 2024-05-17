import pygame
import pygame_menu

import settings.database
import settings.screen
import settings.gui
import settings.noise
import settings.entities

from world.world import World
from entities.animal import Animal

class Simulation():
    base_theme = pygame_menu.pygame_menu.themes.THEME_GREEN.copy()
    runtime_theme = pygame_menu.Theme(
            background_color = pygame_menu.pygame_menu.themes.TRANSPARENT_COLOR,
            title = False,
            widget_margin = (0, 15),
        )

    brush_outline = 2

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
        self.selected_org = None

        self._setup_menus()

    ##### SETUP ######################################################################
    def _setup_menus(self) -> None:
        self.starting_menu = pygame_menu.Menu("Starting Menu", self._surface.get_width(), self._surface.get_height(), theme=self.base_theme)
        self.options_menu = pygame_menu.Menu("Options", self._surface.get_width(), self._surface.get_height(), theme= self.base_theme)
        self.database_options = pygame_menu.Menu("Database Options", self._surface.get_width(), self._surface.get_height(), theme= self.base_theme)
        self._dna_settings_menu = pygame_menu.Menu(
            width=self._surface.get_width()-self.world.rect.right,
            height=self._height,
            position=(self.world.rect.right, 0, False),
            theme=self.runtime_theme,
            title="",
        )
        self._entity_settings_menu = pygame_menu.Menu(
            width=self._surface.get_width()-self.world.rect.right,
            height=self._height,
            position=(self.world.rect.right, 0, False),
            theme=self.runtime_theme,
            title="",
        )
        self._organism_settings_menu = pygame_menu.Menu(
            width=self._surface.get_width()-self.world.rect.right,
            height=self._height,
            position=(self.world.rect.right, 0, False),
            theme=self.runtime_theme,
            title="",
        )
        self._animal_settings_menu = pygame_menu.Menu(
            width=self._surface.get_width()-self.world.rect.right,
            height=self._height,
            position=(self.world.rect.right, 0, False),
            theme=self.runtime_theme,
            title="",
        )
        self._plant_settings_menu = pygame_menu.Menu(
            width=self._surface.get_width()-self.world.rect.right,
            height=self._height,
            position=(self.world.rect.right, 0, False),
            theme=self.runtime_theme,
            title="",
        )

        self._setup_starting_menu()
        self._setup_options_menu()
        self._setup_database_options_menu()
        self._setup_generation_settings_menu()
        self._setup_simulation_settings_menu()
        self._setup_dna_settings_menu()
        self._setup_entity_settings_menu()
        self._setup_organism_settings_menu()
        self._setup_animal_settings_menu()
        self._setup_plant_settings_menu()

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
        self._generation_settings_menu = pygame_menu.Menu(
            width=self._surface.get_width()-self.world.rect.right,
            height=self._height,
            position=(self.world.rect.right, 0, False),
            theme=self.runtime_theme,
            title="",
        )

        #TODO update these so changes to the sliders can be instantly seen on the world
        self._generation_settings_menu.add.range_slider("Fx1", settings.noise.freq_x1, (0,10), increment=1, onchange=settings.noise.set_freq_x1)
        self._generation_settings_menu.add.range_slider("Fy1", settings.noise.freq_y1, (0,10), increment=1, onchange=settings.noise.set_freq_y1)
        self._generation_settings_menu.add.range_slider("Scale1", settings.noise.scale_1, (0,1), increment=.1, onchange=settings.noise.set_scale_1)
        self._generation_settings_menu.add.range_slider("offsx1", settings.noise.offset_x1, (0,20), increment=1, onchange=settings.noise.set_offset_x1)
        self._generation_settings_menu.add.range_slider("offsy1", settings.noise.offset_y1, (0,20), increment=1, onchange=settings.noise.set_offset_y1)
        self._generation_settings_menu.add.range_slider("Fx2", settings.noise.freq_x2, (0,10), increment=1, onchange=settings.noise.set_freq_x2)
        self._generation_settings_menu.add.range_slider("Fy2", settings.noise.freq_y2, (0,10), increment=1, onchange=settings.noise.set_freq_y2)
        self._generation_settings_menu.add.range_slider("Scale2", settings.noise.scale_2, (0,1), increment=.1, onchange=settings.noise.set_scale_2)
        self._generation_settings_menu.add.range_slider("offsx2", settings.noise.offset_x2, (0,20), increment=1, onchange=settings.noise.set_offset_x2)
        self._generation_settings_menu.add.range_slider("offsy2", settings.noise.offset_y2, (0,20), increment=1, onchange=settings.noise.set_offset_y2)
        self._generation_settings_menu.add.range_slider("Fx3", settings.noise.freq_x3, (0,10), increment=1, onchange=settings.noise.set_freq_x3)
        self._generation_settings_menu.add.range_slider("Fy3", settings.noise.freq_y3, (0,10), increment=1, onchange=settings.noise.set_freq_y3)
        self._generation_settings_menu.add.range_slider("Scale3", settings.noise.scale_3, (0,1), increment=.1, onchange=settings.noise.set_scale_3)
        self._generation_settings_menu.add.range_slider("offsx3", settings.noise.offset_x3, (0,20), increment=1, onchange=settings.noise.set_offset_x3)
        self._generation_settings_menu.add.range_slider("offsy3", settings.noise.offset_y3, (0,20), increment=1, onchange=settings.noise.set_offset_y3)
        self._generation_settings_menu.add.range_slider("hpow", settings.noise.height_power, (1, 4), increment=1, onchange=settings.noise.set_height_power)
        self._generation_settings_menu.add.range_slider("hfudge", settings.noise.height_fudge_factor, (.5, 1.5), increment=.1, onchange=settings.noise.set_fudge_factor)

        self._generation_settings_menu.add.range_slider("hfx", settings.noise.height_freq_x, (-.01, .01), increment=.0001, onchange=settings.noise.set_height_freq_x)
        self._generation_settings_menu.add.range_slider("hfy", settings.noise.height_freq_y, (-.01, .01), increment=.0001, onchange=settings.noise.set_height_freq_y)
        self._generation_settings_menu.add.range_slider("mfx", settings.noise.moisture_freq_x, (-.01, .01), increment=.0001, onchange=settings.noise.set_moisture_freq_x)
        self._generation_settings_menu.add.range_slider("mfy", settings.noise.moisture_freq_y, (-.01, .01), increment=.0001, onchange=settings.noise.set_moisture_freq_y)

        self._generation_settings_menu.add.range_slider("moisture", settings.noise.moisture, (0, 1), increment=.01, onchange=settings.noise.set_moisture)
        self._generation_settings_menu.add.range_slider("height", settings.noise.height, (0, 1), increment=.01, onchange=settings.noise.set_height)

        # TODO add a randomise button
        self._generation_settings_menu.add.button("Generate World", self.generate_new_world)

        self.animal_spawning_chance = 0
        self._generation_settings_menu.add.range_slider("ASC", self.animal_spawning_chance, (0,1), increment=.01, onchange=self.update_animal_spawning_chance,)
        self.plant_spawning_chance = 0
        self._generation_settings_menu.add.range_slider("PSC", self.plant_spawning_chance, (0,1), increment=.01, onchange=self.update_plant_spawning_chance,)
        self._generation_settings_menu.add.button("Spawn animals", self.spawn_animals)
        self._generation_settings_menu.add.button("Spawn plants", self.spawn_plants)
        self._generation_settings_menu.add.button("Start simulation", self.run_loop)
        self._generation_settings_menu.add.button("Back", self.starting_menu.mainloop, self._surface)

        self.brush_rect: pygame.Rect = pygame.Rect(0 , 0, 20, 20)

    def _setup_simulation_settings_menu(self) -> None:
        self._simulation_settings_menu = pygame_menu.Menu(
            width=self._surface.get_width()-self.world.rect.right,
            height=self._height,
            position=(self.world.rect.right, 0, False),
            theme=self.runtime_theme,
            title="",
        )
        self._simulation_settings_menu.add.button("Entities", self._entity_settings_menu)
        self._simulation_settings_menu.add.button("DNA", self._dna_settings_menu)
        self._simulation_settings_menu.add.button("Back", self.world_generation_loop)

    def _setup_dna_settings_menu(self) -> None:
        self._dna_settings_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_entity_settings_menu(self) -> None:
        self._entity_settings_menu.add.button("Organisms", self._organism_settings_menu)
        self._entity_settings_menu.add.button("Animals", self._animal_settings_menu)
        self._entity_settings_menu.add.button("Plants", self._plant_settings_menu)
        self._entity_settings_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_organism_settings_menu(self) -> None:
        self._organism_settings_menu.add.range_slider("Value 1", 0, (0, 1), increment=1)
        self._organism_settings_menu.add.range_slider("Value 2", 0, (0, 1), increment=1)
        self._organism_settings_menu.add.range_slider("Value 3", 0, (0, 1), increment=1)
        self._organism_settings_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_animal_settings_menu(self) -> None:
        # self._animal_settings_menu.add.range_slider("Reproduction Chance", Animal.REPRODUCTION_CHANCE, (0, 1), increment=0.01, onchange=Animal.update_reproduction_chance)
        # self._animal_settings_menu.add.range_slider("Minimum Reproduction Health", Animal.MIN_REPRODUCTION_HEALTH, (0, 1), increment=0.01, onchange=Animal.update_min_reproduction_health)
        # self._animal_settings_menu.add.range_slider("Minimum Reproduction Energy", Animal.MIN_REPRODUCTION_ENERGY, (0, 1), increment=0.01, onchange=Animal.update_min_reproduction_energy)
        # self._animal_settings_menu.add.range_slider("Max Health", Animal.MAX_HEALTH, (50, 200), increment=5, onchange=Animal.update_max_health)
        # self._animal_settings_menu.add.range_slider("Max Energy", Animal.MAX_ENERGY, (100, 300), increment=10, onchange=Animal.update_max_energy)
        self._animal_settings_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_plant_settings_menu(self) -> None:
        self._plant_settings_menu.add.range_slider("Value 1", 0, (0, 1), increment=1)
        self._plant_settings_menu.add.range_slider("Value 2", 0, (0, 1), increment=1)
        self._plant_settings_menu.add.range_slider("Value 3", 0, (0, 1), increment=1)
        self._plant_settings_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    ###########################################################################

    def spawn_animals(self):
        self.world.spawn_animals(self.animal_spawning_chance)

    def spawn_plants(self):
        self.world.spawn_plants(self.plant_spawning_chance)

    def update_animal_spawning_chance(self, value):
        self.animal_spawning_chance = value

    def update_plant_spawning_chance(self, value):
        self.plant_spawning_chance = value

    ##### LOOPS ######################################################################
    def _update_gui(self, menu: pygame_menu.Menu = None, draw_menu=True, draw_grid=True, draw_fps = True) -> None:
        self._surface.fill(pygame_menu.pygame_menu.themes.THEME_GREEN.background_color)
        if draw_grid:
            # TODO implement grid drawing
            pass

        self.world.draw(self._surface)

        if draw_menu and menu is not None:
            menu.draw(self._surface)

        if draw_fps:
            fps_screen: pygame.Surface = settings.gui.title_font.render(f"{int(self._clock.get_fps())}", True, pygame.Color("black"))
            fps_screen.set_alpha(100)
            self._surface.blit(
                fps_screen,
                fps_screen.get_rect(topright = self._surface.get_rect().topright)
            )

    def world_generation_loop(self) -> None:
        drawing = False
        while True:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.brush_rect.center = mouse_pos

            self._generation_settings_menu.update(events)

            for event in events:
                if event.type == pygame.QUIT:
                    self._quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    drawing = True
                if event.type == pygame.MOUSEBUTTONUP:
                    drawing = False

            if drawing:
                intersecting_tiles = self.world.get_tiles(self.brush_rect)
                if intersecting_tiles:
                    for tile in intersecting_tiles:
                        change_in_height = 0.01
                        if tile.height >= change_in_height:
                            tile.height -= change_in_height
                    self.world.refresh_tiles()

            self._update_gui(self._generation_settings_menu)

            if self.world.rect.colliderect(self.brush_rect):
                # Draw cursor highlight
                pygame.draw.rect(
                    self._surface,
                    pygame.Color("white"),
                    self.brush_rect,
                    width=self.brush_outline
                )
            pygame.display.flip()
            self._clock.tick(self._fps)

    def generate_new_world(self) -> None:
        # TODO add loading bar
        self.world = World(self.world.rect.copy(), self.world.tile_size)

    def run_loop(self) -> None:
        paused = False
        while True:
            events = pygame.event.get()

            self._simulation_settings_menu.update(events) # TODO change to runtime settings menu

            for event in events:
                if event.type == pygame.QUIT:
                    self._quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                    elif event.key == pygame.K_ESCAPE:
                        self.world_generation_loop()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    tile = self.world.get_tile((pos[0], pos[1]))
                    if tile:
                        if tile.has_animal():
                            self.selected_org = tile.animal.sprite
                        elif tile.has_plant():
                            self.selected_org = tile.plant.sprite
                        else:
                            self.selected_org = None
                            if not tile.has_water:
                                self.world.spawn_animal(tile)
                    else:
                        self.selected_org = None

            if not paused:
                self.world.update()

            self.world.draw(self._surface)
            self._update_gui(self._simulation_settings_menu)
            if self.selected_org:
                # TODO change this so there is a new stat panel that is locked in place
                self.selected_org.show_stats(self._surface, self.world.rect.topleft)
            pygame.display.flip()

            self._clock.tick(self._fps)

    def mainlopp(self) -> None:
        self.starting_menu.mainloop(self._surface)

    def _quit(self) -> None:
        pygame.quit()
        exit()
