import pygame
import pygame_menu

import settings.database
import settings.screen
from entities.animal import Animal
from entities.plant import Plant
import settings.simulation
from dna.dna import DNA
from world.tile import Tile

from world.world import World

class Simulation():
    """
    Class representing the simulation environment for an Evolution Simulation.

    Attributes:
        brush_outline (int): The width of the brush outline.
        base_theme (pygame_menu.Theme): The base theme for the menus.
        runtime_theme (pygame_menu.Theme): The theme for runtime elements.
        TRANSPARENT_BLACK_COLOR (tuple): The color code for transparent black.
        fps_font (pygame.font.Font): The font for displaying frames per second.

    Methods:
        __init__: Initializes the Simulation class.
        _setup_menus: Sets up the menus for the simulation.
        _setup_starting_menu: Sets up the starting menu.
        _setup_options_menu: Sets up the options menu.
        _setup_screen_options_menu: Sets up the screen options menu.
        _setup_database_options_menu: Sets up the database options menu.
        _setup_running_settings_menu: Sets up the running settings menu.
        _setup_world_settings_menu: Sets up the world settings menu.
        _setup_spawning_settings_menu: Sets up the spawning settings menu.
        _setup_dna_settings_menu: Sets up the DNA settings menu.
        _setup_entity_settings_menu: Sets up the entity settings menu.
        _setup_organism_settings_menu: Sets up the organism settings menu.
        _setup_animal_settings_menu: Sets up the animal settings menu.
        _setup_plant_settings_menu: Sets up the plant settings menu.
        toggle_pause: Toggles the pause state of the simulation.
        change_tile_size: Changes the tile size of the world.
        clear_organisms: Clears all organisms from the simulation.
        reset_stats: Resets the statistics of the simulation.
        toggle_alternating_moisture: Toggles the alternating moisture state.
        _update_gui: Updates the graphical user interface of the simulation.
        run_loop: Runs the main loop of the simulation.
        mainlopp: Main loop function for the simulation.
        _quit: Quits the simulation.

    Raises:
        No specific exceptions are raised.

    Returns:
        No specific return value.
    """
    brush_outline = 2
    #region themes
    base_theme = pygame_menu.pygame_menu.themes.THEME_GREEN.copy()
    runtime_theme = pygame_menu.Theme(
            background_color = base_theme.background_color,
            widget_margin = (0, 15),
        )
    menubar_theme = pygame_menu.Theme(
            background_color = base_theme.background_color,
            title = False
        )
    #endregion
    #region colors
    TRANSPARENT_BLACK_COLOR = (0, 0, 0, 100)
    FPS_FONT_COLOR = (0,0,0)
    #endregion
    #region fonts
    fps_font = pygame.font.Font(None, 100)
    #endregion
    fps_alpha: float = 100

    def __init__(self) -> None:
        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN])

        #region surface
        self._surface: pygame.Surface = pygame.display.set_mode(
                (settings.screen.SCREEN_WIDTH, settings.screen.SCREEN_HEIGHT),
                pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SRCALPHA
            )
        pygame.display.set_caption("Evolution Simulation")
        #endregion

        #region time
        self._clock = pygame.time.Clock()
        self._fps = 320
        #endregion

        #region simulation
        # Setting the world size
        world_rect: pygame.Rect = self._surface.get_rect()
        world_rect.width *= .75
        tile_size: int = world_rect.width // 100
        self.world: World = World(world_rect, tile_size)
        # Runtime variables
        self.selected_org = None
        self.paused = True
        self.alternating_moisture = False
        self.brush_rect: pygame.Rect = pygame.Rect(0 , 0, 20, 20)
        self.tool = self.info_tool
        #endregion

        self._setup_menus()

    #region setup
    def _setup_menus(self) -> None:
        """
        Initialising all the menus used by the simulation and setting up their elements.
        """
        #region menu initialisation
        # Regular menu
        self.starting_menu = pygame_menu.Menu("Starting Menu", self._surface.get_width(), self._surface.get_height(), theme=self.base_theme)
        self.options_menu = pygame_menu.Menu("Options", self._surface.get_width(), self._surface.get_height(), theme= self.base_theme)
        self.screen_options = pygame_menu.Menu("Screen Options", self._surface.get_width(), self._surface.get_height(), theme= self.base_theme)
        self.database_options = pygame_menu.Menu("Database Options", self._surface.get_width(), self._surface.get_height(), theme= self.base_theme)
        # Runtime Menu
        runtime_menu_width: float = self._surface.get_width()-self.world.rect.right
        runtime_menu_height: float = self._surface.get_height()
        runtime_menu_position = (self.world.rect.right, self.world.rect.top, False)

        menu_bar_height: float = 50
        self._running_menu_bar = pygame_menu.Menu(
            width=self.world.rect.width * .2,
            height=menu_bar_height,
            position=(self.world.rect.left, self.world.rect.top, False),
            theme=self.menubar_theme,
            title="menubar",
            keyboard_enabled=False,
            columns=8,
            rows=1
        )

        self._running_settings_menu = pygame_menu.Menu(
            width=runtime_menu_width,
            height=runtime_menu_height,
            position=runtime_menu_position,
            theme=self.runtime_theme,
            title="Simulation",
        )
        self._world_settings_menu = pygame_menu.Menu(
            width=runtime_menu_width,
            height=runtime_menu_height,
            position=runtime_menu_position,
            theme=self.runtime_theme,
            title="World",
        )
        self._spawning_settings_menu = pygame_menu.Menu(
            width=runtime_menu_width,
            height=runtime_menu_height,
            position=runtime_menu_position,
            theme=self.runtime_theme,
            title="Spawning",
        )
        self._dna_settings_menu = pygame_menu.Menu(
            width=runtime_menu_width,
            height=runtime_menu_height,
            position=runtime_menu_position,
            theme=self.runtime_theme,
            title="DNA",
        )
        self._entity_settings_menu = pygame_menu.Menu(
            width=runtime_menu_width,
            height=runtime_menu_height,
            position=runtime_menu_position,
            theme=self.runtime_theme,
            title="Entity",
        )
        self._organism_settings_menu = pygame_menu.Menu(
            width=runtime_menu_width,
            height=runtime_menu_height,
            position=runtime_menu_position,
            theme=self.runtime_theme,
            title="Organism",
        )
        self._animal_settings_menu = pygame_menu.Menu(
            width=runtime_menu_width,
            height=runtime_menu_height,
            position=runtime_menu_position,
            theme=self.runtime_theme,
            title="Animal",
        )
        self._plant_settings_menu = pygame_menu.Menu(
            width=runtime_menu_width,
            height=runtime_menu_height,
            position=runtime_menu_position,
            theme=self.runtime_theme,
            title="Plant",
        )
        #endregion

        #region menu setup
        self._setup_starting_menu()
        self._setup_options_menu()
        self._setup_screen_options_menu()
        self._setup_database_options_menu()
        self._setup_running_settings_menu()
        self._setup_running_menu_bar()
        self._setup_world_settings_menu()
        self._setup_spawning_settings_menu()
        self._setup_dna_settings_menu()
        self._setup_entity_settings_menu()
        self._setup_organism_settings_menu()
        self._setup_animal_settings_menu()
        self._setup_plant_settings_menu()
        #endregion

    #region main menus
    def _setup_starting_menu(self) -> None:
        self.starting_menu.add.button("Simulation", self.run_loop)
        self.starting_menu.add.button("Data Analysis") # TODO add fuction call to data analysis module
        self.starting_menu.add.button("Options", self.options_menu)
        self.starting_menu.add.button("Quit", quit)

    def _setup_options_menu(self) -> None:
        self.options_menu.add.button("Screen", self.screen_options)
        self.options_menu.add.button("Database", self.database_options)
        self.options_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_screen_options_menu(self) -> None:
        self.screen_options.add.toggle_switch("Fullscreen", False) # TODO implement fullscreen mode
        self.screen_options.add.dropselect(
            "Screen Resolution",
            [("1920, 1080", (1920, 1080)),
             ("1366, 768", (1366, 768)),
             ("1280, 1024", (1280, 1024)),
             ("1024, 768", (1024, 768)),
             ("4800, 1200", (4800, 1200)),
             ("1600, 1000", (1600, 1000))],
        ) # TODO implement resolution setting

        self.screen_options.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_database_options_menu(self) -> None:
        self.database_options.add.toggle_switch("Create database", settings.database.save_csv, onchange=settings.database.update_save_csv)
        self.database_options.add.toggle_switch("Save Animals to database", settings.database.save_animals_csv, onchange=settings.database.update_save_animals_csv)
        self.database_options.add.toggle_switch("Save Plants to database", settings.database.save_plants_csv, onchange=settings.database.update_save_plants_csv)
        self.database_options.add.button("Back", pygame_menu.pygame_menu.events.BACK)
    #endregion

    #region simulation menus
    def _setup_running_settings_menu(self) -> None:
        self._running_settings_menu.add.button("World", self._world_settings_menu)
        self._running_settings_menu.add.button("Spawning", self._spawning_settings_menu)
        self._running_settings_menu.add.button("Entities", self._entity_settings_menu)
        self._running_settings_menu.add.button("DNA", self._dna_settings_menu)

        self._running_settings_menu.add.toggle_switch("", (not self.paused), self.set_running, state_text=("Paused", "Running"), toggleswitch_id="GameState")
        self._running_settings_menu.add.button("Back", self.starting_menu.mainloop, self._surface)

    def _setup_running_menu_bar(self) -> None:
        self._running_menu_bar.add.button("i", self.choose_info_tool)
        self._running_menu_bar.add.button("A", self.choose_animal_spawning_tool)
        self._running_menu_bar.add.button("P", self.choose_plant_spawning_tool)
        self._running_menu_bar.add.button("KA", self.choose_animal_kill_tool)
        self._running_menu_bar.add.button("KP", self.choose_plant_kill_tool)

    def _setup_world_settings_menu(self) -> None:
        #TODO update these so changes to the sliders can be instantly seen on the world
        self._world_settings_menu.add.range_slider("Fx1", self.world.freq_x1, (0,10), increment=1, onchange=self.world.set_freq_x1)
        self._world_settings_menu.add.range_slider("Fy1", self.world.freq_y1, (0,10), increment=1, onchange=self.world.set_freq_y1)
        self._world_settings_menu.add.range_slider("Scale1", self.world.scale_1, (0,1), increment=.1, onchange=self.world.set_scale_1)
        self._world_settings_menu.add.range_slider("offsx1", self.world.offset_x1, (0,20), increment=1, onchange=self.world.set_offset_x1)
        self._world_settings_menu.add.range_slider("offsy1", self.world.offset_y1, (0,20), increment=1, onchange=self.world.set_offset_y1)
        self._world_settings_menu.add.range_slider("Fx2", self.world.freq_x2, (0,10), increment=1, onchange=self.world.set_freq_x2)
        self._world_settings_menu.add.range_slider("Fy2", self.world.freq_y2, (0,10), increment=1, onchange=self.world.set_freq_y2)
        self._world_settings_menu.add.range_slider("Scale2", self.world.scale_2, (0,1), increment=.1, onchange=self.world.set_scale_2)
        self._world_settings_menu.add.range_slider("offsx2", self.world.offset_x2, (0,20), increment=1, onchange=self.world.set_offset_x2)
        self._world_settings_menu.add.range_slider("offsy2", self.world.offset_y2, (0,20), increment=1, onchange=self.world.set_offset_y2)
        self._world_settings_menu.add.range_slider("Fx3", self.world.freq_x3, (0,10), increment=1, onchange=self.world.set_freq_x3)
        self._world_settings_menu.add.range_slider("Fy3", self.world.freq_y3, (0,10), increment=1, onchange=self.world.set_freq_y3)
        self._world_settings_menu.add.range_slider("Scale3", self.world.scale_3, (0,1), increment=.1, onchange=self.world.set_scale_3)
        self._world_settings_menu.add.range_slider("offsx3", self.world.offset_x3, (0,20), increment=1, onchange=self.world.set_offset_x3)
        self._world_settings_menu.add.range_slider("offsy3", self.world.offset_y3, (0,20), increment=1, onchange=self.world.set_offset_y3)
        self._world_settings_menu.add.range_slider("hpow", self.world.height_power, (1, 4), increment=1, onchange=self.world.set_height_power)
        self._world_settings_menu.add.range_slider("hfudge", self.world.height_fudge_factor, (.5, 1.5), increment=.1, onchange=self.world.set_fudge_factor)

        self._world_settings_menu.add.range_slider("hfx", self.world.height_freq_x, (-.01, .01), increment=.0001, onchange=self.world.set_height_freq_x)
        self._world_settings_menu.add.range_slider("hfy", self.world.height_freq_y, (-.01, .01), increment=.0001, onchange=self.world.set_height_freq_y)
        self._world_settings_menu.add.range_slider("mfx", self.world.moisture_freq_x, (-.01, .01), increment=.0001, onchange=self.world.set_moisture_freq_x)
        self._world_settings_menu.add.range_slider("mfy", self.world.moisture_freq_y, (-.01, .01), increment=.0001, onchange=self.world.set_moisture_freq_y)

        self._world_settings_menu.add.range_slider("moisture", self.world.moisture, (0, 1), increment=.01, onchange=self.world.set_moisture, rangeslider_id="moisture")
        self._world_settings_menu.add.toggle_switch("Enable moisture changing", self.alternating_moisture, onchange=self.set_alternating_moisture) # TODO add method to change moisture over time
        self._world_settings_menu.add.range_slider("height", self.world.height, (0, 1), increment=.01, onchange=self.world.set_height)

        # TODO add a randomise button
        self._world_settings_menu.add.button("Randomize", self.world.randomise_freqs) # TODO update this so when randomising a new world is loaded
        self._world_settings_menu.add.text_input("Tile size: ", self.world.tile_size, input_type=pygame_menu.pygame_menu.locals.INPUT_INT, onreturn=self.change_tile_size)

        self._world_settings_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_spawning_settings_menu(self) -> None:
        self._spawning_settings_menu.add.text_input("Num. Animals: ", 0, input_type=pygame_menu.pygame_menu.locals.INPUT_INT, onreturn=self.world.spawn_animals)
        self._spawning_settings_menu.add.text_input("Num. Plants: ", 0, input_type=pygame_menu.pygame_menu.locals.INPUT_INT, onreturn=self.world.spawn_plants)
        self._spawning_settings_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_dna_settings_menu(self) -> None:
        self._dna_settings_menu.add.label("Attack Power Mutation Range")
        self._dna_settings_menu.add.range_slider("", DNA.attack_power_mutation_range, (0, DNA.attack_power_max), increment=1, onchange=DNA.set_attack_power_mutation_range)
        self._dna_settings_menu.add.label("Color Mutation Range")
        self._dna_settings_menu.add.range_slider("", DNA.color_mutation_range, (0, DNA.color_max), increment=1, onchange=DNA.set_color_mutation_range)
        self._dna_settings_menu.add.label("Prefered Moisture Mutation Range")
        self._dna_settings_menu.add.range_slider("", DNA.prefered_moisture_muation_range, (0, DNA.prefered_moisture_max), increment=.01, onchange=DNA.set_prefered_moisture_mutation_range)
        self._dna_settings_menu.add.label("Prefered Height Mutation Range")
        self._dna_settings_menu.add.range_slider("", DNA.prefered_height_muation_range, (0, DNA.prefered_height_max), increment=.01, onchange=DNA.set_prefered_height_mutation_range)
        self._dna_settings_menu.add.label("Min Reproduction Health Mutation Range")
        self._dna_settings_menu.add.range_slider("", DNA.min_reproduction_health_mutation_range, (0, DNA.min_reproduction_health_max), increment=.01, onchange=DNA.set_min_reproduction_health_mutation_range)
        self._dna_settings_menu.add.label("Min Reproduction Energy Mutation Range")
        self._dna_settings_menu.add.range_slider("", DNA.min_reproduction_energy_mutation_range, (0, DNA.min_reproduction_energy_max), increment=.01, onchange=DNA.set_min_reproduction_energy_mutation_range)

        self._dna_settings_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_entity_settings_menu(self) -> None:
        self._entity_settings_menu.add.button("Organisms", self._organism_settings_menu)
        self._entity_settings_menu.add.button("Animals", self._animal_settings_menu)
        self._entity_settings_menu.add.button("Plants", self._plant_settings_menu)

        self._entity_settings_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_organism_settings_menu(self) -> None:

        self._organism_settings_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_animal_settings_menu(self) -> None:
        self._animal_settings_menu.add.label("Spawning Attack Power Range")
        self._animal_settings_menu.add.range_slider("", Animal._STARTING_ATTACK_POWER_RANGE, (0, DNA.attack_power_max), increment=1, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_starting_attack_power_range)
        self._animal_settings_menu.add.label("Spawning Moisture Preference Range")
        self._animal_settings_menu.add.range_slider("", Animal._STARTING_MOISTURE_PREFERENCE_RANGE, (0, 1), increment=.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_starting_moisture_preference_range)
        self._animal_settings_menu.add.label("Spawning Height Preference Range")
        self._animal_settings_menu.add.range_slider("", Animal._STARTING_HEIGHT_PREFERENCE_RANGE, (0, 1), increment=.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_starting_height_preference)
        self._animal_settings_menu.add.label("Spawning Mutation Chance Range")
        self._animal_settings_menu.add.range_slider("", Animal._STARTING_MUTATION_CHANCE_RANGE, (0, 1), increment=.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_starting_mutation_chance_range)
        self._animal_settings_menu.add.label("Spawning Min Health % to reproduce")
        self._animal_settings_menu.add.range_slider("", Animal._STARTING_MIN_REPRODUCTION_HEALTH_RANGE, (0, 1), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_starting_min_reproduction_health_range)
        self._animal_settings_menu.add.label("Spawning Min Energy % to reproduce")
        self._animal_settings_menu.add.range_slider("", Animal._STARTING_MIN_REPRODUCTION_ENERGY_RANGE, (0, 1), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_starting_min_reproduction_energy_range)

        self._animal_settings_menu.add.label("Energy Maintenance Cost")
        self._animal_settings_menu.add.range_slider("", Animal._BASE_ENERGY_MAINTENANCE, (0, 100), increment=1, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_base_energy_maintenance)
        self._animal_settings_menu.add.label("Max Health")
        self._animal_settings_menu.add.range_slider("", Animal._MAX_HEALTH, (1, 1000), increment=10, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_max_health)
        self._animal_settings_menu.add.label("Max Energy")
        self._animal_settings_menu.add.range_slider("", Animal._MAX_ENERGY, (1, 1000), increment=10, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_max_energy)
        self._animal_settings_menu.add.label("Nutriton Factor")
        self._animal_settings_menu.add.range_slider("", Animal._NUTRITION_FACTOR, (0, 1), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_nutrition_factor)
        self._animal_settings_menu.add.label("Reproduction Chance")
        self._animal_settings_menu.add.range_slider("", Animal._REPRODUCTION_CHANCE, (0, 1), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_reproduction_chance)

        self._animal_settings_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_plant_settings_menu(self) -> None:
        #self._plant_settings_menu.add.label("Spawning Attack Power Range")
        #self._plant_settings_menu.add.range_slider("", Plant._STARTING_ATTACK_POWER_RANGE, (0, 50), increment=1, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_starting_attack_power_range)
        self._plant_settings_menu.add.label("Spawning Moisture Preference Range")
        self._plant_settings_menu.add.range_slider("", Plant._STARTING_MOISTURE_PREFERENCE_RANGE, (0, 1), increment=.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_starting_moisture_preference_range)
        self._plant_settings_menu.add.label("Spawning Height Preference Range")
        self._plant_settings_menu.add.range_slider("", Plant._STARTING_HEIGHT_PREFERENCE_RANGE, (0, 1), increment=.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_starting_height_preference)
        self._plant_settings_menu.add.label("Spawning Mutation Chance Range")
        self._plant_settings_menu.add.range_slider("", Plant._STARTING_MUTATION_CHANCE_RANGE, (0, 1), increment=.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_starting_mutation_chance_range)
        self._plant_settings_menu.add.label("Spawning Min Health % to reproduce")
        self._plant_settings_menu.add.range_slider("", Plant._STARTING_MIN_REPRODUCTION_HEALTH_RANGE, (0, 1), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_starting_min_reproduction_health_range)
        self._plant_settings_menu.add.label("Spawning Min Energy % to reproduce")
        self._plant_settings_menu.add.range_slider("", Plant._STARTING_MIN_REPRODUCTION_ENERGY_RANGE, (0, 1), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_starting_min_reproduction_energy_range)

        self._plant_settings_menu.add.label("Energy Maintenance Cost")
        self._plant_settings_menu.add.range_slider("", Plant._BASE_ENERGY_MAINTENANCE, (0, 100), increment=1, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_base_energy_maintenance)
        self._plant_settings_menu.add.label("Max Health")
        self._plant_settings_menu.add.range_slider("", Plant._MAX_HEALTH, (1, 1000), increment=10, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_max_health)
        self._plant_settings_menu.add.label("Max Energy")
        self._plant_settings_menu.add.range_slider("", Plant._MAX_ENERGY, (1, 1000), increment=10, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_max_energy)
        self._plant_settings_menu.add.label("Nutriton Factor")
        self._plant_settings_menu.add.range_slider("", Plant._NUTRITION_FACTOR, (0, 1), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_nutrition_factor)
        self._plant_settings_menu.add.label("Reproduction Chance")
        self._plant_settings_menu.add.range_slider("", Plant._REPRODUCTION_CHANCE, (0, 1), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_reproduction_chance)

        self._plant_settings_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)
    #endregion
    #endregion

    #region callback functions
    def set_running(self, is_running) -> None:
        """
        Sets the running state of the simulation.

        Parameters:
            is_running (bool): The new running state of the simulation.

        Returns:
            None
        """
        self.paused = not is_running

    def change_tile_size(self, new_tile_size) -> None:
        """
        Change the tile size of the world in the simulation.

        Args:
            new_tile_size (int): The new size of the tiles in the world.

        Returns:
            None

        Raises:
            No specific exceptions are raised.
        """
        try:
            # TODO implement resizing of tile sizes
            pass
        except:
            # TODO implement feedback if value is not valid
            pass

    def clear_organisms(self) -> None:
        """
        Clears all organisms from the simulation.

        Raises:
            No specific exceptions are raised.

        Returns:
            None
        """
        settings.simulation.reset_organisms()

    def reset_stats(self) -> None:
        """
        Resets the statistics of the simulation.

        Parameters:
            None

        Returns:
            None
        """
        settings.simulation.reset_stats()

    def set_alternating_moisture(self, enabled) -> None:
        """
        Sets the state of alternating moisture in the simulation.

        Parameters:
            enabled (bool): A boolean value indicating whether alternating moisture is enabled or not.

        Returns:
            None
        """
        self.alternating_moisture = enabled

    #region tools
    def animal_spawning_tool(self):
        return self.world.spawn_animal

    def choose_animal_spawning_tool(self) -> None:
        self.tool = self.animal_spawning_tool()

    def plant_spawning_tool(self):
        return self.world.spawn_plant

    def choose_plant_spawning_tool(self) -> None:
        self.tool = self.plant_spawning_tool()

    def info_tool(self, tile: Tile) -> None:
        if tile.has_animal():
            self.selected_org = tile.animal.sprite
        elif tile.has_plant():
            self.selected_org = tile.plant.sprite
        else:
            self.selected_org = None

    def choose_info_tool(self) -> None:
        self.tool = self.info_tool

    def animal_kill_tool(self, tile: Tile) -> None:
        if tile.has_animal():
            tile.animal.sprite.kill()

    def choose_animal_kill_tool(self) -> None:
        self.tool = self.animal_kill_tool

    def plant_kill_tool(self, tile: Tile) -> None:
        if tile.has_plant():
            tile.plant.sprite.kill()

    def choose_plant_kill_tool(self) -> None:
        self.tool = self.plant_kill_tool

    #endregion
    #endregion

    #region loops
    def _update_gui(self, draw_menu=True, draw_grid=True, draw_fps = True, draw_world = True) -> None:
        """
        Updates the graphical user interface of the simulation.

        Parameters:
            draw_menu (bool): Whether to draw the menu on the GUI. Default is True.
            draw_grid (bool): Whether to draw the grid on the GUI. Default is True.
            draw_fps (bool): Whether to display the frames per second on the GUI. Default is True.

        Returns:
            None
        """
        if draw_world:
            self.world.draw(self._surface)

        if draw_grid:
            # TODO implement grid drawing
            pass

        if draw_menu and self._running_settings_menu.is_enabled():
            self._running_settings_menu.draw(self._surface)

        if draw_fps:
            fps_surface: pygame.Surface = self.fps_font.render(f"{int(self._clock.get_fps())}", True, self.FPS_FONT_COLOR)
            fps_surface.set_alpha(self.fps_alpha)
            self._surface.blit(
                fps_surface,
                fps_surface.get_rect(bottomleft = self._surface.get_rect().bottomleft)
            )

        self._running_menu_bar.draw(self._surface)

    def run_loop(self) -> None:
        # TODO add setting to disable drawing completely to improve speed
        # TODO improve fps displaying
        #drawing = False
        self.world.draw(self._surface)
        self._update_gui()

        simulating = True
        while simulating:
            # mouse_pos = pygame.mouse.get_pos()
            # self.brush_rect.center = mouse_pos

            events = pygame.event.get()

            menubar_updated = self._running_menu_bar.update(events)
            menu_updated = self._running_settings_menu.update(events)

            for event in events:
                if event.type == pygame.QUIT:
                    self._quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.toggle_pause()
                        menu_updated = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if not(self._running_menu_bar.get_rect().collidepoint(pos)):
                        tile = self.world.get_tile((pos[0], pos[1]))
                        if not tile:
                            self.selected_org = None
                        else:
                            self.tool(tile)
                    #drawing = True
                # if event.type == pygame.MOUSEBUTTONUP:
                #     drawing = False

            if not self.paused:
                self.world.update()
                # TODO reinplement the alternating moisture logic
                # if self.alternating_moisture:
                #     moist = self.world.moisture + math.cos(pygame.time.get_ticks()/100000)/10000
                #     self._world_settings_menu.get_widget("moisture").set_value(moist)
                #     self.world.set_moisture(moist)

            self._update_gui(draw_menu = menu_updated)

            # if self.world.rect.colliderect(self.brush_rect):
            #     # Draw cursor highlight
            #     pygame.draw.rect(
            #         self._surface,
            #         pygame.Color("white"),
            #         self.brush_rect,
            #         width=self.brush_outline
            #     )

            if self.selected_org:
                # TODO change this so there is a new stat panel that is locked in place
                self.selected_org.show_stats(self._surface, self.world.rect.topleft)

            pygame.display.flip()

            self._clock.tick(self._fps)

    def toggle_pause(self) -> None:
        self._running_settings_menu.get_widget("GameState").set_value(self.paused)
        self.paused = not self.paused

    def mainlopp(self) -> None:
        self.starting_menu.mainloop(self._surface)
    #endregion

    def _quit(self) -> None:
        pygame.quit()
        exit()
