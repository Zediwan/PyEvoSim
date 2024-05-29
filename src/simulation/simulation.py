import pygame
import pygame_menu
from abc import ABC, abstractmethod

from .settings import database
from .settings import screen
from .settings import simulation

from .entities.animal import Animal
from .entities.plant import Plant
from .entities.properties.dna import DNA
from .entities.properties.gene import ColorComponentGene, PercentageGene, Gene

from .terrain.tile import Tile
from .terrain.world import World

class ISimulation(ABC):    
    def __init__(self) -> None:
        super().__init__()
        self.drawing = False
        self.running = False

    @abstractmethod
    def update(self) -> None:
        pass
    
    @abstractmethod
    def draw(self, screen) -> None:
        pass
    
    @abstractmethod
    def run(self) -> None: 
        self.running = True
        pass

    def pause(self) -> None:
        self.running = False
    
    @abstractmethod
    def quit(self) -> None:
        pass
    
class IPygameSimulation(ISimulation):
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface(self.rect.size)
        self.clock = pygame.time.Clock()
        self.fps_limit: int
        self.background_color: pygame.Color
        
        self.world: pygame.sprite.GroupSingle
        
        self.drawing = False
        self.running = False
    
    def update(self) -> None:
        super().update()
        self.world.update()
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw()
        self.world.draw(self.surface)

        screen.blit(self.surface, self.rect)
    
    def run(self) -> None:
        super().run()
        while self.running:
            self.update()
        
            if self.drawing:
                self.surface.fill(self.background_color)
                self.world.draw(self.surface)
                
            self.clock.tick(self.fps_limit)
                
    def quit(self) -> None:
        super().quit()
        pygame.quit()
        exit()

class Simulation():
    """
    Class representing a simulation environment for an evolution simulation.

    Attributes:
        brush_outline (int): The width of the brush outline.
        base_theme (pygame_menu.Theme): The base theme for the menus.
        runtime_theme (pygame_menu.Theme): The theme for the runtime menu.
        menubar_theme (pygame_menu.Theme): The theme for the menu bar.
        TRANSPARENT_BLACK_COLOR (tuple): The color code for transparent black.
        FPS_FONT_COLOR (tuple): The color code for the FPS font.
        fps_font (pygame.font.Font): The font for displaying FPS.
        fps_alpha (float): The alpha value for FPS display.
        world (World): The world object for the simulation.
        selected_org (Organism): The currently selected organism.
        paused (bool): Flag indicating if the simulation is paused.
        alternating_moisture (bool): Flag indicating if moisture is alternating.
        brush_rect (pygame.Rect): The rectangle representing the brush.
        tool (function): The current tool function for interaction.

    Methods:
        __init__: Initializes the simulation environment.
        _setup_menus: Sets up all the menus used in the simulation.
        _update_gui: Updates the graphical user interface of the simulation.
        run_loop: Runs the main loop of the simulation.
        toggle_pause: Toggles the pause state of the simulation.
        mainloop: Runs the starting menu loop.
        _quit: Quits the simulation.

    Callbacks:
        set_running: Sets the running state of the simulation.
        clear_organisms: Clears all organisms from the simulation.
        reset_stats: Resets the statistics of the simulation.
        animal_spawning_tool: Tool for spawning animals.
        choose_animal_spawning_tool: Chooses the animal spawning tool.
        plant_spawning_tool: Tool for spawning plants.
        choose_plant_spawning_tool: Chooses the plant spawning tool.
        info_tool: Tool for displaying information about tiles.
        choose_info_tool: Chooses the info tool.
        animal_kill_tool: Tool for killing animals.
        choose_animal_kill_tool: Chooses the animal kill tool.
        plant_kill_tool: Tool for killing plants.
        choose_plant_kill_tool: Chooses the plant kill tool.
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
        """
        Initializes the Simulation environment.

        Parameters:
            None

        Returns:
            None
        """
        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN])

        #region surface
        self._surface: pygame.Surface = pygame.display.set_mode(
                (screen.SCREEN_WIDTH, screen.SCREEN_HEIGHT),
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
        world_rect.width *= .6
        tile_size: int = world_rect.width // 100
        self.world: World = World(world_rect, tile_size)
        # Runtime variables
        self.selected_org = None
        self.paused = True
        self.draw_world = True
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
            width=self.world.rect.width * .5,
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
        self._function_settings_menu = pygame_menu.Menu(
            width=runtime_menu_width,
            height=runtime_menu_height,
            position=runtime_menu_position,
            theme=self.runtime_theme,
            title="Functions",
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
        self._setup_function_settings_menu()
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
        self.database_options.add.toggle_switch("Create database", database.save_csv, onchange=database.update_save_csv)
        self.database_options.add.toggle_switch("Save Animals to database", database.save_animals_csv, onchange=database.update_save_animals_csv)
        self.database_options.add.toggle_switch("Save Plants to database", database.save_plants_csv, onchange=database.update_save_plants_csv)
        self.database_options.add.button("Back", pygame_menu.pygame_menu.events.BACK)
    #endregion

    #region simulation menus
    def _setup_running_settings_menu(self) -> None:
        self._running_settings_menu.add.button("World", self._world_settings_menu)
        self._running_settings_menu.add.button("Spawning", self._spawning_settings_menu)
        self._running_settings_menu.add.button("Entities", self._entity_settings_menu)
        self._running_settings_menu.add.button("DNA", self._dna_settings_menu)

        self._running_settings_menu.add.toggle_switch("", (not self.paused), self.set_running, state_text=("Paused", "Running"), toggleswitch_id="GameState")
        self._running_settings_menu.add.toggle_switch("Draw World", self.draw_world, self.set_draw_world)
        self._running_settings_menu.add.button("Back", self.starting_menu.mainloop, self._surface)

    def _setup_running_menu_bar(self) -> None:
        self._running_menu_bar.add.button("i", self.choose_info_tool)
        self._running_menu_bar.add.button("A", self.choose_animal_spawning_tool)
        self._running_menu_bar.add.button("P", self.choose_plant_spawning_tool)
        self._running_menu_bar.add.button("KA", self.choose_animal_kill_tool)
        self._running_menu_bar.add.button("KP", self.choose_plant_kill_tool)

    def _setup_world_settings_menu(self) -> None:
        # self._world_settings_menu.add.toggle_switch("Enable moisture changing", self.alternating_moisture, onchange=self.set_alternating_moisture) # TODO add method to change moisture over time
        self._world_settings_menu.add.button("Functions", self._function_settings_menu)
        self.world.height_setting.add_controller_to_menu(self._world_settings_menu, randomiser=True)
        self.world.moisture_setting.add_controller_to_menu(self._world_settings_menu, randomiser=True)
        self.world.scale_setting.add_controller_to_menu(self._world_settings_menu)
        self._world_settings_menu.add.button("Randomise Everything", self.world.randomise_freqs)

        self._world_settings_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_function_settings_menu(self) -> None:
        self._function_settings_menu.add.label("------Height------")
        for function in self.world.height_functions:
            function.add_submenu(self._function_settings_menu, add_randomiser=True)
        self._function_settings_menu.add.label("------Moisture------")
        for function in self.world.moisture_functions:
            function.add_submenu(self._function_settings_menu, add_randomiser=True)

        self._function_settings_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_spawning_settings_menu(self) -> None:
        self._spawning_settings_menu.add.text_input("Num. Animals: ", 0, input_type=pygame_menu.pygame_menu.locals.INPUT_INT, onreturn=self.world.spawn_animals)
        self._spawning_settings_menu.add.text_input("Num. Plants: ", 0, input_type=pygame_menu.pygame_menu.locals.INPUT_INT, onreturn=self.world.spawn_plants)
        self._spawning_settings_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_dna_settings_menu(self) -> None:
        self._dna_settings_menu.add.dropselect("Mutation distribution type", [("Gauss", "gauss"), ("Uniform", "uniform")], 0, onreturn=Gene.set_mutation_type)
        self._dna_settings_menu.add.label("Attack Power Mutation Range")
        self._dna_settings_menu.add.range_slider("", DNA.attack_power_mutation_range, (0, DNA.attack_power_max), increment=1, onchange=DNA.set_attack_power_mutation_range)
        self._dna_settings_menu.add.label("Defense Mutation Range")
        self._dna_settings_menu.add.range_slider("", DNA.defense_muation_range, (0, DNA.defense_max), increment=1, onchange=DNA.set_defense_mutation_range)
        self._dna_settings_menu.add.label("Color Mutation Range")
        self._dna_settings_menu.add.range_slider("", DNA.color_mutation_range, (0, ColorComponentGene.MAX), increment=1, onchange=DNA.set_color_mutation_range)
        self._dna_settings_menu.add.label("Prefered Moisture Mutation Range")
        self._dna_settings_menu.add.range_slider("", DNA.prefered_moisture_muation_range, (0, DNA.prefered_moisture_max), increment=.01, onchange=DNA.set_prefered_moisture_mutation_range)
        self._dna_settings_menu.add.label("Prefered Height Mutation Range")
        self._dna_settings_menu.add.range_slider("", DNA.prefered_height_muation_range, (0, DNA.prefered_height_max), increment=.01, onchange=DNA.set_prefered_height_mutation_range)
        self._dna_settings_menu.add.label("Min Reproduction Health Mutation Range")
        self._dna_settings_menu.add.range_slider("", DNA.min_reproduction_health_mutation_range, (0, DNA.min_reproduction_health_max), increment=.01, onchange=DNA.set_min_reproduction_health_mutation_range)
        self._dna_settings_menu.add.label("Min Reproduction Energy Mutation Range")
        self._dna_settings_menu.add.range_slider("", DNA.min_reproduction_energy_mutation_range, (0, DNA.min_reproduction_energy_max), increment=.01, onchange=DNA.set_min_reproduction_energy_mutation_range)
        self._dna_settings_menu.add.label("Reproduction Chance Mutation Range")
        self._dna_settings_menu.add.range_slider("", DNA.reproduction_chance_mutation_range, (0, DNA.reproduction_chance_max), increment=.01, onchange=DNA.set_reproduction_chance_mutation_range)
        self._dna_settings_menu.add.label("Energy to offspring ratio Mutation Range")
        self._dna_settings_menu.add.range_slider("", DNA.energy_to_offspring_mutation_range, (0, DNA.energy_to_offspring_max), increment=.01, onchange=DNA.set_energy_to_offspring_mutation_range)

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
        self._animal_settings_menu.add.range_slider("", Animal._STARTING_ATTACK_POWER_RANGE, (DNA.attack_power_min, DNA.attack_power_max), increment=1, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_starting_attack_power_range)
        self._animal_settings_menu.add.label("Spawning Defense Range")
        self._animal_settings_menu.add.range_slider("", Animal._STARTING_DEFENSE_RANGE, (DNA.defense_min, DNA.defense_max), increment=1, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_starting_defense_range)
        self._animal_settings_menu.add.label("Spawning Moisture Preference Range")
        self._animal_settings_menu.add.range_slider("", Animal._STARTING_MOISTURE_PREFERENCE_RANGE, (DNA.prefered_moisture_min, DNA.prefered_moisture_max), increment=.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_starting_moisture_preference_range)
        self._animal_settings_menu.add.label("Spawning Height Preference Range")
        self._animal_settings_menu.add.range_slider("", Animal._STARTING_HEIGHT_PREFERENCE_RANGE, (DNA.prefered_height_min, DNA.prefered_height_max), increment=.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_starting_height_preference)
        self._animal_settings_menu.add.label("Spawning Mutation Chance Range")
        self._animal_settings_menu.add.range_slider("", Animal._STARTING_MUTATION_CHANCE_RANGE, (DNA.mutation_chance_min, DNA.mutation_chance_max), increment=.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_starting_mutation_chance_range)
        self._animal_settings_menu.add.label("Spawning Min Health % to reproduce")
        self._animal_settings_menu.add.range_slider("", Animal._STARTING_MIN_REPRODUCTION_HEALTH_RANGE, (DNA.min_reproduction_health_min, DNA.min_reproduction_health_max), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_starting_min_reproduction_health_range)
        self._animal_settings_menu.add.label("Spawning Min Energy % to reproduce")
        self._animal_settings_menu.add.range_slider("", Animal._STARTING_MIN_REPRODUCTION_ENERGY_RANGE, (DNA.min_reproduction_energy_min, DNA.min_reproduction_energy_max), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_starting_min_reproduction_energy_range)
        self._animal_settings_menu.add.label("Spawning Reproduction Chance")
        self._animal_settings_menu.add.range_slider("", Animal._STARTING_REPRODUCTION_CHANCE_RANGE, (DNA.reproduction_chance_min, DNA.reproduction_chance_max), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_starting_reproduction_chance_range)
        self._animal_settings_menu.add.label("Spawning Energy to offspring ratio")
        self._animal_settings_menu.add.range_slider("", Animal._STARTING_ENERGY_TO_OFFSPRING_RATIO_RANGE, (DNA.energy_to_offspring_min, DNA.energy_to_offspring_max), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_starting_energy_to_offspring_ratio_range)

        self._animal_settings_menu.add.label("Energy Maintenance Cost")
        self._animal_settings_menu.add.range_slider("", Animal._BASE_ENERGY_MAINTENANCE, (0, 100), increment=1, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_base_energy_maintenance)
        self._animal_settings_menu.add.label("Max Health")
        self._animal_settings_menu.add.range_slider("", Animal._MAX_HEALTH, (1, 1000), increment=10, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_max_health)
        self._animal_settings_menu.add.label("Max Energy")
        self._animal_settings_menu.add.range_slider("", Animal._MAX_ENERGY, (1, 1000), increment=10, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_max_energy)
        self._animal_settings_menu.add.label("Nutriton Factor")
        self._animal_settings_menu.add.range_slider("", Animal._NUTRITION_FACTOR, (0, 1), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Animal.set_nutrition_factor)

        self._animal_settings_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

    def _setup_plant_settings_menu(self) -> None:
        self._plant_settings_menu.add.label("Spawning Attack Power Range")
        self._plant_settings_menu.add.range_slider("", Plant._STARTING_ATTACK_POWER_RANGE, (DNA.attack_power_min, DNA.attack_power_max), increment=1, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_starting_attack_power_range)
        self._plant_settings_menu.add.label("Spawning Defense Range")
        self._plant_settings_menu.add.range_slider("", Plant._STARTING_DEFENSE_RANGE, (DNA.defense_min, DNA.defense_max), increment=1, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_starting_defense_range)
        self._plant_settings_menu.add.label("Spawning Moisture Preference Range")
        self._plant_settings_menu.add.range_slider("", Plant._STARTING_MOISTURE_PREFERENCE_RANGE, (DNA.prefered_moisture_min, DNA.prefered_moisture_max), increment=.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_starting_moisture_preference_range)
        self._plant_settings_menu.add.label("Spawning Height Preference Range")
        self._plant_settings_menu.add.range_slider("", Plant._STARTING_HEIGHT_PREFERENCE_RANGE, (DNA.prefered_height_min, DNA.prefered_height_max), increment=.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_starting_height_preference)
        self._plant_settings_menu.add.label("Spawning Mutation Chance Range")
        self._plant_settings_menu.add.range_slider("", Plant._STARTING_MUTATION_CHANCE_RANGE, (DNA.mutation_chance_min, DNA.mutation_chance_max), increment=.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_starting_mutation_chance_range)
        self._plant_settings_menu.add.label("Spawning Min Health % to reproduce")
        self._plant_settings_menu.add.range_slider("", Plant._STARTING_MIN_REPRODUCTION_HEALTH_RANGE, (DNA.min_reproduction_health_min, DNA.min_reproduction_health_max), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_starting_min_reproduction_health_range)
        self._plant_settings_menu.add.label("Spawning Min Energy % to reproduce")
        self._plant_settings_menu.add.range_slider("", Plant._STARTING_MIN_REPRODUCTION_ENERGY_RANGE, (DNA.min_reproduction_energy_min, DNA.min_reproduction_energy_max), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_starting_min_reproduction_energy_range)
        self._plant_settings_menu.add.label("Spawning Reproduction Chance")
        self._plant_settings_menu.add.range_slider("", Plant._STARTING_REPRODUCTION_CHANCE_RANGE, (DNA.reproduction_chance_min, DNA.reproduction_chance_max), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_starting_reproduction_chance_range)
        self._plant_settings_menu.add.label("Spawning Energy to offspring ratio")
        self._plant_settings_menu.add.range_slider("", Plant._STARTING_ENERGY_TO_OFFSPRING_RATIO_RANGE, (DNA.energy_to_offspring_min, DNA.energy_to_offspring_max), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_starting_energy_to_offspring_ratio_range)

        self._plant_settings_menu.add.label("Energy Maintenance Cost")
        self._plant_settings_menu.add.range_slider("", Plant._BASE_ENERGY_MAINTENANCE, (0, 100), increment=1, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_base_energy_maintenance)
        self._plant_settings_menu.add.label("Max Health")
        self._plant_settings_menu.add.range_slider("", Plant._MAX_HEALTH, (1, 1000), increment=10, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_max_health)
        self._plant_settings_menu.add.label("Max Energy")
        self._plant_settings_menu.add.range_slider("", Plant._MAX_ENERGY, (1, 1000), increment=10, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_max_energy)
        self._plant_settings_menu.add.label("Nutriton Factor")
        self._plant_settings_menu.add.range_slider("", Plant._NUTRITION_FACTOR, (0, 1), increment=0.01, range_box_color=self.TRANSPARENT_BLACK_COLOR, onchange=Plant.set_nutrition_factor)

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

    def set_draw_world(self, draw_world) -> None:
        """
        Sets the flag indicating whether to draw the world in the simulation.

        Parameters:
            draw_world (bool): Flag indicating whether to draw the world.

        Returns:
            None
        """
        self.draw_world = draw_world

    def clear_organisms(self) -> None:
        """
        Clears all organisms from the simulation.

        Raises:
            No specific exceptions are raised.

        Returns:
            None
        """
        simulation.reset_organisms()

    def reset_stats(self) -> None:
        """
        Resets the statistics of the simulation.

        Parameters:
            None

        Returns:
            None
        """
        simulation.reset_stats()

    #region tools
    def animal_spawning_tool(self, tiles: list[Tile]) -> None:
        """
        Animal spawning tool method for the Simulation class.

        Parameters:
            tiles (list[Tile]): A list of Tile objects where animals will be spawned.

        Returns:
            None
        """
        for tile in tiles:
            self.world.spawn_animal(tile)

    def choose_animal_spawning_tool(self) -> None:
        self.tool = self.animal_spawning_tool

    def plant_spawning_tool(self, tiles: list[Tile]) -> None:
        """
        Plant spawning tool method for the Simulation class.

        Parameters:
            tiles (list[Tile]): A list of Tile objects where plants will be spawned.

        Returns:
            None
        """
        for tile in tiles:
            self.world.spawn_plant(tile)

    def choose_plant_spawning_tool(self) -> None:
        self.tool = self.plant_spawning_tool

    def info_tool(self, tiles: list[Tile]) -> None:
        """
        Displays information about the first tile in tiles.

        Args:
            tiles (list[Tile]): A list of tiles to extract the organism information from.

        Returns:
            None
        """
        # TODO improve visual of info tool
        tile = tiles.pop(1)
        if tile.has_animal():
            self.selected_org = tile.animal.sprite
        elif tile.has_plant():
            self.selected_org = tile.plant.sprite
        else:
            self.selected_org = None

    def choose_info_tool(self) -> None:
        self.tool = self.info_tool

    def animal_kill_tool(self, tiles: list[Tile]) -> None:
        """
        Kills animals on the specified list of tiles by setting their health to 0 and calling the die method on their sprite.

        Parameters:
            tiles (list[Tile]): A list of Tile objects representing the tiles where animals should be killed.

        Returns:
            None
        """
        for tile in tiles:
            if tile.has_animal():
                tile.animal.sprite.health = 0
                tile.animal.sprite.die()

    def choose_animal_kill_tool(self) -> None:
        self.tool = self.animal_kill_tool

    def plant_kill_tool(self, tiles: list[Tile]) -> None:
        """
        Kills the plants on the specified list of tiles by setting their health to 0 and calling the die method on their sprite.

        Parameters:
            tiles (list[Tile]): A list of Tile objects on which plants will be killed.

        Returns:
            None
        """
        for tile in tiles:
            if tile.has_plant():
                tile.plant.sprite.health = 0
                tile.plant.sprite.die()

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
            if not draw_world:
                background_surface = pygame.Surface(fps_surface.get_size())
                background_surface.fill((255,255,255))
                self._surface.blit(background_surface, background_surface.get_rect(bottomleft = self._surface.get_rect().bottomleft))
            self._surface.blit(
                fps_surface,
                fps_surface.get_rect(bottomleft = self._surface.get_rect().bottomleft)
            )

        self._running_menu_bar.draw(self._surface)

    def run_loop(self) -> None:
        """
        Runs the main loop of the simulation, handling user input, updating the world, and displaying the graphical user interface.

        Raises:
            No specific exceptions are raised.

        Returns:
            No specific return value.
        """
        # TODO add setting to disable drawing completely to improve speed
        # TODO improve fps displaying
        drawing = False
        self.world.draw(self._surface)
        self._update_gui()

        simulating = True
        while simulating:
            mouse_pos = pygame.mouse.get_pos()
            self.brush_rect.center = mouse_pos

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
                    if not(self._running_menu_bar.get_rect().collidepoint(mouse_pos)):
                        drawing = True
                if event.type == pygame.MOUSEBUTTONUP:
                    drawing = False

            if not self.paused:
                self.world.update()

            if drawing:
                tiles = self.world.get_tiles(self.brush_rect)
                if not tiles:
                    self.selected_org = None
                else:
                    self.tool(tiles)

            self._update_gui(draw_menu = menu_updated, draw_world=self.draw_world)

            if self.world.rect.contains(self.brush_rect) and self.draw_world:
                # Draw cursor highlight
                pygame.draw.rect(
                    self._surface,
                    pygame.Color("white"),
                    self.brush_rect,
                    width=self.brush_outline
                )

            if self.selected_org:
                # TODO change this so there is a new stat panel that is locked in place
                self.selected_org.show_stats(self._surface, self.world.rect.topleft)

            pygame.display.flip()

            self._clock.tick(self._fps)

    def toggle_pause(self) -> None:
        """
        Toggles the pause state of the simulation.

        This method updates the pause state of the simulation by toggling it between paused and running states.
        It retrieves the 'GameState' widget from the running settings menu and sets its value to the current pause state.
        Then, it toggles the pause state by negating the current value of 'paused' attribute.

        Parameters:
            None

        Returns:
            None
        """
        self._running_settings_menu.get_widget("GameState").set_value(self.paused)
        self.paused = not self.paused

    def mainlopp(self) -> None:
        self.starting_menu.mainloop(self._surface)
    #endregion

    def _quit(self) -> None:
        pygame.quit()
        exit()
